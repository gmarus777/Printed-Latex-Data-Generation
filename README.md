# Printed-Latex-Data-Generation

Python and JS tools for generating Printed Latex Dataset (images of tex formulas with labels) via parsing Cornell's [KDDCUP](https://www.cs.cornell.edu/projects/kddcup/datasets.html).
Also see [KDDCUP paper](https://www.cs.cornell.edu/home/kleinber/kddcup2003.pdf).
<br />

**Note: parsing for ArXiv, Wikipedia and Stackexchange sources are coming.** 
**Note: One can use any .tar files with LaTex formulas to parse, need to manually add it to the folder.** 


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

## Generated Dataset im2latex 230k

You can download a prebuilt dataset 230k from [here](https://zenodo.org/record/7738969#.ZBJJSi-B2Lc).

Some Dataset im2latex 230k Characteristics:
- images are of varying sizes with maximum Height of 431 and maximum Width of 6816
- sizes of formulas vary from 6 to 970 (tokenized length) with distribution below

![alt text](histogram.png)

- comes with a vocabulary 230k.json of size 579, which was generated on a bigger Dataset of around 330k
- sample image:
![alt text](sample.png)






**Note: This code is very ad-hoc and requires tinkering with the source**
<br />
<br />

## Depenencies
1. Docker, and make sure that docker daemon is ruuning. 


<br />
<br />

##  Usage 
1. Clone the repo. 
2. Go to the repo folder.
3. run pip install -e . 
4. To see help run: 
```
latex-generator --help
```


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

Idea is based on https://github.com/Miffyli/im2latex-dataset
