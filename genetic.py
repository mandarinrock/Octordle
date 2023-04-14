import word_lists
permitted_answers = word_lists.allowed_answers
permitted_guesses = word_lists.allowed_guesses

import random
from itertools import permutations, product, combinations

def calculate_match_score(word1, word2):
    return sum(1 for a, b in zip(word1, word2) if a == b)

def find_best_starting_sequence(permitted_guesses, permitted_answers, seq_length=3):
    best_fitness = 0
    best_sequence = None
    iteration = 0
    
    for sequence in combinations(permitted_guesses, seq_length):
        total_match_score = 0
        for guess in sequence:
            for answer in permitted_answers:
                total_match_score += calculate_match_score(guess, answer)
        
        if total_match_score > best_fitness:
            best_fitness = total_match_score
            best_sequence = sequence

        if iteration % 100 == 0:
            print(f'Iteration {iteration}: Best sequence {best_sequence}, fitness {best_fitness}')
        iteration += 1

    return best_sequence

best_starting_sequence = find_best_starting_sequence(permitted_guesses, permitted_answers)
print("Best starting sequence:", best_starting_sequence)