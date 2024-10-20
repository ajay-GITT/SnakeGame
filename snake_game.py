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
        x = random.randint(0, (width / size)-1) * size
        y = random.randint(0, (height / size) - 1) * size
        self.coords = [x, y]
        canvas.create_oval(x, y, x + size, y + size, fill=food_colour, tag="food")
def next_turn(snake, food):
    x, y = snake.coords[0]
    if direc == "up":
        y -= size
    elif direc == "down":
        y += size
    elif direc == "left":
        x -= size
    elif direc == "right":
        x += size
    snake.coords.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + size, y + size, fill=snake_colour)
    snake.squares.insert(0, square)

    if x == food.coords[0] and y == food.coords[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coords[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    if collision(snake):
        game_over()
    else:
        window.after(spd, next_turn, snake, food)

def change_direc(collisiontion):
    global direc
    if collisiontion == 'left':
        if direc != 'right':
            direc = collisiontion
    elif collisiontion == 'right':
        if direc != 'left':
            direc = collisiontion
    elif collisiontion == 'up':
        if direc != 'down':
            direc = collisiontion
    elif collisiontion == 'down':
        if direc != 'up':
            direc = collisiontion
def collision(snake):

    x, y = snake.coords[0]

    if x < 0 or x >= width:
        return True
    elif y < 0 or y >= height:
        return True
    for body_part in snake.coords[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('ARIAL',70), text="GAME OVER", fill="red", tag="gameover")

window = Tk()
window.title("Snake!")
window.resizable(False, False)

score = 0
direc = 'down'

label = Label(window, text="Score:{}".format(score), font=('ARIAL', 40))
label.pack()

canvas = Canvas(window, bg=bg_colour, height=height, width=width)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direc('left'))
window.bind('<Right>', lambda event: change_direc('right'))
window.bind('<Up>', lambda event: change_direc('up'))
window.bind('<Down>', lambda event: change_direc('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()