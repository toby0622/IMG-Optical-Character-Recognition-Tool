from paddleocr import PaddleOCR
import datetime


def image_ocr_match(image_path, counter_number):
    process_start = datetime.datetime.now()  # process starting time

    # "use_angle_cls=False" means not to use self-trained datasets
    ocr_model = PaddleOCR(use_angle_cls=False, lang="ch", use_gpu=False)

    # "use_angle_cls=True" means to apply other trained datasets or models
    # the one you would like to apply should be store in "models" folder

    # ocr = PaddleOCR(use_angle_cls=True,lang="ch",
    #                 rec_model_dir='../models/ch_PP-OCRv3_rec_slim_infer/',
    #                 cls_model_dir='../models/ch_ppocr_mobile_v2.0_cls_slim_infer/',
    #                 det_model_dir='../models/ch_PP-OCRv3_det_slim_infer/')

    actual_image_path = image_path + "P" + str(counter_number) + ".jpg"

    recognition_result = ocr_model.ocr(actual_image_path)

    result = recognition_result[0]

    data = [raw[1][0] for raw in result]

    # for result in recognition_result:
    #     print(result[1][0])

    process_finish = datetime.datetime.now()  # process finishing time

    print('Page ' + str(counter_number + 1) + ' OCR Process Time =', (process_finish - process_start).seconds)

    return data
