import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

# Initialize the Selenium WebDriver
def scrape_url(url,device,type,iteration):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    element = driver.find_element(By.XPATH, "//span[text()='See all reviews']/ancestor::button")

    element.click()

    time.sleep(1)

    element_device = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/div/div/div/div[1]')
    element_device.click()
    time.sleep(0.5)

    match device:
        case "phone":
            element_device = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[1]')
            element_device.click()
        case "tablet":
            element_device = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[2]')
            element_device.click()
        case "chromebook":
            element_device = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[3]')
            element_device.click()
    time.sleep(0.5)
    element_inside_popup = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div[2]')
    element_inside_popup.click()
    time.sleep(0.5)

    match type:
        case "relevant":
            element_type = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[1]')
            element_type.click()
        case "newest":
            element_type = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[2]')
            element_type.click()
        
    time.sleep(0.5)
    element_inside_popup = driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div/div[2]')
    for i in range(iteration):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element_inside_popup)
        time.sleep(0.5)

    time.sleep(0.3)
    page_source = driver.page_source

    # Parse the updated page source with Beautiful Soup
    soup = BeautifulSoup(page_source, 'html.parser')

    name_game=soup.find_all("h1",itemprop="name")[0].text
    age=soup.find_all("span",itemprop="contentRating")[0].text
    aux=soup.find_all("div",class_="ClM7O")
    rating=aux[0].text[0:3]
    downloads=aux[1].text
    company=soup.find_all("div",class_="Vbfug auoIOc")[0].text
    icon=soup.find_all("img",class_="T75of")[0]['src']
    price=soup.find_all("span",class_="VfPpkd-vQzf8d")[0].text
    update=soup.find_all("div",class_="xg1aie")[0].text
    
    name=soup.find_all("div",class_="X5PpBb")
    starts=soup.find_all("div",class_="iXRFPc")
    date=soup.find_all("span",class_="bp9Aid")
    text=soup.find_all("div",class_="h3YV2d")

    data=[]
    for i in range(3,len(name)):
        input_date=date[i].text.strip()
        parsed_date = datetime.strptime(input_date, "%B %d, %Y")
        formatted_date = parsed_date.strftime("%Y/%m/%d")
        data.append([name[i].text.strip(),formatted_date,starts[i]['aria-label'][6],text[i].text.strip()])
        
    df = pd.DataFrame(data, columns=['User Name ', 'Date', 'Rating','Content'])
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    total = df["Rating"].mean()

    values = {
    'leng': df.shape[0],
    'date0': df['Date'].min(),
    'date1': df['Date'].max(),
    'name': name_game,
    'rating': rating,
    'downloads': downloads,
    'company': company,
    'icon' : icon,
    'price': price,
    'age' : age,
    'update' : update,
    'device' : device,
    'type' : type,
    'rating_scrape': total
    }

    return df,values