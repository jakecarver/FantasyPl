from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import sys
import time

def fixScraper (EMAIL, PASSWORD):
    

    #path = 'C:/Users/jakep/Downloads/chromedriver_win32/chromedriver.exe'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.fantasyfootballfix.com/price/')
    print(driver.page_source)
    

    email = driver.find_element_by_id('id_email').send_keys(EMAIL)
    password = driver.find_element_by_id('id_password1').send_keys(PASSWORD)
    password = driver.find_element_by_id('loadSquad').click()
    
    driver.get('https://www.fantasyfootballfix.com/price/')
    
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #table = soup.find_all( id ='playerPriceAll')[0]
    table = soup.find( id ='playerPriceAll')
    print (table)
    cols = table.find_all("th")
    df = pd.DataFrame([], columns=['Name','Position','Team','CV',
        'week1','week2','week3','week4','week5'])
    colDict = {}
    for i in range (0,len(cols)):
        if cols[i].getText() == 'Name':
            colDict['Name'] = i
        elif cols[i].getText() == 'Position':
            colDict['Position'] = i
        elif cols[i].getText() == 'Team':
            colDict['Team'] = i
        elif cols[i].getText() == 'CV':
            colDict['CV'] = i
    print (colDict)
    
    innerColDict = {}




    rows = table.find_all("tr")
    driverTable = driver.find_element_by_id('playerPriceAll')
    driverRows = driverTable.find_elements_by_tag_name('tr')


    while True:
        for i in range (1, len(driverRows)):
            data = {}
            
            cells = rows[i].find_all("td")
            
            data['Name']=cells[colDict['Name']].getText().replace(' ','')
            
            data['Position']=cells[colDict['Position']].getText()
            data['Team']=cells[colDict['Team']].getText()
            data['CV']=float(cells[colDict['CV']].getText())
            
            moreInfo = driverRows[i].find_element_by_tag_name('a').click()
            #.find_element_by_tag_name('a').click()
            
            
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "fixturetab"))
                )
                driver.find_element_by_id('fixturetab').click()
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "fixturetable"))
                )
                newSoup = BeautifulSoup(driver.page_source, 'lxml')
                innerTable = newSoup.find( id ='fixturetable')
                innerRows = innerTable.find_all("tr")
                
                driverInnerTable = driver.find_element_by_id('fixturetable')
                driverInnerRows = driverInnerTable.find_elements_by_tag_name('tr')
                if innerColDict == {}:

                    
                    innerCols = innerTable.find_all("th")
                    print(len(innerCols))
                    for j in range (0,len(innerCols)):
                        print (innerCols[j].getText())
                        if innerCols[j].getText().contains('points'):
                            print ('inside')
                            innerColDict['Points'] = j
                            break
                            
                
                for k in range (1, len(innerRows)):
                    print ('HELLO2')
                    innerCells = innerRows[k].find_all("td")
                    print(innerCells)
                    print (colDict['Points'])
                    data['week'+str(k)]=innerCells[colDict['Points']].getText().replace(' ','')
                
                #element = WebDriverWait(driver, 10).until(
                #    EC.presence_of_element_located((By.ID, "resultstable"))
                #)  
                #driver.back()
                #time.sleep(5)
            except:
                
                driver.quit()
            print (data)
            return
        return
    driver.quit()


fixScraper(sys.argv[1], sys.argv[2])