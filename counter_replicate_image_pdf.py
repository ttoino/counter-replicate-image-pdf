#!/usr/bin/env python3
# Dependencies: fpdf
from argparse import ArgumentParser
from fpdf import FPDF
import os


def get_args():
    arg_parser = ArgumentParser()

    arg_parser.add_argument("image", help="the image to add to the pdf")
    arg_parser.add_argument("count",
                            type=int,
                            help="the number of images to add to the pdf")
    arg_parser.add_argument("-o", "--out", help="where to save the pdf")

    font_opts = arg_parser.add_argument_group("font options")
    font_opts.add_argument("-f",
                           "--font",
                           default="Arial",
                           help="the font to use for the counter")
    font_opts.add_argument("-fs",
                           "--font-size",
                           type=float,
                           default=12,
                           help="the font size to use for the counter, in pt")
    font_opts.add_argument("-fc",
                           "--font-color",
                           type=int,
                           nargs=3,
                           metavar=("RED", "GREEN", "BLUE"),
                           default=[0, 0, 0],
                           help="the font color to use for the counter")

    page_opts = arg_parser.add_argument_group("page options")
    page_opts.add_argument("-l",
                           "--landscape",
                           action="store_true",
                           help="sets the page to landscape")
    page_opts.add_argument("-p",
                           "--page-type",
                           default="A4",
                           help="the page type to use")

    pos_opts = arg_parser.add_argument_group("position options")
    pos_opts.add_argument("-s",
                          "--image-size",
                          type=float,
                          nargs=2,
                          metavar=("WIDTH", "HEIGHT"),
                          default=[100, 100],
                          help="the size of the image, in mm")
    pos_opts.add_argument("-n",
                          "--number-pos",
                          type=float,
                          nargs=2,
                          metavar=("X", "Y"),
                          action="append",
                          default=[],
                          help="adds a counter at that position, in mm")
    pos_opts.add_argument("-m",
                          "--margin",
                          type=float,
                          nargs=2,
                          metavar=("MARGIN_X", "MARGIN_Y"),
                          default=[0, 0],
                          help="adds a margin around the images, in mm")
    pos_opts.add_argument("-g",
                          "--gap",
                          type=float,
                          nargs=2,
                          metavar=("GAP_X", "GAP_Y"),
                          default=[0, 0],
                          help="adds a gap between the images, in mm")
    pos_opts.add_argument("-r",
                          "--rows",
                          type=int,
                          default=1,
                          help="the number of rows per page")
    pos_opts.add_argument("-c",
                          "--cols",
                          type=int,
                          default=1,
                          help="the number of columns per page")

    return arg_parser.parse_args()


def main():
    args = get_args()

    if not os.path.exists(args.image):
        print("Image not found. Exiting...")
        exit()

    image_name = args.image[:args.image.index('.')]
    pdf = FPDF('L' if args.landscape else 'P', 'mm', args.page_type)
    pdf.set_font(args.font)
    pdf.set_font_size(args.font_size)
    pdf.set_text_color(*args.font_color)

    counter = 0
    page_counter = 0
    while counter < args.count:
        page_counter += 1
        print(f"Writing page {page_counter}...")
        pdf.add_page()
        curr_gap_y = args.margin[1]
        for i in range(args.rows):
            curr_gap_x = args.margin[0]
            for j in range(args.cols):
                if counter < args.count:
                    pdf.image(args.image,
                              x=j * args.image_size[0] + curr_gap_x,
                              y=i * args.image_size[1] + curr_gap_y,
                              w=args.image_size[0],
                              h=args.image_size[1])
                    for tx, ty in args.number_pos:
                        pdf.text(j * args.image_size[0] + curr_gap_x + tx,
                                 i * args.image_size[1] + curr_gap_y + ty,
                                 f"{counter+1:0>4}")
                    counter += 1
                    curr_gap_x += args.gap[0]
            curr_gap_y += args.gap[1]

    print("Saving PDF...")
    pdf.output(args.out or f"{image_name}.pdf", "F")
    print("Done! Check out folder 'out'.")


if __name__ == "__main__":
    main()
