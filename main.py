import word_lists
real_word = ''

debug = True
debug = False

def load_word_list():
    return word_lists.allowed_answers, word_lists.allowed_guesses

def generate_response(guess, answer=real_word):
    # Generate response
    response = ''
    for index in range(len(guess)):
        if guess[index] == answer[index]:
            response += 'g'
        elif guess[index] in answer:
            response += 'y'
        else:
            response += 'b'
    if debug:
        print("Response:", response)
    return response


def eliminate_words(allowed_answers, guess, response):
    # Eliminate words that don't match the response

    for index in range(len(guess)):
        if response[index] == 'g' or response[index] == 'G':
            answer = 0
            while answer < len(allowed_answers):
                if allowed_answers[answer][index] != guess[index]:
                    if(allowed_answers[answer] == real_word):
                        print("Removing", allowed_answers[answer], "because", guess[index], "is green but", allowed_answers[answer][index], "is not.")
                    allowed_answers.pop(answer)
                    continue
                answer += 1
        elif response[index] == 'b' or response[index] == 'B':
            answer = 0
            while answer < len(allowed_answers):
                if allowed_answers[answer][index] == guess[index]:
                    if(allowed_answers[answer] == real_word): 
                        print("Removing", allowed_answers[answer], "because", guess[index], "is black but", allowed_answers[answer][index], "is not.")
                    allowed_answers.pop(answer)
                    continue
                else:
                    if guess[index] in allowed_answers[answer]:
                        for letter in range(len(guess)):
                            if guess[letter] == guess[index] and response[letter] == 'g' or response[letter] == 'G':
                                break
                        if(allowed_answers[answer] == real_word):
                            print("Removing", allowed_answers[answer], "because", guess[index], "is black but", allowed_answers[answer][index], "is not.")
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
    if debug:
        print("New length:", len(allowed_answers))
        if len(allowed_answers) == 1:
            print(allowed_answers[0])
        # elif guess == 'could':
        #     print(allowed_answers)
        elif len(allowed_answers) < 100 and debug:
            print(allowed_answers)
    return allowed_answers

def score_guesses(guesses, allowed_answers):
    # Score guesses
    score = 0
    print("Scoring guesses:", guesses)
    for answer in allowed_answers:
        temp_answers = allowed_answers.copy()
        for guess in guesses:
            temp_answers = eliminate_words(temp_answers, guess, generate_response(guess, answer))
        score += len(temp_answers)

    score = score / len(allowed_answers)
    print("Score for " + str(guesses) + ":" + str(score))
    return score

def generate_guesses(allowed_guesses, allowed_answers):
    # Generate guesses
    best_guess = ''
    best_score = len(allowed_answers)
    best_score = score_guesses(['shine', 'party', 'could'], allowed_answers)
    for first in range(len(allowed_guesses)):
        for second in range(first + 1, len(allowed_guesses)):
            for third in range(second + 1, len(allowed_guesses)):
                # for fourth in range(third + 1, len(allowed_guesses)):
                guesses = [allowed_guesses[first], allowed_guesses[second], allowed_guesses[third]]
                score = score_guesses(guesses, allowed_answers)
                if score < best_score:
                    best_guess = guesses
                    best_score = score
                    print("New best guess:", best_guess, "with score", best_score)
                    with open('best_guesses.txt', "a") as f:
                        f.write(str(best_guess) + " " + str(best_score) + "\n")
    return best_guess, best_score

def main():
    allowed_answers, allowed_guesses = load_word_list()
    # print(allowed_answers)
    # print(allowed_guesses)
    # print(generate_response('shine', 'dance'))
    # print(generate_response('party', 'dance'))
    # print(generate_response('could', 'dance'))
    # print(generate_response('dance', 'dance'))
    # return

    # print("Length:", len(allowed_answers))

    # while len(allowed_answers) > 1:
    #     guess = input("Guess a word: ")
    #     response = input("Response: ")
    #     allowed_answers = eliminate_words(allowed_answers, guess, response)
    # score_guesses(['shine', 'party', 'could'], allowed_answers)
    # score_guesses(['crane', 'pouty', 'gilds'], allowed_answers)


    generate_guesses(allowed_guesses, allowed_answers)

if __name__ == '__main__':
    main()