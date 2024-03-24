# from seleniumwire import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def get_driver(headless=True, browser='chrome'):
    browser = browser.lower()
    if browser == 'chrome':
        webdriver_service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=webdriver_service, options=options)
    elif browser == 'firefox':
        webdriver_service = FirefoxService(GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Firefox(service=FirefoxService(
            GeckoDriverManager().install()), options=options)
        driver = webdriver.Firefox(service=webdriver_service, options=options)
    else:
        raise ValueError('Valid browsers are chrome and firefox')
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
