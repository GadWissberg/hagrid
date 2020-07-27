import tkinter as tk


def main():
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Project by: Roni, Gad, Elad and Bar")

    pack_tkinter_buttons(root)
    root.mainloop()


def pack_tkinter_buttons(root):
    button_1 = tk.Button(root, text='First Button', width=40, command=counter_label)
    button = tk.Button(root, text='Close', width=40, command=root.destroy)
    button_1.pack()
    button.pack()


def counter_label():
    print("test")


if __name__ == "__main__":
    main()
