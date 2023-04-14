import word_lists
from itertools import product
from collections import Counter

permitted_answers = word_lists.allowed_answers
permitted_guesses = word_lists.allowed_guesses

def calculate_match_score(word1, word2):
    return sum(1 for a, b in zip(word1, word2) if a == b)

def find_best_starting_sequence(permitted_answers, permitted_guesses, seq_length=3):
    scores = Counter()

    for guess_sequence in product(permitted_guesses, repeat=seq_length):
        for answer in permitted_answers:
            seq_score = sum(calculate_match_score(guess, answer) for guess in guess_sequence)
            scores[guess_sequence] += seq_score

    best_starting_sequence = scores.most_common(1)[0][0]
    return best_starting_sequence

best_starting_sequence = find_best_starting_sequence(permitted_answers, permitted_guesses)
print("Best starting sequence:", best_starting_sequence)