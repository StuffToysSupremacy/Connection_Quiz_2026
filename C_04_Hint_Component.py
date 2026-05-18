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
        self.quiz_box = Toplevel()

        self.quiz_frame = Frame(self.quiz_box, bg="#C09CD2")
        self.quiz_frame.grid(padx=10, pady=10)

        self.quiz_heading_label = Label(self.quiz_frame, text=f"Question 0 of {how_many}",
                                        font=("Arial", 16, "bold"), bg="#C09CD2",
                                        padx=5, pady=5)
        self.quiz_heading_label.grid(row=0)

        self.to_hints_button = Button(self.quiz_frame, font=("Arial", 14, "bold"),
                                      text="Hints", width=15, fg="#000000",
                                      bg="#FAD7AC", padx=10, pady=10, command=self.to_hints)
        self.to_hints_button.grid(row=1)

    def to_hints(self):
        """
        Displays hints for playing game
        :return:
        """
        DisplayHints(self)


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
                      "the answer is that they are one word\n\n"
                      "The answer can either be before the given word\n"
                      "or after the given word. \n\n"
                      "____(given word)  or  (given word)____ \n\n"
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


if __name__ == "__main__":
    root = Tk()
    root.title("Connection Quiz")
    StartQuiz()
    root.mainloop()






