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
        self.qns_passed = StringVar()

        # Lists for stats component
        # 1 = pass
        # 0 = fail

        # Highest Result Test Data...
        self.all_result_list = [1,1,1,1,1]
        self.highest_result_list = [1,1,1,1,1]
        self.qns_passed.set(5)

        # # Lowest Result Test Data...
        # self.all_result_list = [0,0,0,0,0]
        # self.highest_result_list = ["pass","pass","pass","pass","pass"]
        # self.qns_passed.set(0)

        # # Random Result Test Data...
        # self.all_result_list = ["pass","fail","pass","fail","pass"]
        # self.highest_result_list = ["pass","pass","pass","pass","pass"]
        # self.qns_passed.set(3)

        self.quiz_box = Toplevel()

        self.quiz_frame = Frame(self.quiz_box, bg="#C09CD2")
        self.quiz_frame.grid(padx=10, pady=10)

        self.quiz_heading_label = Label(self.quiz_frame, text=f"Connection Quiz",
                                        font=("Arial", 16, "bold"), bg="#C09CD2",
                                        padx=5, pady=5)
        self.quiz_heading_label.grid(row=0)

        self.to_stats_button = Button(self.quiz_frame, font=("Arial", 14, "bold"),
                                      text="Stats", width=15, fg="#000000",
                                      bg="#B1DDF0", padx=10, pady=10, command=self.to_stats())
        self.to_stats_button.grid(row=1)

    def to_stats(self):
        """
        Retrieves everything we need to display the quiz / questions statistics
        """

        # IMPORTANT: retrieve # of questions
        # w



if __name__ == "__main__":
    root = Tk()
    root.title("Connection Quiz")
    StartQuiz()
    root.mainloop()






