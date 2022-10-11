import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import json

# GUI for AnaylzerApp
window = tk.Tk()
window.geometry("300x100")  # Size of the window
window.title('DataAnalyzer')
my_font1 = ('times', 18, 'bold')
l1 = tk.Label(window, text='Analyzer for visual data', width=20, font=my_font1)
l1.grid(row=1, column=1)

b1 = tk.Button(window, text='Browse directory', width=20, command=lambda: upload_file())
b1.grid(row=2, column=1)


# Button to return to main menu (for now is close)
def close():
    window.quit()


b2 = tk.Button(window, text='Return', width=10, command=close)
b2.grid(row=3, column=1)


def upload_file():
    file = filedialog.askopenfilename()
    file = json.load(open(file, 'r'))

    # Converting JSON to a dictionary i.e. datecount={08 Oct : 1}
    storiesdata = file['Stories']
    newdata = str(storiesdata).replace('[', '').replace(']', '').replace('{', '').replace('}', '').replace('\'',
                                                                                                           '').replace(
        '\"', '')

    def convert(string):
        newdata = list(string.split(","))
        return newdata

    newdata = convert(newdata)

    datedata = []

    for i in newdata:
        if 'Date' in i:
            datedata.append(i)

    datecount = dict()
    for i in datedata:
        datecount[i] = datecount.get(i, 0) + 1
    datecount = dict(sorted(datecount.items()))

    def truncate_keys(datecount, length):
        return dict((k[6:length], v) for k, v in datecount.items())

    shortendate = truncate_keys(datecount, -4)

    # Plotting
    xAxis = [key for key, value in shortendate.items()]
    yAxis = [value for key, value in shortendate.items()]
    plt.grid(True)

    ## LINE GRAPH ##
    plt.plot(xAxis, yAxis, color='maroon', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Number of Scam Cases')

    ## BAR GRAPH ##
    fig = plt.figure()
    plt.bar(xAxis, yAxis, color='maroon')
    plt.xlabel('Date')
    plt.ylabel('Number of Scam Cases')

    plt.show()


window.mainloop()  # Keep the window open
