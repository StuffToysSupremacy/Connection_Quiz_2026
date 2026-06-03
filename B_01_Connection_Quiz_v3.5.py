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

    # find the position of the selected item
    word_index = four_words.index(word_given)
    connected_answer = four_answer[word_index]

    print(four_words)
    print(four_answer)

    print("Word", word_given)
    print("Answer", connected_answer)

    return four_answer, connected_answer, word_given


class StartQuiz():
    """
    Initial Game inter-face (asks users how many questions they would like to do)
    """

    def __init__(self):
        """
        Gets number of questions from user
        """

        self.start_frame = Frame(padx=10, pady=10, bg="#E1D5E7")
        self.start_frame.grid()

        # Strings for labels
        intro_string = ("In each question you will be asked to choose between four "
                        "options. Your goal is to select the right option of which word "
                        "connects with the word given. \n\n "
                        "To begin, please decide how many questions you want to do.")

        #  choose_string = "Oops - Please choose a whole number more than zero"
        choose_string = "How many questions would you like to do?"

        # List of labels to be made (text | font | fg | bg)
        start_labels_list = [
            ["Connection Quiz", ("Arial", 16, "bold"), None],
            [intro_string, ("Arial", 12), None ],
            [choose_string, ("Arial", 12, "bold"), "#009900" ]
        ]

        # create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0],font=item[1],
                               fg=item[2], bg="#E1D5E7",
                               wraplength=350, justify="left", pady=10,padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)


        # extract choice label so that it can be change to an
        # error message if necessary.

        self.choose_label = start_label_ref[2]

        #  Frame so that entry box and button can be in the same row.
        self.entry_area_frame = Frame(self.start_frame, bg="#E1D5E7")
        self.entry_area_frame.grid(row=3)

        self.num_question_entry = Entry(self.entry_area_frame, font=("Arial", 20, "bold"),
                                        width=12)
        self.num_question_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create start button...
        self.start_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                   fg="#FFFFFF", bg="#5555D4", text="Start", width=11,
                                   command=self.check_questions)

        self.start_button.grid(row=0, column=1)


    def check_questions(self):
            """
             Checks users have entered 1 or more question
            """

            # Retrieve how many questions wanted
            questions_wanted = self.num_question_entry.get()

            # Reset label and entry box (for when users come back to home screen)
            self.choose_label.config(fg="#009900", font=("Arial", 12, "bold"))
            self.num_question_entry.config(bg="#FFFFFF")

            error = "Oops - Please choose a whole number more than zero."
            has_errors = "no"

            # checks that # to do is a number above absolute zero
            try:
                questions_wanted = int(questions_wanted)
                if questions_wanted > 0:
                    # Invoke Quiz Class (and take across number of rounds)
                    Quiz(questions_wanted)
                    # Hide root window (ie: hide question choice window)
                    root.withdraw()
                else:
                    has_errors = "yes"

            except ValueError:
                has_errors = "yes"

            # display the error if necessary
            if has_errors == "yes":
                self.choose_label.config(text=error, fg="#990000",
                                         font=("Arial", 10, "bold"))
                self.num_question_entry.config(bg="#F4CCCC")
                self.num_question_entry.delete(0, END)


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

        self.qns_passed = IntVar()
        self.longest_streak = IntVar()
        self.current_streak = IntVar()

        self.qn_words_list = []
        self.all_result_list = []
        self.highest_result_list = []

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
            ["Your answer was...(result)", body_font, "#C09CD2", 5]

        ]
        
        quiz_labels_ref = []
        for item in quiz_labels_list:
            self.make_label = Label(self.quiz_frame, text=item[0], font=item[1],
                                    bg=item[2], wraplength=300, justify="left")
            self.make_label.grid(row=item[3], pady=10, padx=10)
            
            quiz_labels_ref.append(self.make_label)

        # Retrieve Labels so they can be configured later
        self.heading_label = quiz_labels_ref[0]
        self.given_word_label = quiz_labels_ref[1]
        self.results_label = quiz_labels_ref[4]

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
            [self.quiz_frame, "Next Question", "#FAF4AB", self.new_question, 21, 6, None],
            [self.hints_stats_frame, 'Hints',"#FAD7AC", self.to_hints, 10, 7, 0],
            [self.hints_stats_frame, "Stats","#B1DDF0", self.to_stats, 10, 7, 1],
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
        self.to_hints_button = control_ref_list[2]
        self.to_stats_button = control_ref_list[2]
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
        self.results_label.config(text=f"{'-' * 60}", bg="#C09CD2")

        # Configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at the end of the last round
        for count, item in enumerate(self.word_button_ref):
            item.config(text=self.qn_words_list[count], state=NORMAL)


        self.next_button.config(state=DISABLED)


    def question_result(self, user_choice):
        """
        Retrieve which button was pushed (index 0-3), retrieves
        answer and then compare it with connected_answer, updates result,
        and adds result to stats list.
        """

        # way to get button name. Good for if buttons have been scrambled!
        word_chosen = self.word_button_ref[user_choice].cget('text')

        # retrieve connected_answer and compare with user choice to find round result
        answer = self.target_word.get()


        if word_chosen == answer:
            result_text = f"Success! {word_chosen} is the correct answer :D"
            result_bg = "#71EB5F"
            self.all_result_list.append("1")

            qns_passed = self.qns_passed.get()
            qns_passed += 1
            self.qns_passed.set(qns_passed)

            current_streak = self.current_streak.get()
            current_streak += 1
            self.current_streak.set(current_streak)

        else:
            result_text = f"Oops {word_chosen} is not the right answer D:"
            result_bg = "#FF9992"
            self.all_result_list.append("0")
            self.current_streak.set(0)

        self.results_label.config(text=result_text, bg=result_bg)


        # enable stats & next buttons, disable word buttons
        self.next_button.config(state=NORMAL)
        self.to_stats_button.config(state=NORMAL)

        # check to see if quiz is over
        questions_done = self.questions_done.get()
        questions_wanted = self.questions_wanted.get()

        if questions_done == questions_wanted:
            self.next_button.config(state=DISABLED, text="End of Quiz")
            self.end_quiz_button.config(text="Start Again", bg="#72BDFF")

        for item in self.word_button_ref:
            item.config(state=DISABLED)


    def to_hints(self):
        """
        Displays hints for playing game
        :return:
        """
        DisplayHints(self)


    def close_quiz(self):
        # reshow root (ie: choose questions) and end current
        # quiz / allow new quiz to start
        root.deiconify()
        self.quiz_box.destroy()

    def to_stats(self):
        """
        Retrieves everything we need to display the quiz / questions statistics
        """

        # IMPORTANT: retrieve # of questions
        # pass / fail as a number (rather than the 'self' container)
        qns_passed = self.qns_passed.get()
        longest_streak = self.longest_streak.get()
        current_streak = self.current_streak.get()
        stats_bundle = [qns_passed, self.all_result_list,
                        self.highest_result_list, longest_streak, current_streak]

        Stats(self, stats_bundle)


class DisplayHints:
    """
    Displays hints for Connection Quiz
    """

    def __init__(self, partner):

        # setup dialogue box and background color
        background = "#FAD7AC"
        self.hints_box = Toplevel()

        # disable hints button
        partner.to_hints_button.config(state=DISABLED)

        # If users press cross at top, closes hints and
        # 'releases' hints_button
        self.hints_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_hints, partner))
        self.hints_frame = Frame(self.hints_box, width=300,
                                 height=200)
        self.hints_frame.grid()

        self.hints_heading_label = Label(self.hints_frame,
                                         text="Hints",
                                         font=("Arial", 14, "bold"))
        self.hints_heading_label.grid(row=0)

        hints_text = ("The connection between the given word and "
                      "the answer is that they are one word.\n\n"
                      "The answer can either be before the given word"
                      "or after the given word. \n\n"
                      "E.g:\n"
                      "          ____(given word)  or  (given word)____ \n\n"
                      "Good Luck!")
        self.hints_text_label = Label(self.hints_frame,
                                      text=hints_text, wraplength=350,
                                      justify="left")
        self.hints_text_label.grid(row=1, pady=10)

        self.dismiss_button = Button(self.hints_frame,
                                     font=("Arial", 12, "bold"),
                                     text="Dismiss", bg="#DE852C",
                                     fg="#000000",
                                     width=30,
                                     command=partial(self.close_hints, partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set background colour on
        # everything except the buttons.
        recolour_list = [self.hints_frame, self.hints_heading_label,
                         self.hints_text_label]

        for item in recolour_list:
            item.config(bg=background)

    def close_hints(self, partner):
        """
        Closes hints dialogue box (and enables hints button)
        """
        # Put hints button back to normal...
        partner.to_hints_button.config(state=NORMAL)
        self.hints_box.destroy()


class Stats:
    """
    Displays stats for Connection Quiz
    """

    def __init__(self, partner, all_stats_info):

        # Extract information from master list...
        qns_passed = all_stats_info[0]
        user_result = all_stats_info[1]
        high_results = all_stats_info[2]
        longest_streak = all_stats_info[3]
        current_steak = all_stats_info[4]

        self.stats_box = Toplevel()

        # disable stats button
        partner.to_stats_button.config(state=DISABLED)

        # If users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))
        self.stats_frame = Frame(self.stats_box, width=350, bg="#B1DDF0")
        self.stats_frame.grid()

        print(user_result)

        # Math to populate Stats dialogue...
        questions_done = len(user_result)

        print(questions_done)
        print(user_result)

        success_rate = qns_passed / questions_done * 100

        print(f"qns passed ={qns_passed}")


        # Strings for Stats labels...
        success_string = f"Success Rate: {qns_passed} / {questions_done} "
        accuracy_string = f"Accuracy: {success_rate:.0f}%"
        current_streak_string = f"Current Streak: {current_steak}"


        # custom comment text and formatting
        if qns_passed == questions_done:
            comment_string = "Excellent!! You got the highest result possible!"
            comment_colour = "#71EB5F"

        elif qns_passed == 0:
            comment_string = "Oops - You've lost every round! You might want to look at the hints!"
            comment_colour = "#FF9992"

        else:
            comment_string = ""
            comment_colour = "#B1DDF0"

        bg = "#B1DDF0"

        heading_font = ("Arial", 16, "bold")
        normal_font = ("Arial", 14)
        comment_font = ("Arial", 13)

        # Label list (text | font | bg | 'Sticky') "W" is west or left aligned if "" its centered
        all_stats_string = [
            ["Statistics", heading_font, bg, ""],
            [success_string, normal_font, bg, "W"],
            [accuracy_string, normal_font, bg, "W"],
            [comment_string, comment_font, bg, "W"],
            [current_streak_string, normal_font, bg, "W"]
        ]

        stats_label_ref_list = []
        for count, item in enumerate(all_stats_string):
            self.stats_label = Label(self.stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left",bg=item[2],
                                     padx=30, pady=5)
            self.stats_label.grid(row=count, sticky=item[3], padx=10)
            stats_label_ref_list.append(self.stats_label)

        # Configure comment label background (for all won / all lost)
        stats_comment_label = stats_label_ref_list[3]
        stats_comment_label.config(bg=comment_colour)

        self.dismiss_button = Button(self.stats_frame,
                                     font=("Arial", 16, "bold"),
                                     text="Dismiss", bg="#3774DE",
                                     fg="#000000", width=30,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=7, padx=10, pady=10)

        # closes stats dialogue (used by button and x at top of dialogue)

    def close_stats(self, partner):
            """
            Closes stats dialogue box (and enables stats button)
            """
            # Put stats button back to normal...
            partner.to_stats_button.config(state=NORMAL)
            self.stats_box.destroy()




if __name__ == "__main__":
    root = Tk()
    root.title("Connection Quiz")
    StartQuiz()
    root.mainloop()

        
        
        
        
        
        
        