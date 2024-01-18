import random
from tkinter import *
from tkinter import ttk
import tkinter 
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import csv
from datetime import timedelta

#how many characters it can show at once
part_size = 114
hover_turned_on = False

#utility functions
def fetch_data_from_csv(kanji_list, hint_list, file_path):
    
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            kanji_list.append(row[0])
            hint_list.append(row[1])

def find_index(lists, name):
    try:
        index = lists.index(name)
        return index
    except ValueError:
        return -1

def partition(kanji_list, part_size):
    return [kanji_list[i:i+part_size] for i in range(0, len(kanji_list), part_size)]

def calculate_parts(parted_list):
    return ['Part {}'.format(i+1) for i in range(len(parted_list))]

def on_arrow_key(event):
    if event.keysym == 'Left':
        left_arrow_clicked()
    elif event.keysym == 'Right':
        right_arrow_clicked()



#functions for creating elements
def create_character_buttons(character_list):
    global buttons_list
    char_index = 0
    for i in range(row):
        for j in range(column):
            if len(character_list) > char_index:
                temp = character_list[char_index]
            else:
                temp = " "
            buttons_list[i][j] = Button(root, text=str(temp), width=button_width, height=button_height,
                            font=("MS Gothic", button_fontsize), bg=bg_color, fg=fg_color, activebackground=ac_color, disabledforeground="#ffffff",
                            command=lambda char_index=char_index, i=i, j=j: character_button_clicked(char_index, i, j))
            buttons_list[i][j].grid(row=i, column=j)
            char_index += 1

    for i in range(column):
        root.grid_columnconfigure(i, weight=1)

    for i in range(row):
        root.grid_rowconfigure(i, weight=1)

    # Bind the on_enter function to each character button
    for i in range(row):
        for j in range(column):
            char_index = i * column + j
            buttons_list[i][j].bind("<Enter>", lambda event, char_index=char_index: on_enter(event, char_index))

def create_hint_label():
    global hint_label
    hint_label = Label(root, text="Click Any Kanji", font=("Bahnschrift", hint_label_fontsize),
                    bg=bg_color, fg=fg_color, wraplength=500)
    hint_label.grid(row=row+1, column=6, columnspan=6, pady=0)

def create_kanji_label():
    global kanji_label
    kanji_label = Label(root, text="-", font=("Bahnschrift", kanji_label_fontsize),
                   bg=bg_color, fg=fg_color)
    kanji_label.grid(row=row+1, column=13, columnspan=2, pady=10)

def create_timer_label():
    global timer_label
    timer_label = Label(root, text="15:00", font=("Arial Rounded MT Bold", timer_label_fontsize),
                   bg=bg_color, fg=fg_color)
    timer_label.grid(row=row+1, column=17, columnspan=2, pady=35)

def create_score_label():
    global score_label
    score_label = Label(root, text="--/--", font=("Bahnschrift", score_label_fontsize),
                   bg=bg_color, fg=fg_color)
    score_label.grid(row=row+1, column=15, columnspan=1, pady=35)

def create_levels_dropdown():
    global level_clicked
    global level_dropdown

    level_clicked = StringVar()
    level_dropdown = ttk.Combobox(root, textvariable=level_clicked, values=levels, style='TCombobox', font=("Helvetica", 8))
    level_dropdown.bind("<<ComboboxSelected>>", set_level)
    level_dropdown.grid(row=row+1, column=0, columnspan=2, pady=35, sticky="s")

    style = ttk.Style()
    style.theme_use('clam')  # Choose a theme (e.g., 'clam', 'alt', 'default', etc.)
    style.configure('TCombobox', background=bg_color, foreground=fg_color, fieldbackground=bg_color)

def create_parts_dropdown():
    global part_clicked
    global part_dropdown
    part_clicked = StringVar()
    part_dropdown = ttk.Combobox(root, textvariable=part_clicked, values=parts, style='TCombobox', font=("Helvetica", 8))
    part_dropdown.bind("<<ComboboxSelected>>", set_part)
    part_dropdown.grid(row=row+1, column=2, columnspan=2, pady=35, sticky="se")

def create_randomize_checkbox():
    global randomize_checkbox
    global randomize_checkbox_clicked
    randomize_checkbox_clicked = StringVar()
    randomize_checkbox =  Checkbutton(root, text="Randomize upto the selected level",
                                    variable=randomize_checkbox_clicked, command=randomize_level_clicked,
                                        font=("Helvetica", 8),
                                        background=bg_color, fg=fg_color,
                                            activeforeground=fg_color,
                                            selectcolor=bg_color,
                                            activebackground=bg_color)

    randomize_checkbox.deselect()
    randomize_checkbox.grid(row=row+1, column=0, columnspan=3, pady=25, sticky="n")

def create_shuffle_button():
    global shuffle_button
    shuffle_button = Button(root, text="Shuffle", command=shuffle_deck, font=("Helvetica", 15), bg=bg_color, fg=fg_color)
    shuffle_button.grid(row=row+1, column=3, columnspan=1, pady=20, sticky="N")

def create_interaction_buttons():
    global left_arrow_button
    global right_arrow_button
    global restart_button
    global play_button

    left_arrow_button = Button(root, image=left_arrow_image, command=left_arrow_clicked,width=arrows_image_width, height=arrows_image_height, borderwidth=0, bg=bg_color, activebackground=bg_color )
    right_arrow_button = Button(root, image=right_arrow_image, command=right_arrow_clicked,width=arrows_image_width, height=arrows_image_height, borderwidth=0, bg=bg_color, activebackground=bg_color )
    restart_button = Button(root, image=restart_image, command=restart_clicked,width=restart_image_width, height=restart_image_height, borderwidth=0, bg=bg_color, activebackground=bg_color )
    play_button = Button(root, image=play_button_image, command=play_clicked,width=restart_image_width, height=restart_image_height, borderwidth=0, bg=bg_color, activebackground=bg_color )


    left_arrow_button.grid(row=row+1, column= 5, columnspan=1, pady=35)
    right_arrow_button.grid(row=row+1, column= 12, columnspan=1, pady=35)
    restart_button.grid(row=row+1, column= 16, columnspan=1, pady=35)
    play_button.grid(row=row+1, column= 16, columnspan=1, pady=35)

    restart_button.grid_forget()


#functions for updating elements
def update_character_buttons(character_list):
    char_index = 0
    for i in range(row):
        for j in range(column):
            if len(character_list) > char_index:
                temp = character_list[char_index]
            else:
                temp = " "
            buttons_list[i][j].config(text=temp)

            char_index += 1

def update_hint_label(text):
    hint_label.config(text=text)

def update_deck(level, part):
    global current_kanji_list
    global current_hint_list

    current_kanji_list = parted_kanjis[level][part]
    current_hint_list = parted_hints[level][part]
    update_character_buttons(current_kanji_list)

def update_kanji_label(text):
    kanji_label.config(text=text)

def generate_quiz_order(max):
    global quiz_order
    quiz_order = list(range(max))
    random.shuffle(quiz_order)
    
def reset_all_character_buttons(color):
    for i in range(row):
        for j in range(column):
            buttons_list[i][j].config(bg=color)
            buttons_list[i][j].config(state=tkinter.NORMAL)

def randomize_level_clicked():
    global current_hint_list, current_kanji_list

    if randomize_checkbox_clicked.get() == "1":
        current_level = level_clicked.get()
        level = find_index(levels, current_level)

        randomized_hint_list = [hint for sublist in hint_lists[:level+1] for hint in sublist]
        randomized_kanji_list = [kanji for sublist in kanji_lists[:level+1] for kanji in sublist]

        merged_list = list(zip(randomized_kanji_list, randomized_hint_list))
        random.shuffle(merged_list)
        randomized_kanji_list, randomized_hint_list = zip(*merged_list)

        current_hint_list = list(randomized_hint_list)[:part_size]
        current_kanji_list = list(randomized_kanji_list)[:part_size]

        update_character_buttons(current_kanji_list)


#command functions
def set_level(event=None):
    global current_hint_list_position
    global randomize_checkbox
    current_level = level_clicked.get()
    level = find_index(levels, current_level)

    global parts
    parts = calculate_parts(parted_kanjis[level])
    
    part_dropdown['values'] = parts
    part_clicked.set(parts[0])

    update_deck(level, 0)
    current_hint_list_position = 0
    randomize_checkbox.deselect()

def set_part(event=None):
    global current_hint_list_position
    global randomize_checkbox

    current_level = level_clicked.get()
    current_part = part_clicked.get()


    level = find_index(levels, current_level)
    part = find_index(parts, current_part)
    
    part_clicked.set(parts[part])
    update_deck(level, part)
    current_hint_list_position = 0
    randomize_checkbox.deselect()

def shuffle_deck():
    global current_kanji_list
    global current_hint_list

    merged_list = list(zip(current_kanji_list, current_hint_list))
    random.shuffle(merged_list)

    current_kanji_list, current_hint_list = zip(*merged_list)

    update_character_buttons(current_kanji_list)

def button_click():
    return

def character_button_clicked(char_index, i, j):
    global current_hint_list_position, score

    if not is_timer_running:
        if len(current_hint_list) > char_index:
            current_hint_list_position = char_index
            update_hint_label(current_hint_list[current_hint_list_position])
            update_kanji_label(current_kanji_list[current_hint_list_position])
    else:
        if len(current_hint_list) > char_index:
            if quiz_order[current_hint_list_position] not in solved_hint_list_positions:
                solved_hint_list_positions.append(quiz_order[current_hint_list_position])

            if quiz_order[current_hint_list_position] == char_index:
                score += 1
                buttons_list[i][j].config(bg="#1d8500")
                buttons_list[i][j].config(state=tkinter.DISABLED)
                score_label.config(text=str(score) + "/" + str(len(current_hint_list)))

            right_arrow_clicked()
            if len(solved_hint_list_positions) == len(current_hint_list):
                restart_clicked()

# Add this function to update the kanji_label when a button is hovered over
def on_enter(event, char_index):
    global current_hint_list_position
    if(hover_turned_on):
        if is_timer_running:
            if quiz_order[current_hint_list_position] not in solved_hint_list_positions:
                if(char_index < len(current_hint_list)):
                    kanji_label.config(text=current_kanji_list[char_index])



def restart_clicked():
    global solved_hint_list_positions
    global current_hint_list_position

    restart_button.grid_forget()
    play_button.grid(row=row+1, column= 16, columnspan=1, pady=35)
    shuffle_button.config(state=tkinter.NORMAL)
    level_dropdown.config(state="normal")
    part_dropdown.config(state="normal")
    randomize_checkbox.config(state=tkinter.NORMAL)
    solved_hint_list_positions = []

    reset_all_character_buttons(bg_color)

    reset_timer()

def play_clicked():
    global score
    global current_hint_list_position
    play_button.grid_forget()
    restart_button.grid(row=row+1, column= 16, columnspan=1, pady=35)
    shuffle_button.config(state=tkinter.DISABLED)
    level_dropdown.config(state="disabled")
    part_dropdown.config(state="disabled")
    randomize_checkbox.config(state=tkinter.DISABLED)

    generate_quiz_order(len(current_hint_list))
    update_hint_label(current_hint_list[quiz_order[current_hint_list_position]])

    score = 0
    score_label.config(text=str(score)+"/"+str(len(current_hint_list)))
    
    update_kanji_label("-")

    start_timer()

def left_arrow_clicked():
    global current_hint_list_position
    current_hint_list_position -= 1
    current_hint_list_position %= len(current_hint_list)
    if(not is_timer_running):
        update_hint_label(current_hint_list[current_hint_list_position])
        update_kanji_label(current_kanji_list[current_hint_list_position])
    else:
        while((quiz_order[current_hint_list_position] in solved_hint_list_positions) and not(len(solved_hint_list_positions) == len(current_hint_list))):
            current_hint_list_position -= 1
        update_hint_label(current_hint_list[quiz_order[current_hint_list_position]])

def right_arrow_clicked():
    global current_hint_list_position
    current_hint_list_position += 1
    current_hint_list_position %= len(current_hint_list)
    if(not is_timer_running):
        update_hint_label(current_hint_list[current_hint_list_position])
        update_kanji_label(current_kanji_list[current_hint_list_position])
    else:
        while((quiz_order[current_hint_list_position] in solved_hint_list_positions) and not(len(solved_hint_list_positions) == len(current_hint_list))):
            current_hint_list_position += 1
        update_hint_label(current_hint_list[quiz_order[current_hint_list_position]])


#timer functions
def start_timer():
    global is_timer_running, timer_value
    if not is_timer_running:
        is_timer_running = True
        update_timer()

def reset_timer():
    global is_timer_running, timer_value
    is_timer_running = False
    # timer_value = 900  # 15 minutes in seconds
    timer_str = str(timedelta(seconds=timer_value))
    timer_label["text"] = timer_str[2:]  # Remove days from the display
    timer_value = 900

def update_timer():
    global is_timer_running, timer_value
    if is_timer_running and timer_value > 0:
        timer_value -= 1
        timer_str = str(timedelta(seconds=timer_value))
        timer_label["text"] = timer_str[2:]  # Remove days from the display
        root.after(1000, update_timer)
    elif timer_value == 0:
        timer_label["text"] = "00:00"
        is_timer_running = False
        timer_finished() 

def timer_finished():
    restart_clicked()

is_timer_running = False
timer_value = 900 


total_levels = 5
kanji_lists = [[] for _ in range(total_levels)]
hint_lists = [[] for _ in range(total_levels)]
kanji_file_paths = [[] for _ in range(total_levels)]
parted_kanjis = [[] for _ in range(total_levels)]
parted_hints = [[] for _ in range(total_levels)]


kanji_file_paths[0] = "./data/JLPT_N5.csv"
kanji_file_paths[1] = "./data/JLPT_N4.csv"
kanji_file_paths[2] = "./data/JLPT_N3.csv"
kanji_file_paths[3] = "./data/JLPT_N2.csv"
kanji_file_paths[4] = "./data/JLPT_N1.csv"

for i in range(total_levels):
    fetch_data_from_csv(kanji_lists[i], hint_lists[i], kanji_file_paths[i])


root = Tk()
root.title("Grind Kanji Grind")

root.bind('<Left>', on_arrow_key)
root.bind('<Right>', on_arrow_key)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

bg_color = "#222222"
fg_color = "#FFFFFF"
ac_color = "#333333"

root.configure(bg=bg_color)
root.wm_state('zoomed')

button_width = 10
button_height = 4

arrows_image_width = 25
arrows_image_height = 25

restart_image_width = 35
restart_image_height = 35

button_fontsize = 25
hint_label_fontsize = 20
timer_label_fontsize = 30
score_label_fontsize = 15
kanji_label_fontsize = 65


left_arrow_image = ImageTk.PhotoImage(Image.open("./assets/left_arrow.png").resize((arrows_image_width, arrows_image_height)))
right_arrow_image = ImageTk.PhotoImage(Image.open("./assets/right_arrow.png").resize((arrows_image_width, arrows_image_height)))
restart_image = ImageTk.PhotoImage(Image.open("./assets/restart.png").resize((restart_image_width, restart_image_height)))
play_button_image = ImageTk.PhotoImage(Image.open("./assets/right_arrow.png").resize((restart_image_width, restart_image_height)))


column_val = 19
row_val = 9

column = min(column_val, screen_width // 50)
row = min(row_val, screen_height // 50)

buttons_list = [[0]*column for _ in range(row)]

levels = ["JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1"]
parts = []

for i in range(total_levels):
    parted_kanjis[i] = partition(kanji_lists[i], part_size)
    parted_hints[i] = partition(hint_lists[i], part_size)

current_kanji_list = []
current_hint_list = []

current_hint_list_position = 0
solved_hint_list_positions = []

score = 0


create_character_buttons(parted_kanjis[0])
create_hint_label()
create_shuffle_button()

create_levels_dropdown()
create_parts_dropdown()
create_randomize_checkbox()

level_clicked.set(levels[0])
set_level()
part_clicked.set(parts[0])
set_part()

create_kanji_label()
create_score_label()
create_timer_label()
create_interaction_buttons()



root.mainloop()
