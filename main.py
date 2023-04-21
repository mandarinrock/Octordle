import word_lists
from concurrent.futures import ProcessPoolExecutor
real_word = ''

def load_word_list():
    """
    Load allowed answers and allowed guesses from the word_lists module.

    Returns:
        tuple: A tuple containing the list of allowed answers and the list of allowed guesses.
    """
    return word_lists.allowed_answers

def generate_response(guess, answer=real_word):
    """
    Generate a response based on the guess and the answer.

    Args:
        guess (str): The guessed word.
        answer (str): The correct answer. Defaults to real_word.

    Returns:
        str: A string representing the response.
    """
    response = ''
    for index in range(len(guess)):
        if guess[index] == answer[index]:
            response += 'g'
        elif guess[index] in answer:
            response += 'y'
        else:
            response += 'b'
    return response


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
                    if(allowed_answers[answer] == real_word):
                        print("Removing", allowed_answers[answer], "because", guess[index], "is yellow but", allowed_answers[answer][index], "is not.")
                    allowed_answers.pop(answer)
                    continue
                elif guess[index] not in allowed_answers[answer]:
                    if(allowed_answers[answer] == real_word):
                        print("Removing", allowed_answers[answer], "because", guess[index], "is yellow2 but", allowed_answers[answer][index], "is not.")
                    allowed_answers.pop(answer)
                    continue
                answer += 1
    return allowed_answers

def score_guesses(guesses, allowed_answers, best_score):
    """
    Score the guesses based on their ability to reduce the list of allowed answers.

    Args:
        guesses (list): The list of guessed words.
        allowed_answers (list): The list of allowed answers.

    Returns:
        float: The score for the given guesses.
    """
    score = 0
    for answer in allowed_answers:
        temp_answers = allowed_answers.copy()
        for guess in guesses:
            temp_answers = eliminate_words(temp_answers, guess, generate_response(guess, answer))
        score += len(temp_answers)
        if score > best_score:
            # print("Score for " + str(guesses) + ":" + str(score))
            print("bad")
            return score
    print(score)
    # print("Score for " + str(guesses) + ":" + str(score))
    return score

# def process_guesses(allowed_answers, best_score):
#     with ProcessPoolExecutor() as executor:
#         # Prepare a list of tuples containing all unique pairs of indices
#         guess_pairs = [(i, j) for i in range(len(allowed_answers)) for j in range(i + 1, len(allowed_answers))]

#         # Use the executor to process the score_guesses function for each pair of indices
#         results = list(executor.map(score_guesses, guess_pairs, [allowed_answers] * len(guess_pairs), [best_score] * len(guess_pairs)))

#     return results

def generate_guesses(allowed_answers):
    """
    Generate the best guesses based on their ability to reduce the list of allowed answers.

    Args:
        allowed_answers (list): The list of allowed answers.

    Returns:
        tuple: A tuple containing the best guesses and the best score.
    """
    best_guess = ''
    best_score = len(allowed_answers) * len(allowed_answers) * len(allowed_answers) * len(allowed_answers)
    # best_score = score_guesses(['oaken', 'cupid'], allowed_answers, best_score)
    # best_score = score_guesses(['shine', 'party'], allowed_answers, best_score)
    # best_score = score_guesses(['shine', 'party', 'could'], allowed_answers, best_score)
    # best_score = 10000
    # results = process_guesses(allowed_answers, best_score)
    # print("Results:", results)
    cur = 0
    for first in range(len(allowed_answers)):
        for second in range(first + 1, len(allowed_answers)):
            for third in range(second + 1, len(allowed_answers)):

                # score = results[cur]
                cur += 1
                guesses = [allowed_answers[first], allowed_answers[second], allowed_answers[third]]
                if guesses[0][0] == guesses[1][0] or guesses[0][1] == guesses[1][1] or guesses[0][2] == guesses[1][2] or guesses[0][3] == guesses[1][3] or guesses[0][4] == guesses[1][4]:
                    continue
                if guesses[0][0] == guesses[2][0] or guesses[0][1] == guesses[2][1] or guesses[0][2] == guesses[2][2] or guesses[0][3] == guesses[2][3] or guesses[0][4] == guesses[2][4]:
                    continue
                if guesses[1][0] == guesses[2][0] or guesses[1][1] == guesses[2][1] or guesses[1][2] == guesses[2][2] or guesses[1][3] == guesses[2][3] or guesses[1][4] == guesses[2][4]:
                    continue
                if 's' not in guesses[0] and 's' not in guesses[1] and 's' not in guesses[2]:
                    continue
                if 'e' not in guesses[0] and 'e' not in guesses[1] and 'e' not in guesses[2]:
                    continue
                if 'a' not in guesses[0] and 'a' not in guesses[1] and 'a' not in guesses[2]:
                    continue
                if 't' not in guesses[0] and 't' not in guesses[1] and 't' not in guesses[2]:
                    continue
                if 'o' not in guesses[0] and 'o' not in guesses[1] and 'o' not in guesses[2]:
                    continue
                if 'n' not in guesses[0] and 'n' not in guesses[1] and 'n' not in guesses[2]:
                    continue
                if 'i' not in guesses[0] and 'i' not in guesses[1] and 'i' not in guesses[2]:
                    continue
                if 'r' not in guesses[0] and 'r' not in guesses[1] and 'r' not in guesses[2]:
                    continue
                if 'l' not in guesses[0] and 'l' not in guesses[1] and 'l' not in guesses[2]:
                    continue

                print("[" + str(cur) + "] Score for " + str(guesses), end=": ")
                score = score_guesses(guesses, allowed_answers, best_score)
                # print("[" + str(cur) + "] Score for " + str(guesses) + ":" + str(score))
                if score < best_score:
                    best_guess = guesses
                    best_score = score
                    print("New best guess:", best_guess, "with score", best_score)
                    with open('best_guesses.txt', "a") as f:
                        f.write(str(best_guess) + " " + str(best_score) + "\n")
    return best_guess, best_score

def main():
    """
    The main function to run the program.
    """
    allowed_answers = load_word_list()
    generate_guesses(allowed_answers)

if __name__ == '__main__':
    main()