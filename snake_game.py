from tkinter import *
import random

# Constants
width = 700
height = 700
spd = 70
size = 50
starting_amt = 3
snake_colour = "#316e9b"
food_colour = "#f4d33a"
bg_colour = "#000000"


class Snake:
    def __init__(self):
        self.bod_sz = starting_amt
        self.coords = []
        self.squares = []
        for i in range(0, starting_amt):
            self.coords.append([0, 0])
        for x, y in self.coords:
            square = canvas.create_rectangle(x, y, x + size, y + size, fill=snake_colour, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        # Integer division (//) to avoid float issues
        x = random.randint(0, (width // size) - 1) * size
        y = random.randint(0, (height // size) - 1) * size
        self.coords = [x, y]
        canvas.create_oval(x, y, x + size, y + size, fill=food_colour, tag="food")


def next_turn(snake, food):
    global direc, score  # Declare global variables
    x, y = snake.coords[0]

    # Move the snake based on the current direction
    if direc == "up":
        y -= size
    elif direc == "down":
        y += size
    elif direc == "left":
        x -= size
    elif direc == "right":
        x += size

    # Insert new head position
    snake.coords.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + size, y + size, fill=snake_colour)
    snake.squares.insert(0, square)

    # Check if snake eats food
    if x == food.coords[0] and y == food.coords[1]:
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()  # Generate new food
    else:
        # Remove the tail (if no food is eaten)
        del snake.coords[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions
    if collision(snake):
        game_over()
    else:
        window.after(spd, next_turn, snake, food)


def change_direc(direction):
    global direc
    # Prevent reversing the direction of the snake
    if direction == 'left' and direc != 'right':
        direc = direction
    elif direction == 'right' and direc != 'left':
        direc = direction
    elif direction == 'up' and direc != 'down':
        direc = direction
    elif direction == 'down' and direc != 'up':
        direc = direction


def collision(snake):
    x, y = snake.coords[0]

    # Check if snake hits the wall
    if x < 0 or x >= width or y < 0 or y >= height:
        return True

    # Check if snake collides with itself
    for body_part in snake.coords[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def game_over():
    # Clear the canvas and display "Game Over" message
    canvas.delete("all")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('ARIAL', 70), text="GAME OVER", fill="red", tag="gameover")


# Set up the main window
window = Tk()
window.title("Snake!")
window.resizable(False, False)

# Initialize the score and direction
score = 0
direc = 'down'

# Create a label to display the score
label = Label(window, text="Score: {}".format(score), font=('ARIAL', 40))
label.pack()

# Create a canvas for the game
canvas = Canvas(window, bg=bg_colour, height=height, width=width)
canvas.pack()

# Update window to get the correct dimensions
window.update()

# Center the game window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

# Set window geometry
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys to change the direction of the snake
window.bind('<Left>', lambda event: change_direc('left'))
window.bind('<Right>', lambda event: change_direc('right'))
window.bind('<Up>', lambda event: change_direc('up'))
window.bind('<Down>', lambda event: change_direc('down'))

# Initialize the snake and the food
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Run the main loop
window.mainloop()
