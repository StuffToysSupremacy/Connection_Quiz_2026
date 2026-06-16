from tkinter import *
from functools import partial # To prevent unwanted windows


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
        # Retrieve number of questions wanted
        questions_wanted = 5
        self.to_quiz(questions_wanted)

    def to_quiz(self, num_question):
        """
        Invokes Quiz GUI and takes across number of questions to be done
        """
        Quiz(num_question)
        # Hide root window (ie: hide questions choice window).
        root.withdraw()


class Quiz:
    """
    Interface for answering the Connection Quiz
    """

    def __init__(self, how_many):
        self.qns_passed = IntVar()

        # Lists for stats component
        # 1 = pass
        # 0 = fail

        # Highest Result Test Data...
        # self.all_result_list = [1,1,1,1,1]
        # self.highest_result_list = [1,1,1,1,1]
        # self.qns_passed.set(5)

        # # Lowest Result Test Data...
        # self.all_result_list = [0,0,0,0,0]
        # self.highest_result_list = [1,1,1,1,1]
        # self.qns_passed.set(0)

        # # Random Result Test Data...
        self.all_result_list = ["1","1","0","1","1"]
        self.highest_result_list = ["1","1","1","1","1"]
        self.qns_passed.set(4)

        self.quiz_box = Toplevel()

        self.quiz_frame = Frame(self.quiz_box, bg="#C09CD2")
        self.quiz_frame.grid(padx=10, pady=10)

        self.quiz_heading_label = Label(self.quiz_frame, text=f"Connection Quiz",
                                        font=("Arial", 16, "bold"), bg="#C09CD2",
                                        padx=5, pady=5)
        self.quiz_heading_label.grid(row=0)

        self.to_stats_button = Button(self.quiz_frame, font=("Arial", 14, "bold"),
                                      text="Stats", width=15, fg="#000000",
                                      bg="#B1DDF0", padx=10, pady=10, command=self.to_stats)
        self.to_stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everything we need to display the quiz / questions statistics
        """

        # IMPORTANT: retrieve # of questions
        # pass / fail as a number (rather than the 'self' container)
        qns_passed = self.qns_passed.get()
        stats_bundle = [qns_passed, self.all_result_list,
                        self.highest_result_list]

        Stats(self, stats_bundle)


class Stats:
    """
    Displays stats for Connection Quiz
    """

    def __init__(self, partner, all_stats_info):

        # Extract information from master list...
        qns_passed = all_stats_info[0]
        user_result = all_stats_info[1]
        high_results = all_stats_info[2]

        # sort user results to find high score...
        # user_result.sort()

        self.stats_box = Toplevel()

        # disable stats button
        partner.to_stats_button.config(state=DISABLED)

        # If users press cross at top, closes stats and
        # 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW',
                                partial(self.close_stats, partner))
        self.stats_frame = Frame(self.stats_box, width=350, bg="#B1DDF0")
        self.stats_frame.grid()

        # Math to populate Stats dialogue...
        questions_done = len(user_result)

        success_rate = qns_passed / questions_done * 100

        # Strings for Stats labels...
        success_string = f"Success Rate: {qns_passed} / {questions_done} "
        accuracy_string = f"Accuracy: {success_rate:.0f}%"


        # custom comment text and formatting
        if qns_passed == questions_done:
            comment_string = "Excellent!! You got the highest result possible!"
            comment_colour = "#71EB5F"

        elif qns_passed == 0:
            comment_string = {"Oops - You've lost every round! "
                              "You might want to look at the hints!"}
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
            [comment_string, comment_font, bg, "W"]
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






