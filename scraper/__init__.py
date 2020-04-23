import time
import traceback

from statistics import mean

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


def lexical_grade(text):
    """
    Woordhonorering
    Bron: http://abcd.windesheim.nl/CvB/Besluit_2017-023_Cum_Laude.pdf

    Kolom A             Kolom B
    Uitmuntend          10
    Zeer goed           9
    Goed                8
    Ruim voldoende      7
    Voldoende           6

    "Voldaan" is being skipped, as this grade isn't being taken into account when calculating your average grade.
    """
    text = text.lower()
    grading = {
        "uitmuntend": 10.0,
        "zeer goed": 9.0,
        "goed": 8.0,
        "ruim voldoende": 7.0,
        "voldoende": 6.0,
        "onvoldoende": 5.0,
    }

    if text == "voldaan":
        return None
    else:
        return grading[text]


def get_grades_from_webpage(educator_soup):
    grade_containers = educator_soup.find_all("div", class_="studyplanning-unit")

    if not grade_containers:
        print("Could not find any grades.")
        raise

    raw_grades = []

    print("\t----------------------------------------------------------------------------------------------------")
    print("\tYour grades:")
    print("\t----------------------------------------------------------------------------------------------------")

    for grade_container in grade_containers:
        grade_span = grade_container.find("span", class_=lambda cls: cls and "grade" in cls)
        grade_title = grade_container.find("a", class_="btn-link")

        if grade_title:
            grade_title = grade_title.text

        if grade_span:
            if "data-content" in grade_span.attrs:
                raw_grade = grade_span.attrs["data-content"]

                if raw_grade != "-":
                    raw_grades.append(raw_grade)

                    if grade_title:
                        print("\t{:40s} {:40s}".format(raw_grade, grade_title))

    return raw_grades


def parse_raw_grades(raw_grades):
    grades = []

    for raw_grade in raw_grades:
        try:
            grade = float(raw_grade)
        except Exception as e:
            # Grade not castable to float, probably be textual
            grade = lexical_grade(raw_grade)

        if grade:
            grades.append(grade)

    return grades


def get_average_grade(args):
    driver = webdriver.Chrome()

    try:
        driver.get(args.url)

        username_field = driver.find_element_by_xpath('//*[@id="userNameInput"]')
        username_field.send_keys(args.username)

        password_field = driver.find_element_by_xpath('//*[@id="passwordInput"]')
        password_field.send_keys(args.password)

        submit = driver.find_element_by_xpath('//*[@id="submitButton"]')
        submit.click()

        time.sleep(5)

        educator_soup = BeautifulSoup(driver.page_source, "lxml")
        driver.close()

        raw_grades = get_grades_from_webpage(educator_soup)
        parsed_grades = parse_raw_grades(raw_grades)

        if parsed_grades:
            return round(mean(parsed_grades), 2)
        else:
            return None

    except Exception as e:
        print(e)
        print(traceback.print_exc())
        driver.close()