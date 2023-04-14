import word_lists
from itertools import combinations

permitted_answers = word_lists.allowed_answers
permitted_guesses = word_lists.allowed_guesses

def calculate_match_score(word1, word2):
    return len(set(word1) & set(word2))

def sequence_penalty(sequence):
    unique_letter_coverage = len(set(''.join(sequence)))
    return -0.1 * unique_letter_coverage

def find_best_starting_sequence(permitted_guesses, permitted_answers, seq_length=3):
    best_fitness = 0
    best_sequence = None
    iteration = 0
    
    for sequence in combinations(permitted_guesses, seq_length):
        total_match_score = 0
        for guess in sequence:
            for answer in permitted_answers:
                total_match_score += calculate_match_score(guess, answer)
        
        penalty = sequence_penalty(sequence)
        fitness = total_match_score - penalty

        if fitness > best_fitness:
            best_fitness = fitness
            best_sequence = sequence

        if iteration % 100 == 0:
            print(f'Iteration {iteration}: Best sequence {best_sequence}, fitness {best_fitness}')
        iteration += 1

    return best_sequence

best_starting_sequence = find_best_starting_sequence(permitted_guesses, permitted_answers)
print("Best starting sequence:", best_starting_sequence)
