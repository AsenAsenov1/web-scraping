import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os


def main():
    url = input("Paste URL:  ")
    # url = "https://www.jobs.bg/front_job_search.php?subm=1&categories%5B%5D=56&techs%5B%5D=Python&salary_from=1"
    table, job_count = extract(url)
    print_result(table, job_count)
    write = input("Write to file? y/n  ")
    write_file(write, table)


def extract(url):
    table = []
    cities = ["София", "Пловдив", "Русе", "Бургас", "Варна", "Стара Загора", "Плевен"]  # The most populated cities
    expression = r"<a class=\"black-link-b\" href=\"[.^\S]+\stitle=\"([^\"]+)\">"  # RegEx used to find the job position

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    job_tabs = soup.find_all("div", class_="mdc-card")  # Find all job offers tabs by class
    found_jobs = len(job_tabs)

    for job in job_tabs:  # for each job offer tab -> extract info
        days_off = "Undefined"
        salary = "Undefined"
        city = "Undefined"
        workplace = "Undefined"
        try:
            job_position = re.findall(expression, str(job))  # Find job position
            card = job.find("div", class_="card-info card__subtitle")  # Find overall info by class
            general_info = card.get_text().strip()  # Found items as a string
            company_name = job.find('div', class_="secondary-text").get_text()
            general_info_split = general_info.replace("chair ", "").replace("3p ", "").replace("wifi ", "") \
                .split("; ")  # List of found items - company name, city etc.
            link = job.find("a").get('href')
            job_id = link[-7:]  # last 7 elements of the link
            current_job = "".join(job_position)  # Transform from list to string

            # check if there are any of these parameters and then add them into dictionary
            for current_info in general_info_split:
                if current_info in cities:
                    city = current_info
                if "вкъщи" in current_info:
                    workplace = current_info
                if "Заплата" in current_info:
                    salary = current_info
                if "Отпуск" in current_info:
                    days_off = current_info

            # Add all the found items to key : value pairs
            dict_info = {"ID": job_id,
                         "Company": company_name,
                         "Job": current_job,
                         "Link": link,
                         "City": city,
                         "Workplace": workplace,
                         "Salary": salary,
                         "Days Off": days_off}
            table.append(dict_info)  # Add current dictionary into the list named table
        except AttributeError:
            pass
    return table, found_jobs


def print_result(table, job_count):
    for job_offer in table:
        for key, value in job_offer.items():
            print(key + ": " + value)
        print()
    print("Total Jobs:", job_count)


def write_file(char, table):
    while True:
        if char == "n":
            break
        elif char == "y":
            while True:
                extension = input(".csv or .txt extension? (type 1 or 2)  ")
                if extension == "1":
                    extension = 'csv'
                elif extension == "2":
                    extension = 'txt'
                else:
                    continue
                path = input("Enter path: ")
                while True:
                    if os.path.exists(path):
                        df = pd.DataFrame(table)  # list
                        df.to_csv(fr'{path}\jobs.{extension}', index=False, header=False, encoding='utf-8-sig')
                        print('Done')
                        exit()
                    else:
                        print("Invalid Path")
                        path = input("Enter path: ")
        else:
            char = input("Write to file? y/n  ")


if __name__ == '__main__':
    main()
