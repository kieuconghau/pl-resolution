from MyAlgorithms import *

INPUT_FILENAME_LIST = [r'../INPUT/input_1.txt',
                       r'../INPUT/input_2.txt',
                       r'../INPUT/input_3.txt',
                       r'../INPUT/input_4.txt',
                       r'../INPUT/input_5.txt']

OUTPUT_FILENAME_LIST = [r'../OUTPUT/output_1.txt',
                        r'../OUTPUT/output_2.txt',
                        r'../OUTPUT/output_3.txt',
                        r'../OUTPUT/output_4.txt',
                        r'../OUTPUT/output_5.txt']

TESTCASE_NUMBER = len(INPUT_FILENAME_LIST)


def main():
    for index in range(TESTCASE_NUMBER):
        my_algo = MyAlgorithms()
        my_algo.read_input_data(input_filename=INPUT_FILENAME_LIST[index])
        my_algo.pl_resolution()
        my_algo.write_output_data(output_filename=OUTPUT_FILENAME_LIST[index])


if __name__ == '__main__':
    main()
