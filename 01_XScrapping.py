from tqdm import tqdm
from time import sleep
import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from webdriver_manager.chrome import ChromeDriverManager
import json
import pandas as pd
import sys
from bs4 import BeautifulSoup
DRIVER_PATH="D:\downloadss\chromedriver-win64\chromedriver-win64\chromedriver.exe"

for fecha in [30]:
    print("Extracting tweets from " + str(fecha) + " dic 2022...")
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)

    driver.get("https://twitter.com/i/flow/login")
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='username']"))).send_keys("javiermunoz600")
    #WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='Next']"))).click()
    driver.find_element(by=By.XPATH, value='//span[contains(text(), "Next")]').click()
    WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='current-password']"))).send_keys("rovvsrot")

    driver.find_element(by=By.XPATH, value='//span[contains(text(), "Log in")]').click()
    #driver.find_element(by=By.XPATH, value="//input[@name='password']").send_keys("rovvsrot")
    subject="nasdaq lang:en until:2022-03-"+str(fecha+1).zfill(2)+" since:2022-03-"+str(fecha).zfill(2)
    subject='nasdaq lang:en until:2022-04-01 since:2022-03-31'
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='off']"))).send_keys(subject)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='off']"))).send_keys(Keys.ENTER)
    driver.find_element(by=By.XPATH, value='//span[contains(text(), "Aceptar todas las cookies")]').click()
    sleep(1)

    tweets=[]
    dates=[]
    author=[]
    reacts=[]
    comments=[]
    rts=[]
    favs=[]
    final_tweet=[]
    final_tweet2=[]
    
    print("% of scrolls performed on that date...")

    for _ in tqdm(range(11)):
        

        tweet_divs = driver.page_source    
        soup = BeautifulSoup(tweet_divs, "lxml")      #css-901oao css-cens5h r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0
        tabla = soup.find_all('div', attrs={'class': 'css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu'})  

        for iss,fila in enumerate(tabla):
            fila2=fila
            final_tweet.append(fila2.text)

        tabla = soup.find_all('div', attrs={'class': 'css-901oao css-cens5h r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})  

        for iss,fila in enumerate(tabla):
            fila2=fila
            final_tweet2.append(fila2.text)        

        #tabla = soup.find_all('div', attrs={'class': 'css-1dbjc4n r-18u37iz r-1q142lx'})  
        #for iss,fila2 in enumerate(tabla):
        #    dates.append(fila2.find('time')['datetime'])

        #tabla = soup.find_all('div', attrs={'data-testid': 'User-Name'})  
        #for iss,fila3 in enumerate(tabla):
        #    author.append(fila3.text)

        tabla = soup.find_all('div', attrs={'class': 'css-1dbjc4n r-xoduu5 r-1udh08x'})  
        tabla = soup.find_all('div', attrs={'data-testid': 'retweet'})  

        for iss,fila4 in enumerate(tabla):
            reacts.append(fila4.text)

        tabla = soup.find_all('div', attrs={'data-testid': 'like'})  

        for iss,fila4 in enumerate(tabla):
            favs.append(fila4.text)

        tabla = soup.find_all('div', attrs={'data-testid': 'reply'})  

        for iss,fila4 in enumerate(tabla):
            comments.append(fila4.text)

        driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
        sleep(5)

    df3 = pd.DataFrame(
        {'TweetsTodo': final_tweet,
         'Tweets': final_tweet2,
         'comments': comments,
         'rts': reacts,
         'favs': favs,
        })#crear dataframe
    
    def autor(valor):
        return valor.split("·")[0]
    def fecha2(valor):
        return valor.split("·")[1].split("2022")[0]+"2022"

    
    def lowering_tweets_aux(v):
        return v.lower()


    
    
    archivename="prueba_marzo"+str(fecha).zfill(2)+".xlsx"
    dfinal=df3.drop_duplicates(subset=["Tweets"]).reset_index(drop=True)
    dfinal["auxtweets"]=dfinal["TweetsTodo"].map(lowering_tweets_aux)
    df_Final=dfinal[dfinal.auxtweets.str.contains('2022')]
    df_Final["Autor"]=df_Final["TweetsTodo"].map(autor)
    df_Final["Fecha"]=df_Final["TweetsTodo"].map(fecha2)
    df_Final.to_excel(archivename,index=False)  