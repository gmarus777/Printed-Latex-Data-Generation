# Printed-Latex-Data-Generation

Python and JS tools for generating Printed Latex Dataset (images of tex formulas with labels) via parsing Cornell's [KDDCUP](https://www.cs.cornell.edu/projects/kddcup/datasets.html). Also see [KDDCUP paper](https://www.cs.cornell.edu/home/kleinber/kddcup2003.pdf).


**Note: parsing for ArXiv, Wikipedia and Stackexchange sources are coming.** 


<br />
<br />

## How to generate data
The easiest way to generate data is via Jupyter Notebook `Data generation.ipynb` located in folder `Jupyter Notebooks/`.


Running it will output all the data in `Data` folder.

Final outputs
- folder `generated_png_images` contianing PNG images
- `corresponding_png_images.txt` each new line contains png images filename for the folder `generated_png_images`
- `final_png_formulas.txt` each new line contains a carresponing LaTex formula
- folder `raw_data` containing raw downaloded data
- folder `temporary_data` containing formulas from various stages of processing and svg images generated along the way

<br />
<br />


You can download a prebuilt dataset 180k from [here](https://zenodo.org/record/7480549#.Y6duWC2B30o).


**Note: This code is very ad-hoc and requires tinkering with the source**
<br />
<br />

## Depenencies
1. Tested with Python 3.9.7 and [Anaconda version 2021.11] (https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh)
2. `pip install opencv-python`
3. `pip install smart_open`
4. For Tex to SVG [see](https://www.npmjs.com/package/tex2svg):

    `sudo apt install nodejs npm`\
    `sudo npm install --global mathjax-node-cli`
     

5. For SVG to PNG:


  Linux:
  
  
  https://ubuntu.pkgs.org/20.04/ubuntu-universe-arm64/librsvg2-bin_2.48.2-1_arm64.deb.html
  
  
  `sudo apt install librsvg2-bin`
  
  <br />

  For MacOS:
  Download [Inkscape](https://inkscape.org), also see [here](https://stackoverflow.com/questions/9853325/how-to-convert-a-svg-to-a-png-with-imagemagick) 
  
 


<br />
<br />

## Contents
- `Printed_Tex.py`
  - Main module 
- `download_data_utils.py`
  - Contains tools for downlaoding tex tars and unpacking and parisng them.
- `configs.py`
  - Contains Paths and command line script commands.
- `third_party/`
  - Contains Katex for parsing LaTex formulas
- `preprocess_formulas.py` and `preprocess_formulas.js`
  - Collection of tools for handling and parsing LaTex formulas
- `svg_to_png.py`
  - Funcitons to convert LaTex formulas to SVG images using MathJax
- `png_to_svg.py`
  - Funcitons to convert SVG images formulas to PNG images using `inkscape` for (Darwin) MacOS and `rsvg-convert` for all other systems. 
- `Data/`
  - Contains `generated_png_images/` folder, `corresponding_png_images.txt`  and `final_png_formulas.txt`. Also temporary folder `temporary_data` (formulas for various stages of processing and generated SVG images) and `raw_data` where raw data is downloaded.
- `Jupyter Notebooks`
  - Contains examples of generating data using Jupyter notebooks


<br />
<br />

Based on https://github.com/Miffyli/im2latex-dataset
