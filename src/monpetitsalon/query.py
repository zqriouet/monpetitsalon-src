from typing import List
import pendulum


class Query:

    def __init__(self, rent_sale: str, zipcodes: List[str | int], from_date: pendulum.datetime):
        self.rent_sale = rent_sale
        self.zipcodes = [str(zipcode) for zipcode in zipcodes]
        self.date = pendulum.now("Europe/Paris")
        self.date_str = self.date.format('YYYY-MM-DDTHH:mm:ss')
        self.from_date = from_date
        self.from_date_str = self.from_date.format('YYYY-MM-DDTHH:mm:ss')
        self.from_date_str = self.from_date.format('YYYY-MM-DDTHH:mm:ss')
        self.url = f'https://www.bienici.com/recherche/{self.rent_sale}/{",".join(self.zipcodes)}?mode=liste&tri=modification-desc'
        self.base_file_name = f'{self.rent_sale}_{",".join(self.zipcodes)}_{self.date_str}'

    def __str__(self):
        return self.base_file_name

    def __dict__(self):
        q_dict = {
            'rent_sale': self.rent_sale,
            'zipcodes': self.zipcodes,
            'date': self.date_str,
            'from_date': self.from_date_str,
            'url': self.url
        }
        return q_dict
