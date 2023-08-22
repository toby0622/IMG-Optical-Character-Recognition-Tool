import datetime
import csv


def txt_export_web(datafile):
    # process_start = datetime.datetime.now()  # process starting time

    storage_path = "download/output.txt"

    text_file = open(storage_path, 'w', encoding='UTF-8')

    # with open(output_folder + "SunHan" + ".txt", 'w', encoding='UTF-8') as textfile:
    #     textfile.write(str(datafile))

    text_file.write(datafile)
    text_file.close()

    # process_finish = datetime.datetime.now()  # process finishing time


def json_export_web(datafile):
    # process_start = datetime.datetime.now()  # process starting time

    storage_path = "download/output.json"

    text_file = open(storage_path, 'w', encoding='UTF-8')

    # with open(output_folder + "SunHan" + ".txt", 'w', encoding='UTF-8') as textfile:
    #     textfile.write(str(datafile))

    text_file.write(datafile)
    text_file.close()

    # process_finish = datetime.datetime.now()  # process finishing time


def txt_export_total(datafile, output_folder):
    # process_start = datetime.datetime.now()  # process starting time

    text_file = open(output_folder + "SunHan" + ".txt", 'w', encoding='UTF-8')

    # with open(output_folder + "SunHan" + ".txt", 'w', encoding='UTF-8') as textfile:
    #     textfile.write(str(datafile))

    for data in datafile:
        text_file.write(str(data))

    text_file.close()

    # process_finish = datetime.datetime.now()  # process finishing time


def csv_export_total(datafile, output_folder):
    # process_start = datetime.datetime.now()  # process starting time

    with open(output_folder + "SunHan" + ".csv", 'w', encoding='UTF-8', newline='') as textfile:
        writer = csv.writer(textfile)

        writer.writerow(datafile)

    # process_finish = datetime.datetime.now()  # process finishing time
