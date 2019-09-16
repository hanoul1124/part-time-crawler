# -*- coding: utf-8 -*-
import json

import requests
from selenium import webdriver
from selenium.common.exceptions import *

options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
options.add_argument('--headless')

driver = webdriver.Chrome(executable_path='***/part-time-crawler/chromedriver', chrome_options=options)

secrets = json.load(open('secrets.json'))
albamon_url = secrets['URL']

driver.implicitly_wait(3)
driver.get(albamon_url)

new_alba_list = []
alba_list = driver.find_elements_by_css_selector('div.gListWrap > table > tbody > tr')

try:
    for index, alba in enumerate(alba_list):
        if '3시간전' in alba.find_element_by_css_selector('td.recently > em').text:
            new_alba_list.append(int(index))

    for index in new_alba_list:
        new_alba = driver.find_elements_by_css_selector('div.gListWrap > table > tbody > tr')[index]
        name = new_alba.find_element_by_css_selector('p.cName > a').text
        discription = new_alba.find_element_by_css_selector('p.cTit > a').text
        time = new_alba.find_element_by_css_selector('td:nth-child(4)').text
        link = new_alba.find_element_by_css_selector('p.cName > a').get_attribute('href')
        alba_text = f'{name}\n{discription}/{time}'
        alba_link = f'{link}'

        message = f'♬도향봇 신규 알바♬\n' + alba_text

        service_id = secrets["SENS_SERVICE_ID"]
        send_url = f'https://api-sens.ncloud.com/v1/sms/services/{service_id}/messages'
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "X-NCP-auth-key": secrets["X-NCP-AUTH-KEY"],
            "X-NCP-service-secret": secrets["X-NCP-SERVICE-SECRET"]
        }
        body = {
            "type": "SMS",
            "from": secrets["FROM_PHONE_NUMBER"],
            "to": [
                secrets["TO_PHONE_NUMBER"]
            ],
            "content": message
        }
        body2 = {
            "type": "SMS",
            "from": secrets["FROM_PHONE_NUMBER"],
            "to": [
                secrets["TO_PHONE_NUMBER"]
            ],
            "content": alba_link
        }

        res1 = requests.post(send_url, headers=headers, data=json.dumps(body))
        res2 = requests.post(send_url, headers=headers, data=json.dumps(body2))

except NoSuchElementException:
    service_id = secrets["SENS_SERVICE_ID"]
    send_url = f'https://api-sens.ncloud.com/v1/sms/services/{service_id}/messages'
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-NCP-auth-key": secrets["X-NCP-AUTH-KEY"],
        "X-NCP-service-secret": secrets["X-NCP-SERVICE-SECRET"]
    }
    body = {
        "type": "SMS",
        "from": secrets["FROM_PHONE_NUMBER"],
        "to": [
            secrets["TO_PHONE_NUMBER"]
        ],
        "content": 'test'
    }

    res = requests.post(send_url, headers=headers, data=json.dumps(body))


driver.quit()
driver.close()
