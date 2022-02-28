import time
import random
import pyfiglet
import requests
from bs4 import BeautifulSoup
from colorama import Fore, init
from logging import getLogger

init()
blue = Fore.LIGHTBLUE_EX
red = Fore.LIGHTRED_EX
reset = Fore.RESET


class WebScraper:

    def __init__(self, url):
        self._user_agent_list = [
            "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
        ]
        self.user_agent = self.random_agent()
        self.url = url
        # etc...

    # _user_agentsからランダムに選ぶ
    def random_agent(self):
        return random.choice(self._user_agent_list)

    # urlのhtmlを取得しBeautifulSoupで解析する
    def get_html(self, url, headers=None):
        logger = getLogger("get_html()")
        try:
            resp = requests.get(url)
            time.sleep(1)
            soup = BeautifulSoup(resp.text, "lxml")
            if resp.status_code == 200:
                return soup
            else:
                raise Exception("status code error")
        except Exception as e:
            logger.warning(e)
            return None

    # スクレイピング処理
    def scrape(self):
        logger = getLogger("scrape()")
        try:
            headers = {"User-Agent": self.user_agent}
            soup = self.get_html(self.url, headers)
            if soup is not None:
                # ここに書いた処理が実行される
                print("HEADER:", headers)
                top_news_list = []
                for top_news_list in soup.select(".newsFeed_item a"):
                    print(blue + "\n", top_news_list.text + reset)
                    print(red + top_news_list.get("href") + reset)
            else:
                raise Exception
        except Exception as e:
            logger.warning(e)
            return None


def main():
    try:
        url = "https://news.yahoo.co.jp/topics/top-picks"
        scraper = WebScraper(url)
        scraper.scrape()
    except Exception as e:
        raise e


if __name__ == "__main__":
    figlet = pyfiglet.figlet_format("Yahoo NEWS")
    print(figlet)
    main()
