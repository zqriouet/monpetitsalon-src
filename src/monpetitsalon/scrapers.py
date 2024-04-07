from bs4 import BeautifulSoup

from monpetitsalon.utils import soupify


class BasePageScraper:

    def __init__(self, css_selector):
        self.css_selector = css_selector

    def scrape(self, driver):
        soup = soupify(driver)
        items = soup.select(self.css_selector)
        return items

    def scrape_file(self, file_path, binary=False):
        with open(file_path, "r" + ("b" * binary), encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, "lxml")
        items = soup.select(self.css_selector)
        return items


CardsPageScraper = BasePageScraper("div.resultsListContainer > article.sideListItem")
DetailsPageScraper = BasePageScraper("section.section-detailedSheet")
