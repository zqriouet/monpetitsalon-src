import pytest
import pendulum
from selenium.webdriver.common.by import By
from monpetitsalon.utils import wait_for_element
from monpetitsalon.query import Query
from monpetitsalon.driver import get_driver
from monpetitsalon.scrapers import CardsPageScraper
from monpetitsalon.agents import CardsNavigationAgent, DetailsNavigationAgent
from monpetitsalon.etl import extract_data

headless = True


@pytest.fixture
def query():
    rent_sale, zipcodes, from_date = 'location', [
        75, 92, 93, 94], pendulum.now("Europe/Paris").add(days=-10)
    return Query(rent_sale, zipcodes, from_date)


def test_extract_cards(query):
    max_pages = 2
    cards_agent = CardsNavigationAgent(query, None, max_it=max_pages)
    driver = next(get_driver(headless))
    driver.get(query.url)
    cards_agent.reject_cookies(driver)
    cards = extract_data(cards_agent, driver, query, items=[])
    assert len(cards) == max_pages * 24


# @pytest.mark.flaky(reruns=3, reruns_delay=5)
def test_extract_details(query):
    max_it = 5
    details_agent = DetailsNavigationAgent(query, None, max_it=max_it)
    driver = next(get_driver(headless))
    driver.get(query.url)
    details_agent.reject_cookies(driver)
    wait_for_element(driver, CardsPageScraper.css_selector, 10)
    driver.find_elements(by=By.CSS_SELECTOR,
                         value=CardsPageScraper.css_selector)[-1].click()
    details = extract_data(details_agent, driver, query, items=[])
    assert len(details) == max_it
