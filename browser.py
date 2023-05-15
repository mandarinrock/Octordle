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
time.sleep(5)

guess = 'party'
key = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[2]/button[10]')
key.click()
key = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[3]/button[1]')
key.click()
key = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[2]/button[4]')
key.click()
key = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[2]/button[5]')
key.click()
key = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[2]/button[6]')
key.click()
key = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[4]/button[9]')
key.click()
time.sleep(10)
driver.quit()
exit()
keyboard = ['qwertyuiop','asdfghjkl','zxcvbnm']
# For each letter in 'party', find the corresponding key and click it
for letter in guess:
    for row in range(len(keyboard)):
        # print(letter)
        if letter in keyboard[row]:
            print(f'letter: {letter}')
            print(f'keyboard[row+1] ({row+1}): {keyboard[row+1]}')
            # //*[@id="keyboard-wrap"]/div[3]/button[5]
            
            print(f'keyboard[row+1].index({letter}) : {keyboard[row+1].index(letter)}')
            # break
            # key = driver.find_element(By.XPATH, f'//*[@id="keyboard-wrap"]/div[{row+1}]/button[{keyboard[row].index(letter)+1}]')
            
            key.click()
            break


# Remember to close the driver after you're done
# driver.quit()
