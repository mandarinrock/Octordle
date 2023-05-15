from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Selenium
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service)

# Navigate to the webpage
driver.get('https://octordle.com/daily/100')

# Wait for the page to load
# time.sleep(1)

guesses = ['party']

# Define the layout of the keyboard
keyboard_layout = [
    # list('1234567890'),
    '',
    '',
    list(' qwertyuiop'),
    list(' asdfghjkl'),
    list(' zxcvbnm')
]

# Convert the layout into a dictionary mapping keys to their positions
keyboard_mapping = {
    key: (i, j)
    for i, row in enumerate(keyboard_layout)
    for j, key in enumerate(row)
}

for guess in guesses:
    for letter in guess:
        position = keyboard_mapping[letter]
        # print(f'The position of {letter} is {position}') # DEBUG
        driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[{position[0]}]/button[{position[1]}]').click()
        # key.click()
    driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[4]/button[9]').click()

wait = input('Press enter to quit')
# time.sleep(10)
driver.quit()
exit()
