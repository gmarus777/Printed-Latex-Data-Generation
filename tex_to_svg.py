"""
Purpose of this script is to turn list of tex formulas into svg images

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

# Max number of formulas included
MAX_NUMBER_TO_RENDER = 100  # 150*1000



THREADS = 64

ROOT_DIRNAME = Path(__file__).resolve().parents[0]  # gives the root directory
DATA_DIRNAME = ROOT_DIRNAME / "Data"
NORMALIZED_FORMULAS_DIR =  DATA_DIRNAME / "temporary_data"
GENERATED_SVG_IMAGES_DIR_NAME = NORMALIZED_FORMULAS_DIR / "generated_svg_images"




IMAGE_DIR = 'Data/temporary_data/generated_svg_images'

SVG_IMAGES_NAMES = NORMALIZED_FORMULAS_DIR / "corresponding_svg_images.txt"  # consists of line number and image_name.svg
SVG_IMAGES_FORMULAS = NORMALIZED_FORMULAS_DIR / "final_svg_formulas.txt"  # consists of tex formulas on every new line

# Running a thread pool masks debug output. Set DEBUG to 1 to run
# formulas over images sequentially to see debug errors more clearly
DEBUG = False

DEVNULL = open(os.devnull, "w")

'''
outputs: 
 -- corresponding_svg_images.txt 
 -- final_svg_formulas.txt
 --  svg images in generated_svg_images folder
'''


def main(formula_list):
    formulas = open(formula_list).read().split("\n")[:MAX_NUMBER_TO_RENDER]

    
    formula_names = [None] * len(formulas)
    print(f'Generating { len(formulas) } images from Filtered Formulas')

    names_n_formulas = zip(formula_names, formulas)

    # Nawaf already creates IMAGE_DIR, so no need?
    try:
        os.mkdir(IMAGE_DIR)
    # except because throws OSError if dir exists
    except OSError as e:
        pass

    print("Turning formulas into svg...")

    oldcwd = os.getcwd()  # /Root directory
    print(oldcwd)


    if not IMAGE_DIR in os.getcwd():
        os.chdir(IMAGE_DIR)  # Data/processed_data/generated_svg_images

    pool = Pool(processes=THREADS)

    # os.chdir(oldcwd)  # /Data/

    final_names_and_formulas = pool.map(formula_to_svg, names_n_formulas)  # outputs ['file_name', 'tex_formula']

    number_of_images = len(final_names_and_formulas)



    # print(final_names_and_formulas[1][0]) # ['filename', 'formula'] this is $ to broad $jok
    # print(final_names_and_formulas[1][0][0], final_names_and_formulas[1][0][1]) # filename ; formula

    list_of_names = []
    list_of_formulas = []
    # control = 0

    # Now we need to filter out non-rendered images or images with size zero




    for i in range(number_of_images):

        if final_names_and_formulas[i][0] is not None:
            filename = final_names_and_formulas[i][0][0]

            # we get the size of the file
            try:
                size = os.path.getsize(filename)

            # in case file is not rendered at all
            except:
                size = 0

            if size > 1000:

                # final_svg_formulas.txt consists of tex formulas on every new line
                list_of_formulas.append(final_names_and_formulas[i][0][1])

                # corresponding_images consists of line number and image_name.svg
                list_of_names.append(final_names_and_formulas[i][0][0])




    os.chdir(oldcwd) # # /Data/

    print(SVG_IMAGES_NAMES)
    with open(SVG_IMAGES_NAMES, "w") as f:

        f.write("\n".join(list_of_names))

    with open(SVG_IMAGES_FORMULAS, "w") as f:

        f.write("\n".join(list_of_formulas))

    print(f'Generated {len(list_of_formulas)} images from formulas')


def formula_to_svg(name_n_formula):
    """
    Takes a tex formula and image_name zip and convert them to svg using shell command.
      EXAMPLE: python tex2svg '\sqrt(\alpha)' > image_folder/image_name.svg



    """

    final_image_name = []

    name, formula = name_n_formula

    # print('formulas is ', formula)
    # formula = formula.strip("%")
    try:
        # Need try/catch block since some of the formulas have non-utf8 characters
        # causing a UnicodeDecodeError exception
        if name is None:
            name = hashlib.sha1(formula.encode('utf-8')).hexdigest()[:15]

    except Exception as e:
        print(e)
        print('Error processing formula line "%s". Moving on ...' % (formula,))
        return None

    ret = []

    svg_generation_script_command = f"tex2svg \'{formula}\' >  {name}.svg"

    # generate the svg
    os.system(svg_generation_script_command)

    final_image_name.append([f'{name}.svg', formula])

    return final_image_name




'''    # Now we remove svg files which did not render properly
    filename = f'{name}.svg'
    try:
        size = os.path.getsize(filename)
        # if file is nor rendered at all we give it a code 1 (one byte size)
    except:

        size = 1

    # images with size 0
    if size == 0:
        # now saves the names and in the end remove these files
        os.remove(f'{name}.svg')
        name = None

    # images that did not render
    if size == 1:
        # now saves the names and in the no need to remove these files

        name = None

    if name != None:
        final_image_name.append([f'{name}.svg', formula])

        return final_image_name
    else:
        return name
'''


if __name__ == '__main__':
    main(sys.argv[1])
