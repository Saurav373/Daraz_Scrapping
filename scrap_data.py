from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os


query='laptop'#Your Searching item 

driver = webdriver.Firefox()
driver.get(f"https://www.daraz.com.np/catalog/?spm=a2a0e.searchlist.pagination.2.74565d72AaaoAb&_keyori=ss&from=input&q={query}&page=1")


searchresults=driver.find_element(By.XPATH,'/html/body/div[3]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/span[1]').text
res = searchresults.split(' ')
totalresults = res[0].replace(',','')
# totalresults = int(totalresults)
totalresults = 500

for i in range(2,int(totalresults/41)):
    with open(f'data/index{i}.html','w',encoding='utf-8') as f:
        elem = driver.find_element(By.XPATH,'/html/body/div[3]/div/div[3]/div/div/div[1]/div[2]').get_attribute('innerHTML')
        f.write(elem)
        f.close()
    driver.get(f"https://www.daraz.com.np/catalog/?spm=a2a0e.searchlist.pagination.2.74565d72AaaoAb&_keyori=ss&from=input&q={query}&page={i}")




totaldata = len(os.listdir('./data'))

data={
    'desc':[],
    'price':[],
    'link':[]
}

for i in range(2,totaldata):
    with open(f'./data/index{i}.html','r',encoding='utf-8') as html:
        soup = BeautifulSoup(html,'html.parser')
        childrens = soup.find_all(class_='gridItem--Yd0sa')
        for html_content in childrens:
            link = html_content.find(id='id-a-link').get('href')
            desc = html_content.find(id='id-title').text
            price = html_content.find(class_='currency--GVKjl').text

            data['link'].append(link)
            data['desc'].append(desc)
            data['price'].append(price)
    html.close()
        
df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)


driver.close()
