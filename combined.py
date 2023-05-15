from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from colorama import Fore
import word_lists

def eliminate_words(allowed_answers, guess, response):
    """
    Eliminate words from the allowed answers list based on the guess and response.

    Args:
        allowed_answers (list): The list of allowed answers.
        guess (str): The guessed word.
        response (str): The generated response for the guess.

    Returns:
        list: The updated list of allowed answers.
    """

    for index in range(len(guess)):
        if response[index] == 'g' or response[index] == 'G':
            answer = 0
            while answer < len(allowed_answers):
                if allowed_answers[answer][index] != guess[index]:
                    allowed_answers.pop(answer)
                    continue
                answer += 1
        elif response[index] == 'b' or response[index] == 'B':
            answer = 0
            while answer < len(allowed_answers):
                if allowed_answers[answer][index] == guess[index]:
                    allowed_answers.pop(answer)
                    continue
                else:
                    if guess[index] in allowed_answers[answer]:
                        for letter in range(len(guess)):
                            if guess[letter] == guess[index] and response[letter] == 'g' or response[letter] == 'G':
                                break
                        allowed_answers.pop(answer)
                        continue
                answer += 1
            # TODO add code to eliminate words that contain black letters as long as they are not marked green or yellow elsewhere
        elif response[index] == 'y' or response[index] == 'Y':
            # TODO add functionality to require multiple of the yellow'd letter if it is marked yellow but is also marked green elsewhere
            answer = 0
            while answer < len(allowed_answers):
                if allowed_answers[answer][index] == guess[index]:
                    allowed_answers.pop(answer)
                    continue
                elif guess[index] not in allowed_answers[answer]:
                    allowed_answers.pop(answer)
                    continue
                answer += 1
    return allowed_answers

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

answer_lists = [word_lists.allowed_answers.copy(), word_lists.allowed_answers.copy(), word_lists.allowed_answers.copy(), word_lists.allowed_answers.copy(), word_lists.allowed_answers.copy(), word_lists.allowed_answers.copy(), word_lists.allowed_answers.copy(), word_lists.allowed_answers.copy()]

# for cur_guess in range(guesses):
for cur_guess in range(14):
    if len(guesses) <= cur_guess:
        # possible_answers = []
        for answer_list in answer_lists:
            if len(answer_list) > 1:
                print(f'Answer list {answer_lists.index(answer_list)+1}: {answer_list}')

        guesses.append(input("Enter guess: ").lower())
    guess = guesses[cur_guess]
    print(f'Guesses: {guesses}')
    print(f'Guess {cur_guess+1}: {guess}')
    for letter in guess:
        position = keyboard_mapping[letter]
        # print(f'The position of {letter} is {position}') # DEBUG
        driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[{position[0]}]/button[{position[1]}]').click()
        # key.click()
    time.sleep(1)
    driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[4]/button[9]').click()

    # print(f"Guess {cur_guess+1}: {guess}")
    for word_num in range(1, 9):
        if len(answer_lists[word_num-1]) == 1:
            print(f'Answer {word_num}: {answer_lists[word_num-1][0]}')
            continue
        elif len(answer_lists[word_num-1]) < 0:
            print(f'Something went wrong with word {word_num}')
            continue
        result = ''
        for letter_num in range(0, 5):
            XPATH = f'/html/body/div[1]/div/div[2]/div[1]/div[{word_num}]/div[{cur_guess+1}]/div[{letter_num+1}]'
            output = driver.find_element(By.XPATH, XPATH).get_attribute("style")
            if output == 'background-color: rgb(255, 221, 102);':
                print(Fore.YELLOW + guess[letter_num] + Fore.RESET, end='')
                result += 'y'
            elif output == 'background-color: rgb(0, 187, 51);':
                print(Fore.GREEN + guess[letter_num] + Fore.RESET, end='')
                result += 'g'
            else:
                try:
                    print(guess[letter_num], end='')
                    result += 'b'
                except:
                    print(guess)
                    print(letter_num)
                # print(guess[letter_num], end='')
                # result += 'b'
        print(f'\tlength before: {len(answer_lists[word_num-1])}', end='')
        #TEMP
        backup = answer_lists[word_num-1].copy()
        answer_lists[word_num-1] = eliminate_words(answer_lists[word_num-1], guess, result)
        print(f'\t length after: {len(answer_lists[word_num-1])}', end='')
        if len(answer_lists[word_num-1]) == 1:
            print(f'\tAnswer {word_num}: {answer_lists[word_num-1][0]}')
            if answer_lists[word_num-1][0] not in guesses:
                guesses.append(answer_lists[word_num-1][0])
        elif len(answer_lists[word_num-1]) == 0:
            print(f'\n Something went wrong')
            print(f'Guess {cur_guess+1}: {guess}')
            print(f'Answer {word_num}: {backup}')
        print()


wait = input('Press enter to quit')
driver.quit()
exit()