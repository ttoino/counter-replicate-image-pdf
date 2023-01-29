#!/usr/bin/env python3
# Dependencies: fpdf
from fpdf import FPDF
import os

FONTS_PATH = "./fonts"
IMAGES_PATH = "./images"
OUT_PATH = "./out"


def cleanup_out(remove_pdf=True):
    if not os.path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)
    for file in os.listdir(OUT_PATH):
        if not remove_pdf and file.endswith(".pdf"):
            continue
        os.remove(f"{OUT_PATH}/{file}")


if __name__ == "__main__":
    ######### PROGRAM BEHAVIOR #########
    path = "car.jpg"
    xs = [10, 30]
    ys = [10, 30]
    font_size = 10
    font = "Arial"
    color = (0, 0, 0)
    no_images = 1000
    img_width = 140
    img_height = 70
    imgs_per_row = 2
    rows_per_page = 3
    landscape = True
    margin_y = 1
    margin_x = 8
    gap_y = 1
    gap_x = 1
    cleanup_out_on_start = True
    cleanup_out_on_end = True
    #####################################

    if cleanup_out_on_start:
        cleanup_out(remove_pdf=False)

    if not os.path.exists(f"{IMAGES_PATH}/{path}"):
        print("Image not found. Exiting...")
        exit()

    image_name = path[:path.index('.')]
    image_ext = path[path.index('.') + 1:]
    pdf = FPDF('P' if not landscape else 'L', 'mm', 'A4')
    pdf.set_font(font)
    pdf.set_font_size(font_size)
    pdf.set_text_color(*color)

    counter = 0
    page_counter = 0
    while counter < no_images:
        page_counter += 1
        print(f"Writing page {page_counter}...")
        pdf.add_page()
        curr_gap_y = margin_y
        for i in range(rows_per_page):
            curr_gap_x = margin_x
            for j in range(imgs_per_row):
                if counter < no_images:
                    pdf.image(f"{IMAGES_PATH}/{image_name}.{image_ext}",
                              x=j * img_width + curr_gap_x,
                              y=i * img_height + curr_gap_y,
                              w=img_width,
                              h=img_height)
                    for tx, ty in zip(xs, ys):
                        pdf.text(j * img_width + curr_gap_x + tx,
                                 i * img_height + curr_gap_y + ty,
                                 f"{counter+1:0>4}")
                    counter += 1
                    curr_gap_x += gap_x
            curr_gap_y += gap_y

    print("Saving PDF...")
    pdf.output(f"{OUT_PATH}/{image_name}.pdf", "F")
    print("Done! Check out folder 'out'.")

    if cleanup_out_on_end:
        cleanup_out(remove_pdf=False)
