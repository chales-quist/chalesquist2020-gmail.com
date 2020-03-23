import requests
import time
import pprint
import re
import csv
import pyperclip
from bs4 import BeautifulSoup
from lxml import html
from lxml.cssselect import CSSSelector
import json
from datetime import datetime
import urllib3
from functools import partial
import lxml.html
from goto import with_goto
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# please insert CSV file name into line 24 and output file name
# please create initial json file like below example

#[{"url":"","title": "", "description": "", "owner name": "", "phone number": ""}]

with open('bakeca.csv','rt')as f:
    data = csv.reader(f)
    for row in data:
        iurl =  str(row).strip('[]')
        iurl = iurl[1:]
        iurl = iurl[:-1]
        print(iurl)
        base_url = iurl
        length = len(base_url) + 1

        file_name = "bakeca.json"
        print(file_name)

        now = datetime.now()
        current_time = now.strftime("%m%d%y_%H%M%S")
        print(now)

        def write_json(datas, filename=file_name): 
            with open(filename,'w') as f: 
                json.dump(datas, f, indent=4)

        @with_goto
        def Playerinfoscraper(urllast):
            http = urllib3.PoolManager()
            responses = http.request('GET', urllast)
            soups = BeautifulSoup(responses.data, 'lxml')
            for title_pres in soups.select('div.b-dett-title h1'):
                title_pre = title_pres.getText()

            data_file = json.load(open(file_name))
            for item in data_file:
                my_dict = {}
                my_dict = item.get('title')
                if my_dict == title_pre:
                    goto .end

            for descriptions in soups.select('div.b-dett-block-content div.b-dett-description'):
                description = descriptions.getText()
                description = description[25:]
            name_of_owner = "Privato"
            # print("ddd")
            phone_number = []
            for phone_numbers in soups.select('div.b-dett-contacts-telefoni p strong'):
                phone = phone_numbers.getText()
                phone_number.append(phone)
            phone_number = str(phone_number).strip('[]')
            phone_number = phone_number.replace("'", "")
            
            my_details = {
            'url': urllast,
            'title': title_pre,
            'description': description,
            'name of owner': name_of_owner,
            'phone number': phone_number
            }
            output_json.append(my_details)

            with open(file_name) as json_file:
                datas = json.load(json_file)
                datas.append(my_details)
                write_json(datas)
            label .end

        http = urllib3.PoolManager()
        response = http.request('GET', base_url)
        soup = BeautifulSoup(response.data, 'lxml')

        # soup = BeautifulSoup(data, 'html.parser')
        stored_urls = [];
        output_json = [];
        title_pre = "hello";
        # print(page_number)
        i = 25
        j = 1
        while j < i:
            for link in soup.select('div.b-ann-item-unico figure a'):
                list_url = link.get('href')
                stored_urls.append(list_url)
            # print(stored_urls)
            jj = str(j + 1)
            insert_url = "page/" + jj + "/"
            base_urls = base_url[:length] + insert_url
            print(base_urls)
            response = http.request('GET', base_urls)
            # tree=html.fromstring(page.content)
            soup = BeautifulSoup(response.data, 'lxml')
            j += 1
        k = 1
        for url in stored_urls:
            Playerinfoscraper(url)
            if title_pre == "":
                break;
            print("done%s" % k)
            k += 1
            if k % 10 ==0:
                print("please wait!")


        print("all done!")