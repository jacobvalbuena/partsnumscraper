import requests
from bs4 import BeautifulSoup
import re

url = "https://www.partselect.com/PartSearchResult.aspx?PartNum=40A15"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36" }

class PSScraper:
    def __init__(self, partnum):
        self.url = f"https://www.partselect.com/PartSearchResult.aspx?PartNum={partnum}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    
    def get_data(self):
        r = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

    def parse(soup):
        products_list=[]
        results = soup.find_all('div', {'class': 'parts-order-list__list-info'})
        for item in results:
            if item.find('span', {'class': 'dollar'}) is not None:
                product={
                    'title': item.find('div', {'class': 'parts-order-list__list-info__description__part-name'}).text,
                    'condition': 'N/A',
                    'price': item.find('div', {'class':'price'}).text.replace('$','').strip(),
                    'availability': item.find('a', {'class': 'parts-order-list__list-info__inventory__availability stock-text js-tooltip'}).text.strip(),
                    'link': item.find('a', {'id': re.compile('Central_Content_rptPartGrid_PartDescription1_*')})['href']
                }
                products_list.append(product)
        return products_list
    
class CAScraper (PSScraper):

    def __init__(self, partnum):
        self.url = f"https://www.classicautomation.com/Part/{partnum}"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

    
    def parse(self, soup):
        products_list=[]
        results = soup.find_all('tr', {'id': re.compile('dnn_ctr1219_View_RepeaterConditions_TRCondition_*')})
        for item in results:
            product={
                'title': soup.find('h2', {'class': 'partSubTitle'}).text.strip(),
                'condition': item.find('span', {'id': re.compile('dnn_ctr1219_View_RepeaterConditions_LabelCondition_*')}).text.strip(),
                'price': item.find('span', {'id': re.compile('dnn_ctr1219_View_RepeaterConditions_LabelPrice_*')}).text.replace('USD', '').strip(),
                'availability': item.find('span', {'id': re.compile('dnn_ctr1219_View_RepeaterConditions_LabelInventory_*')}).text.strip(),
                'link': self.url,
            }
            products_list.append(product)
        return products_list
    
class PSRCScraper:

    # Involves using the catalog API and POSTMAN to get data from the website
    # Then parsing the JSON data to get the required information
    pass

    
        
        
        


# if __name__ == '__main__':
    # obj1 = PSScraper('40A15')
    # soup = obj1.get_data()
    # print(PSScraper.parse(soup))
    # obj2 = CAScraper('75d73070c')
    # soup = obj2.get_data()
    # print(obj2.parse(soup))
    # obj3 = PSRCScraper('453563477')
    # soup = obj3.get_data()
    # print(obj3.parse(soup))

