import requests
from requests.adapters import HTTPAdapter, Retry
from urllib.parse import urljoin
import json
from bs4 import BeautifulSoup

class FundAPI:
    BASE_URL = 'https://www.finnomena.com'
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()


        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[ 500, 502, 503, 504 ])

        self.session.mount('https://', HTTPAdapter(max_retries=retries))


    def __retrieve(self, url: str, params: dict = None) -> str:
        res = self.session.get(url, params=params)
        if res.status_code == 200:
            return res.text
        else:
            print('Error', url, params, res.text)
            return None

    def __retrieve_json(self, url: str, params: dict = None) -> dict:
        response_text = self.__retrieve(url, params=params)
        if response_text is not None:
            response_json = json.loads(response_text)
            if response_json['status']:
                return response_json['data']
            else:
                return None
        else:
            return None

    def __scrap(self, url: str, params: dict = None) -> BeautifulSoup:
        response_text = self.__retrieve(url, params=params)
        if response_text is not None:
            return BeautifulSoup(response_text)
        else:
            return None

    def get_funds(self) -> dict:
        url = urljoin(self.base_url, '/fn3/api/fund/v2/public/funds')

        return self.__retrieve_json(url)

    def get_fund(self, fund_id: str) -> dict:
        url = urljoin(self.base_url, f'/fn3/api/fund/v2/public/funds/{fund_id}')

        return self.__retrieve_json(url)

    def get_fund_daily_update_detail(self, fund_id: str) -> dict:
        url = urljoin(self.base_url, f'/fn3/api/fund/v2/public/funds/{fund_id}/latest')

        return self.__retrieve_json(url)

    def get_portfolio(self, fund_id: str) -> dict:
        url = urljoin(self.base_url, f'/fn3/api/fund/v2/public/funds/{fund_id}/portfolio')

        return self.__retrieve_json(url)

    def get_nav(self, fund_id: str) -> dict:
        url = urljoin(self.base_url, f'fn3/api/fund/v2/public/funds/{fund_id}/nav/q')

        return self.__retrieve_json(url, params={'range': 'MAX'})

if __name__ == '__main__':
    fund_api = FundAPI()
    funds = fund_api.get_funds()
    print(funds)