import pendulum
from bs4 import BeautifulSoup

from monpetitsalon.utils import get_item, replace_if_error

CARD_DATA_PATHS = {
    "listing_id": "",
    "url": "a.detailedSheetLink",
    "title": "span.ad-overview-details__ad-title",
    "address": "span.ad-overview-details__address-title",
    "price": "span.ad-price__the-price",
    "price_down": "div.ad-price__price-evolution",
    "description": "div.ad-overview-description",
    "publication_date": "div.photoPublicationDate",
    "modification_date": "div.photoModificationDate",
    "reference": "div.reference",
    "photo_url": "img.img__image",
    "photos_counter": "div.ad-overview-photo__photos-counter",
}

CARD_DATA_ATTRIBUTES = {
    "listing_id": "data-id",
    "url": "href",
    "publication_date": "title",
    "modification_date": "title",
    "price_down": "title",
    "reference": "title",
    "photo_url": "src",
}

DETAIL_DATA_PATHS = {
    "listing_id": "",
    # 'title': 'span.ad-overview-details__ad-title',
    # 'address': 'span.ad-overview-details__address-title',
    # 'price': 'span.ad-price__the-price',
    # 'price_down': 'div.ad-price__price-evolution',
    # 'description': 'div.ad-overview__description',
    # 'publication_date': 'div.photoPublicationDate',
    # 'modification_date': 'div.photoModificationDate',
    # 'reference': 'div.reference',
    "with_charges": "span.ad-price__per-month",
    "charges": "div.ad-price__fees-infos",
    "phone_in_listing": "span.showPhoneNumber",
    "energy_consumption_value": "p.energy-consumption__value",
    "energy_consumption_date": "p.energy-consumption__date",
    "dpe_value": "div.energy-diagnostic__dpe span.energy-diagnostic-rating__value, div.dpe-data > div.value > span:first-child",
    "dpe_class": "div.energy-diagnostic__dpe span.energy-diagnostic-rating__classification, div.dpe-line__classification > span > div:first-child",
    "ges_value": "div.energy-diagnostic__ges span.energy-diagnostic-rating__value, div.ges-data > div.value > span",
    "ges_class": "div.energy-diagnostic__ges span.energy-diagnostic-rating__classification, div.ges-line__classification > span",
    "agency_name": "div.contact-name, div.agency-overview__info-name",
    "agency_address": "div.contact-address, div.agency-overview__info-address",
    "agency_phone_nb": "span.phone-contact-info__phone-to-display",
    "details": "section.detailsSection_aboutThisProperty div.allDetails div.labelInfo",
    "extra_details": "section.detailsSection_aboutThisAd div.allDetails div.labelInfo",
}

DETAIL_DATA_ATTRIBUTES = {
    "listing_id": "id",
    "modification_date": "title",
    "phone_in_listing": "data-phone",
    "details": "list",
    "extra_details": "list",
}


class BaseItemParser:

    def __init__(self, data_paths, data_attributes, css_selector):
        self.data_paths = data_paths
        self.data_attributes = data_attributes
        self.css_selector = css_selector

    def get_item(self, soup, item_key):
        item = get_item(
            soup,
            self.data_paths.get(item_key),
            self.data_attributes.get(item_key) or "text",
        )
        return item

    def get_id(self, soup):
        return self.get_item(soup, "listing_id")

    @replace_if_error((AttributeError, TypeError))
    def parse_raw_item(self, soup):
        parsed_raw_item = {
            item_key: self.get_item(soup, item_key)
            for item_key in self.data_paths.keys()
        }
        return parsed_raw_item

    def parse_file(self, file_path, binary=False):
        with open(file_path, "r" + ("b" * binary), encoding="utf-8") as fp:
            soup = BeautifulSoup(fp, "lxml")
        soups = soup.select(self.css_selector)
        items = [self.parse_raw_item(item) for item in soups]
        return items

    def parse_modification_date(self, soup):
        modification_dates = [
            pendulum.from_format(
                e["title"].replace("1er", "1"),
                "D MMMM YYYY HH:mm:ss",
                locale="fr",
            )
            for e in soup.select(self.data_paths.get("modification_date"))
        ]
        return max(modification_dates)


CardItemParser = BaseItemParser(
    CARD_DATA_PATHS, CARD_DATA_ATTRIBUTES, "article.sideListItem"
)
DetailItemParser = BaseItemParser(
    DETAIL_DATA_PATHS, DETAIL_DATA_ATTRIBUTES, "section.section-detailedSheet"
)
