from bs4 import BeautifulSoup
import requests
import csv
import pandas
from lxml import etree

header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

class Parser:
    def __init__(self, url:str) -> None:
        self.url = url
        self.response = requests.get(self.url,
         headers=header)
        if self.response.status_code == 404:
            raise Exception('page not found')
        self.soup = BeautifulSoup(self.response.content, 'html.parser')


    def find_by_xpath(self, xpath:str) -> str :
        dom = etree.HTML(str(self.soup))

        return dom.xpath(xpath)[0].text
# table/tbody/tr[5]/td[2]/a
    def get_data(self) -> list:
        print('---Get data---')
        title = self.find_by_xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[1]/h1')
        imdb = self.find_by_xpath('//*[@class="b-post__info"]/tr[1]/td[2]/span[1]/span')
        name_of_orig =  self.find_by_xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[2]')
        country = self.find_by_xpath('//*[@class="b-post__info"]/tr[5]/td[2]/a')
        time = self.find_by_xpath('//*[@class="b-post__info"]/tr[10]/td[2]')
        about = self.find_by_xpath('//*[@id="main"]/div[4]/div/div[2]/div[1]/div[5]/div[2]')
        return [title, imdb, name_of_orig, country, time, about]


    def write_data(self, data:list) -> None:
        print('---Write data to .csv---')
        with open('test.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def read_data_from_csv(self, path:str) -> None:
        df = pandas.read_csv(path)
        print(df)


    def main(self) -> None:
        self.write_data(self.get_data())
        self.read_data_from_csv('test.csv')


film=Parser(input('Paste movie link: '))
film.main()


