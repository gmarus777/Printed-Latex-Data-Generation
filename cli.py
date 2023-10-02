import argparse 

from Printed_Tex import Generate_Printed_Tex


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--info", action="store_true")
    parser.add_argument("-d", "--download", action="store_true", help="Download the dataset")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate the dataset")
    parser.add_argument("-s", "--svg", action="store_true", help="Generate the svg images")
    parser.add_argument("-p", "--png", action="store_true", help="Generate the png images")

    parser.add_argument("--label-length", type=int, default=128, help="Max length of the label")
    parser.add_argument("--number-formulas", type=int, default=150, help="Number of formulas to generate")
    parser.add_argument("--number-png", type=int, default=120, help="Number of png images to generate")

    return parser.parse_args()  

if __name__ == "__main__": 
    args = parse_args() 

    generator = Generate_Printed_Tex(
        download_tex_dataset=args.download,
        generate_tex_formulas=args.generate,
        max_label_length=args.label_length,
        number_tex_formulas_to_generate=args.number_formulas,
        generate_svg_images_from_tex=args.svg,
        generate_png_from_svg=args.png,
        number_png_images_to_use_in_dataset=args.number_png,
    )






