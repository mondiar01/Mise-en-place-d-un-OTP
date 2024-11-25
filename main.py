# main.py
import tkinter as tk
from src.gui.auth_gui import AuthGUI

def main():
    root = tk.Tk()
    app = AuthGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()