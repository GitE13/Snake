import multiprocessing
import random
import keyboard
import tkinter as tk
import random
import keyboard  # pip install keyboard

def spam_tkinter(i):
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    width = root.winfo_screenwidth()+10
    height = root.winfo_screenheight()+10

    canvas = tk.Canvas(root, width=width, height=height, highlightthickness=0)
    canvas.pack()

    def draw():
        if keyboard.is_pressed('q'):
            root.destroy()
            return

        canvas.delete("all")

        for _ in range(random.randint(1, 10)):
            r = random.randint(50, 250)
            x = random.randint(0, width)
            y = random.randint(0, height)

            color = "#%02x%02x%02x" % (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )

            canvas.create_oval(
                x - r, y - r,
                x + r, y + r,
                fill=color,
                outline=""
            )

        delay = int(random.uniform(10, 100))  # milliseconds
        if random.randint(0,4) > 3:
            root.destroy()
            return
        root.after(delay, draw)

    draw()
    root.mainloop()

if __name__ == '__main__':
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(spam_tkinter, range(3000))