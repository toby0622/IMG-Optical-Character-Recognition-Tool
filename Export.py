import datetime


def txt_export(datafile, output_folder):
    # process_start = datetime.datetime.now()  # process starting time

    with open(output_folder + "Cover" + ".txt", 'w', encoding='UTF-8') as textfile:
        textfile.write(str(datafile))

    # process_finish = datetime.datetime.now()  # process finishing time


# def csv_export():
