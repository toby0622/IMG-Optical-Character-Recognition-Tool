from OCR import *
from Export import *
from opencc import OpenCC


if __name__ == "__main__":
    image_path = "SunHan Dataset/"
    ocr_txt_output = "SunHan Text Output/"

    print("PIC Optical Character Recognition Process Ongoing...")
    print("Waiting...")

    data = []

    cc = OpenCC('s2tw')

    for i in range(0, 154):
        textfile = image_ocr_match(image_path, i)

        for j in textfile:
            j = cc.convert(str(j))
            data.append(j)
            # print(type(data))

    txt_export(data, ocr_txt_output)
    csv_export(data, ocr_txt_output)

    print("All Process Finished.\n")
