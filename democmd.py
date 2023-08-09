from ocr import *
from export import *
from opencc import OpenCC

"""
if __name__ == "__main__":
    # image_path = "SunHan Dataset/"
    # ocr_txt_output = "SunHan Text Output/"

    # image_path = "Qing Dataset/"
    # ocr_txt_output = "Qing Text Output/"

    image_path = "Split Dataset/"
    ocr_txt_output = "Split Text Output/"

    print("PIC Optical Character Recognition Process Ongoing...")
    print("Waiting...")

    data = []
    modified = []

    cc = OpenCC('s2tw')

    # total 383 images
    for i in range(0, 383):
        textfile = image_ocr_match(image_path, i)

        for j in textfile:
            data.append(j)
            # print(j)
            # print(j[0][1][0])

        # sorting using box x-axis, from right to left
        data = sorted(data, key=lambda x: (x[0][1][0]), reverse=True)

        for d in data:
            cc.convert(str(d))
            modified.append(d[1][0])

        data.clear()

        # print(modified)

    txt_export_total(modified, ocr_txt_output)
    csv_export_total(modified, ocr_txt_output)

    # counter = 2
    #
    # for i in range(2, 11):
    #     textfile = image_ocr_match(image_path, i)
    #
    #     for j in textfile:
    #         data.append(j)
    #         print(j)
    #         print(j[0][1][0])
    #
    #     data = sorted(data, key=lambda x: (x[0][1][0]), reverse=True)
    #
    #     data = data[1][0]
    #
    #     txt_export(data, ocr_txt_output, counter)
    #     csv_export(data, ocr_txt_output, counter)
    #
    #     data.clear()
    #     counter += 1

    print("All Process Finished.\n")
"""
