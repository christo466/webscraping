from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from openpyxl.workbook import Workbook
import pandas as pd
import numpy as np
import time
import datetime


def main():
    dff = pd.DataFrame(
        columns=['Job Title', 'Description', 'Experience Reqd', 'Company', 'City', 'Date Posted',
                 'URL'])

    driver = webdriver.Chrome()

    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=&txtLocation=India#'
    driver.get(url)

    # print(driver.page_source)

    try:
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/table/tbody/tr/td[2]/div/span').click()
    except Exception as e:
        print('EXCEPTION OCCURED')
        pass

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html5lib')

    # print(soup.encode('utf-8'))

    result = soup.find('ul', class_='new-joblist')
    result2 = result.find_all('li', class_='clearfix job-bx wht-shd-bx')

    page_counter = 0

    # print(result2)
    pages = np.arange(1, 25)

    exception = 0

    for page in pages:
        if page_counter == 0:
            next_counter = 0
        else:
            next_counter = 1

        page_next_counter = np.arange(2, 12)

        for page_next in page_next_counter:
            for i in result2:
                # TITLE
                title = i.find('a')
                title = title.text
                print(title.encode('utf-8'))

                # Description
                description = i.find('label').next_sibling.strip()
                print(description)

                # COMPANY
                text = i.find('h3', class_='joblist-comp-name')
                text = text.text
                initial_company = text.find('(')
                Company = text[:initial_company]
                Company = Company.strip()
                print(Company)

                # Exp
                Mat_icons = i.find_all('i', class_='material-icons')
                # print('THIS IS MATERIAL ICONS:', Mat_icons)
                Exp = Mat_icons[0].next_sibling.text.strip()
                # print(Exp)

                # City
                spans = i.find_all('span')
                City = spans[1].text

                # Date Posted
                Date = i.find('span', class_='sim-posted')
                Date = Date.text.strip()
                print(Date)

                URL = i.find('a').get('href')
                # print(URL)

                dff = pd.concat([dff, pd.DataFrame([[title, description, Exp, Company, City,  Date, URL]],
                                                   columns=['Job Title', 'Description', 'Experience Reqd', 'Company',
                                                            'City', 'Date Posted', 'URL'])],
                                ignore_index=True)

                dff.to_excel('TimesJobs_' + str(datetime.date.today()) + '.xlsx')

            dff.to_excel('TimesJobs_' + str(datetime.date.today()) + '.xlsx')
            driver.execute_script("window.scrollTo(0,(document.body.scrollHeight))")
            scroll_time = 1
            time.sleep(scroll_time)

            page_counter = page_counter + 1

            final_page_next = next_counter + page_next
            driver.find_element(By.XPATH, '/html/body/div[3]/div[4]/section/div[2]/div[2]/div[4]/em[' + str(
                final_page_next) + ']/a').click()

            loading_time = 3
            time.sleep(loading_time)

            print('NUMBER OF EXCEPTIONS: ', exception)



main()




