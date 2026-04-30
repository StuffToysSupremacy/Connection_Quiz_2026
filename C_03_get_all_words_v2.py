import csv
import random

# Retrieve words from csv file and put them in a list
file = open("connections_quiz(Questions).csv","r")
all_words = list(csv.reader(file, delimiter=","))
file.close()

# Remove the first row (labels of what they are)
all_words.pop(0)

four_words = []
four_answer = []

given_word = []



# Loop until we have four words with different connections
while len(four_words) < 4:
    potential_words = random.choice(all_words)

    # Get the words combination and check it's not all duplicate
    if potential_words[1] not in four_answer:
        four_words.append(potential_words[4])
        four_answer.append(potential_words[0])

        given_word = random.choice(four_words)

word_index = four_words.index(given_word)
connected_answer = four_answer[word_index]

print(four_words)
print(four_answer)

print(f"The word = {given_word} \n" 
      f"the answer = {connected_answer}")