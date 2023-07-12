from OCR import *
from Search import *
from Export import *

if __name__ == "__main__":
    image_path = "Book Cover Dataset/"
    ocr_txt_output = "Cover TXT/"

    print("PIC Optical Character Recognition Process Ongoing...")
    print("Waiting...")

    data = []

    # book cover ocr
    for i in range(0, 1544):
        textfile = image_ocr_match(image_path, i)
        data.append(textfile)

    txt_export(data, ocr_txt_output)

    print("All Process Finished.\n")
