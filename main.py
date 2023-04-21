import word_lists
real_word = ''

def load_word_list():
    """
    Load allowed answers and allowed guesses from the word_lists module.

    Returns:
        tuple: A tuple containing the list of allowed answers and the list of allowed guesses.
    """
    return word_lists.allowed_answers, word_lists.allowed_guesses

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
    worst = 7
    # print("Scoring guesses:", guesses)
    for answer in allowed_answers:
        temp_answers = allowed_answers.copy()
        for guess in guesses:
            temp_answers = eliminate_words(temp_answers, guess, generate_response(guess, answer))
        # if len(temp_answers) > worst:
        #     return best_score
        score += len(temp_answers)
        if score > best_score:
            return score
        # print(answer, temp_answers)
    # score = score / len(allowed_answers)
    print("Score for " + str(guesses) + ":" + str(score))
    return score

def generate_guesses(allowed_guesses, allowed_answers):
    """
    Generate the best guesses based on their ability to reduce the list of allowed answers.

    Args:
        allowed_guesses (list): The list of allowed guesses.
        allowed_answers (list): The list of allowed answers.

    Returns:
        tuple: A tuple containing the best guesses and the best score.
    """
    best_guess = ''
    best_score = len(allowed_answers) * 1.7
    # best_score = 3000
    # best_score = score_guesses(['shine', 'party', 'could'], allowed_answers, best_score)
    cur = 0
    for first in range(len(allowed_answers)):
        for second in range(first + 1, len(allowed_answers)):
            # print(allowed_answers[first], allowed_answers[second], cur)
            for third in range(second + 1, len(allowed_answers)):
                cur += 1
                guesses = [allowed_answers[first], allowed_answers[second], allowed_answers[third]]
                if allowed_answers[first][0] == allowed_answers[second][0] or allowed_answers[first][0] == allowed_answers[third][0] or allowed_answers[second][0] == allowed_answers[third][0]:
                    continue
                if allowed_answers[first][1] == allowed_answers[second][1] or allowed_answers[first][1] == allowed_answers[third][1] or allowed_answers[second][1] == allowed_answers[third][1]:
                    continue
                if allowed_answers[first][2] == allowed_answers[second][2] or allowed_answers[first][2] == allowed_answers[third][2] or allowed_answers[second][2] == allowed_answers[third][2]:
                    continue
                if allowed_answers[first][3] == allowed_answers[second][3] or allowed_answers[first][3] == allowed_answers[third][3] or allowed_answers[second][3] == allowed_answers[third][3]:
                    continue
                if allowed_answers[first][4] == allowed_answers[second][4] or allowed_answers[first][4] == allowed_answers[third][4] or allowed_answers[second][4] == allowed_answers[third][4]:
                    continue
                if 's' not in allowed_answers[first] and 's' not in allowed_answers[second] and 's' not in allowed_answers[third]:
                    continue
                if 'e' not in allowed_answers[first] and 'e' not in allowed_answers[second] and 'e' not in allowed_answers[third]:
                    continue


                score = score_guesses(guesses, allowed_answers, best_score)
                # print("[" + str(cur) + "/12406605875] Score for " + str(guesses) + ":" + str(score))
                # print("Score for " + str(guesses) + ":" + str(score))
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
    allowed_answers, allowed_guesses = load_word_list()
    generate_guesses(allowed_guesses, allowed_answers)

if __name__ == '__main__':
    main()