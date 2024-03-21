import tkinter as tk
from tkinter import messagebox
import random



class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.wordlists = {
              "Animals": ["cat", "dog", "lion", "elephant", "tiger", "giraffe"],
            "Fruits": ["apple", "banana", "orange", "grape", "strawberry", "kiwi"],
            "Colors": ["red", "blue", "green", "yellow", "purple", "orange"],
            "Countries": ["usa", "canada", "japan", "australia", "germany", "brazil"],
            "Sports": ["football", "basketball", "tennis", "soccer", "volleyball", "swimming"],
            "Vegetables": ["carrot", "potato", "tomato", "cucumber", "lettuce", "broccoli"],
            "Planets": ["mercury", "venus", "mars", "jupiter", "saturn", "neptune"],
            "Languages": ["python", "java", "javascript", "c++", "ruby", "swift"],
            "Transportation": ["car", "train", "airplane", "bicycle", "boat", "helicopter"],
        }


        self.category = tk.StringVar()
        self.word_to_guess = ""
        self.guesses = []
        self.remaining_attempts = 6

        self.select_category_label = tk.Label(root, text="Select a category:")
        self.select_category_label.pack(side=tk.LEFT)

        self.category_dropdown = tk.OptionMenu(root, self.category, *self.wordlists.keys())
        self.category_dropdown.pack(side=tk.LEFT)

        self.start_game_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_game_button.pack()

        self.game_frame = tk.Frame(root)
        self.game_frame.pack()

        self.word_label = tk.Label(self.game_frame, text="", font=('Helvetica', 24))
        self.word_label.pack()

        self.hangman_canvas = tk.Canvas(self.game_frame, width=300, height=300)
        self.hangman_canvas.pack()

        self.guess_label = tk.Label(self.game_frame, text="", font=('Helvetica', 12))
        self.guess_label.pack()

        self.keyboard_frame = tk.Frame(self.game_frame)
        self.keyboard_frame.pack()

        self.buttons = {}  
    


    def start_game(self):
        self.word_to_guess = random.choice(self.wordlists[self.category.get()])
        self.guesses = []
        self.remaining_attempts = 6
        self.update_display()
        self.create_keyboard()

        
        for button in self.buttons.values():
            button.config(state=tk.NORMAL)

    def hide_word(self):
        return ' '.join([letter if letter in self.guesses else '_' for letter in self.word_to_guess])

    def make_guess(self, letter):
        if letter in self.guesses:
            return

        self.guesses.append(letter)
        if letter not in self.word_to_guess:
            self.remaining_attempts -= 1
        self.update_display()
        self.check_game_over()

        self.buttons[letter].config(state=tk.DISABLED, fg="black")

    def update_display(self):
        self.word_label.config(text=self.hide_word())
        self.guess_label.config(text=f"Remaining Attempts: {self.remaining_attempts}")
        self.draw_hangman()

    def check_game_over(self):
        if self.remaining_attempts == 0:
            messagebox.showinfo("Game Over", f"Sorry, you've run out of attempts! The word was '{self.word_to_guess}'.")
            replay = messagebox.askyesno("Replay", "Do you want to play again?")
            if replay:
                self.restart_game()
            else:
                self.root.destroy() 
        elif '_' not in self.hide_word():
            messagebox.showinfo("Congratulations", f"Congratulations, you've guessed the word '{self.word_to_guess}'!")
            replay = messagebox.askyesno("Replay", "Do you want to play again?")
            if replay:
                self.restart_game()
            else:
                self.root.destroy()  

            

    def draw_hangman(self):
        self.hangman_canvas.delete("hangman")
        
        self.hangman_canvas.create_line(50, 250, 250, 250, width=5, tags="hangman")  # Stand
        self.hangman_canvas.create_line(150, 50, 150, 250, width=5, tags="hangman")  # Rope
        self.hangman_canvas.create_line(150, 50, 210, 50, width=5, tags="hangman")  # Top bar
        if self.remaining_attempts < 7:
            parts = {
                0: self.hangman_head,
                1: self.hangman_body,
                2: self.hangman_left_arm,
                3: self.hangman_right_arm,
                4: self.hangman_left_leg,
                5: self.hangman_right_leg
            }
            for i in range(6 - self.remaining_attempts):
                parts[i]()

    def hangman_head(self):
        self.hangman_canvas.create_oval(177, 70, 237, 130, tags="hangman")

    def hangman_body(self):
        self.hangman_canvas.create_line(207, 130, 207, 220, tags="hangman")

    def hangman_left_arm(self):
        self.hangman_canvas.create_line(207, 150, 177, 180, tags="hangman")

    def hangman_right_arm(self):
        self.hangman_canvas.create_line(207, 150, 237, 180, tags="hangman")

    def hangman_left_leg(self):
        self.hangman_canvas.create_line(207, 220, 177, 250, tags="hangman")

    def hangman_right_leg(self):
        self.hangman_canvas.create_line(207, 220, 237, 250, tags="hangman")

    def create_keyboard(self):
       
        for button in self.buttons.values():
            button.destroy()
        self.buttons = {}

        qwerty_layout = [
            ' qwertyuiop ',
            ' asdfghjkl ',
            '  zxcvbnm '
        ]

        colors = ["#FF5733", "#FFBD33", "#E1FF33", "#33FF57", "#33FFBD", "#339DFF", "#5733FF", "#BD33FF", "#FF33E1", "#FF3357", "#A833FF"]

        for i, row in enumerate(qwerty_layout):
            for j, letter in enumerate(row):
                color = colors[(i*3+j) % len(colors)]
                if letter == ' ':
                    tk.Label(self.keyboard_frame, text=letter, width=2, height=2).grid(row=i, column=j, padx=2, pady=2)
                else:
                    button = tk.Button(self.keyboard_frame, text=letter, width=4, height=2, command=lambda l=letter: self.make_guess(l), bg=color)
                    button.grid(row=i, column=j, padx=2, pady=2)
                    self.buttons[letter] = button  

    def restart_game(self):
       
        self.root.destroy()

       
        root = tk.Tk()
        root.title("Hangman Game")
        hangman_game = HangmanGame(root)
        root.mainloop()





def main():
    root = tk.Tk()
    root.title("Hangman Game")
    hangman_game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

