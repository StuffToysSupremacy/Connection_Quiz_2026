import csv
import random
from tkinter import *
from functools import partial # To prevent unwanted windows

# helper functions go here
def get_word():
    """
    Retrieves words from csv file
    :return: list of words which each list item has the
    4 words and a word where the 4 words can be connected to form another word
    """
    # Retrieve words from csv file and put them in a list
    file = open("connections_quiz(Questions).csv", "r")
    all_words = list(csv.reader(file, delimiter=","))
    file.close()

    # Remove the first row (labels of what they are)
    all_words.pop(0)

    return all_words

def get_qn_words():
    """
    Choose four colours from larger list ensuring that the results are all different.
    :return: list of words and given word (connecting the words)
    """
    all_words_list = get_word()

    four_words = []
    four_answer = []

    word_given = []

    # Loop until we have four words with different connections
    while len(four_words) < 4:
        potential_words = random.choice(all_words_list)

        # Get the words combination and check it's not all duplicate
        if potential_words[1] not in four_answer:
            four_words.append(potential_words[4])
            four_answer.append(potential_words[0])

            word_given = random.choice(four_words)

    word_index = four_words.index(word_given)
    connected_answer = four_answer[word_index]

    print(four_words)
    print(four_answer)

    print("Word", word_given)
    print("Answer", connected_answer)

    return four_answer, connected_answer, word_given


class StartQuiz:
    """
    Initial Game inter-face (asks users how many questions they would like to do)
    """

    def __init__(self):
        """
        Gets number of questions from user
        """

        self.start_frame = Frame(padx=10, pady=10, bg="#E1D5E7")
        self.start_frame.grid()

        # Create start button...
        self.start_button = Button(self.start_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#5555D4", text="Start", width=30,
                                  command=self.check_questions)

        self.start_button.grid(row=1)

    def check_questions(self):
        """
        Checks users have entered 1 or more number of questions
        """
        Quiz(5)
        # Hide root window (ie: hide questions choice window).
        root.withdraw()


class Quiz:
    """
    Interface for answering the Connection Quiz
    """

    def __init__(self, how_many):

        # String Variables
        self.target_word = StringVar()

        # questions done - start with zero
        self.questions_done = IntVar()
        self.questions_done.set(0)

        self.questions_wanted = IntVar()
        self.questions_wanted.set(how_many)

        self.qn_words_list = []
        self.all_result_list = []
        self.all_answer_list = []

        self.quiz_box = Toplevel()

        self.quiz_frame = Frame(self.quiz_box, padx=10, pady=10, bg="#C09CD2")
        self.quiz_frame.grid()

        # body font for most labels...
        body_font = ("Arial", 12)

        # list for label details (text | font | background | row)
        quiz_labels_list = [
            ["Question # of #", ("Arial", 16, "bold"), "#C09CD2", 0 ],
            ["The word given: #", body_font, "#D0CEE2", 1],
            ["Choose the correct word. Good luck!", body_font, "#B4E8B4", 2],
            ["-" * 60, body_font, "#C09CD2", 3],
            ["Your answer was...(result)", body_font, "#71EB5F", 5]

        ]
        
        quiz_labels_ref = []
        for item in quiz_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)
            
            quiz_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = quiz_labels_ref[0]
        print("head label", self.heading_label)

        self.given_word_label = quiz_labels_ref[1]
        self.results_label = quiz_labels_ref[3]

        # set up word buttons...
        self.word_frame = Frame(self.quiz_frame, bg="#C09CD4")
        self.word_frame.grid(row=4)

        self.word_button_ref = []

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.word_button = Button(self.word_frame, font=("Arial", 12),
                                        text="Word", width=15,
                                      command=partial(self.question_result, item))
            self.word_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

            self.word_button_ref.append(self.word_button)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame, bg="#C09CD2")
        self.hints_stats_frame.grid(row=7)

        # List for buttons ( frame | text | bg | command | width | row | column )
        control_button_list = [
            [self.quiz_frame, "Next Question", "#FAF4AB", "", 21, 6, None],
            [self.hints_stats_frame, 'Hints',"#FAD7AC", "", 10, 7, 0],
            [self.hints_stats_frame, "Stats","#B1DDF0", "", 10, 7, 1],
            [self.quiz_frame, "End", "#FAD9D5", self.close_quiz,21, 8, None],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2],
                                         command=item[3], font=("Arial", 16, "bold"),
                                         fg="#000000", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # Retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_quiz_button = control_ref_list[3]

        # Once interface has been created, invoke new
        # question function for first question
        self.new_question()

    def new_question(self):
        """
        Chooses four words, pick one out of four words,
        works out which word has a connection to it.
        """

        # Retrieve number of questions done, add one to it and configure heading
        questions_done = self.questions_done.get()
        questions_done += 1
        self.questions_done.set(questions_done)

        questions_wanted = self.questions_wanted.get()

        # Get qn_word,  connected answer, and word_given...
        self.qn_words_list, connected_answer, word_given = get_qn_words()

        # Set the given word as word_given
        self.target_word.set(connected_answer)

        # Update heading and given word label. "Hide" result label
        self.heading_label.config(text=f"Question {questions_done} of {questions_wanted}")
        self.given_word_label.config(text=f"Given Word: {word_given}",
                                     font=("Arial", 14, "bold"))
        self.results_label.config(text=f"{'-' * 20}", bg="#F0F0F0")

        # Configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at the end of the last round
        for count, item in enumerate(self.word_button_ref):
            item.config(text=self.qn_words_list[count][0], state=NORMAL)

        self.next_button.config(state=DISABLED)

    def question_result(self, user_choice):
        """
        Retrieve which button was pushed (index 0-3), retrieves
        answer and then compare it with connected_answer, updates result,
        and adds result to stats list.
        """
        # Get qn_word,  connected answer, and word_given...
        self.qn_words_list, connected_answer, word_given = get_qn_words()

        # Get user answer word based on button pressed...
        # result = int(self.qn_words_list[user_choice][1])

        # alternate way to get button name. Good for if buttons have been scrambled!
        word_chosen = self.word_button_ref[user_choice].cget('text')

        # retrieve connected_answer and compare with user choice to find round result
        answer = self.target_word.get()
        self.all_answer_list.append(word_chosen)

        if word_chosen == answer:
            result_text = f"Success! {word_chosen} is connected to {connected_answer} :D"
            result_bg = "#71EB5F"
            self.all_result_list.append(word_chosen)

        else:
            result_text = f"Oops {word_chosen} is not the right answer D: It was {connected_answer}"
            result_bg = "#FF9992"
            self.all_result_list.append(0)

        self.results_label.config(text=result_text, bg=result_bg)

        # enable stats & next buttons, disable word buttons
        self.next_button.config(state=NORMAL)
        self.stats_button.config(state=NORMAL)

        # check to see if quiz is over
        questions_done = self.questions_done.get()
        questions_wanted = self.questions_wanted.get()

        if questions_done == questions_wanted:
            self.next_button.config(state=DISABLED, text="End of Quiz")
            self.end_quiz_button.config(text="Start Again", bg="#72BDFF")

        for item in self.word_button_ref:
            item.config(state=DISABLED)

    def close_quiz(self):
        # reshow root (ie: choose questions) and end current
        # quiz / allow new quiz to start
        root.deiconify()
        self.quiz_box.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Connection Quiz")
    StartQuiz()
    root.mainloop()

        
        
        
        
        
        
        