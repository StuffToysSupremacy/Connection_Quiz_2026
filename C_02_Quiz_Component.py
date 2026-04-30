from logging import root
from tkinter import *

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
            
            quiz_labels_ref.append(item)

        # Retrieve Labels so they can be configured later
        self.heading_label = quiz_labels_ref[0]
        self.given_word_label = quiz_labels_ref[1]
        self.results_label = quiz_labels_ref[3]

        # set up word buttons...
        self.word_frame = Frame(self.quiz_frame, bg="#C09CD4")
        self.word_frame.grid(row=4)

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.word_button = Button(self.word_frame, font=("Arial", 12),
                                        text="Word ", width=15)
            self.word_button.grid(row=item // 2,
                                    column=item % 2,
                                    padx=5, pady=5)

        # Frame to hold hints and stats buttons
        self.hints_stats_frame = Frame(self.quiz_frame, bg="#C09CD2")
        self.hints_stats_frame.grid(row=7)

        # List for buttons ( frame | text | bg | command | width | row | column )
        control_button_list = [
            [self.quiz_frame, "Next Question", "#FAF4AB", "", 21, 5, None],
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

        
        
        
        
        
        
        