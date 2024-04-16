# TODO 1. Error Handling in File Reading
# Implement error handling when opening and reading the file to prevent the program from crashing if the file does not exist or is empty.
#
# TODO 2. Optimization in random_choice_words Function
# The random_choice_words function currently uses a potentially inefficient method to choose random words due to the repeated popping of elements from the list. This can be optimized to be more efficient and safer, particularly regarding handling edge cases.
#
# TODO 3. Enhancement of GUI Appearance
# Enhance the GUI appearance and usability by adjusting the layout, possibly using a grid system instead of pack for better control, adding margins, and improving widget alignments.
#
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
    with open('source.txt', 'r') as file:
        file_contents = file.read()

    return file_contents.split(" ")


def random_choice_words(list_of_words):
    list_to_return = []
    for _ in range(NUMBER_WORDS_CONTEST):
        random_index = random.randint(0, len(list_of_words))
        list_to_return.append(list_of_words.pop(random_index))

    return list_to_return


class SpeedTest:
    def __init__(self, contest_words):
        self.contest_words_list = contest_words
        self.words_count = len(contest_words)
        self.chars_count = len("".join(contest_words))

        self.test_timer = None
        self.window = Tk()

        self.window.geometry("300x150")
        self.window.resizable(False, False)
        self.window.title("Type Speed Test v.0.9")

        # label
        self.welcome_label = Label(self.window, text="Welcome.")
        self.welcome_label.pack(fill='x', expand=True)

        # text area
        self.text_area = Text(self.window, height=5, width=52)
        self.text_area.insert(1.0, " ".join(self.contest_words_list))
        self.text_area.pack(fill='x', expand=True)

        # entry to type
        self.user_entry = Entry(self.window, state='disabled')
        self.user_entry.pack(fill='x', expand=True)
        self.user_entry.focus()

        # start button
        self.my_button = Button(text="Start test", command=self.start_timer)
        self.my_button.pack()

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
                self.text_area.insert(1.0, f"Your time is {total:.1f} sec."
                                           f" {(self.words_count / total * 60):.1f} words/min,"
                                           f" {(self.chars_count / total * 60):.1f} chars/min,")

    def start_timer(self):
        if self.test_timer is None:
            self.test_timer = time.time()
            self.window.bind('<KeyPress>', self.check_word)
            self.user_entry.config(state='normal')
            self.my_button.config(state='disabled')
            self.welcome_label.config(text='Start typing')

    def stop_timer(self):
        end_time = time.time()
        return end_time - self.test_timer


def main():
    words_list_from_file = load_text_to_test()
    contest_words_list = random_choice_words(words_list_from_file)

    st = SpeedTest(contest_words_list)


if __name__ == '__main__':
    main()