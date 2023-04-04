"""
Purpose of this script is to turn svg images into png images

"""

import glob
import sys
import os
import hashlib
from multiprocessing import Pool
from subprocess import call
import pandas as pd
from pathlib import Path
import subprocess
import platform
from configs import PrintedLatexDataConfig



# Max number of formulas included
# MAX_NUMBER_TO_RENDER = 50  # 150*1000

THREADS = 95
PNG_WIDTH = 512
PNG_HEIGHT = 64



ROOT_DIRNAME = Path(__file__).resolve().parents[0]  # gives the root directory
DATA_DIRNAME = ROOT_DIRNAME / "Data"
CHROME_RAW_DATA_DIRNAME = DATA_DIRNAME / "raw_data" / "chrome"
UNPROCESSED_FORMULA_FILENAME = DATA_DIRNAME / "not_normalized" / "formulas.txt"
NORMALIZED_FORMULAS_DIR = DATA_DIRNAME / "temporary_data"
FORMULAS_PATH_NO_TMP = NORMALIZED_FORMULAS_DIR / "formulas.norm.txt"
PREPROCESS_FORMULAS_SCRIPT_PATH = ROOT_DIRNAME / "preprocess_formulas.py"
GENERATED_SVG_IMAGES_DIR_NAME = NORMALIZED_FORMULAS_DIR / "generated_svg_images"
GENERATED_PNG_DIR_NAME = DATA_DIRNAME / "generated_png_images"
SVG_IMAGES_FORMULAS = NORMALIZED_FORMULAS_DIR / "final_svg_formulas.txt"  # consists of tex formulas on every new line
PNG_IMAGE_DIR = 'Data/generated_png_images'
PNG_IMAGES_NAMES_FILE = DATA_DIRNAME / "corresponding_png_images.txt"
PNG_FORMULA_FILE = DATA_DIRNAME / "final_png_formulas.txt"













# Running a thread pool masks debug output. Set DEBUG to 1 to run
# formulas over images sequentially to see debug errors more clearly
DEBUG = False

DEVNULL = open(os.devnull, "w")



def main(corresponding_images):
    images = open(corresponding_images).read().split("\n")#[:MAX_NUMBER_TO_RENDER]



    formulas = open(SVG_IMAGES_FORMULAS).read().split("\n")


    try:
        os.mkdir(PNG_IMAGE_DIR)
    # except because throws OSError if dir exists
    except OSError as e:
        pass

    print("Turning svg into png...")

    images_and_formulas = zip(images, formulas)


    root_dir = os.getcwd()  # /root


    os.chdir(DATA_DIRNAME)


    pool = Pool(processes=THREADS)

    image_names_and_formulas = pool.map(svg_to_png, images_and_formulas)  # outputs ['file_name', 'tex_formula']



    #print(image_names_and_formulas)
    #print(image_names_and_formulas[1][0]) # ['filename', 'formula']
    #print(image_names_and_formulas[1][0][0], image_names_and_formulas[1][0][1]) # filename ; formula

    if not PNG_IMAGE_DIR in os.getcwd():
        #os.chdir(PNG_IMAGE_DIR)  # Paragraph_to_Tex/harvardnlp_im2markup/generated_images
        os.chdir(GENERATED_PNG_DIR_NAME)
    number_of_images = len(image_names_and_formulas)


    list_of_names = []
    list_of_formulas = []


    for i in range(number_of_images):


        if image_names_and_formulas[i][0] is not None:


            filename = image_names_and_formulas[i][0][0]


            # we get the size of the file
            try:
                size = os.path.getsize(filename)


            # in case file is not rendered at all
            except:
                size = 0

            if size > 1000:

                # final_formulas.txt consists of tex formulas on every new line
                list_of_formulas.append(image_names_and_formulas[i][0][1])

                # corresponding_images consists of line number and image_name.svg
                list_of_names.append(image_names_and_formulas[i][0][0])


    os.chdir(DATA_DIRNAME)  # /Data
    
    


    with open(PNG_IMAGES_NAMES_FILE, "w") as f:

        f.write("\n".join(list_of_names))
        
    

    with open(PNG_FORMULA_FILE, "w") as f:

        f.write("\n".join(list_of_formulas))
    

    print(f'Generated {len(list_of_formulas)} images from formulas')




def svg_to_png(images_and_formulas):
    """
    Takes a svg image and converts to png using Inkscape
      EXAMPLE: inkscape -w 1024 -h 1024 input.svg -o output.png



    """
    final_output = []  # outputs processed image_name and corresponding formula
    image_name, formula = images_and_formulas

    # png_generation_script_command =  f"inkscape -z -w {PNG_WIDTH} -h {PNG_HEIGHT} generated_images/{image_name} -o generated_png_images/{image_name[:-4]}.png"

    png_generation_inkscape_script_command = f"inkscape -b FFFFFF -z -w {PNG_WIDTH} -h {PNG_HEIGHT} temporary_data/generated_svg_images/{image_name} -o generated_png_images/{image_name[:-4]}.png"

    png_generation_linux_command = f"/usr/local/bin/inkscape  -b FFFFFF -z -w {PNG_WIDTH} -h {PNG_HEIGHT}  generated_svg_images/{image_name} -o generated_png_images/{image_name[:-4]}.png"


    #png_generation_rsvg = f" rsvg-convert -b white -w {PNG_WIDTH} -h {PNG_HEIGHT}  temporary_data/generated_svg_images/{image_name} -o generated_png_images/{image_name[:-4]}.png "
    # --dpi-x=96 --dpi-y=96
    png_generation_rsvg = f" rsvg-convert --dpi-x=250 --dpi-y=250 -b white  temporary_data/generated_svg_images/{image_name} -o generated_png_images/{image_name[:-4]}.png "







    # generate the svg
    # MacOS uses inkscape
    if platform.system() == 'Darwin':
        os.system(png_generation_inkscape_script_command)
        image_name = image_name[:-4] + '.png'
        final_output.append([image_name, formula])
        return final_output

    # Linux uses rsvg
    else:
        os.system(png_generation_rsvg)
        image_name = image_name[:-4] + '.png'
        final_output.append([image_name, formula])
        return final_output


if __name__ == '__main__':
    main(sys.argv[1])
