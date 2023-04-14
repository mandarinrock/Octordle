import word_lists
permitted_answers = word_lists.allowed_answers
permitted_guesses = word_lists.allowed_guesses

def calculate_match_score(word1, word2):
    return sum(1 for a, b in zip(word1, word2) if a == b)

def test_sequence_fitness(sequence, permitted_answers):
    total_match_score = 0
    for guess in sequence:
        for answer in permitted_answers:
            total_match_score += calculate_match_score(guess, answer)
    return total_match_score

# Input your own sequence of 3 words
# your_sequence = ('shine', 'party', 'could')
# your_sequence = ('crane', 'pouty', 'gilds')
# your_sequence = ('field', 'mount', 'spark')
your_sequence = ('aahed', 'aargh', 'saree')
fitness = test_sequence_fitness(your_sequence, permitted_answers)
print(f'Fitness of your sequence {your_sequence}: {fitness}')