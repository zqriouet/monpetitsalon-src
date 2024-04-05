import json
import logging
import os
import time
from typing import List

import pendulum
from airflow.decorators import dag, task, task_group
from airflow.models import Variable
from airflow.utils.dates import days_ago
from monpetitsalon.agents import CardsNavigationAgent, DetailsNavigationAgent
from monpetitsalon.driver import get_driver
from monpetitsalon.etl import extract_cards, extract_details
from monpetitsalon.query import Query

HEADLESS, REMOTE_HOST = True, None
zipcodes = [75, 92, 93, 94]


@dag(
    dag_id="etl",
    schedule="@hourly",
    start_date=days_ago(0),
    catchup=False,
    tags=["etl"],
)
def etl():

    @task(task_id="get_extraction_dates")
    def get_extraction_dates():
        try:
            from_date = Variable.get(key="TO_DATE")
        except KeyError:
            from_date = pendulum.now("Europe/Paris").add(hours=-10)
        to_date = pendulum.now("Europe/Paris")
        return {"FROM_DATE": from_date, "TO_DATE": to_date}

    @task(task_id="etl-cards")
    def scrape_cards(rent_sale: str, zipcodes: List[int], dates: dict):
        query = Query(rent_sale, zipcodes, dates.get("FROM_DATE"))
        cards_agent = CardsNavigationAgent(query, None)
        cards, _ = extract_cards(cards_agent, [], 1, HEADLESS, REMOTE_HOST)
        return {
            "cards": cards,
            "rent_sale": rent_sale,
            "zipcodes": zipcodes,
            "dates": dates,
        }

    @task(task_id="etl-details")
    def scrape_details(input: dict):
        cards = input.get("cards")
        rent_sale = input.get("rent_sale")
        zipcodes = input.get("zipcodes")
        dates = input.get("dates")
        query = Query(rent_sale, zipcodes, dates.get("FROM_DATE"))
        # details_agent = DetailsNavigationAgent(query, None, max_it=2 * len(cards))
        details_agent = DetailsNavigationAgent(query, None, max_it=2)
        details_agent.set_page_ct(len(cards) + 1)
        details, _ = extract_details(details_agent, [], 1, HEADLESS, REMOTE_HOST)
        # details, _ = [], None
        return {
            "cards": cards,
            "details": details,
            "rent_sale": rent_sale,
            "dates": dates,
        }

    @task(task_id="etl-store-data")
    def store_data(input: dict):
        cards = input.get("cards")
        details = input.get("details")
        rent_sale = input.get("rent_sale")
        dates = input.get("dates")
        path = os.path.join(
            "/usr/local/airflow/data",
            dates.get("FROM_DATE").format("YYYY-MM-DDTHH:mm:ss"),
            rent_sale,
        )
        if not os.path.exists(path):
            os.makedirs(path)
        for data, label in zip([cards, details], ["cards", "details"]):
            file_path = os.path.join(path, f"{label}.json")
            with open(file_path, "w") as f:
                json.dump(data, f)

    @task_group(group_id="etl-extract-store-data")
    def extract_store_data(rent_sale: str, zipcodes: List[int], dates: dict):
        return store_data(scrape_details(scrape_cards(rent_sale, zipcodes, dates)))

    dates = get_extraction_dates()
    extract_store_data.partial(zipcodes=zipcodes, dates=dates).expand(
        rent_sale=["rent"]
    )


etl()

# @dag(dag_id='etl', schedule='@hourly', start_date=days_ago(0), catchup=False, tags=['etl'])
# def etl():

#     @task(task_id='get_extraction_dates')
#     def get_extraction_dates():

#         from utils_etl import shift_date

#         try:
#             from_date = Variable.get(key='TO_DATE')
#         except KeyError:
#             from_date = shift_date(shift={'days': -7})
#         to_date = shift_date(shift={'days': -1})

#         return {'FROM_DATE': from_date, 'TO_DATE': to_date}

#     @task(task_id='store_cleaned_articles')
#     def store_cleaned_articles(dates: dict):

#         from sqlalchemy import create_engine
#         from sqlalchemy.orm import sessionmaker
#         from airflow.hooks.base import BaseHook
#         from newsapi import NewsApiClient
#         from models import Article
#         from utils_etl import scroll_results_pages, clean_article_dict

#         FROM_DATE, TO_DATE = dates['FROM_DATE'], dates['TO_DATE']

#         connection_id = 'mariadb_newsfeed'
#         db_conn = BaseHook.get_connection(connection_id)
#         engine = create_engine(db_conn.get_uri())
#         SessionLocal = sessionmaker(
#             autocommit=False, autoflush=False, bind=engine)
#         db = SessionLocal()

#         newsapi = NewsApiClient(api_key=Variable.get(key='NEWSAPI_API_KEY'))
#         query_params = {'sources': Variable.get(key='SOURCES')}
#         dates_params = {
#             'from_param': FROM_DATE,
#             'to': TO_DATE
#         }

#         articles, _ = scroll_results_pages(
#             newsapi, query_params, dates_params, initial_page=1)
#         articles = list(map(clean_article_dict, articles))

#         try:
#             for article in articles:
#                 db_article = Article(**article)
#                 db.add(db_article)
#             db.commit()
#         except:
#             db.rollback()
#         finally:
#             db.close()

#         return dates

#     @task(task_id='set_extraction_dates')
#     def set_extraction_dates(dates: dict):

#         Variable.set(key='FROM_DATE', value=dates['FROM_DATE'])
#         Variable.set(key='TO_DATE', value=dates['TO_DATE'])

#     set_extraction_dates(store_cleaned_articles(get_extraction_dates()))
