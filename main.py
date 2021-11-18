from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pandas.read_csv("./data/to_learn_german_words.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/german_words.csv")

to_learn = data.to_dict(orient="records")

word = None


# ___________________________Functions__________________________________________________________


def next_card():
    global word, flip_timer
    window.after_cancel(flip_timer)
    word = random.choice(to_learn)
    german_word = word['German']
    canvas.itemconfig(front_image, image=card_front_img)
    canvas.itemconfig(language_text, text="German", fill="black")
    canvas.itemconfig(word_text, text=german_word, fill="black")
    flip_timer = window.after(3000, flip)


def flip():
    english_word = word['English']
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=english_word, fill="white")
    canvas.itemconfig(front_image, image=card_back_img)


def right():
    to_learn.pop(to_learn.index(word))
    try:
        next_card()
    except IndexError or ValueError:
        canvas.itemconfig(language_text, text="Congrats")
        canvas.itemconfig(word_text, text="You know all words")
    finally:
        new_data = pandas.DataFrame(to_learn)
        new_data.to_csv("./data/to_learn_words.csv")

# ___________________________UI__________________________________________________________

window = Tk()
window.title("Flash cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip)

# CANVAS

canvas = Canvas(height=526, width=800)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
front_image = canvas.create_image(400, 263, image=card_front_img)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3, rowspan=3)
language_text = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

# BUTTONS
cross_image=PhotoImage(file="./images/wrong.png")
button_yes = Button(image=cross_image, command=next_card)
button_yes.grid(row=3, column=0)

tick_image=PhotoImage(file="./images/right.png")
button_no = Button(image=tick_image, command=right)
button_no.grid(row=3, column=2)

next_card()

window.mainloop()


