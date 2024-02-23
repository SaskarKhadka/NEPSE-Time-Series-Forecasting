from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import codecs
import pandas as pd

# Path for chrome driver
# check if chrome driver has expired
chrome_driver = "D:/Development/chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

service = Service(chrome_driver)
driver = webdriver.Chrome(service=service, options=options)

website = "https://www.sharesansar.com/index-history-data"

from selenium.webdriver.support.ui import Select

df = pd.DataFrame(columns=["S.N.","Open","High","Low","Close","Change","Per Change(%)","Turnover","Date"])

# Open website
driver.get(website)

# Set from date
from_date = driver.find_element(By.ID, "fromDate")
from_date.clear()
from_date.send_keys("1990-10-12")

time.sleep(2)

# Set to date
to_date = driver.find_element(By.ID, "toDate")
to_date.clear()
to_date.send_keys("2024-02-15")

time.sleep(2)

# Click on search button
search_button = driver.find_element(By.ID, "btn_indxhis_submit")
search_button.click()

time.sleep(2)

# Select list 50 elements
select = Select(driver.find_element(By.XPATH, '//*[@id="myTable_length"]/label/select'))
select.select_by_visible_text("50")

time.sleep(5)

# Until all data is collected(until next button is not disabled) collect data
while True:
    table = driver.find_element(By.ID, "myTable")
    table_body = table.find_element(By.TAG_NAME, "tbody")
    table_rows = table_body.find_elements(By.TAG_NAME, "tr")
    for row in table_rows:
        row_elements = row.find_elements(By.TAG_NAME, "td")
        new_row = {
            "S.N.": row_elements[0].text,
            "Open": row_elements[1].text,
            "High": row_elements[2].text,
            "Low": row_elements[3].text,
            "Close": row_elements[4].text,
            "Change": row_elements[5].text,
            "Per Change(%)": row_elements[6].text,
            "Turnover": row_elements[7].text,
            "Date": row_elements[8].text, 
        }
        df.loc[len(df)] = new_row
        df.to_csv('../data/nepse_data.csv', index=None)
    # time.sleep(2)
    next_button = driver.find_element(By.ID, "myTable_next")
    is_disabled = next_button.get_property('disabled')
    if is_disabled:
        break
    next_button.click()
    time.sleep(2)
            