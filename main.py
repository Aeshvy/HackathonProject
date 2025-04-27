import tkinter as tk
from app import HangmanApp


if __name__ == '__main__':
    root = tk.Tk()
    app = HangmanApp(root)
    root.mainloop()