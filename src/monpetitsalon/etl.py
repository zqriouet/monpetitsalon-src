import math
import time
import pendulum
from selenium.common.exceptions import NoSuchWindowException, ElementClickInterceptedException, WebDriverException
from selenium.webdriver.common.by import By
from monpetitsalon.utils import wait_for_element
from monpetitsalon.query import Query
from monpetitsalon.driver import get_driver
from monpetitsalon.parsers import CardItemParser, DetailItemParser
from monpetitsalon.scrapers import CardsPageScraper, DetailsPageScraper
from monpetitsalon.agents import CardsNavigationAgent, DetailsNavigationAgent


def extract_single_page_data(agent, driver):
    agent.wait_loading(driver)
    soup = agent.scrape(driver)
    agent.save_data()
    new_items = [agent.parse_raw_item(item) for item in soup]
    agent.add_iteration()
    return new_items


def extract_data(agent, driver, query, items=[]):
    terminated = False
    while not terminated:
        new_items = extract_single_page_data(agent, driver)
        items.extend(new_items)
        terminated = agent.terminated(driver, query.from_date)
        if not terminated:
            agent.go_to_next_page(driver)
    return items
