import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait


def do_login(driver):
    username = ""
    password = ""
    driver.get('https://ais.usvisa-info.com/es-co/niv/users/sign_in')
    input_email = driver.find_element(By.XPATH, '//input[@name="user[email]"]')
    input_password = driver.find_element(By.XPATH, '//input[@name="user[password]"]')

    for i in range(10):
        try:
            box = driver.find_element(By.XPATH, '//input[@name="policy_confirmed"]')
            driver.execute_script("arguments[0].click();", box)
            break
        except NoSuchElementException as e:
            print('Retry in 1 second')
            time.sleep(1)
    else:
        raise e

    input_email.send_keys(username)
    input_password.send_keys(password)
    driver.find_element(By.XPATH, '//input[@name="commit"]').click()


def do_scheduler_init(driver):
    driver.get('https://ais.usvisa-info.com/es-co/niv/schedule//appointment')
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@id="appointments_consulate_appointment_date"]').click()
    dates_available = False
    while not dates_available:
        all_dates = driver.find_elements(By.XPATH, '//table[@class="ui-datepicker-calendar"]//td')
        if len(all_dates) > 0:
            all_dates = list(filter(lambda x: "disabled" not in x.get_attribute("class"), all_dates))
            if len(all_dates) == 0:
                print("not filtered dates available")
                driver.find_element(By.XPATH, '//span[@class="ui-icon ui-icon-circle-triangle-e"]').find_element(
                    By.XPATH, './..').click()
            else:
                first_valid_date = all_dates[0]
                first_valid_date.click()
                print("some data available")
                break
        else:
            time.sleep(1)


def process():
    driver = webdriver.Chrome('/driver.zip')
    do_login(driver)
    do_scheduler_init(driver)

    print("hello")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process()
