from tkinter import *

class StartQuiz():
    """
    Initial Game inter-face (asks users how many questions they would like to do)
    """

    def __init__(self):
        """
        Gets number of question/s from user
        """
        background = "#ffe6cc"
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

        self.num_question_entry = Entry(self.entry_area_frame, font=("Arial",20, "bold"),
                                      width=12)
        self.num_question_entry.grid(row=0, column=0, padx=10, pady=10)

        # Create start button...
        self.start_button = Button(self.entry_area_frame, font=("Arial", 16, "bold"),
                                  fg="#FFFFFF", bg="#5555D4", text="Start", width=11,
                                  command=self.check_questions)

        self.start_button.grid(row=0, column=1)

    def check_questions(self):
        """F
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
                # temporary success message, replace with call to StartQuiz class
                self.choose_label.config(text=f"You have chosen to do {questions_wanted} question(s)")
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


if __name__ == "__main__":
    root = Tk()
    root.title("Connection Quiz")
    StartQuiz()
    root.mainloop()
