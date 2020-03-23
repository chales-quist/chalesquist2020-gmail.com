import csv
import sys
import re
import os
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import InvalidArgumentException

from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver

import requests
from bs4 import BeautifulSoup

import time

now = datetime.now()
current_time = now.strftime("%m%d%y_%H%M%S")
print(now)
output_file = "bekeca(" + current_time + ").json"
print(output_file)


# def add_csv_head():
#     with open(output_file, 'w', newline='') as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow(['Title', 'Description', 'Name of owner', 'phone number'])

# def add_csv_row(title_pre, description, name_of_owner, phone_number):

#     with open(output_file, 'a', newline='', encoding="utf-8") as csv_file:
#         writer = csv.writer(csv_file)
#         writer.writerow([title_pre, description, name_of_owner, phone_number])

# add_csv_head()

driver = selenium.webdriver.Chrome()

base_url = 'https://roma.bakeca.it/annunci/offro-casa/inserzionistacase/privato/'

driver.get(base_url)
time.sleep(10)
driver.implicitly_wait(30)

# element=driver.find_element_by_xpath('//span[@class="last-page"]')

# print(element.text)

# i=driver.find_elements_by_css_selector('span.last-page').text


j = 1
time.sleep(10)
stored_urls = [];
output_json=[];
while j<30:

    urls=driver.find_elements_by_css_selector('div.b-j-linkannuncio>figure>a')
    print(urls)
    # time.sleep(10)
    # driver.implicitly_wait(20)
    for url in urls:

        list_url=url.get_attribute('href')
        stored_urls.append(list_url)
        time.sleep(1)
    next_button = driver.find_element_by_css_selector("div.b-succLink>a.b-btn")
    button = next_button.get_attribute("href")
    if button == 'javascript:void(0);':
        break;
    driver.execute_script("arguments[0].click();", next_button)
    time.sleep(5)
    j += 1;

for url in stored_urls:
    driver.get(url)
    time.sleep(20)

    title_pre=driver.find_element_by_css_selector("div.b-dett-title>h1").text
    print(title_pre)
    description=driver.find_element_by_css_selector("div.b-dett-block-content>div.b-dett-description").text
    print(description)
    name_of_owner=driver.find_elements_by_css_selector("strong.b-dett-meta-value")[1].text
    print(name_of_owner)
    try:
        phone_button=driver.find_element_by_css_selector("a.b-j-telefono")
        driver.execute_script("arguments[0].click();", phone_button)
        phone_number=driver.find_element_by_css_selector("div.btn-telefono>p>strong").text
    except:
        phone_number="N/A"

    print(phone_number)
    
    my_details = {
        'title': title_pre,
        'description': description,
        'name of owner': name_of_owner,
        'phone number': phone_number
    }

    output_json.append(my_details)

with open('bekeca.json', 'w') as json_file:
    json.dump(output_json, json_file)

    # add_csv_row(title_pre, description, name_of_owner, phone_number)

print("done")



