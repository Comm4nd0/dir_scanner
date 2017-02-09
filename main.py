#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    # must be python2
    import Tkinter as tk
    import ttk

import os

class GUI(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.center(500, 600)
        self.master.configure(background='black')
        self.master.title("Directory Scanner")

        # causes the full width of the window to be used
        self.columnconfigure(2, weight=1)
        self.columnconfigure(1, weight=1)

        self.CHOP_CHARS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        self.DELIMS = (".", ",", "/", "\\", "|")
        self.OUTPUT = ""

        self.make_UI()

    def make_UI(self):
        style = ttk.Style()
        # global style changes
        style.configure(".", background='black', foreground='grey', anchor="center")
        # Button style changes
        style.map("TButton", background=[('hover', 'blue')])

        style.map("TMenubutton", background=[('hover', 'blue')])
        style.map("TEntry", foreground=[('focus', 'blue2')])
        style.map("TEntry", foreground=[('active', 'green2')])

        # Clear
        exit_button = ttk.Button(self, text="Clear", command=self.clear)
        exit_button.grid(column=0, row=0, sticky='NW')

        # EXIT
        exit_button = ttk.Button(self, text="Exit", command=self.exit)
        exit_button.grid(column=0, row=0, sticky='N')

        heading = ttk.Label(self, text="DIR SCANNER", font=("Courier", 44))
        heading.grid(column=0, row=1, rowspan=2, columnspan=2, sticky='WENS')

        intro = ttk.Label(self, font=("Courier", 16))
        intro['text']="Welcome to Directory Scanner!"
        intro.grid(column=0, row=3, rowspan=2, columnspan=2, sticky='WENS', padx=5, pady=20)

        # browse text label
        self.browse_text = ttk.Label(self, font=("Courier", 12))
        self.browse_text['text'] = "Select root folder"
        self.browse_text.grid(column=0, row=5, sticky='E', padx=5, pady=5)

        # browse button
        button = ttk.Button(self, text="Browse", command=self.browse_dir)
        button.grid(column=1, row=5, sticky='WENS', padx=5, pady=5)

        # file types text label
        file_typestxt = ttk.Label(self, font=("Courier", 12))
        file_typestxt['text'] = "Type file types e.g. txt,ini,cfg"
        file_typestxt.grid(column=0, row=6, sticky='E', padx=5, pady=5)

        # free text box
        self.file_types_entry = ttk.Entry(self)
        self.file_types_entry.grid(column=1, row=6, sticky='WENS', padx=5, pady=5)

        # chop chars label
        drop_down_text = ttk.Label(self, font=("Courier", 12))
        drop_down_text['text'] = "Chop text from front of string"
        drop_down_text.grid(column=0, row=7, sticky='E', padx=5, pady=5)

        # chop chars options
        self.chop_char = tk.StringVar(self)
        self.chop_char.set("0")
        option = ttk.OptionMenu(self, self.chop_char, "Make selection", *self.CHOP_CHARS)
        option.grid(column=1, row=7, sticky='WENS', padx=5, pady=5)

        # line number text label
        line_numbertxt = ttk.Label(self, font=("Courier", 12))
        line_numbertxt['text'] = "Type line number to extract"
        line_numbertxt.grid(column=0, row=8, sticky='E', padx=5, pady=5)

        # line number text box
        self.line_number_entry = ttk.Entry(self)
        self.line_number_entry.grid(column=1, row=8, sticky='WENS', padx=5, pady=5)

        # delimter label
        drop_down_delim = ttk.Label(self, font=("Courier", 12))
        drop_down_delim['text'] = "Select a delimiter"
        drop_down_delim.grid(column=0, row=9, sticky='E', padx=5, pady=5)

        # delimter options
        self.delim_char = tk.StringVar(self)
        self.delim_char.set("0")
        option = ttk.OptionMenu(self, self.delim_char, "Make selection", *self.DELIMS)
        option.grid(column=1, row=9, sticky='WENS', padx=5, pady=5)

        # button
        button = ttk.Button(self, text="GO!", command=self.traverse_dirs)
        button.grid(column=1, row=10, sticky='WENS', padx=5, pady=5)

        # output text
        self.output = ttk.Label(self, font=("Courier", 12))
        self.output['text'] = " "
        self.output.grid(column=0, row=11, rowspan=2, columnspan=2, sticky='WENS', padx=5, pady=20)

    def center(self, width, height):
        """center the window on the screen"""
        # get screen width and height
        ws = self.master.winfo_screenwidth()  # width of the screen
        hs = self.master.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.master.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def clear(self):
        print("This needs doing...")

    def exit(self):
        quit()

    def browse_dir(self):
        from tkinter import filedialog
        self.rootdir = filedialog.askdirectory()
        self.browse_text['text'] = self.rootdir

    def set_filetypes(self):
        self.file_types = self.file_types_entry.get()
        self.file_types = self.file_types.split(",")
        print(self.file_types)

    def update_otput(self):
        self.output['text'] = self.OUTPUT

    def create_file(self, subdirs, completeline):
        # if statement to ensure you're not searching the root dir
        if subdirs != self.rootdir:
            # split the subdirs string at the /
            folder = subdirs.split("/")
            # get the last item in the array
            folder = folder[len(folder) - 1]
            # piece together the full path
            full_path = self.rootdir + "/" + folder + "/" + folder + ".txt"
            # open the txt file or create it, if it doesn't exist
            f = open(full_path, "w+")
            # write the long string to the file
            f.write(completeline)
            # close the file
            f.close()

    def traverse_dirs(self):
        self.set_filetypes()
        line_number = self.line_number_entry.get()
        chop_count = self.chop_char.get()
        delimeter = self.delim_char.get()

        # a for loop for iterate through the directories starting from your current thread working directory
        for subdirs, dirs, files in os.walk(self.rootdir):
            # create an empty string to add top line of files to
            completeline = ""
            # for loop to iterate through files saved in the files list that is created in the first for loop
            for file in files:
                file_split = file.split(".")
                ftype = file_split[len(file_split)-1]
                # if statement to make sure you only read .ini files
                if ftype in self.file_types:
                    # builds the variable for specifying the file to open
                    file_name = subdirs + "/" + file
                    # open the file
                    with open(file_name) as f:
                        # read and split the lines into an array
                        data = f.read().splitlines()
                        print(line_number)
                        print(chop_count)
                        try:
                            # get the first item in the array(the first line from the file) and chop it from its 10th character to the end
                            line = data[int(line_number)][int(chop_count):]
                            # append the amended line to a variable
                            completeline += line
                            # append a comma
                            completeline += delimeter
                        except IndexError:
                            print("Line number not valid for this file")

                    self.OUTPUT += completeline

            self.create_file(subdirs, completeline)


if __name__ == '__main__':
    root = tk.Tk()
    window = GUI(root)
    window.pack(fill=tk.X, expand=True, anchor=tk.N)
root.mainloop()
