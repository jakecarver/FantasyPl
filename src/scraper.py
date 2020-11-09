"""
Scrapes www.fantasyfootballfix.com for fantasy football (Premier League) prediction data.
When run from terminal, requires fantasyfootballfix email and password as arguments to use.

Author: Jake Carver
"""

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

    #Install webdrivers if necessary and create driver instance
    driver = webdriver.Chrome(ChromeDriverManager().install())

    #Open login page
    driver.get('https://www.fantasyfootballfix.com/price/')

    #Enter user email and ID to access site
    email = driver.find_element_by_id('id_email').send_keys(EMAIL)
    password = driver.find_element_by_id('id_password1').send_keys(PASSWORD)
    login = driver.find_element_by_id('loadSquad').click()
    
    #Navigate to page with the dataset
    driver.get('https://www.fantasyfootballfix.com/price/')

    #Wait for data table to load
    element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, "playerPriceAll"))
                )
    #Generate BeautifulSoup and find the data table
    soup = BeautifulSoup(driver.page_source, 'lxml')
    table = soup.find( id ='playerPriceAll')
    
    #Index columns for later use
    cols = table.find_all("th")
    #Dictionary holding column indices
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
    
    #Initialize dictionary for popup column indexes
    innerColDict = {}
    
    #End driver instance
    driver.quit()

    
    
    #Initialize page count
    page = 0

    #For every page in the table
    while True:
        #Initialize dataframe
        df = pd.DataFrame([], columns=['Name','Position','Team','CV',
        'week1','week2','week3','week4','week5','week6'])

        #Output Data list, to be put into dataframe
        dataList = []

        #print page number
        print('PAGE: '+str(page))

        #Create new driver  instance and login (same as before)
        #Driver restart is an attempt to avoid the server dropping our connection
        driver = webdriver.Chrome(ChromeDriverManager().install())
        
        driver.get('https://www.fantasyfootballfix.com/price/')

        #Enter Email
        element = WebDriverWait(driver, 50).until( EC.presence_of_element_located((By.ID, "id_email")))
        email = driver.find_element_by_id('id_email').send_keys(EMAIL)

        #Enter password
        element = WebDriverWait(driver, 50).until( EC.presence_of_element_located((By.ID, "id_password1")))
        password = driver.find_element_by_id('id_password1').send_keys(PASSWORD)

        #Load Squad
        element = WebDriverWait(driver, 50).until( EC.presence_of_element_located((By.ID, "loadSquad")))
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "loadSquad"))).click()
        
        driver.get('https://www.fantasyfootballfix.com/price/')

        
        
        #Wait till rows have generated
        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#playerPriceAll tr")))

        #Wait until the "loading" row has disappeared
        while (True):
            
            driver.implicitly_wait(1)
            #Generate new soup, table element, and list of rows
            soup = BeautifulSoup(driver.page_source, 'lxml')
            table = soup.find( id ='playerPriceAll')
            rows = table.select("tbody > tr")
            if  not rows[0].select('.dataTables_empty'):
                break
        iters = len(rows)
        #For every row
        for i in range (0, iters):
            driver.get('https://www.fantasyfootballfix.com/price/')

        
        
            #Wait till rows have generated
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#playerPriceAll tr")))

            #Wait until the "loading" row has disappeared
            while (True):
                
                driver.implicitly_wait(1)
                #Generate new soup, table element, and list of rows
                soup = BeautifulSoup(driver.page_source, 'lxml')
                table = soup.find( id ='playerPriceAll')
                rows = table.select("tbody > tr")
                if  not rows[0].select('.dataTables_empty'):
                    break


            #Data to be output into dataframe
            data = {}
            
            #Create list of data points and use the index dictionary to input data into our output
            cells = rows[i].find_all("td")
            data['Name']=cells[colDict['Name']].getText().replace(' ','')
            data['Position']=cells[colDict['Position']].getText()
            data['Team']=cells[colDict['Team']].getText()
            data['CV']=float(cells[colDict['CV']].getText())

            #Revisit the price page (closing the popup table)
            driver.get('https://www.fantasyfootballfix.com/price/')
            
            #try to click to correct table page
            try:
                for q in range (0, page):
                    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"playerPriceAll_paginate\"]/ul/li[7]/a")))
                    driver.find_element_by_css_selector("#playerPriceAll_paginate > ul > li.next > a").click()
                    
            #Return an error and output the rest of our data into the dataframe if error      
            except: 
                print ('Fail 1')
                df.append(data, ignore_index=True)
                break    
            
            

            #Wait for the new page table to load
            element = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#playerPriceAll tr"))
                )
            
            #Wait for "loading" row to disappear
            while (driver.find_elements_by_xpath("//playerPriceAll[contains(text(),'Loading')]")):
                driver.implicitly_wait(1)

            #Open popup table
            driverRows = driver.find_elements_by_css_selector('#playerPriceAll > tbody > tr')
            print (driverRows[i].text)
            moreInfo = driverRows[i].find_element_by_tag_name('a').click()

            print('entering try')
            #Scraping the popup table
            try:
                #Wait until the appropriate tab appears
                element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, "fixturetab"))
                )

                #Click on tab
                driver.find_element_by_id('fixturetab').click()

                #Wait for table to appear
                element = WebDriverWait(driver, 50).until(
                    EC.presence_of_element_located((By.ID, "fixturetable"))
                )

                print('clicked correctly')

                #Create a new soup from table
                newSoup = BeautifulSoup(driver.page_source, 'lxml')
                innerTable = newSoup.find( id ='fixturetable')
                innerRows = innerTable.find_all("tr")
                
                #Find element in driver
                #driverInnerTable = driver.find_element_by_id('fixturetable')
                #driverInnerRows = driverInnerTable.find_elements_by_tag_name('tr')

                #If inner table dictionary is empty, fill with header indexes
                if innerColDict == {}:
                    #Find all headers
                    innerCols = innerTable.find_all("th")
                    #search for the correct strings and add to dictionary
                    for j in range(0,len(innerCols)):
                        if 'points' in innerCols[j].getText():
                            innerColDict['Points'] = j
                            break
                
                #Add prediction data for every week
                for k in range (1, len(innerRows)):
                    innerCells = innerRows[k].find_all("td")
                    data['week'+str(k)]=float(innerCells[innerColDict['Points']].getText().replace(' ',''))
                
                
                #Add data to list
                dataList.append(data)

            #Return error if popup scraping fails
            except:
                print ("ERROR")

                #Empty dataframe on failure, so nothing is written to csv
                df = pd.DataFrame([], columns=['Name','Position','Team','CV',
                'week1','week2','week3','week4','week5','week6'])

                #De-incriment so we try the same page next time
                page -= 1
                break
        #Once all rows on table page are completed, iterate page and close current driver
        page += 1
        df = pd.DataFrame(dataList)    
        df.to_csv('out.csv', mode='a',index=False, header=False)  
        driver.quit()

    #Create csv and end    
    #df.to_csv('out.csv', index=False)  
    #driver.quit()


fixScraper(sys.argv[1], sys.argv[2])