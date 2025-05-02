#Main function to call the ui
from gui import show_main_screen
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    root.title("Leveraging Data Analytics for Ukulele Tuesday Band")
    root.geometry("1000x600")
    show_main_screen(root)  # Pass root explicitly
    root.mainloop()
