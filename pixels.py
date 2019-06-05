#pixels
from tkinter import *

#creating objects
root = Tk()
canvas = Canvas(root, width=500, height=500, bg="white")

#X,Y
X50= [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
     600, 650, 700, 750, 800, 850, 900, 950, 1000]

Y50 = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550,
     600, 650, 700, 750, 800, 850, 900, 950, 1000]

X20 = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200,
       220, 240, 260, 280, 300, 320, 340, 360, 380, 400,
       420, 440, 460, 480, 500, 520, 540, 560, 580, 600,
       620, 640, 660, 680, 700, 720, 740, 760, 780, 800,
       820, 840, 860,  880, 900, 920, 940, 960, 980, 1000]

Y20 = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200,
       220, 240, 260, 280, 300, 320, 340, 360, 380, 400,
       420, 440, 460, 480, 500, 520, 540, 560, 580, 600,
       620, 640, 660, 680, 700, 720, 740, 760, 780, 800,
       820, 840, 860,  880, 900, 920, 940, 960, 980, 1000]

X10 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120,
       130, 140, 150, 160, 170, 180, 190, 200, 220, 230, 240,
       250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350,
       360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460,
       470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570,
       580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680,
       690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790,
       800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900,
       910, 920, 930, 940, 950, 960, 970, 980, 990, 1000]

Y10 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120,
       130, 140, 150, 160, 170, 180, 190, 200, 220, 230, 240,
       250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350,
       360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460,
       470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570,
       580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680,
       690, 700, 710, 720, 730, 740, 750, 760, 770, 780, 790,
       800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900,
       910, 920, 930, 940, 950, 960, 970, 980, 990, 1000]

#functions
def change(item, color):
    canvas.itemconfigure(item, fill=color)
def onclick(event):
    item = canvas.find_closest(event.x, event.y)
    color = canvas.itemcget(item, "fill")
    if color == "black":
        canvas.itemconfigure(item, fill="#3B3B3B")
    if color == "#3B3B3B":
        canvas.itemconfigure(item, fill="#757575")
    if color == "#757575":
        canvas.itemconfigure(item, fill="#A8A8A8")
    if color == "#A8A8A8":
        canvas.itemconfigure(item, fill="#AB8D8D")
    if color == "#AB8D8D":
        canvas.itemconfigure(item, fill="#AD6E6E")
    if color == "#AD6E6E":
        canvas.itemconfigure(item, fill="#B64141")
    if color == "#B64141":
        canvas.itemconfigure(item, fill="#CD2525")
    if color == "#CD2525":
        canvas.itemconfigure(item, fill="#E30F0F")
    if color == "#E30F0F":
        change(item, "#F00707")
    if color == "#F00707":
        change(item, "white")
    if color == "white":
        change(item, "black")


class Pixel():
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.draw()
    def draw(self):
        self.avatar = canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill="black")
        


#pixel objects
def GENERATE(lsx, lsy):
    diff = lsx[1]-lsx[0]
    for x in range(0, len(lsx)):
        for y in range(0, len(lsy)):
            OO = Pixel(lsx[x], lsy[y], lsx[x]+diff, lsy[y]+diff)

def START():
    size = input("Block size: ")
    if int(size) == 20:
        GENERATE(X20, Y20)
    elif int(size) == 50:
        GENERATE(X50, Y50)
    elif int(size) == 10:
        GENERATE(X10, Y10)
    else:
        print("Not a value")

START()

#packing objects
canvas.pack()

canvas.bind("<Button-1>", onclick)

root.mainloop()
