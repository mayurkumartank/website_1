import json
import os
import time
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()

options = ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = Chrome(options=options)

url = 'https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true'
driver.get(url)

output_data = []

def download_files(file_links, folder_path):
    file_count = len(file_links)
    for file_link in file_links:
        file_link.click()
        time.sleep(2)

    move_files(file_count,folder_path)

def move_files(file_count,folder_path):
    downloaded_file_paths = os.getenv("DEFAULT_DOWNLOAD_PATH")
    all_downloads = os.listdir(downloaded_file_paths)
    all_downloads.sort(key=lambda f: os.path.getmtime(os.path.join(downloaded_file_paths, f)), reverse=True)
    all_file = all_downloads[:file_count]
    if any('.crdownload' in file_name for file_name in all_file):
        time.sleep(5)
        move_files(file_count,folder_path)
    else:
        for filename in all_file:
            source_file = os.path.join(downloaded_file_paths, filename)
            destination_file = os.path.join(folder_path, filename)
            if os.path.exists(destination_file):
                os.remove(destination_file)
            os.rename(source_file, destination_file)

def fetch_data():
    while True:
        results = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//tbody[@id="bidSearchResultsForm:bidResultId_data"]/tr')))

        for row in results:
            bid_solicitation = row.find_element(By.XPATH, './td[1]/a').text
            print(bid_solicitation)
            bid_solicitation_link = row.find_element(By.XPATH, './td[1]/a')

            buyer = row.find_element(By.XPATH, './td[6]').text
            description = row.find_element(By.XPATH, './td[7]').text
            bid_opening_date = row.find_element(By.XPATH, './td[8]')

            bid_solicitation_link.click()
            time.sleep(2)
            driver.switch_to.window(driver.window_handles[-1])
            try:
                bid_number = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '//html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]'))).text
            except:
                bid_number = ""
            try:
                description = driver.find_element(By.XPATH, '//td[contains(text(),"Bid Number:")]/following::td').text.strip()
            except:
                description = ""
            try:
                bid_opening_date = driver.find_element(By.XPATH, '//td[contains(text(),"Bid Opening Date:")]/following::td').text.strip()
            except:
                bid_opening_date = ""
            try:
                purchaser = driver.find_element(By.XPATH, '//td[contains(text(),"Purchaser:")]/following::td').text.strip()
            except:
                purchaser = ""
            try:
                organization = driver.find_element(By.XPATH, '//td[contains(text(),"Organization:")]/following::td').text.strip()
            except:
                organization = ""
            try:
                department = driver.find_element(By.XPATH, '//td[contains(text(),"Department:")]/following::td').text.strip()
            except:
                department = ""
            try:
                location = driver.find_element(By.XPATH, '//td[contains(text(),"Location:")]/following::td').text.strip()
            except:
                location = ""
            try:
                fiscal_year = driver.find_element(By.XPATH, '//td[contains(text(),"Fiscal Year:")]/following::td').text.strip()
            except:
                fiscal_year = ""
            try:
                type_code = driver.find_element(By.XPATH, '//td[contains(text(),"Type Code:")]/following::td').text.strip()
            except:
                type_code = ""
            try:
                allow_electronic_quote = driver.find_element(By.XPATH, '//td[contains(text(),"Allow Electronic Quote:")]/following::td').text.strip()
            except:
                allow_electronic_quote = ""
            try:
                alternate_id = driver.find_element(By.XPATH, '//td[contains(text(),"Alternate Id:")]/following::td').text.strip()
            except:
                alternate_id = ""
            try:
                required_date = driver.find_element(By.XPATH, '//td[contains(text(),"Required Date:")]/following::td').text.strip()
            except:
                required_date = ""
            try:
                available_date = driver.find_element(By.XPATH, '//td[contains(text(),"Available Date")]/following::td').text.strip()
            except:
                available_date = ""
            try:
                info_contact = driver.find_element(By.XPATH, '//td[contains(text(),"Info Contact:")]/following::td').text.strip()
            except:
                info_contact = ""
            try:
                bid_type = driver.find_element(By.XPATH, '//td[contains(text(),"Bid Type:")]/following::td').text.strip()
            except:
                bid_type = ""
            try:
                informal_bid_flag = driver.find_element(By.XPATH, '//td[contains(text(),"Informal Bid Flag:")]/following::td').text.strip()
            except:
                informal_bid_flag = ""
            try:
                purchase_method = driver.find_element(By.XPATH, '//td[contains(text(),"Purchase Method:")]/following::td').text.strip()
            except:
                purchase_method = ""
            try:
                pre_bid_conference = driver.find_element(By.XPATH, '//td[contains(text(),"Pre Bid Conference:")]/following::td').text.strip()
            except:
                pre_bid_conference = ""
            try:
                bulletin_desc = driver.find_element(By.XPATH, '//td[contains(text(),"Bulletin Desc:")]/following::td').text.strip()
            except:
                bulletin_desc = ""
            try:
                ship_to_address = driver.find_element(By.XPATH, '//td[contains(text(),"Ship-to Address:")]/following::td').text.strip()
            except:
                ship_to_address = ""
            try:
                bill_to_address = driver.find_element(By.XPATH, '//td[contains(text(),"Bill-to Address:")]/following::td').text.strip()
            except:
                bill_to_address = ""
            bid_data = {
                        "Bid Solicitation": bid_solicitation,
                        "Buyer": buyer,
                        "Description": description,
                        "Bid Opening Date": bid_opening_date,
                        "Bid Number": bid_number,
                        "Purchaser": purchaser,
                        "Organization": organization,
                        "Department": department,
                        "Location": location,
                        "Fiscal Year": fiscal_year,
                        "Type Code": type_code,
                        "Allow Electronic Quote": allow_electronic_quote,
                        "Alternate Id": alternate_id,
                        "Required Date": required_date,
                        "Available Date": available_date,
                        "Info Contact": info_contact,
                        "Bid Type": bid_type,
                        "Informal Bid Flag": informal_bid_flag,
                        "Purchase Method": purchase_method,
                        "Pre Bid Conference": pre_bid_conference,
                        "Bulletin Desc": bulletin_desc,
                        "Ship-to Address": ship_to_address,
                        "Bill-to Address": bill_to_address
                    }

            output_data.append(bid_data)

            folder_path = os.path.join(os.getcwd(), "File Attachments", bid_solicitation)
            os.makedirs(folder_path, exist_ok=True)
            file_links =driver.find_elements(By.XPATH, '//td[contains(text(),"File Attachments:")]/following::td[1]/a')
            if file_links != []:
                download_files(file_links, folder_path)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])


        time.sleep(3)
        driver.execute_script("window.scrollTo(0, 0);")
        try:
            next_page = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH,'//span[@class="ui-paginator-next ui-state-default ui-corner-all"]')))
        except:
            next_page = ""
        if next_page:
            next_page.click()
            time.sleep(5)
            return fetch_data()
        else:
            break

def write_output(output_data):
    with open("output_task_1.json", "w") as json_file:
        json.dump(output_data, json_file, indent=2)

fetch_data()
write_output(output_data)
driver.close()