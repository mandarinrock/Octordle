import word_lists
from itertools import combinations

permitted_answers = word_lists.allowed_answers
permitted_guesses = word_lists.allowed_guesses

def calculate_match_score(word1, word2):
    return len(set(word1) & set(word2))

def sequence_penalty(sequence):
    unique_letter_coverage = len(set(''.join(sequence)))
    return -0.1 * unique_letter_coverage

def test_sequence_fitness(sequence, permitted_answers):
    total_match_score = 0
    for guess in sequence:
        for answer in permitted_answers:
            total_match_score += calculate_match_score(guess, answer)
    penalty = sequence_penalty(sequence)
    return total_match_score - penalty

# Input your own sequence of 3 words
sequences = [('shine', 'party', 'could'), ('crane', 'pouty', 'gilds'), ('field', 'mount', 'spark'), ('aahed', 'abcee', 'saree'), ('aahed', 'aargh', 'saree')]
for your_sequence in sequences:
    fitness = test_sequence_fitness(your_sequence, permitted_answers)
    print(f'Fitness of your sequence {your_sequence}: {fitness}')
