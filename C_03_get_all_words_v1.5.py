import csv
import random

# Retrieve words from csv file and put them in a list
file = open("connections_quiz(Questions).csv","r")
all_words = list(csv.reader(file, delimiter=","))
file.close()

# Remove the first row (labels of what they are)
all_words.pop(0)

word_given = []
connected_answer = []


# Loop until we have four words with different connections
while len( word_given) < 4:
    potential_words = random.choice(all_words)
    
    # Get the words combination and check it's not all duplicate
    if potential_words[1] not in connected_answer:
        word_given.append(potential_words)
        connected_answer.append(potential_words[1])

print(word_given)
print(connected_answer)

print(f"The words are {word_given} their connected answer is {connected_answer}")


