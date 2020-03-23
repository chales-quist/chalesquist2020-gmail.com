import requests
import time
import pprint
import re
import pyperclip
from bs4 import BeautifulSoup
from lxml import html
from lxml.cssselect import CSSSelector
import json
from datetime import datetime
from goto import with_goto
import csv

# please insert CSV file name into line 19 and output file name
# please create initial json file like below example

#[{"url":"","title": "", "description": "", "owner name": "", "phone number": ""}]

with open('subito.csv','rt')as f:
    data = csv.reader(f)
    for row in data:
        iurl =  str(row).strip('[]')
        iurl = iurl[1:]
        iurl = iurl[:-1]
        print(iurl)
        base_url = iurl

        file_name = "subito.json"
        print(file_name)

        now = datetime.now()
        current_time = now.strftime("%m%d%y_%H%M%S")
        print(now)

        def write_json(datas, filename=file_name): 
            with open(filename,'w') as f: 
                json.dump(datas, f, indent=4)


        @with_goto
        def Playerinfoscraper(urllast):

            url3page = requests.get(urllast, timeout=30)
            treelast = html.fromstring(url3page.content)  

            title_pre = treelast.xpath('//h1[contains(@class,"ad-info__title")]/text()')
            title_pre = str(title_pre).strip('[]')
            title_pre = title_pre[1:]
            title_pre = title_pre[:-1]

            data_file = json.load(open(file_name))
            for item in data_file:
                my_dict = {}
                my_dict = item.get('title')
                # print(my_dict)
                if my_dict == title_pre:
                    goto .end

            description = treelast.xpath('//p[contains(@class,"jsx-436795370")]/text()')
            description =  str(description).strip('[]')
            description = description[1:]
            description = description[:-1]
            name_of_owner = treelast.xpath('//p[contains(@class,"user-name")]/text()')
            name_of_owner = str(name_of_owner).strip('[]')
            name_of_owner = name_of_owner[1:]
            name_of_owner = name_of_owner[:-1]
            phone_number_id = treelast.xpath('//div[contains(@id,"contact-actions-container")]')
            for dd in phone_number_id:
                phone_number = dd.get("data-prop-phone")

            my_details = {
            'url': urllast,
            'title': title_pre,
            'description': description,
            'name of owner': name_of_owner,
            'phone number': phone_number
            }

            with open(file_name) as json_file: 
                datas = json.load(json_file) 
            # appending data to emp_details  
                datas.append(my_details) 
                write_json(datas) 
              
            # output_json.append(my_details)
            label .end

        page=requests.get(base_url)
        tree=html.fromstring(page.content)
        showcaseslist=tree.xpath('//button[contains(@class,"pagination__btn")]//span[contains(@class,"UIElements__Button--button-text-L2hvbWUv")]/text()')
        page_number = showcaseslist[2]
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')
        stored_urls = [];
        output_json = [];
        print(page_number)
        i = int(page_number) + 1
        j = 1
        while j < i:
            for link in soup.select('html body a.jsx-1356703816.link'):
                list_url = link.get('href')
                stored_urls.append(list_url)
            # print(stored_urls)
            jj = str(j+1)
            if jj == i:
                break;
            posi = base_url.index('?')
            posi = posi + 1
            insert_url = "o=" + jj + "&"
            base_urls = base_url[:posi] + insert_url + base_url[posi:]
            print(base_urls)
            page=requests.get(base_urls)
            data = page.text
            soup = BeautifulSoup(data, 'html.parser')
            j += 1
        k = 1
        for url in stored_urls:
            Playerinfoscraper(url)
            print("done%s" % k)
            k += 1
            if k % 10 ==0:
                print("please wait!")

        print("all done!")