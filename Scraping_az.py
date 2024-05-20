import requests
from bs4 import BeautifulSoup 
import pandas as pd
url = "https://www.amazon.com/Titanfall-2-Online-Game-Code/product-reviews/B01H0LFJWA/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1"
body = []
rating = []

def get_soup(url):
    r = requests.get("http://localhost:8050/render.html",params={"url":url,"wait":2})
    soup = BeautifulSoup(r.text,"html.parser")
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div',{'data-hook':'review'})
    try:
        for item in reviews:
            body.append(item.find('span',{'data-hook':'review-body'}).text.strip())
            rating.append(float(item.find('i',{'data-hook':'review-star-rating'}).text.replace("out of 5 stars",'').strip()))
    except:
        pass

i = 1
while True:
    link = f"https://www.amazon.com/Titanfall-2-Online-Game-Code/product-reviews/B01H0LFJWA/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber={i}"
    soup = get_soup(link)
    get_reviews(soup)
    i += 1
    if not soup.find('li',{'class':'a-disabled a-last'}):
        pass
    else:
        break

df = pd.DataFrame(data={"body":body,"rating":rating})
df.to_csv('az_rev.csv',index=False,columns=['body','rating'])