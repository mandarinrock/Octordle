import word_lists
real_word = ''
def load_word_list():
    return word_lists.allowed_answers, word_lists.allowed_guesses

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
    print("New length:", len(allowed_answers))
    if len(allowed_answers) == 1:
        print(allowed_answers[0])
    elif guess == 'could':
        print(allowed_answers)
    elif len(allowed_answers) < 100:
        print(allowed_answers)
    return allowed_answers

def main():
    allowed_answers, allowed_guesses = load_word_list()
    # print(allowed_answers)
    # print(allowed_guesses)
    print("Length:", len(allowed_answers))

    while len(allowed_answers) > 1:
        guess = input("Guess a word: ")
        response = input("Response: ")
        allowed_answers = eliminate_words(allowed_answers, guess, response)

if __name__ == '__main__':
    main()