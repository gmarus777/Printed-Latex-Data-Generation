import argparse 
from Printed_Tex import Generate_Printed_Tex, extract_formulas


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--info", action="store_true")
    parser.add_argument("--default", action="store_true")
    parser.add_argument("-d", "--download", action="store_true", help="Download the dataset")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate the dataset")
    parser.add_argument("-s", "--svg", action="store_true", help="Generate the svg images")
    parser.add_argument("-p", "--png", action="store_true", help="Generate the png images")

    parser.add_argument("--max_formula_size", type=int, default=1024, help="Max size of formulas to include in bytes")
    parser.add_argument("--minimum_formula_size", type=int, default=40, help="Min size of formulas to include in bytes")

    parser.add_argument("--urls-file", type=str, help="File containing urls to download, otherwise use default")
    parser.add_argument("--filter_words_file", type=str, help="File containing words to filter out to add, otherwise use default")
    parser.add_argument("--dpi_x", type=int, help="x-DPI to use for png images")
    parser.add_argument("--dpi_y", type=int, help="y-DPI to use for png images")
    parser.add_argument("--width", type=int, help="Width of png images")
    parser.add_argument("--height", type=int, help="Height of png images")

    parser.add_argument("--label-length", type=int, default=128, help="Max length of the label")
    parser.add_argument("--number-formulas", type=int, default=150, help="Number of formulas to generate")
    parser.add_argument("--number-png", type=int, default=120, help="Number of png images to generate")


    parser.add_argument("-e", "--extract", action="store_true", help="Extract data")

    return parser.parse_args()  

if __name__ == "__main__": 
    args = parse_args() 
    Generate_Printed_Tex(
        download_tex_dataset=args.download,
        generate_tex_formulas=args.generate,
        max_label_length=args.label_length,
        number_tex_formulas_to_generate=args.number_formulas,
        generate_svg_images_from_tex=args.svg,
        generate_png_from_svg=args.png,
        number_png_images_to_use_in_dataset=args.number_png,
        max_formula_size=args.max_formula_size,
        minimum_formula_size=args.minimum_formula_size,
        filter_words_file=args.filter_words_file,
        urls_file=args.urls_file,
        dpi_x=args.dpi_x,
        dpi_y=args.dpi_y,
        width=args.width,
        height=args.height
    )








