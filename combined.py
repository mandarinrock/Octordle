from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from colorama import Fore
import word_lists
import random

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
                        # Get the count of green and yellow for the guess letter
                        green_count = response.count('g')
                        yellow_count = response.count('y')
                        # Get the count of the guess letter in the word
                        letter_count = allowed_answers[answer].count(guess[index])

                        if letter_count > green_count + yellow_count:
                            allowed_answers.pop(answer)
                            continue
                answer += 1
        elif response[index] == 'y' or response[index] == 'Y':
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

def get_keyboard_mapping():
    # Define the layout of the keyboard
    keyboard_layout = [
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
    return keyboard_mapping

def setup_driver():
    options = Options()
    options.add_argument("--log-level=3")  # Suppress messages below ERROR level
    options.add_argument("user-data-dir=/path/to/your/custom/profile")
    driver = webdriver.Chrome(options=options)
    return driver

def navigate_to_game(driver, url):
    driver.get(url)

def make_guess(driver, guess, keyboard_mapping):
    for letter in guess:
        position = keyboard_mapping[letter]
        driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[{position[0]}]/button[{position[1]}]').click()
    # time.sleep(1)
    driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[4]/button[9]').click()

def game_logic(driver, guesses, answer_lists, keyboard_mapping):
    answered = [False] * 8
    for cur_guess in range(14):
        if len(guesses) <= cur_guess:
            possible_answers = []
            for answer_list in answer_lists:
                if not answered[answer_lists.index(answer_list)]:
                    possible_answers.extend(answer_list)

            # count the frequency of each letter in the possible answers
            letter_freq = {}
            for word in possible_answers:
                for letter in word:
                    if letter in letter_freq:
                        letter_freq[letter] += 1
                    else:
                        letter_freq[letter] = 1

            # find the word with the most common letters
            max_common_letters = -1
            best_guess = None
            for word in possible_answers:
                common_letters = sum(letter_freq[letter] for letter in word)
                if common_letters > max_common_letters:
                    max_common_letters = common_letters
                    best_guess = word

            guesses.append(best_guess)

        guess = guesses[cur_guess]
        # print(f'Guesses: {guesses}')
        print(f'\nGuess {cur_guess+1}: {guess}\n')
        for letter in guess:
            position = keyboard_mapping[letter]
            # print(f'The position of {letter} is {position}') # DEBUG
            driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[{position[0]}]/button[{position[1]}]').click()
            # key.click()
        # time.sleep(1)
        driver.find_element(By.XPATH, f'/html/body/div[1]/div/div[3]/div/div[4]/button[9]').click()

        # wait = input('Press enter to continue')

        # print(f"Guess {cur_guess+1}: {guess}")
        # num_answered = 0
        try:
            for word_num in range(1, 9):
                # if len(answer_lists[word_num-1]) == 1:
                if answered[word_num-1]:
                    print(f'Answer {word_num}: {answer_lists[word_num-1][0]}')
                    # num_answered += 1
                    continue
                elif len(answer_lists[word_num-1]) < 1:
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
                if result == 'ggggg':
                    print(f'\tAnswer {word_num}: {guess}')
                    answered[word_num-1] = True
                    answer_lists[word_num-1] = [guess]
                    continue
                # print(f'\tlength before: {len(answer_lists[word_num-1])}', end='')
                #TEMP
                # backup = answer_lists[word_num-1].copy()
                answer_lists[word_num-1] = eliminate_words(answer_lists[word_num-1], guess, result)
                print(f'\t Possibilities: {len(answer_lists[word_num-1])}', end='')
                if len(answer_lists[word_num-1]) == 1:
                    print(f'\tAnswer {word_num}: {answer_lists[word_num-1][0]}', end='')
                    if answer_lists[word_num-1][0] not in guesses:
                        guesses.append(answer_lists[word_num-1][0])

                # elif len(answer_lists[word_num-1]) == 0:
                #     print(f'\n Something went wrong')
                #     print(f'Guess {cur_guess+1}: {guess}')
                #     print(f'Answer {word_num}: {backup}')
                print()
            # if num_answered == 8:
            #     print(f'All answers found!')
            #     break
        except:
            print(f'All answers found in {cur_guess} guesses!')
            for word_num in range(1, 9):
                print(f'Answer {word_num}: {answer_lists[word_num-1][0]}')
            return

def main():
    driver = setup_driver()
    navigate_to_game(driver, f'https://octordle.com/daily/{random.randint(1, 365)}')
    keyboard_mapping = get_keyboard_mapping()
    answer_lists = [word_lists.allowed_answers.copy() for _ in range(8)]
    # guesses = ['party', 'shine', 'could']
    # guesses = ['party']
    guesses = []
    game_logic(driver, guesses, answer_lists, keyboard_mapping)
    # wait = input('Press enter to quit')
    driver.quit()
    exit()

if __name__ == "__main__":
    main()
