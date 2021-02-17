from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

# URLS
GOOGLE_FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSeEQhFQIrbEhknKrFBaFknFRSA9utAKxRGFcjLVR0fpGCzWjA/viewform?usp=sf_link'
RENTAL_WEBSITE_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'

# BROWSER INFORMATION FOR WEB SCRAPPING
header = {
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "Accept-Language" : "en-US,en;q=0.9"
}

# WEB SCRAPPING SET-UP
response = requests.get(RENTAL_WEBSITE_URL, headers=header)
rental_page = response.text
soup = BeautifulSoup(rental_page, 'html.parser')
# print(soup.prettify())

# Extracting required information from the soup
all_listings_address = soup.find_all(class_="list-card-addr")
all_listings_price = soup.find_all(class_='list-card-price')
all_listings_links = soup.find_all(class_='list-card-link')

# Selenium set up
chrome_driver_path = '/Users/shaznaz/Desktop/Web development/chromedriver'
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# Loop to take extracted information and using those to answer questions in the form and submitting
for i in range(len(all_listings_address)):
    # opening up the form
    driver.get(GOOGLE_FORM_URL)
    time.sleep(3)

    # Question 1
    question_1 = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    question_1.send_keys(all_listings_address[i].text)

    # Question 2
    question_2 = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    if '/' in all_listings_price[i].text:
        question_2.send_keys(all_listings_price[i].text.split('/')[0])
    else:
        question_2.send_keys(all_listings_price[i].text.split('+')[0])

    # Question 3
    question_3 = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    question_3.send_keys(all_listings_links[i].get('href'))

    # Submitting the information
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div')
    submit_button.click()
    time.sleep(5)


print("All done!")
