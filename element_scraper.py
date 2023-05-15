from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Setup Selenium
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

# Navigate to a webpage
driver.get('https://octordle.com/daily/100')

# Get the HTML of the page and create a BeautifulSoup object
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Close the browser
driver.quit()

# Print all elements of the webpage
for element in soup.recursiveChildGenerator():
    if element.name:
        print(element.name)
