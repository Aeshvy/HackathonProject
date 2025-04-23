import tkinter as tk

def build_main_menu(app):
    app.clear_window()

    title = """
888                                                           
888                                                           
888                                                           
88888b.  8888b. 88888b.  .d88b. 88888b.d88b.  8888b. 88888b.  
888 "88b    "88b888 "88bd88P"88b888 "888 "88b    "88b888 "88b 
888  888.d888888888  888888  888888  888  888.d888888888  888 
888  888888  888888  888Y88b 888888  888  888888  888888  888 
888  888"Y888888888  888 "Y88888888  888  888"Y888888888  888 
                             888                              
                        Y8b d88P                              
                         "Y88P"                               
"""

    tk.Label(app.root, text=title, font=("Courier", 10), justify="left").pack(pady=10)

    tk.Button(app.root, text="Start Game", command=app.start_game, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(app.root, text="Rules", command=app.show_rules, font=("Helvetica", 14)).pack(pady=10)
    tk.Button(app.root, text="Exit", command=app.root.quit, font=("Helvetica", 14)).pack(pady=10)