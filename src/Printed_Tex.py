from pathlib import Path
from download_data_utils import _download_raw_dataset_from_list, ImageProcessor, _unpack_a_tar,  _unpack_tars, _normalize_latex_data, _clean_formulas, _generate_svg_images, _turn_svg_to_png, _get_formulas
from configs import PrintedLatexDataConfig






'''

Module to Generate Printed LaTex data from KDDCup, Arxiv, Wikipedia and other sources.


The following Global Parameters for parsing formulas are set in

-- FILTER out Words when parsing is set in configs.py:  FILTER_OUT_WORDS


-- Formula Length while parsing is set in download_data_utils.py:
                MAX_FORMULA_LENGTH_in_Bytes = 1024,
                MIN_FORMULA_LENGTH_BYTES = 40,
                
                
-- Tex to SVG parameters are set in tex_to_svg.py:
                MAX_NUMBER_TO_RENDER = 1000 
                THREADS = 10
                

-- SVG to PNG parameters are set in svg_to_png.py:
                THREADS = 64
                PNG_WIDTH = 512
                PNG_HEIGHT = 64       
                

'''



def Generate_Printed_Tex(download_tex_dataset = False,
                generate_tex_formulas= False,
                max_label_length = 128,
                # if number_tex_formulas_to_generate < 1001 only parses one tar file
                number_tex_formulas_to_generate=150,
                generate_svg_images_from_tex = False,
                generate_png_from_svg = False,
                number_png_images_to_use_in_dataset=120, 
                max_formula_size=1024,
                minimum_formula_size=40,
                filter_words_file=None,
                urls_file=None,
                dpi_x=100,
                dpi_y=100,
                width=512,
                height=64
                ):
    '''
           Printed Tex Data Module Parameters:


            -- download_tex_dataset: if Set True/False downloads the dataset TODO: upgrade to choose source arxiv,wiki etc
            -- generate_tex_formulas: if set True will download and generate the whole thing by running self._prepare_data_on_file() in Repository
            -- max_label_length: only keep the labels of len < max_label_length in the dataframe
            -- number_tex_formulas_to_generate: currently when set <1001 =, only unpacks one .tar file  TODO: make this better
            -- generate_svg_images_from_tex:  generates svg images using MathJax
            -- generate_png_from_svg: if set True will use the generated svg images to produce png images.
            -- number_png_images_to_use_in_dataset: number of png images to be used for the model from pandas dataframe
           '''
    
    if download_tex_dataset == True:
        urls = PrintedLatexDataConfig.metadata["urls"]
        destination_dir = PrintedLatexDataConfig.CHROME_RAW_DATA_DIRNAME
        _download_raw_dataset_from_list(urls, destination_dir)
        

    if generate_tex_formulas == True:
        if number_tex_formulas_to_generate < 1001:
            _unpack_a_tar(max_formula_size, minimum_formula_size)
        else: 
            _unpack_tars(max_formula_size, minimum_formula_size)
        _normalize_latex_data()
        _clean_formulas()


    if generate_svg_images_from_tex == True:
        _generate_svg_images()

    if generate_png_from_svg == True:
        _turn_svg_to_png(dpi_x, dpi_y, width, height)



        




def extract_formulas(args): 
    latex_file_path = args.path
    latex = get_content_from_file(latex_file_path)
    formulas = _get_formulas(latex)
    save_formulas_to_file(formulas, args)


def get_content_from_file(path):
    with open(path, "r") as f:
        return f.read()
    
def save_formulas_to_file(formulas, args):
    with open(args.output, "w") as f:
        for formula in formulas:
            f.write(formula + "\n")

