from OCR import *
from Export import *
from opencc import OpenCC


if __name__ == "__main__":
    # image_path = "SunHan Dataset/"
    # ocr_txt_output = "SunHan Text Output/"

    image_path = "Qing Dataset/"
    ocr_txt_output = "Qing Text Output/"

    print("PIC Optical Character Recognition Process Ongoing...")
    print("Waiting...")

    data = []

    cc = OpenCC('s2tw')

    # for i in range(0, 154):
    #     textfile = image_ocr_match(image_path, i)
    #
    #     for j in textfile:
    #         j = cc.convert(str(j))
    #         data.append(j)

    counter = 2

    for i in range(2, 11):
        textfile = image_ocr_match(image_path, i)

        for j in textfile:
            j = cc.convert(str(j))
            data.append(j)

        txt_export(data, ocr_txt_output, counter)
        csv_export(data, ocr_txt_output, counter)

        data.clear()
        counter += 1

    print("All Process Finished.\n")
