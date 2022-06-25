from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")
timer = None
current_card = {}

# ---------------------------- Remove learnt Card ------------------------------- #


def remove_card():
    to_learn.remove(current_card)
    next_card()

# ---------------------------- Generate New Card ------------------------------- #


def next_card():
    global current_card, file_timer
    window.after_cancel(file_timer)

    words_to_learn = [entry for entry in to_learn]
    df = pandas.DataFrame(words_to_learn)
    df.to_csv("./data/words_to_learn.csv", index=False)

    current_card = random.choice(to_learn)
    canvas.itemconfig(front_card, image=card_front_image)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    file_timer = window.after(3000, flip_card)


# ---------------------------- Generate New Card ------------------------------- #

def flip_card():
    canvas.itemconfig(front_card, image=card_back_image)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")


# ---------------------------- Read Data and Place a Random card ------------------------------- #
# Read CSV Data
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")
finally:
    # Convert df into list of dictionaries
    to_learn = data.to_dict(orient="records")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

file_timer = window.after(3000, flip_card)

correct_choice_image = PhotoImage(file="./images/right.png")
wrong_choice_image = PhotoImage(file="./images/wrong.png")
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = canvas.create_image(400, 263, image=card_front_image)

title_text = canvas.create_text(400, 150, text="", font=TITLE_FONT)
word_text = canvas.create_text(400, 263, text="", font=WORD_FONT)
canvas.grid(column=0, row=0, columnspan=2)

correct_choice_button = Button(image=correct_choice_image, highlightthickness=0, command=remove_card)
correct_choice_button.grid(column=1, row=1)

wrong_choice_button = Button(image=wrong_choice_image, highlightthickness=0, command=next_card)
wrong_choice_button.grid(column=0, row=1)

next_card()

window.mainloop()
