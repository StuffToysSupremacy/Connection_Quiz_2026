import csv
import random

# Retrieve words from csv file and put them in a list
file = open("connections_quiz(Questions).csv","r")
all_answers = list(csv.reader(file, delimiter=","))
# all_words = list(csv.reader(file, nrow=))
file.close()


#
# # Remove the first row (labels of what they are)
# all_words.pop(0)
#
#
given_word = []
connected_answer = []
#
#
# # Loop until we have four words with different connections
# while len( given_word) < 4:
#     potential_words = random.choice(all_words)
#
#     # Get the words combination and check it's not all duplicate
#     if potential_words[1] not in connected_answer:
#         given_word.append(potential_words[4])
#         connected_answer.append(potential_words[1])
#
# print(f"The colour is {given_word} the correct answer is {connected_answer}")

while len(given_word) <4:
    potential_words = random.choice(all_answers)
    #
    # # Get the words combination and check it's not all duplicate
    if potential_words[1] not in connected_answer:
        given_word.append(potential_words[3])
        connected_answer.append(potential_words[0])



