import json
from selenium.webdriver.common.by import By
from monpetitsalon.driver import get_driver


def test_driver() -> None:
    driver = next(get_driver())
    URL = 'https://httpbin.org/anything/test_driver'
    driver.get(URL)
    json_txt = driver.find_element(By.CSS_SELECTOR, 'pre').text
    json_dict = json.loads(json_txt)
    assert json_dict.get('url') == URL
