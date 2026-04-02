# Imports/Libraries
import customtkinter as tk
from wordfreq import top_n_list
import random


# Main Loop Function
def main_loop():
    # Window Config
    window = tk.CTk()
    window.title("Typing Speed Test")
    window.minsize(width=700, height=500)

    # Header Label
    label = tk.CTkLabel(window, text="Typing Speed Test", font=("Arial", 24, "bold"))
    label.pack(pady=5)

    # Variables
    current_index = 0
    count = 0
    letter = 0
    time = 60
    time_seconds = 60000
    number_of_words = 5000

    # Words Setup
    words = top_n_list("en", number_of_words, wordlist="best")
    words = [w for w in words if w.isalpha()]
    random.shuffle(words)

    # Time Countdown Label
    time_label = tk.CTkLabel(window, text="Current Time: 60 seconds", font=("Arial", 13, "bold"))
    time_label.pack()

    # Previous Word Label
    prev_word_label = tk.CTkLabel(window, text="", font=("Arial", 15, "bold"), text_color="gray")
    prev_word_label.pack()

    # Current Word Label
    word_label = tk.CTkLabel(window, text=words[current_index], font=("Arial", 17, "bold"), text_color="black",
                             fg_color="#FFFF66", corner_radius=5)
    word_label.pack()

    # Show Current/Previous Word Function
    def show_word():
        if current_index != 0:
            prev_word_label.configure(text=words[current_index - 1])
        word_label.configure(text=words[current_index])

    if current_index == 0:
        show_word()

    def next_word():
        nonlocal current_index
        current_index += 1
        show_word()

    # Restart Function
    def restart():
        window.destroy()
        main_loop()

    # Main Word Entry/Input
    entry = tk.CTkEntry(window, placeholder_text="Type Word...", font=("Arial", 15, "bold"), border_color="#FFFF66",
                        text_color="#FFFF66")
    entry.focus()
    entry.pack(pady=10)

    # WPM Label
    word_count_label = tk.CTkLabel(window, text="Word Count: 0", font=("Arial", 13, "bold"))
    word_count_label.pack()
    # CPM Label
    letter_count_label = tk.CTkLabel(window, text="Character Count: 0", font=("Arial", 13, "bold"))
    letter_count_label.pack()

    # Restart Button
    button = tk.CTkButton(window, text="Restart", command=restart, font=("Arial", 15, "bold"), height=30,
                          corner_radius=12, fg_color="#3B82F6", hover_color="#2563EB", text_color="white")
    button.pack(pady=10)

    # Exit Button
    button = tk.CTkButton(window, text="Exit", command=window.destroy, font=("Arial", 15, "bold"), height=30,
                          corner_radius=12, fg_color="transparent", border_width=2, border_color="red",
                          hover_color="red", text_color="white")
    button.pack()

    # Time End Function
    def time_end():
        time_label.configure(text=f"Times Up!")

        word_count_label.configure(text=f"Words Per Minute (WPM): {count}")

        letter_count_label.configure(text=f"Characters Per Minute (CPM): {letter}")

        entry.configure(state="disabled")

    # Next Word Function (when space is pressed)
    def space_press(event):
        nonlocal count, letter
        current_word = entry.get().strip()
        if current_word == words[current_index]:
            count += 1
            letter += len(current_word)
            entry.delete(0, tk.END)
            next_word()
        word_count_label.configure(text=f"Word Count: {count}")
        letter_count_label.configure(text=f"Letter Count: {letter}")

    # First Press Function (when first pressed on the entry the timer starts)
    time_start = False

    def type_press(event):
        nonlocal time_start
        if not time_start:
            time_start = True
            window.after(time_seconds, time_end)
            update_timer()

    # Updating Timer Live Function
    def update_timer():
        nonlocal time
        time_label.configure(text=f"Current Time: {time} seconds")
        time -= 1
        if time > 0:
            window.after(1000, update_timer)

    # Event Bindings
    entry.bind("<space>", space_press)
    entry.bind("<Key>", type_press)
    window.mainloop()


# Main Loop Function Call
main_loop()
