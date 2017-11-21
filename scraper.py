from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from config import username, password, wait_timeout, start_url, begin_date, end_date


def extract_attributes_from_by_date_range(driver, begin_date, end_date):
    """
    :param driver:  selenium webdriver object
    :param begin_date: A datetime.date object, denotes range to begin with
    :param end_date:  A datetime.date object, denotes range to end with
    :return: A list of dictionary; scraped data items
    """

    try:
        begin_date_field = driver.find_element_by_id('start_date')
    except NoSuchElementException:
        begin_date_field = driver.find_element_by_id('beginDate')

    begin_date_field.clear()
    begin_date_field.send_keys(begin_date.strftime('%Y-%m-%d'))

    try:
        end_date_field = driver.find_element_by_id('end_date')
    except NoSuchElementException:
        end_date_field = driver.find_element_by_id('endDate')

    end_date_field.clear()
    end_date_field.send_keys(end_date.strftime('%Y-%m-%d'))

    try:
        run_button = driver.find_element_by_xpath('//input[@type = "submit"]')
    except:
        run_button = driver.find_element_by_xpath('//button[@type = "submit"]')

    run_button.click()

    table = WebDriverWait(driver, wait_timeout).until(
        EC.presence_of_element_located((By.TAG_NAME, 'table'))
    )
    resources = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')

    try:
        _ = table.find_element_by_tag_name('tfoot')
    except NoSuchElementException:
        resources = resources[:-1]
    finally:
        attribute_elements = table.find_element_by_tag_name('thead').find_elements_by_tag_name('th')
        attribute_list = [i.text.lower().replace(' ', '_') for i in attribute_elements]

    return [{attr: value.text for attr, value in zip(attribute_list, resource.find_elements_by_tag_name('td'))}
            for resource in resources]


## Started from http://www.lead5media.com/

driver = webdriver.PhantomJS()
driver.set_window_size(1024, 768)
driver.get(start_url)

try:
    element = WebDriverWait(driver, wait_timeout).until(
        EC.presence_of_element_located((By.XPATH, '//a[text() = "partner login"]'))
    )
except:
    driver.save_screenshot('snapshot.png')
    driver.quit()

element.click()

## Redirected to www.upward.net

driver.execute_script("$('.signInWrapper').toggleClass('open'); return false;")

driver.find_element_by_id('username').send_keys(username)
driver.find_element_by_id('password').send_keys(password)

driver.find_element_by_id('submit').submit()

# Got a logged in session

tabs_length = len(driver.find_element_by_class_name("nav-list").find_elements_by_tag_name('a'))

while tabs_length:
    tab_root = WebDriverWait(driver, wait_timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'nav-list'))
    )

    tab_root.find_elements_by_tag_name('a')[tabs_length - 1].click()

    data_list = extract_attributes_from_by_date_range(driver, begin_date, end_date)

    print(data_list)
    tabs_length -= 1

driver.quit()
