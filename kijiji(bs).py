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

with open('kijiji.csv','rt')as f:
    data = csv.reader(f)
    for row in data:
        iurl =  str(row).strip('[]')
        iurl = iurl[1:]
        iurl = iurl[:-1]
        print(iurl)
        base_url = iurl

        file_name = "kijiji.json"
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

            title_pre = treelast.xpath('//div/header//h1[contains(@class,"vip__title")]/text()')
            title_pre = str(title_pre).strip('[]')
            title_pre = title_pre.replace("                                ","")
            title_pre = title_pre[7:]
            title_pre = title_pre[:-3]

            data_file = json.load(open(file_name))
            for item in data_file:
                my_dict = {}
                my_dict = item.get('title')
                if my_dict == title_pre:
                    goto .end

            description = treelast.xpath('//p[contains(@class,"vip__text-description")]/text()')
            description = str(description).strip('[]')
            description = description[1:]
            description = description[:-1]
            try:
                name_of_owner = treelast.xpath('//div[contains(@class,"title")]/text()')[0]
                name_of_owner = str(name_of_owner).strip('[]')
            except:
                name_of_owner = "N/A"
            # print("ddd")
            try:
                phone_number = treelast.xpath('//h3[contains(@class,"modal-phone__text")]/text()')
                phone_number = str(phone_number).strip('[]')
                phone_number = phone_number[27:]
                phone_number = phone_number[:-23]
                # print("aaa")
            except:
                phone_number="N/A"

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

        page=requests.get(base_url)
        tree=html.fromstring(page.content)
        showcaseslist=tree.xpath('//span[contains(@class,"last-page")]/text()')
        page_number = str(showcaseslist).strip('[]')
        page_number = page_number.replace("'","")
        data = page.text
        soup = BeautifulSoup(data, 'html.parser')
        stored_urls = [];
        output_json = [];
        i = int(page_number) + 1
        j = 1
        while j < i:
            for link in tree.xpath('//ul[@id="search-result"]/li[@data-id]'):
                list_url = link.get('data-href')
                stored_urls.append(list_url)
            # print(stored_urls)
            jj = str(j+1)
            if jj == i:
                break;
            posi = base_url.index('?') + 1
            insert_url = "p=" + jj + "&"
            base_urls = base_url[:posi] + insert_url + base_url[posi:]
            print(base_urls)
            page=requests.get(base_urls)
            tree=html.fromstring(page.content)
            # soup = BeautifulSoup(data, 'html.parser')
            j += 1
        # print(stored_urls)
        k = 1
        for url in stored_urls:
            Playerinfoscraper(url)
            print("done%s" % k)
            k += 1
            if k % 10 == 0:
                print("please wait!")

        print("all done!")