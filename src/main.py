from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import glob
import os
from PIL import Image, ImageOps

root = Tk()
root.title("TexPorter")
root.minsize(400,400)
root.maxsize(400,400)

def updateProgressBar(increment):
    
    try:
        maximum = float(progressbar["maximum"])
    except Exception:
        maximum = 100.0

    new_value = progressbar["value"] + increment
    
    progressbar["value"] = new_value if new_value < maximum else maximum
    root.update_idletasks()



def findDirectory(entry):
    directory = filedialog.askdirectory()
    
    entry.delete(0, END)
    entry.insert(0,directory)

def convertAlpha(original):
    r,g,b,a = original.split()
    ra = ImageOps.invert(a)
    newimg = Image.merge("RGBA", (r,g,b,ra))
    return newimg

def convertNormal(original):
    r,g,b,a = original.split()
    fullwhite = Image.new(mode ="L", size= (original.width, original.height), color='white')
    newimg = Image.merge("RGB", (a,g,fullwhite))
    return newimg

    

def convert(input_path, output_path):

    if (os.path.exists(input_path) and os.path.exists(output_path)):
        number_of_files = 0
        for file in glob.glob(input_path + '/*.dds'):
            number_of_files = number_of_files + 1
        onestep = float(0)
        if(number_of_files>0):
            onestep = 100/number_of_files
        bar_var = onestep
        for file in glob.glob(input_path + "/*_c.dds"):
            cfile = Image.open(file)
            newcfile = convertAlpha(cfile)
            name = os.path.basename(file).replace('.dds', '.png')
            newpath = os.path.join(output_path,name)
            newcfile.save(newpath)
            updateProgressBar(bar_var)
        for file in glob.glob(input_path + "/*_n.dds"):
            nfile = Image.open(file)
            newnfile = convertNormal(nfile)
            name = os.path.basename(file).replace('.dds', '.png')
            newpath = os.path.join(output_path, name)
            newnfile.save(newpath)
            updateProgressBar(bar_var)
        for file in glob.glob(input_path + "/*_ao.dds"):
            aofile = Image.open(file)
            name = os.path.basename(file).replace('.dds', '.png')
            newpath = os.path.join(output_path, name)
            aofile.save(newpath)
            updateProgressBar(bar_var)

            
    else:
        print("FAIL!")

mainframe = ttk.Frame(root)

mainframe.pack()

in_label = Label(master=mainframe,text="Please select your input directory")
in_label.grid(row = 1, column=1, sticky="W", padx= 20, pady= 20)

in_entry = Entry(master=mainframe, text="Input")
in_entry.grid(row = 1, column = 2, sticky="W")

in_entry.get()

in_button = Button(master=mainframe,text="Browse", command =lambda: findDirectory(in_entry))
in_button.grid(row = 1, column = 3, sticky="W")


out_label = Label(master=mainframe,text="Please select your output directory")
out_label.grid(row = 2, column = 1, sticky="W")

out_entry = Entry(master=mainframe, text="Output")
out_entry.grid(row = 2, column = 2, sticky="W")

out_button = Button(master=mainframe,text = "Browse", command = lambda: findDirectory(out_entry))
out_button.grid(row = 2, column = 3, sticky="W")


convert_button = Button(master = mainframe, text = "Convert DDS to PNG", command = lambda: convert(in_entry.get(), out_entry.get()) )
convert_button.grid(row = 3, column = 1, pady=50, sticky=N+S+W+E)


progressbar = ttk.Progressbar(orient=HORIZONTAL, length=160)
progressbar.place(x = 230, y = 140)

    

warning_label = Label(master = mainframe, text="Both file paths necessary for app to work.", fg="red")
warning_label.grid(row=4, column = 1)


root.mainloop()