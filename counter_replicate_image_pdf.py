#!/usr/bin/env python3
# Dependencies: fpdf, pillow
from argparse import ArgumentParser
from fpdf import FPDF
from math import floor
import os


def get_args():
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "image",
        help="the image to add to the pdf",
    )
    arg_parser.add_argument(
        "count",
        type=int,
        help="the number of images to add to the pdf",
    )
    arg_parser.add_argument(
        "-o",
        "--out",
        help="where to save the pdf",
    )

    font_opts = arg_parser.add_argument_group("font options")
    font_opts.add_argument(
        "-f",
        "--font",
        default="Arial",
        help="the font to use for the counter",
    )
    font_opts.add_argument(
        "-fs",
        "--font-size",
        type=float,
        default=12,
        help="the font size to use for the counter, in pt",
    )
    font_opts.add_argument(
        "-fc",
        "--font-color",
        type=int,
        nargs=3,
        metavar=("RED", "GREEN", "BLUE"),
        default=[0, 0, 0],
        help="the font color to use for the counter",
    )

    page_opts = arg_parser.add_argument_group("page options")
    page_opts.add_argument(
        "-l",
        "--landscape",
        action="store_true",
        help="sets the page to landscape",
    )
    page_opts.add_argument(
        "-p",
        "--page-type",
        default="A4",
        help="the page type to use",
    )

    pos_opts = arg_parser.add_argument_group("position options")
    pos_opts.add_argument(
        "-s",
        "--image-size",
        type=float,
        nargs=2,
        metavar=("WIDTH", "HEIGHT"),
        default=[100, 100],
        help="the size of the image, in mm, use 0 for auto",
    )
    pos_opts.add_argument(
        "-n",
        "--number",
        type=float,
        nargs=2,
        metavar=("X", "Y"),
        action="append",
        default=[],
        help="adds a counter at that position, in mm, "
        "numbers between 0 and 1 are interpreted as relative to the image size",
    )

    margin = pos_opts.add_mutually_exclusive_group()
    margin.add_argument(
        "-m",
        "--margin",
        type=float,
        nargs=2,
        metavar=("MARGIN_X", "MARGIN_Y"),
        default=[0, 0],
        help="adds a margin around the images, in mm",
    )
    margin.add_argument(
        "-ma",
        "--margin-auto",
        action="store_true",
        help="automatically adds a margin around the images",
    )

    gap = pos_opts.add_mutually_exclusive_group()
    gap.add_argument(
        "-g",
        "--gap",
        type=float,
        nargs=2,
        metavar=("GAP_X", "GAP_Y"),
        default=[0, 0],
        help="adds a gap between the images, in mm",
    )
    gap.add_argument(
        "-ga",
        "--gap-auto",
        action="store_true",
        help="automatically adds a gap between the images",
    )

    rows = pos_opts.add_mutually_exclusive_group()
    rows.add_argument(
        "-r",
        "--rows",
        type=int,
        default=1,
        help="the number of rows per page",
    )
    rows.add_argument(
        "-ra",
        "--rows-auto",
        action="store_true",
        help="calculates the number of rows per page automatically",
    )

    cols = pos_opts.add_mutually_exclusive_group()
    cols.add_argument(
        "-c",
        "--cols",
        type=int,
        default=1,
        help="the number of columns per page",
    )
    cols.add_argument(
        "-ca",
        "--cols-auto",
        action="store_true",
        help="calculates the number of cols per page automatically",
    )

    return arg_parser.parse_args()


def main():
    args = get_args()

    if not os.path.exists(args.image):
        print("Image not found. Exiting...")
        exit()

    pdf = FPDF('L' if args.landscape else 'P', 'mm', args.page_type)
    pdf.set_font(args.font)
    pdf.set_font_size(args.font_size)
    pdf.set_text_color(*args.font_color)

    if args.cols_auto:
        args.cols = floor(pdf.w / args.image_size[0])
    if args.rows_auto:
        args.rows = floor(pdf.h / args.image_size[1])

    if args.gap_auto and args.margin_auto:
        args.margin = [
            (pdf.w - args.cols * args.image_size[0]) / (args.cols + 1),
            (pdf.h - args.rows * args.image_size[1]) / (args.rows + 1)
        ]
        args.gap = args.margin
    elif args.gap_auto:
        args.gap = [
            (pdf.w - args.cols * args.image_size[0] - args.margin[0] * 2) /
            (args.cols - 1),
            (pdf.h - args.rows * args.image_size[1] - args.margin[1] * 2) /
            (args.rows - 1)
        ]
    elif args.margin_auto:
        args.margin = [(pdf.w - args.cols * args.image_size[0] -
                        (args.cols - 1) * args.gap[0]) / 2,
                       (pdf.h - args.rows * args.image_size[1] -
                        (args.rows - 1) * args.gap[1]) / 2]

    for i in range(args.count):
        col = i % args.cols
        row = (i // args.cols) % args.rows

        if col == 0 and row == 0:
            pdf.add_page()

        x = args.margin[0] + col * (args.gap[0] + args.image_size[0])
        y = args.margin[1] + row * (args.gap[1] + args.image_size[1])

        pdf.image(args.image, x, y, args.image_size[0], args.image_size[1])

        for tx, ty in args.number:
            if 0 <= tx < 1:
                tx *= args.image_size[0]
            if 0 <= ty < 1:
                ty *= args.image_size[1]

            pdf.text(x + tx, y + ty, f"{i+1:0>4}")

    pdf.output(args.out or '')


if __name__ == "__main__":
    main()
