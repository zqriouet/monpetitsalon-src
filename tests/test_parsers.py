import json
import os

from monpetitsalon.parsers import CardItemParser, DetailItemParser

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

CARDS_HTML_PATH = os.path.join(BASE_PATH, "data", "cards.html")
CARDS_JSON_PATH = os.path.join(BASE_PATH, "data", "cards.json")
DETAIL_HTML_PATH = os.path.join(BASE_PATH, "data", "detail.html")
DETAIL_JSON_PATH = os.path.join(BASE_PATH, "data", "detail.json")


def test_parse_card() -> None:
    cards = CardItemParser.parse_file(CARDS_HTML_PATH)
    with open(CARDS_JSON_PATH, "r", encoding="utf-8") as f:
        cards_json = json.load(f)
    assert cards == cards_json


def test_parse_detail() -> None:
    detail = DetailItemParser.parse_file(DETAIL_HTML_PATH)
    with open(DETAIL_JSON_PATH, "r", encoding="utf-8") as f:
        detail_json = json.load(f)
    assert detail == detail_json
