from tkinter import *
from tkinter import messagebox
from textfile import *
import random

# GLOBAL VARIABLES
BG_COLOR = '#ECF8F9'
BUTTON_COLOR = '#068DA9'
TITLE_COLOR = '#B70404'
TIMER_COLOR = '#E55807'
font_title = ('times', 16, 'bold')
font_body = ('times', 13, 'normal')
font_type = ('times', 11, 'normal')

TIME = 60
words_per_row = 15


# --------------- CLASS INHERITING FROM TK WITH ALL FUNCTIONS NEEDED ---------------
class TypingTest(Tk):
    def __init__(self):
        super().__init__()
        self.title("Typing speed test")
        self.config(padx=50, pady=15, bg=BG_COLOR)

        self.label1 = Label(self)
        self.text_label = Label(self)
        self.typing = Text(self)
        self.high_score_label = Label(self)
        self.results = Button(self, text='See results', width=20, command=self.show_results, bg=BUTTON_COLOR, font=font_title)

        self.model_text = None
        self.formatted_text = None
        try:
            with open('high_score.txt') as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            with open('high_score.txt', 'w') as file:
                self.high_score = 0
                file.write(f'{self.high_score}')

        self.setup()

    def setup(self):
        """Setup all widgets and get new text.
        Separated from 'init' to optimize a second try at the test"""
        self.model_text = random.choice(texts).split()
        self.formatted_text = [" ".join(self.model_text[i - words_per_row:i]) for i in
                               range(words_per_row, len(self.model_text), words_per_row)]

        self.label1.config(text='Welcome to typing speed test!\nStart typing whenever you are ready', font=font_title,
                           fg=TITLE_COLOR, bg=BG_COLOR)
        self.label1.pack(pady=15)

        self.text_label.config(text="\n".join(self.formatted_text[:5]), font=font_body, justify='left', bg=BG_COLOR)
        self.text_label.pack(pady=15)

        self.typing.config(height=18, font=font_type, wrap=WORD, width=100, state='normal')
        self.typing.delete(1.0, END)
        self.typing.bind_all('<Key>', self.start_timer)
        self.typing.pack(pady=15)

        self.high_score_label.config(text=f'High score: {self.high_score}', fg=TITLE_COLOR, bg=BG_COLOR, font=font_title)
        self.high_score_label.pack(pady=15)

    def finish(self):
        """When time expires, disable typing and show button to see results"""
        self.typing.config(state='disabled')
        self.results.pack(pady=15)

    def show_results(self):
        """Calculate numbers of correct and wrong words, and show them in a messagebox.
        Ask user if try again or close the program"""
        words_total = {'right': 0, 'wrong': 0}
        written_text = self.typing.get("1.0", END).lower().split()
        for i in range(len(written_text)):
            written_word = written_text[i]
            correct_word = self.model_text[i].lower()
            # print(written_word, correct_word)
            if written_word == correct_word:
                words_total['right'] += 1
            else:
                words_total['wrong'] += 1
        if words_total['right'] > self.high_score:
            self.high_score = words_total['right']
            with open('high_score.txt', 'w') as f:
                f.write(f'{self.high_score}')
        if messagebox.askyesno(title="End of test",
                               message=f"Right words: {words_total['right']}.\nWrong words: {words_total['wrong']}.\n Wanna try again?"):
            self.results.pack_forget()
            self.setup()
        else:
            self.destroy()

    def start_timer(self, event):
        """When user starts typing, start the timer"""
        self.typing.unbind_all('<Key>')
        self.typing.bind('<space>', self.word_count)
        self.high_score_label.pack_forget()
        self.count_down(TIME)

    def count_down(self, n):
        """Support function for timer"""
        self.label1.config(text=n, fg=TIMER_COLOR)
        if n > 0:
            w.after(1000, self.count_down, n - 1)
        else:
            self.finish()

    def word_count(self, event):
        """ Count words typed and scroll down text if needed"""
        words_tot = len(self.typing.get("1.0", END).split())
        if words_tot >= words_per_row * 3 and words_tot % words_per_row == 0:
            curr_row = words_tot // words_per_row
            self.text_label.config(text="\n".join(self.formatted_text[curr_row - 2:curr_row + 3]))


# --------------------- EXECUTE PROGRAM DEFINED IN THE ABOVE CLASS -----------------------
w = TypingTest()
# w.geometry(WINDOW_SIZE)  # Size of the window
w.mainloop()
