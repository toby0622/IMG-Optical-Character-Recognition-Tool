from OCR import *
from Search import *
from Export import *

if __name__ == "__main__":
    image_path = "Book Cover Dataset/"
    ocr_txt_output = "Cover TXT/"

    print("PIC Optical Character Recognition Process Ongoing...")
    print("Waiting...")

    for i in range(0, 1544):
        textfile = image_ocr_match(image_path, i)
        txt_export(textfile, ocr_txt_output, i)

    print("All Process Finished.\n")
