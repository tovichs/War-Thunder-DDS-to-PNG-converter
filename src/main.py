from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import glob
import os
from PIL import Image, ImageOps

root = Tk()
root.title("TexPorter")
root.minsize(500,500)
root.maxsize(500,500)

def updateProgressBar(increment):

    try:
        maximum = float(progressbar["maximum"])
    except Exception:
        maximum = 100.0

    try:
        current = float(progressbar["value"])
    except Exception:
        current = 0.0

    new_value = current + float(increment)
    
    if new_value > maximum:
        new_value = maximum
    if new_value < 0:
        new_value = 0

    progressbar["value"] = new_value
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

        progressbar["value"] = 0
        

        files_to_process = (
            glob.glob(input_path + "/*_c.dds") + 
            glob.glob(input_path + "/*_c_uhq.dds") +
            glob.glob(input_path + "/*_n*") +
            glob.glob(input_path + "/*_n_uhq.dds") +
            glob.glob(input_path + "/*_ao*")
        )
        number_of_files = len(files_to_process)
        
  
        onestep = 100.0 / number_of_files if number_of_files > 0 else 0
        bar_var = onestep
        for file in glob.glob(input_path + "/*_c.dds") + glob.glob(input_path + "/*_c_uhq.dds"):
            cfile = Image.open(file)
            newcfile = convertAlpha(cfile)
            name = os.path.basename(file).replace('.dds', '.png')
            newpath = os.path.join(output_path,name)
            newcfile.save(newpath)
            updateProgressBar(bar_var)
        for file in glob.glob(input_path + "/*_n*") + glob.glob(input_path + "/*_n_uhq.dds"):
            nfile = Image.open(file)
            newnfile = convertNormal(nfile)
            name = os.path.basename(file).replace('.dds', '.png')
            newpath = os.path.join(output_path, name)
            newnfile.save(newpath)
            updateProgressBar(bar_var)
        for file in glob.glob(input_path + "/*_ao*"):
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



progressbar = ttk.Progressbar(master=mainframe, orient=HORIZONTAL, length=150, mode='determinate', maximum=100, value=0)
progressbar.grid(row=3, column=2, padx=10, sticky="W")

    

warning_label = Label(master = mainframe, text="Both file paths necessary for app to work.", fg="red")
warning_label.grid(row=4, column = 1)


root.mainloop()