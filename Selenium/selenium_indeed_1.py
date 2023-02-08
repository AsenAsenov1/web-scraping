import selenium.common
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import selenium.webdriver.common.keys
import re

browser = webdriver.Chrome()
url = "https://www.indeed.com/jobs?q=red+team&l=Remote&vjk=4af45f7f7d054a0f"
browser.implicitly_wait(2)
browser.get(url)
page_num = 2
page_list = []
time.sleep(2)
print(f"Extracting Page 1...")

while True:
    # Extract jobs info
    jobs_info = browser.find_elements(By.CLASS_NAME, "resultContent")
    for job in jobs_info:
        split_jobs = job.text.split('\n')  # From string to list
        company_without_rating = "".join(re.findall("[A-Za-z\s]+", split_jobs[1]))  # Remove rating
        split_jobs[1] = company_without_rating

        # Find the job link
        link_class = job.find_element(By.TAG_NAME, "a")
        link_href = link_class.get_attribute('href')

        split_jobs.insert(0, link_href)
        page_list.append(split_jobs)

    if page_num == 5:
        break

    try:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        buttons = browser.find_element(By.LINK_TEXT, f"{page_num}")
        print(f"Extracting Page {page_num}...")
        buttons.click()
        page_num += 1
    except selenium.common.NoSuchElementException:
        print("Extraction Complete.")
        break

# Print all collected jobs
for current_job_card in page_list:
    print('\n'.join(current_job_card))
    print()

# Jobs found number
total_jobs = browser.find_element(By.CLASS_NAME, "jobsearch-JobCountAndSortPane-jobCount")
print(total_jobs.text)
time.sleep(3)
browser.close()
