from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

# from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def get_driver(headless=True, remote_host=None, browser="chrome"):
    browser = browser.lower()
    if browser == "chrome":
        webdriver_service = ChromeService(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("enable-automation")
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--dns-prefetch-disable")
            options.add_argument("--disable-gpu")
        if remote_host:
            driver = webdriver.Remote(
                command_executor=f"http://{remote_host}:4444/wd/hub", options=options
            )
        else:
            driver = webdriver.Chrome(service=webdriver_service, options=options)
    # elif browser == 'firefox':
    #     webdriver_service = FirefoxService(GeckoDriverManager().install())
    #     options = webdriver.FirefoxOptions()
    #     if headless:
    #         options.add_argument('--headless=new')
    #     options.add_argument('--no-sandbox')
    #     options.add_argument('--disable-dev-shm-usage')
    #     if remote_host:
    #         driver = webdriver.Remote(
    #             command_executor=f'http://{remote_host}:4444/wd/hub', options=options)
    #     else:
    #         driver = webdriver.Firefox(
    #             service=webdriver_service, options=options)
    # else:
    #     raise ValueError('Valid browsers are chrome and firefox')
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(20)
    return driver
    # yield driver
    # driver.quit()
