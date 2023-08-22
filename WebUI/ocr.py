import numpy as np
from paddleocr import PaddleOCR
import cv2
import datetime


def image_ocr_match(image_path, counter_number):
    process_start = datetime.datetime.now()  # process starting time

    ocr_model = PaddleOCR(lang="ch", use_gpu=True, enable_mkldnn=True)

    # ocr_model = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=True, enable_mkldnn=True,
    #                 rec_model_dir='models/ch_PP-OCRv3_rec_infer.tar',
    #                 cls_model_dir='models/ch_ppocr_mobile_v2.0_cls_infer.tar',
    #                 det_model_dir='models/ch_PP-OCRv3_det_infer.tar')

    # OpenCV threshold process
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, 7)
    # threshole_image = cv2.threshold(gray_image, 165, 255, cv2.THRESH_BINARY)[1]
    inverted_image = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY_INV)[1]

    # OpenCV morphological transformation
    kernel = np.ones((2, 2), np.uint8)
    # opening_image = cv2.morphologyEx(inverted_image, cv2.MORPH_OPEN, kernel)
    # erode_image = cv2.erode(inverted_image, kernel, iterations=1)
    dilation_image = cv2.dilate(inverted_image, kernel, iterations=1)

    # cv2.imwrite('WebUI/opencv/' + 'P' + str(counter_number) + '.png', dilation_image)

    recognition_result = ocr_model.ocr(dilation_image)

    # result = recognition_result[0]
    #
    # data = [raw[1][0] for raw in result]

    # for result in recognition_result:
    #     print(result[1][0])

    data = recognition_result[0]

    process_finish = datetime.datetime.now()  # process finishing time

    print('Page ' + str(counter_number) + ' OCR Process Time =', (process_finish - process_start).seconds)

    return data
