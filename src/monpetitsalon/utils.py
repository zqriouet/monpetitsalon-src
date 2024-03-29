import re
import unicodedata
import logging
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def replace_if_error(error, default=None, todo=logging.warning):
    def deco(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error as e:
                todo(e)
                return default
        return wrapper
    return deco


def soupify(driver):
    return BeautifulSoup(driver.page_source, 'lxml')


def textify_raw_data(items):
    return '\n'.join([str(item) for item in items])


def save_string_to_file(string, file_path, binary=False):
    with open(file_path, 'w' + ('b' * binary), encoding='utf-8') as f:
        f.write(string)


def normalize(text, form='NFKC', replace_semicolons=True):
    normalized_text = re.sub(
        '\s+', ' ', unicodedata.normalize(form, text)).strip()
    if replace_semicolons:
        return normalized_text.replace(';', ',')
    return normalized_text


def normalize_price(price):
    try:
        return int(re.sub('\s', '', re.search('(?<![\d\s,.])[\d\s,.]*(?=€)', price)[0]).replace(',', '.'))
    except Exception as e:
        print(e)
        return price


def wait_for_element(driver, css_selector, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    return element


@replace_if_error((AttributeError, TypeError))
def get_item(soup: BeautifulSoup, item_path, attribute='text'):

    if len(item_path) == 0:
        element = soup
    elif attribute == 'list':
        element = soup.select(item_path)
    else:
        element = soup.select_one(item_path)

    if attribute == 'list':
        items = [
            normalize(e.get_text(strip=True))
            for e in element
            if len(e.get_text(strip=True)) > 0
        ]
        return items
    elif attribute == 'text':
        item = element.get_text(strip=True)
    elif attribute == 'id':
        item = element[attribute].strip().replace('section-detailedSheet_', '')
    else:
        item = element[attribute].strip()
    return normalize(item)
