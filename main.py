# TODO 4. Additional UI Features
# Add more features like a reset button to restart the test without restarting the program, and display more detailed statistics or feedback on the user's typing patterns.
#
# TODO 5. Improved End of Test Handling
# Refine the handling at the end of the test, perhaps by disabling the input field and offering options to restart or quit.
#
# TODO 6. Accurate Word Boundaries in Input Checking
# Modify the input checking logic to more accurately recognize word boundaries and to improve user experience by allowing more natural typing behavior.
#
# TODO 7. Refactoring and Code Structure
# Refactor the code to better separate the concerns (e.g., separating GUI code from logic for test timing and word checking), making it easier to manage and extend.

from tkinter import *
import time
import random

THEME_COLOR = "#375362"
NUMBER_WORDS_CONTEST = 20


def load_text_to_test():
    # Open the text file in read mode
    try:
        with open('source.txt', 'r') as file:
            file_contents = file.read()
            if file_contents:
                return file_contents.split(" ")
            else:
                print("File is empty.")
                return []
    except FileNotFoundError:
        print("Source file is not present.")
    return []


def random_choice_words(list_of_words):
    if len(list_of_words) < NUMBER_WORDS_CONTEST:
        return list_of_words
    return random.sample(list_of_words, NUMBER_WORDS_CONTEST)


class SpeedTest:
    def __init__(self, contest_words):
        self.contest_words_list = contest_words
        self.words_count = len(contest_words)
        self.chars_count = len("".join(contest_words))

        self.test_timer = None
        self.window = Tk()
        self.window.config(padx=40, pady=40, bg=THEME_COLOR)

        # self.window.geometry("600x600")
        # self.window.resizable(False, False)
        self.window.title("Type Speed Test v.0.9")

        # label
        self.welcome_label = Label(self.window, text="Welcome to type speed test.", bg=THEME_COLOR)
        self.welcome_label.grid(row=0, column=1, padx=20, pady=20)

        # text area
        self.text_area = Text(self.window, height=5, width=52, wrap=WORD)
        self.text_area.insert(1.0, " ".join(self.contest_words_list))
        self.text_area.bind("<Key>", lambda e: "break")
        self.text_area.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

        # entry to type
        self.user_entry = Entry(self.window, state='disabled')
        self.user_entry.grid(row=2, column=0, columnspan=3, padx=20, pady=20)
        self.user_entry.focus()

        # start button
        self.my_button = Button(text="Start test", command=self.start_timer, padx=20, pady=20)
        self.my_button.grid(row=3, column=1, padx=20, pady=20)

        self.window.mainloop()

    def check_word(self, e):
        # Check if are any available words
        if len(self.contest_words_list):
            # The word typed by user is the same as the first in textarea
            if self.user_entry.get() == self.contest_words_list[0] + " ":
                self.contest_words_list.pop(0)
                self.text_area.delete(1.0, END)
                self.user_entry.delete(0, END)
                if len(self.contest_words_list):
                    self.text_area.insert(1.0, " ".join(self.contest_words_list))
            elif self.user_entry.get() == self.contest_words_list[0] and len(self.contest_words_list) == 1:
                total = self.stop_timer()
                self.text_area.delete(1.0, END)
                self.user_entry.delete(0, END)
                self.welcome_label.config(text='End of test')
                self.text_area.insert(1.0, f"Your time is {total:.1f} sec.\n"
                                           f" {(self.words_count / total * 60):.1f} words/min,\n"
                                           f" {(self.chars_count / total * 60):.1f} chars/min,")

    def start_timer(self):
        if self.test_timer is None:
            self.test_timer = time.time()
            self.window.bind('<KeyPress>', self.check_word)
            self.user_entry.config(state='normal')
            self.my_button.config(state='disabled')
            self.welcome_label.config(text='Start typing')
            self.user_entry.focus()

    def stop_timer(self):
        end_time = time.time()
        return end_time - self.test_timer


def main():
    words_list_from_file = load_text_to_test()

    if len(words_list_from_file):
        contest_words_list = random_choice_words(words_list_from_file)
        SpeedTest(contest_words_list)


if __name__ == '__main__':
    main()
