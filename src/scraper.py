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
    login = driver.find_element_by_id('loadSquad').click()
    
    driver.get('https://www.fantasyfootballfix.com/price/')

    element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, "playerPriceAll"))
                )
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #table = soup.find_all( id ='playerPriceAll')[0]
    table = soup.find( id ='playerPriceAll')
    
    cols = table.find_all("th")
    df = pd.DataFrame([], columns=['Name','Position','Team','CV',
        'week1','week2','week3','week4','week5','week6'])
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
    
    innerColDict = {}
    rows = table.find_all("tr")
    driver.quit()

    page = 0
    while True:
        print('PAGE: '+str(page))
        driver.get('https://www.fantasyfootballfix.com/price/')
        email = driver.find_element_by_id('id_email').send_keys(EMAIL)
        password = driver.find_element_by_id('id_password1').send_keys(PASSWORD)
        login = driver.find_element_by_id('loadSquad').click()
        
        driver.get('https://www.fantasyfootballfix.com/price/')
        element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, "playerPriceAll"))
                )
        
        try:
            for i in range (0, page):
                WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"playerPriceAll_paginate\"]/ul/li[7]/a")))
                WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"playerPriceAll_paginate\"]/ul/li[7]/a"))).click()
                
        except: 
            print ('Click Failure')
            break
        element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#playerPriceAll tr"))
                )
        while (driver.find_elements_by_xpath("//playerPriceAll[contains(text(),'Loading')]")):
                driver.implicitly_wait(1)
        #Wait a little longer just in case only half of the table loaded
        driver.implicitly_wait(3)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        table = soup.find( id ='playerPriceAll')
        rows = table.find_all("tr")
        
        
        for i in range (1, len(rows)):

            data = {}
            
            cells = rows[i].find_all("td")
            data['Name']=cells[colDict['Name']].getText().replace(' ','')
            
            data['Position']=cells[colDict['Position']].getText()
            data['Team']=cells[colDict['Team']].getText()
            data['CV']=float(cells[colDict['CV']].getText())

            driver.get('https://www.fantasyfootballfix.com/price/')
            
            try:
                for q in range (0, page):
                    
                    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"playerPriceAll_paginate\"]/ul/li[7]/a")))
                    
                    driver.find_element_by_css_selector("#playerPriceAll_paginate > ul > li.next > a").click()
                    
                    
            except: 
                print ('Fail 1')
                df.append(data, ignore_index=True)
                break    
            

            element = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#playerPriceAll tr"))
                )
            
            while (driver.find_elements_by_xpath("//playerPriceAll[contains(text(),'Loading')]")):
                driver.implicitly_wait(1)
            driverRows = driver.find_elements_by_css_selector('#playerPriceAll tr')
            
            
            
            moreInfo = driverRows[i].find_element_by_tag_name('a').click()
            
            
            
            try:
                element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, "fixturetab"))
                )
                driver.find_element_by_id('fixturetab').click()
                element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, "fixturetable"))
                )
                newSoup = BeautifulSoup(driver.page_source, 'lxml')
                innerTable = newSoup.find( id ='fixturetable')
                innerRows = innerTable.find_all("tr")
                
                driverInnerTable = driver.find_element_by_id('fixturetable')
                driverInnerRows = driverInnerTable.find_elements_by_tag_name('tr')
                if innerColDict == {}:

                    
                    innerCols = innerTable.find_all("th")
                    
                    for j in range(0,len(innerCols)):
                        
                        if 'points' in innerCols[j].getText():
                            
                            innerColDict['Points'] = j
                            break
                    
                for k in range (1, len(innerRows)):
                    
                    innerCells = innerRows[k].find_all("td")
                    
                    data['week'+str(k)]=float(innerCells[innerColDict['Points']].getText().replace(' ',''))
                
                print (data)
                df.append(data, ignore_index=True)
                
            except:
                print ("ERROR")
                driver.quit()
        page += 1
        driver.quit()
            
    df.to_csv('out.csv', index=False)  
    driver.quit()


fixScraper(sys.argv[1], sys.argv[2])