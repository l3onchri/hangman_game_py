import tkinter as tk
from tkinter import messagebox
import random

def random_line(file_path):
    with open(file_path, "r", encoding="utf-8") as afile:
        line = next(afile)
        for num, aline in enumerate(afile, 2):
            if random.randrange(num):
                continue
            line = aline
    return line.strip()

def hidden_word(word):
    h_word = ""
    for i in word:
        if i == word[0] or (i == word[len(word) - 1]):
            h_word += i
        else:
            h_word += "-"
    return h_word

def check_letter(word, c_letter):
    return c_letter in word

def sub_letter(word, h_word, c):
    if c == word:
        return word
    new_word = ""
    for i in range(len(word)):
        if c == word[i]:
            new_word += c
        else:
            new_word += h_word[i]
    return new_word

# --- GUI CLASS ---
class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.word = random_line("words.txt").lower()
        self.hidden = hidden_word(self.word)
        self.lives = 10
        self.guessed_letters = set()

        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.word_label = tk.Label(root, text=f"Word: {self.hidden}", font=("Courier", 18))
        self.word_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.entry = tk.Entry(root, width=5, font=("Courier", 18))
        self.entry.grid(row=2, column=0, pady=5)

        self.submit_btn = tk.Button(root, text="Submit", command=self.submit_letter)
        self.submit_btn.grid(row=2, column=1)

        self.lives_label = tk.Label(root, text="❤" * self.lives, font=("Courier", 16), fg="red")
        self.lives_label.grid(row=2, column=2)

        self.draw_hangman()

    def submit_letter(self):
        letter = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if not letter or len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return

        if letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)

        if check_letter(self.word, letter):
            self.hidden = sub_letter(self.word, self.hidden, letter)
            self.word_label.config(text=f"Word: {self.hidden}")
        else:
            self.lives -= 1
            self.lives_label.config(text="❤" * self.lives)
            self.draw_hangman()

        if self.hidden == self.word:
            messagebox.showinfo("Victory!", "You guessed the word! ⸜(˃ᵕ˂)⸝")
            self.root.destroy()
        elif self.lives == 0:
            self.word_label.config(text=f"The word was: {self.word}")
            messagebox.showerror("Game Over", "You lost! (•᷄_•᷅)")
            self.root.destroy()

    def draw_hangman(self):
        self.canvas.delete("all")
        # base
        self.canvas.create_line(50, 280, 250, 280)
        self.canvas.create_line(100, 280, 100, 50)
        self.canvas.create_line(100, 50, 180, 50)
        self.canvas.create_line(180, 50, 180, 80)

        # Draw based on lives left
        parts = 10 - self.lives
        if parts >= 1:  # head
            self.canvas.create_oval(160, 80, 200, 120)
        if parts >= 2:  # body
            self.canvas.create_line(180, 120, 180, 180)
        if parts >= 3:  # left arm
            self.canvas.create_line(180, 130, 150, 160)
        if parts >= 4:  # right arm
            self.canvas.create_line(180, 130, 210, 160)
        if parts >= 5:  # left leg
            self.canvas.create_line(180, 180, 150, 230)
        if parts >= 6:  # right leg
            self.canvas.create_line(180, 180, 210, 230)
        if parts >= 7:  # left eye
            self.canvas.create_line(170, 90, 175, 95)
            self.canvas.create_line(175, 90, 170, 95)
        if parts >= 8:  # right eye
            self.canvas.create_line(185, 90, 190, 95)
            self.canvas.create_line(190, 90, 185, 95)
        if parts >= 9:  # mouth
            self.canvas.create_line(170, 110, 190, 110)
        if parts >= 10:  # X over head (death)
            self.canvas.create_line(160, 80, 200, 120)
            self.canvas.create_line(160, 120, 200, 80)

# --- START GAME ---
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGUI(root)
    root.mainloop()
