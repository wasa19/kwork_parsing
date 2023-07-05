import requests
from bs4 import BeautifulSoup
import csv
from time import sleep

from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0'
}

def get_full_html(url='https://triopol.by/catalog/laminat/'):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    service = ChromeService(executable_path='/home/wasa/PythonProjects/Scrapping/Kwork/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Proxy;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
    '''
    })

    driver.maximize_window()
    driver.get(url=url)
    sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[5]/div/div/a').click()
    sleep(3)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[5]/div[3]/ul/div[2]/ul/li[2]/a').click()
    sleep(5)
    html = driver.page_source
    sleep(10)
    with open('tripol.html', 'w') as f:
        f.write(html)

def find_urls():
    urls_list = []
    with open('/home/wasa/PythonProjects/Scrapping/tripol.html', 'r') as f:
        src = f.read()
        soup = BeautifulSoup(src, 'lxml')
        all_urls = soup.find_all('li', class_='col-lg-2')
        for g_url in all_urls:
            url = g_url.find('a', class_='product-name').get('href').strip()
            url = 'https://triopol.by' + url
            if url not in urls_list:
                urls_list.append(url)
    print(len(urls_list))
    return urls_list[767:770]


def get_info(urls_list):
    res_list = []
    
    for item_url in urls_list:
        resp = requests.get(item_url, headers=headers, timeout=2).text
        try:
            soup = BeautifulSoup(resp, 'lxml')
            name = soup.find('h1', class_='name__product').text.strip()
            res_dict = {}
            res_dict['name'] = name
            res_list.append(res_dict)
        except Exception as e:
            pass

    print(res_list)
    return res_list



def main():
    # get_full_html('https://triopol.by/catalog/laminat/')
    get_info(find_urls())


if __name__ == '__main__':
    main()