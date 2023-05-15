from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from colorama import Fore

options = Options()
options.add_argument("--log-level=3")  # Suppress messages below ERROR level

driver = webdriver.Chrome(options=options)

# Setup Selenium
# webdriver_service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=webdriver_service, options=options)

# Navigate to the webpage
driver.get('https://octordle.com/daily/100')

# Wait for the page to load
# time.sleep(1)

guesses = ['party', 'shine', 'could']

# Define the layout of the keyboard
keyboard_layout = [
    # list('1234567890'),
    '',
    '',
    list(' qwertyuiop'),
    list(' asdfghjkl'),
    list('  zxcvbnm')
]
# Convert the layout into a dictionary mapping keys to their positions
keyboard_mapping = {
    key: (i, j)
    for i, row in enumerate(keyboard_layout)
    for j, key in enumerate(row)
}

for cur_guess in range(len(guesses)):
    for letter in guesses[cur_guess]:
        position = keyboard_mapping[letter]
        # print(f'The position of {letter} is {position}') # DEBUG
        driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[{position[0]}]/button[{position[1]}]').click()
        # key.click()
    # time.sleep(0.5)
    driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[4]/button[9]').click()

    print(f"Guess {cur_guess+1}: {guesses[cur_guess]}")
    for word_num in range(1, 9):
        for letter_num in range(0, 5):
            XPATH = f'/html/body/div[1]/div/div[2]/div[1]/div[{word_num}]/div[{cur_guess+1}]/div[{letter_num+1}]'
            output = driver.find_element(By.XPATH, XPATH).get_attribute("style")
            if output == 'background-color: rgb(255, 221, 102);':
                print(Fore.YELLOW + guesses[cur_guess][letter_num] + Fore.RESET, end='')
            elif output == 'background-color: rgb(0, 187, 51);':
                print(Fore.GREEN + guesses[cur_guess][letter_num] + Fore.RESET, end='')
            else:
                print(guesses[cur_guess][letter_num], end='')
        print()


wait = input('Press enter to quit')
# time.sleep(10)
driver.quit()
exit()
