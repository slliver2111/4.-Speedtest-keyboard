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


# TODO Show in the end words and char per minute

class SpeedTest:
    def __init__(self, contest_words):
        self.contest_words_list = contest_words
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
                self.text_area.insert(1.0, f"End of test. Your time is {total:.2f} sec.")

    def start_timer(self):
        if self.test_timer is None:
            self.test_timer = time.time()
            self.window.bind('<KeyPress>', self.check_word)
            self.user_entry.config(state='normal')
            self.welcome_label.config(text='Start typing!')

    def stop_timer(self):
        end_time = time.time()
        return end_time - self.test_timer


def main():
    words_list_from_file = load_text_to_test()
    contest_words_list = random_choice_words(words_list_from_file)

    st = SpeedTest(contest_words_list)


if __name__ == '__main__':
    main()
