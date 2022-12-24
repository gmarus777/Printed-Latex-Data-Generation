import hashlib
from pathlib import Path
from typing import Dict, Union, List
from urllib.request import urlretrieve
import tarfile
import glob
import pandas as pd
import numpy as np

import os
import re
import cv2

import PIL
from PIL import ImageOps
import smart_open
from PIL import Image
from tqdm import tqdm
from configs import PrintedLatexDataConfig



# TODO: integrate the variables below
MAX_FORMULA_LENGTH_in_Bytes = 1024
MIN_FORMULA_LENGTH_BYTES = 40



def get_max_label_length(labels):
    return max([len(label) for label in labels])


######################### DOWNLOAD UTILS ###################################
class TqdmUpTo(tqdm):
    """From https://github.com/tqdm/tqdm/blob/master/examples/tqdm_wget.py"""

    def update_to(self, blocks=1, bsize=1, tsize=None):
        """
        Parameters
        ----------
        blocks: int, optional
            Number of blocks transferred so far [default: 1].
        bsize: int, optional
            Size of each block (in tqdm units) [default: 1].
        tsize: int, optional
            Total size (in tqdm units). If [default: None] remains unchanged.
        """
        if tsize is not None:
            self.total = tsize  # pylint: disable=attribute-defined-outside-init
        self.update(blocks * bsize - self.n)  # will also set self.n = b * bsize


def compute_sha256(filename: Union[Path, str]):
    with open(filename, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()


def download_url(url, filename):
    """Download a file from url to filename, with a progress bar."""
    with TqdmUpTo(unit="B", unit_scale=True, unit_divisor=1024, miniters=1) as t:
        urlretrieve(url, filename, reporthook=t.update_to, data=None)


def _download_raw_dataset(metadata: Dict, dl_dirname: Path):
    dl_dirname.mkdir(parents=True, exist_ok=True)
    filename = dl_dirname / metadata["filename"]
    if filename.exists():
        return filename
    print(f"Downloading raw dataset from {metadata['url']} to {filename}...")
    download_url(metadata["url"], filename)
    print("Computing SHA-256...")
    sha256 = compute_sha256(filename)
    if sha256 != metadata["sha256"]:
        raise ValueError("Downloaded data file SHA-256 does not match the one listed in the metadata")
    return filename


def _download_raw_dataset_from_list(urls: List[str], dl_dirname: Path):
    print(dl_dirname)
    dl_dirname.mkdir(parents=True, exist_ok=True)
    for url in urls:
        filename = dl_dirname/url[-18:]
        if filename.exists():
            continue
        print(f"Downloading raw dataset from {url} to {filename}")
        download_url(url, filename)




################################ IMAGE PROCESSING #########################




# processing images for data generation.
class ImageProcessor:
    @staticmethod
    def process_latex_image(file_name):
        image = ImageProcessor.read_image_pil(file_name)
        image = PIL.ImageOps.grayscale(image)
        image = PIL.ImageOps.invert(image)
        return image

    @staticmethod
    def read_image_pil(image_uri, grayscale=False) -> PIL.Image:
        #print(os.getcwd())
        with smart_open.open(image_uri, "rb") as image_file:
            return ImageProcessor.read_image_pil_file(image_file, grayscale)

    @staticmethod
    def read_image_pil_file(image_file, grayscale=False) -> PIL.Image:
        with Image.open(image_file) as image:
            if grayscale:
                image = image.convert(mode="L")
            else:
                image = image.convert(mode=image.mode)

            return image





########### Below are functions that download and process raw data #############


# unpacks all downloaded tars
def _unpack_tars():


    if not Path.exists(PrintedLatexDataConfig.UNPROCESSED_FORMULA_FILENAME):
        directory = PrintedLatexDataConfig.CHROME_RAW_DATA_DIRNAME
        output_folder = PrintedLatexDataConfig.NORMALIZED_FORMULAS_DIR
        output_folder.mkdir(parents=True, exist_ok=True)
        latex_tars = glob.glob(str(directory) + "/*.tar.gz")
        formulas = []
        ctr = 0
        # print(len(latex_tars)) == 12
        for filename in latex_tars:
            # print(filename)
            tar = tarfile.open(filename)
            # List latex files
            files = tar.getnames()
            # Loop over and extract results
            for latex_name in files:
                if not "/" in latex_name:  # .getnames() includes directory-only
                    continue

                tar.extract(latex_name)
                latex = open(latex_name, encoding="utf8", errors='ignore').read()
                formulas.extend(_get_formulas(latex))
                os.remove(latex_name)

                #os.rmdir(latex_name)
            ctr += 1

            os.rmdir(latex_name[:-8])
            print("Done {} of {}".format(ctr, len(latex_tars)))
        formulas = list(set(formulas))
        print("Parsed {} formulas".format(len(formulas)))
        print("Saving formulas...")
        output = output_folder / "formulas.txt"
        with open(output, "w") as f:
            f.write("\n".join(formulas))




# unpacks one tar and writes respective formulas in formula.txt (FOR TESTING PURPOSES)
def _unpack_a_tar():
    if not Path.exists(PrintedLatexDataConfig.UNPROCESSED_FORMULA_FILENAME):
        directory = PrintedLatexDataConfig.CHROME_RAW_DATA_DIRNAME
        output_folder = PrintedLatexDataConfig.NORMALIZED_FORMULAS_DIR
        output_folder.mkdir(parents=True, exist_ok=True)
        latex_tars = glob.glob(str(directory) + "/*.tar.gz")
        formulas = []
        ctr = 0
        #


        # print(len(latex_tars)) == 12
        # print(filename)
        tar = tarfile.open(latex_tars[0])
        # List latex files
        files = tar.getnames()
        # Loop over and extract results
        for latex_name in files:
            if not "/" in latex_name:  # .getnames() includes directory-only
                continue

            tar.extract(latex_name)
            latex = open(latex_name, encoding="utf8", errors='ignore').read()
            formulas.extend(_get_formulas(latex))
            os.remove(latex_name)

            #os.rmdir(latex_name)
        ctr += 1

        os.rmdir(latex_name[:-8])
        print("Done {} of {}".format(ctr, len(latex_tars)))
        formulas = list(set(formulas))
        print("Parsed {} formulas".format(len(formulas)))
        print("Saving formulas...")
        output = output_folder / "formulas.txt"
        with open(output, "w") as f:
            f.write("\n".join(formulas))


def _normalize_latex_data():
    os.chdir(PrintedLatexDataConfig.ROOT_DIRNAME)
    #if not Path.exists(PrintedLatexDataConfig.NORMALIZED_FORMULAS_DIR / "formulas.norm.txt.tmp"):
    os.system(PrintedLatexDataConfig.normalizing_script_command)

def _clean_formulas():
    print('Cleaning and Filtering Formulas')
    # words to clean: list of words in repository_configs
    words_to_clean = PrintedLatexDataConfig.FILTER_OUT_WORDS

    # get formulas path

    path_to_formulas = PrintedLatexDataConfig.FORMULAS_PATH_NO_TMP  # If formulas.norm.txt is empty change the path to FORMULAS_PATH_TMP or vice versa in




    # convert formulas to pandas series
    formulas_series = readlines_to_sr(path_to_formulas)


    if formulas_series.shape[0] == 0 or formulas_series.shape[0] == 1:
        path_to_formulas = PrintedLatexDataConfig.FORMULAS_PATH_NO_TMP
        formulas_series = readlines_to_sr(path_to_formulas)


    print('Original size', formulas_series.shape)

    # cleanup series

    formulas_series_stripped = formulas_series.str.strip()

    # remove short formulas
    formulas_series_stripped_length = formulas_series_stripped[(formulas_series_stripped.str.split().str.len() > 3)]

    # print('size w/o short formulas', formulas_series_stripped_length.shape)

    final_formulas = filter_words(formulas_series_stripped_length, words_to_clean)

    print('Final filtered size', final_formulas.shape)

    # Save the final formulas
    print('Saving Filtered Formulas')
    path_to_save_formulas = PrintedLatexDataConfig.NORMALIZED_FORMULAS_DIR / "formulas.norm.filtered.txt"

    sr_to_lines(final_formulas, path_to_save_formulas)

def _generate_svg_images():
    os.chdir(PrintedLatexDataConfig.ROOT_DIRNAME)
    os.system(PrintedLatexDataConfig.svg_generation_script_command)

def _turn_svg_to_png():
    os.chdir(PrintedLatexDataConfig.ROOT_DIRNAME)
    os.system(PrintedLatexDataConfig.png_generation_script_command)

def _get_formulas(latex: str):
    """ Returns detected latex formulas from given latex string
    Returns list of formula strings"""

    ret = []
    PATTERNS = [r"\\begin\{equation\}(.*?)\\end\{equation\}",
                # r"\$\$(.*?)\$\$",
                # r"\$(.*?)\$",
                # r"\\\[(.*?)\\\]",
                # r"\\\((.*?)\\\)"
                ]

    for pattern in PATTERNS:
        res = re.findall(pattern, latex, re.DOTALL)
        # Remove short ones
        res = [x.strip().replace("\n", "").replace("\r", "") for x in res if
               MAX_FORMULA_LENGTH_in_Bytes > len(x.strip()) > MIN_FORMULA_LENGTH_BYTES]
        ret.extend(res)
    return ret

def filter_words(sr, words):
    for word in words:
        sr = sr[~(sr.str.contains(word))]
    return sr




# converts formulas txt to pandas series
def readlines_to_sr(path):
    rows = []
    n = 0
    with open(path, 'r') as f:
        # print('opened file %s' % path)
        for line in f:
            n += 1
            line = line.strip()  # remove \n
            if len(line) > 0:
                rows.append(line)  # .encode('utf-8')
    # print('processed %d lines resulting in %d rows' % (n, len(rows)))
    return pd.Series(rows, dtype=np.str_)


# converts pandas series to formulas.txt

def sr_to_lines(sr, path):
    #   df.to_csv(path, header=False, index=False, columns=['formula'], encoding='utf-8', quoting=csv.QUOTE_NONE, escapechar=None, sep='\t')
    assert sr.dtype == np.str_ or sr.dtype == np.object_
    with open(path, 'w') as f:
        for s in sr:
            assert '\n' not in s
            f.write(s.strip())
            f.write('\n')


def _get_dataframe():
    # take final formula list
    path_to_formulas = PrintedLatexDataConfig.PNG_FINAL_FORMULAS
    formulas_df = readlines_to_df(path_to_formulas, 'formula')

    # get png image names
    image_names_path = PrintedLatexDataConfig.PNG_IMAGES_NAMES_FILE
    image_names_df = readlines_to_df(image_names_path, 'image_name')

    formulas_df['image_name'] = image_names_df

    return formulas_df


# outputs formula length, image height and width.
def _get_stats(datasetDF):
    widths = []
    heights = []
    formula_lens = []

    dataset = datasetDF
    for _, row in datasetDF.iterrows():
        image_name = row.image_name
        # print(image_name)
        im = Image.open(os.path.join(PrintedLatexDataConfig.GENERATED_PNG_DIR_NAME, image_name))
        widths.append(im.size[0])
        heights.append(im.size[1])
        formula_lens.append(len(row.formula))

    # datasetDF = datasetDF.assign(width=widths, height=heights, formula_len=formula_lens)
    dataset['height'] = heights
    dataset['width'] = widths
    dataset['formula_length'] = formula_lens

    return dataset