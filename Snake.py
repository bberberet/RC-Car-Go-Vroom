#!/usr/bin/env python
# coding: utf-8

# In[29]:


import tkinter as tk
import random

# === Game Constants ===
CELL_SIZE = 20                 # Size of each square cell in pixels
GRID_WIDTH = 40                # Number of cells horizontally
GRID_HEIGHT = 40               # Number of cells vertically
BORDER_OFFSET = 4 * 4 // CELL_SIZE  # Accounts for 4 border layers of 4px each

# Direction mapping
DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

# === Game State Variables ===
snake = [(20, 20)]            # Player snake starting position
direction = "Right"           # Initial direction
snake_rects = []              # Graphics for each snake segment

reset_btn = None              # Reference to reset button
food_pos = None               # Coordinates of the current food
food_symbol = None           # The symbol string shown as food
food_item = None             # Canvas object for the food
score = 0                    # Player score
top_score = 0                # Highest score this session
score_text = None
top_score_text = None

symbols = ["π", "Σ", "√", "∫", "θ", "Δ", "∞", "ℏ", "∇"]  # Fun food symbols

# Enemy snake setup
enemy_snake = [(5, 5), (5, 6)]
enemy_rects = []

# === Main Game Launcher ===
def launch_window():
    global canvas, snake_rects, direction, window, reset_btn
    global food_item, score_text, top_score_text, enemy_rects

    # Create window and canvas
    window = tk.Tk()
    window.title("Snake Game")
    window.resizable(False, False)

    width = CELL_SIZE * GRID_WIDTH
    height = CELL_SIZE * GRID_HEIGHT
    canvas = tk.Canvas(window, width=width, height=height, bg="black")
    canvas.pack()

    # Initial draw
    draw_border()
    draw_snake()
    draw_enemy_snake()
    spawn_food()
    draw_scores()

    # === Main Snake Movement Logic ===
    def move_snake():
        global snake, snake_rects, direction, reset_btn
        global food_pos, food_item, score, score_text, top_score, top_score_text
        global enemy_snake, enemy_rects

        dx, dy = DIRECTIONS[direction]
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        # Game over checks
        if (
            new_head[0] < BORDER_OFFSET or new_head[0] >= GRID_WIDTH - BORDER_OFFSET or
            new_head[1] < BORDER_OFFSET or new_head[1] >= GRID_HEIGHT - BORDER_OFFSET or
            new_head in snake or
            new_head in enemy_snake
        ):
            canvas.create_text(
                CELL_SIZE * GRID_WIDTH // 2,
                CELL_SIZE * GRID_HEIGHT // 2 - 20,
                text="GAME OVER",
                font=("Courier", 32, "bold"),
                fill="red"
            )

            # Update top score
            if score > top_score:
                top_score = score
                canvas.itemconfig(top_score_text, text=f"Top Score: {top_score}")

            # Show reset button
            reset_btn = tk.Button(
                window, text="Reset Game",
                font=("Courier", 14),
                bg="black", fg="lime",
                command=reset_game
            )
            reset_btn.place(
                x=CELL_SIZE * GRID_WIDTH // 2 - 60,
                y=CELL_SIZE * GRID_HEIGHT // 2 + 10
            )
            return

        # Check food collision
        if new_head == food_pos:
            snake = [new_head] + snake
            canvas.delete(food_item)
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
            spawn_food()
            rect = canvas.create_rectangle(0, 0, 0, 0, fill="lime", outline="")
            snake_rects.insert(0, rect)
        else:
            snake = [new_head] + snake[:-1]

        # Update graphics for player snake
        for i, (x, y) in enumerate(snake):
            canvas.coords(snake_rects[i],
                          x * CELL_SIZE, y * CELL_SIZE,
                          (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE)

        # Move enemy
        move_enemy()

        # Speed scales with snake length
        speed = max(50, 150 - (len(snake) - 1) * 5)
        window.after(speed, move_snake)

    # === Player Input ===
    def change_direction(event):
        global direction
        if event.keysym in DIRECTIONS:
            opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if direction != opposite[event.keysym]:
                direction = event.keysym

    # === Game Reset ===
    def reset_game():
        global snake, snake_rects, direction, reset_btn
        global food_item, food_pos, score, score_text
        global enemy_snake, enemy_rects

        if reset_btn:
            reset_btn.destroy()
            reset_btn = None

        canvas.delete("all")
        snake.clear()
        snake.append((20, 20))
        direction = "Right"
        snake_rects.clear()
        food_pos = None
        score = 0
        enemy_snake = [(5, 5), (5, 6)]
        enemy_rects.clear()

        draw_border()
        draw_snake()
        draw_enemy_snake()
        spawn_food()
        draw_scores()
        move_snake()

    # Bind arrow keys
    window.bind("<KeyPress>", change_direction)
    move_snake()
    window.mainloop()

# === Enemy Snake Logic ===
def move_enemy():
    global enemy_snake, enemy_rects, food_pos, food_item

    head = enemy_snake[0]
    player_head = snake[0]

    # Choose the closer target
    target = food_pos if manhattan(head, food_pos) <= manhattan(head, player_head) else player_head

    # Valid directions
    options = [(head[0] + dx, head[1] + dy) for dx, dy in DIRECTIONS.values()]
    valid = [
        pos for pos in options
        if BORDER_OFFSET <= pos[0] < GRID_WIDTH - BORDER_OFFSET and
           BORDER_OFFSET <= pos[1] < GRID_HEIGHT - BORDER_OFFSET and
           pos not in enemy_snake and
           pos not in snake
    ]

    if not valid:
        return

    # 25% chance to act randomly
    RANDOMNESS_PROBABILITY = 0.25
    if random.random() < RANDOMNESS_PROBABILITY:
        new_head = random.choice(valid)
    else:
        valid.sort(key=lambda pos: manhattan(pos, target))
        new_head = valid[0]

    # Food collision
    if new_head == food_pos:
        canvas.delete(food_item)
        spawn_food()
        enemy_snake.insert(0, new_head)
        rect = canvas.create_rectangle(0, 0, 0, 0, fill="red", outline="")
        enemy_rects.insert(0, rect)
    else:
        enemy_snake = [new_head] + enemy_snake[:-1]

    # Update enemy graphics
    for i, (x, y) in enumerate(enemy_snake):
        canvas.coords(enemy_rects[i],
                      x * CELL_SIZE, y * CELL_SIZE,
                      (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE)

# === Helper: Manhattan Distance ===
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# === Draw Functions ===
def draw_border():
    border_colors = ["purple", "yellow", "green", "red"]
    border_spacing = 4
    for i, color in enumerate(border_colors):
        offset = i * border_spacing
        canvas.create_rectangle(
            offset, offset,
            CELL_SIZE * GRID_WIDTH - offset,
            CELL_SIZE * GRID_HEIGHT - offset,
            outline=color,
            width=2
        )

def draw_snake():
    for x, y in snake:
        rect = canvas.create_rectangle(
            x * CELL_SIZE, y * CELL_SIZE,
            (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
            fill="lime", outline=""
        )
        snake_rects.append(rect)

def draw_enemy_snake():
    for x, y in enemy_snake:
        rect = canvas.create_rectangle(
            x * CELL_SIZE, y * CELL_SIZE,
            (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE,
            fill="red", outline=""
        )
        enemy_rects.append(rect)

def spawn_food():
    global food_pos, food_symbol, food_item

    min_pos = BORDER_OFFSET + 1
    max_pos = GRID_WIDTH - BORDER_OFFSET - 2

    while True:
        pos = (random.randint(min_pos, max_pos), random.randint(min_pos, max_pos))
        if pos not in snake and pos not in enemy_snake:
            break

    food_pos = pos
    food_symbol = random.choice(symbols)
    x, y = pos
    food_item = canvas.create_text(
        x * CELL_SIZE + CELL_SIZE // 2,
        y * CELL_SIZE + CELL_SIZE // 2,
        text=food_symbol,
        font=("Courier", 20, "bold"),
        fill="white"
    )

def draw_scores():
    global score_text, top_score_text
    top_score_text = canvas.create_text(
        10, 10,
        anchor="nw",
        text=f"Top Score: {top_score}",
        font=("Courier", 12, "bold"),
        fill="yellow"
    )
    score_text = canvas.create_text(
        10, 30,
        anchor="nw",
        text=f"Score: {score}",
        font=("Courier", 14, "bold"),
        fill="white"
    )

# === Start the Game ===
launch_window()


# In[ ]:





# In[ ]:




