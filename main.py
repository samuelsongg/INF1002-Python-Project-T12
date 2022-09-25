import sys
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import xlsxwriter
import pandas as pd
# import requests
# import selenium.webdriver.remote.webdriver
# from newspaper import Article
# import nltk
# nltk.download("punkt")
# nltk.download("stopwords")

def data_scraping():
    WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "job-card-list__title")))
    #scrolling page to load all jobs
    browser.find_element(By.CLASS_NAME, "job-card-list__title").click()
    while True:
        action.send_keys(Keys.TAB * 250).perform()
        time.sleep(0.5)
        job_list = browser.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__title")
        if len(job_list) >= 24:
            break
        else:
            pass

    job_list = browser.find_elements(By.CLASS_NAME, "scaffold-layout__list-item")
    for job in job_list:
        try:
            job.find_element(By.CLASS_NAME, "artdeco-entity-lockup__title").click()
        except:
            job.find_element(By.CLASS_NAME, "job-card-list__title").click()

        WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__posted-date")))
        WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, "jobs-unified-top-card__job-insight")))

        soup = BeautifulSoup(browser.page_source, "lxml")
        job_name = soup.find("h2", class_="jobs-unified-top-card__job-title").text.strip()
        company_name = soup.find("span", class_="jobs-unified-top-card__company-name").text.strip()
        posted_date = soup.find("span", class_="jobs-unified-top-card__posted-date").text.strip()
        location = soup.find("span", class_="jobs-unified-top-card__bullet").text.strip()

        job_insight_list = browser.find_elements(By.CLASS_NAME, "jobs-unified-top-card__job-insight")
        job_spec_list = []
        for job_insight in job_insight_list:
            job_spec_list.append(job_insight.text)
        job_spec_1 = job_spec_list[0]
        job_spec_2 = job_spec_list[1]

        try:
            work_type = soup.find("span", class_="jobs-unified-top-card__workplace-type").text.strip()
        except:
            work_type = "Nil"

        try:
            applicants = soup.find("span", class_="jobs-unified-top-card__applicant-count").text.strip()
        except:
            applicants = "Nil"

        #extract text for keyword analysis. Ignore for now.
        # job_desc = soup.find_all("div", class_="jobs-description-content__text--stretch")
        # for details in job_desc:
        #     keywords = details.text

        if len(job_spec_1.split(" · ")) == 2:
            job_spec_1 = job_spec_1.split(" · ")
            employment_type = job_spec_1[0]
            position_level = job_spec_1[1]
        else:
            employment_type = job_spec_1
            position_level = "Nil"

        if len(job_spec_2.split(" · ")) == 2:
            job_spec_2 = job_spec_2.split(" · ")
            employee_number = job_spec_2[0]
            company_sector = job_spec_2[1]
        else:
            employee_number = job_spec_2
            company_sector = "Nil"

        if "premium" in employee_number.lower():
            employee_number = "Nil"

        list_1 = [job_name,company_name,company_sector,employment_type,position_level,location,work_type,employee_number,posted_date,applicants]
        excel_list.append(list_1)

        # global i
        # i += 1
        # print(f"{i}.\t{'Job Title:' : <18}{job_name}")
        # print(f"\t{'Company Name:' : <18}{company_name}")
        # print(f"\t{'Sector:' : <18}{company_sector}")
        # print(f"\t{'Employment Type:' : <18}{employment_type}")
        # print(f"\t{'Position Level:' : <18}{position_level}")
        # print(f"\t{'Location:' : <18}{location}")
        # print(f"\t{'Work Type:' : <18}{work_type}")
        # print(f"\t{'No. of Employees:' : <18}{employee_number}")
        # print(f"\t{'Job Posted Date:' : <18}{posted_date}")
        # print(f"\t{'Applicants:' : <18}{applicants}\n\n")

def page_navigator():
    for y in range(pages-1):
        if y + 2 > pages:
            break
        else:
            y_fm = "Page " + str(y + 2)
            p = browser.find_element(By.XPATH, "//button[@aria-label='{}']/span".format(y_fm))
            action.move_to_element(p).click().perform()
            time.sleep(1.5)
            data_scraping()

def excel_write():
    workbook = xlsxwriter.Workbook(f'{xl_name}.xlsx')
    worksheet = workbook.add_worksheet()
    header_value = ["Job Title","Company Name","Sector","Employment Type","Position Level","Location","Work Type","No. of Employees","Job Posted Date","Applicants"]
    for col_index, value in enumerate(header_value):
        worksheet.write(0, col_index, value)
    for row_index, row in enumerate(excel_list, start=1):
        for col_index, value in enumerate(row):
            worksheet.write(row_index, col_index, value)

    workbook.close()

def excel_print():
    try:
        pd.set_option('display.max_colwidth', 200)
        pd.set_option("display.expand_frame_repr", False)
        pd.set_option("display.max_rows", None)
        df = pd.read_excel(f"{xl_name}.xlsx")
        print(df)
    except:
        print("No such file.")

#change accordingly
username = ""
password = ""
software_engineer_url = "https://www.linkedin.com/jobs/search/?currentJobId=3204289656&keywords=software%20engineer&refresh=true"
cyber_security_specialist_url = "https://www.linkedin.com/jobs/search/?currentJobId=3150477953&keywords=cyber%20security%20specialist&refresh=true"
data_analyst_url = "https://www.linkedin.com/jobs/search/?currentJobId=3246469376&keywords=data%20analyst&refresh=true"
excel_list = []

while True:
    try:
        menu_option = int(input("Please select an option:\n1. Scrape data\n2. Print data\n3. Exit\n"))
        if menu_option in range(1, 4):
            if menu_option == 3:
                sys.exit()
            else:
                break
    except SystemExit:
        sys.exit()
    except:
        pass


while True:
    try:
        job_option = int(input("Please select an option:\n1. Software Engineer\n2. Cyber Security Specialist\n3. Data Analyst\n"))
        if job_option in range(1, 4):
            break
    except:
        pass

if job_option == 1:
    search_field = software_engineer_url
    xl_name = "SoftwareEngineer"
elif job_option == 2:
    search_field = cyber_security_specialist_url
    xl_name = "CyberSecuritySpecialist"
elif job_option == 3:
    search_field = data_analyst_url
    xl_name = "DataAnalyst"

if menu_option == 1:
    while True:
        try:
            pages = int(input("How many pages do you want to scrape data from? "))
            #limit pages to 5 otherwise account/IP might get ban
            if pages in range(1, 6):
                break

        except:
            pass

    # change file path accordingly
    path_to_chromedriver = "C:/Program Files/Google/Chrome/Application/chromedriver.exe"
    browser = webdriver.Chrome(executable_path=path_to_chromedriver)
    browser.get("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F%3FdoFeedRefresh%3Dtrue%26nis%3Dtrue&fromSignIn=true&trk=cold_join_sign_in")
    browser.find_element(By.ID, "username").send_keys(username)
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.CLASS_NAME, "login__form_action_container").submit()
    WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.CLASS_NAME, "scaffold-layout__sidebar")))
    browser.get(search_field)
    action = ActionChains(browser)
    i = 0

    data_scraping()
    page_navigator()
    excel_write()
    browser.close()
    while True:
        try:
            option1 = int(input("Would you like to print out the data scraped?\n1. Yes\n2. No\n"))
            if option1 in range(1, 3):
                if option1 == 1:
                    excel_print()
                    sys.exit()
                elif option1 == 2:
                    sys.exit()
        except SystemExit:
            sys.exit()
        except:
            pass

if menu_option == 2:
    excel_print()


