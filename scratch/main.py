import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import base64
import time
import pandas as pd
import pdfplumber

''' Input Definition '''
# firm: the insurance is sold by which firm
# target: the target insurance's name
# inMarket: whether or not the insurance is currently available in the market

def Scratch_GP_File(firm, target, inMarket=True):
    with webdriver.Chrome(executable_path='C:\\Users\\shih\\ActuaViz\\scratch\\chromedriver_win32\\chromedriver.exe') as driver:
        url = 'http://insprod1.tii.org.tw/database/insurance/query.asp'
        driver.get(url)
        driver.implicitly_wait(5)
        Login(driver, firm, target, inMarket)
        driver.implicitly_wait(5)
        DownloadPDF(driver, firm, target)
    df = PDFtoDataFrame(firm, target)
    try:
        os.remove('captcha_login.png')
    except OSError as e:
        print(str(e))
    try:
        os.remove(f'{firm}_{target}_GP.pdf')
    except OSError as e:
        print(str(e))
    return df

def Login(driver, firm, target, inMarket=True):
    firm_ele = Select(driver.find_element(By.NAME, 'CompanyID'))
    firm_ele.select_by_value(firm)
    inMarket_ele = driver.find_element(By.ID, 'endDate2')
    if inMarket:
        inMarket_ele.click()
    target_ele = driver.find_element(By.NAME, 'fQueryAll')
    target_ele.send_keys(target)
    captcha_text = getCaptcha(driver)
    captcha_ele = driver.find_element(By.NAME, 'bmpC')
    captcha_ele.send_keys(captcha_text)
    login_ele = driver.find_element(By.ID, 'Go2225')
    login_ele.click()

def getCaptcha(driver):
    img_base64 = driver.execute_script('''
    var ele = arguments[0];
    var cnv = document.createElement('canvas');
    cnv.width = ele.width; cnv.height = ele.height;
    cnv.getContext('2d').drawImage(ele, 0, 0);
    return cnv.toDataURL('image/jpeg').substring(22);    
    ''', driver.find_element(By.XPATH, '//img[@src="bmp.asp"]'))
    with open('captcha_login.png', 'wb') as image:
        image.write(base64.b64decode(img_base64))
    file = {'file': open('captcha_login.png', 'rb')}
    api_key = 'e468dc37ee8e7682b9f0facf2d2be7c9'
    data = {
        'key': api_key,
        'method': 'post'
    }
    with requests.post('http://2captcha.com/in.php', files=file, data=data) as response:
        if response.ok and response.text.find('OK') > -1:
            captcha_id = response.text.split('|')[1]
            for i in range(10):
                response = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')
                if response.text.find('CAPCHA_NOT_READY') > -1:
                    time.sleep(5)
                elif response.text.find('OK') > -1:
                    return response.text.split('|')[1]
                else:
                    print('Get validation code failed')
        else:
            print('Post validation code failed')

def DownloadPDF(driver, firm, target):
    a = driver.find_element(By.CLASS_NAME, 'link01')
    a.click()
    driver.implicitly_wait(5)
    a = driver.find_element(By.PARTIAL_LINK_TEXT, '-C.pdf')
    url = a.get_attribute('href')
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    try:
        with requests.get(url, headers=headers, timeout=10) as response:
            if response.status_code == 200:
                with open(f'{firm}_{target}_GP.pdf', 'wb') as pdf:
                    pdf.write(response.content)
            else:
                print('Response error')
    except requests.ConnectionError as conn_ex:
        print(str(conn_ex))
    except requests.Timeout as timeout_ex:
        print(str(timeout_ex))
    except requests.RequestException as request_ex:
        print(str(request_ex))
    except Exception as e:
        print(str(e))

def PDFtoDataFrame(firm, target):
    cols = ['id', 'Age', 'Gender', 'PPP', 'GP']
    df = pd.DataFrame(columns=cols)
    PPPs = [6, 10, 15, 20]
    id = 0
    with pdfplumber.open(f'{firm}_{target}_GP.pdf') as pdf:
        for page in pdf.pages:
            table = page.extract_tables()[0]
            for row in table:
                if not (row[0] == '投保' or row[0] == '年齡'):
                    x = int(row[0])
                    for index, value in enumerate(row):
                        if index > 0 and value:
                            data = [[id, x, 1 if (index - 1) // 4 == 0 else 2, PPPs[index % 4 - 1], int(value.replace(',', ''))]]
                            next = pd.DataFrame(data, columns=cols)
                            df = pd.concat([df, next])
                            id += 1
    return df