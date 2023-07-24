import datetime
import csv


def txt_export(datafile, output_folder, counter):
    # process_start = datetime.datetime.now()  # process starting time

    with open(output_folder + "Qing" + str(counter) + ".txt", 'w', encoding='UTF-8') as textfile:
        textfile.write(str(datafile))

    # process_finish = datetime.datetime.now()  # process finishing time


def txt_export_total(datafile, output_folder):
    # process_start = datetime.datetime.now()  # process starting time

    with open(output_folder + "SunHan" + ".txt", 'w', encoding='UTF-8') as textfile:
        textfile.write(str(datafile))

    # process_finish = datetime.datetime.now()  # process finishing time


def csv_export(datafile, output_folder, counter):
    # process_start = datetime.datetime.now()  # process starting time

    with open(output_folder + "Qing" + str(counter) + ".csv", 'w', encoding='UTF-8', newline='') as textfile:
        writer = csv.writer(textfile)

        writer.writerow(datafile)

    # process_finish = datetime.datetime.now()  # process finishing time


def csv_export_total(datafile, output_folder):
    # process_start = datetime.datetime.now()  # process starting time

    with open(output_folder + "SunHan" + ".csv", 'w', encoding='UTF-8', newline='') as textfile:
        writer = csv.writer(textfile)

        writer.writerow(datafile)

    # process_finish = datetime.datetime.now()  # process finishing time
