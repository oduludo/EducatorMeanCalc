import argparse

import scraper
from cli import welcome


if __name__ == '__main__':
    welcome()

    parser = argparse.ArgumentParser(description='Calculate the average grade from an Educator webpage.')
    parser.add_argument('username', type=str, help='Username for the Educator account.')
    parser.add_argument('password', type=str, help='Password for the Educator account.')
    parser.add_argument('url', type=str, help='A URL which points to <your school\'s domain>/studyprogress')
    args = parser.parse_args()

    average_grade = scraper.get_average_grade(args)

    print("\n\t----------------------------------------------------------------------------------------------------")
    if average_grade:
        print("\tAverage grade is: {0}".format(average_grade))
    else:
        print("\tFailed to calculate average grade.")
    print("\t----------------------------------------------------------------------------------------------------")
