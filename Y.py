#---UPDATES FOR NEXT WORK TIME---

#prepare to build landscapes
#IF TIME - Prep enemies/attacking
#Enemies (basic) attacking (basic)
#enemy homelands
#VILLAGES!


#Y.py
from tkinter import *

#creating objects
root = Tk()
root.title("Y")
WORLD = Canvas(root, width=500, height=500)


#Garbage Collection Prevention Lists (can be used to store other images, etc etc)
WALL_PHOTOS = []
VILLAGE_PHOTOS = []

#WORLD VARIABLES - (lands, etc etc. Vars/functions to build maps)
LANDSCAPE = {"The Fields": "green",
             "The Forest": "#026400",
             "The Shirelands": "green",
             "The BorderLands": "#B7D052",
             "High Feet of the Mountain": "#998321",
             "Crown Mountains": "#6D5C0F",
             "Low Feet of the Mountain": "#998321",
             "The Desert" : "#D7BB0A", "Snowdin": "#F9F9F9", "Tundra": "#E5E5E5",
             "Isle Point": "#34BE83", "Islelands": "#04B62A", "Dark Desert" : "#A19303",
             "Bloodlands" : "#7D2D2D"}

LANDSCAPENUMS = ["The Fields", "The Forest", "The Shirelands",
                 "The BorderLands", "High Feet of the Mountain",
                 "Crown Mountains", "Low Feet of the Mountain",
                 "The Desert", "Snowdin", "Tundra", "Isle Point",
                 "Islelands", "Dark Desert", "Bloodlands"]
LANDNUM = 0
FixVar = [0, len(LANDSCAPENUMS)-1]

#COLLISION VARIABLES - For detecting collisions
BUILDINGS = []
ENEMIES = []
LANDSCAPE_ITEMS = []

#object tracking variables:
OBJECTS = {} #keeps track of objects and their unique ids

#changes landscape based upon coordinates of player object
#if the coordinates are too far left, the player moves left on the map
#if the coordinates are too far right, the player moves right on the map
#The WORLD changes the landscape as the player has entered a new region of
#the game.
def FIXVAR():
    #In case of list index being out of range, this function will "fix"
    #the variable so it can be used.
    global LANDNUM
    #print(LANDNUM)
    if LANDNUM > FixVar[1]:
        LANDNUM = FixVar[1]
    if LANDNUM < FixVar[0]:
        LANDNUM = FixVar[0]
    else:
        pass
def ChangeLandscapeLEFT(player):
    global LANDNUM
    Coords = WORLD.coords(player.avatar)
    WORLD.itemconfigure(LandscapeName, text=LANDSCAPENUMS[LANDNUM])
    #print(Coords)
    x1 = Coords[0]
    x2 = Coords[2]
    if x1 <= 0 and x2 <= 10:
        #print("NEXTLANDSCAPELEFT")
        if LANDNUM <= 0:
            WORLD.itemconfigure(LandscapeName, text="You cannot pass")
        else:
            try:
                LANDNUM -= 1
                WORLD.configure(bg=LANDSCAPE[LANDSCAPENUMS[LANDNUM]])
                WORLD.itemconfigure(LandscapeName, text=LANDSCAPENUMS[LANDNUM])
                del player.avatar
                player.draw(420, 250, 430, 260)
                player.homeland = LANDSCAPENUMS[LANDNUM]
            except:
                FIXVAR()
def ChangeLandscapeRIGHT(player):
    global LANDNUM
    Coords = WORLD.coords(player.avatar)
    WORLD.itemconfigure(LandscapeName, text=LANDSCAPENUMS[LANDNUM])
    #print(Coords)
    x1 = Coords[0]
    x2 = Coords[2]
    if x1 >= 500 and x2 >= 510:
        #print("NEXTLANDSCAPERIGHT")
        if LANDNUM == len(LANDSCAPENUMS) or LANDNUM >= len(LANDSCAPENUMS):
            LANDNUM = len(LANDSCAPENUMS)-1
            #print(LANDNUM)
            WORLD.itemconfigure(LandscapeName, text="You cannot pass")
        else:
            try:
                LANDNUM += 1
                WORLD.configure(bg=LANDSCAPE[LANDSCAPENUMS[LANDNUM]])
                WORLD.itemconfigure(LandscapeName, text=LANDSCAPENUMS[LANDNUM])
                del player.avatar
                player.draw(10, 250, 20, 260)
                player.homeland = LANDSCAPENUMS[LANDNUM]
            except:
                #print("Index out of range")
                FIXVAR()
                
def DetectCollision(object1, object2):
    #checks for overlapping xs and ys of the two rectangles,
    #This checks if one side is overlapping
    #print("DETECTING")
    '''
    x1 = object1.x
    x2 = object2.x
    y1 = object1.y
    y2 = object2.y
    w1 = object1.width
    w2 = object2.width
    h1 = object1.height
    h2 = object2.height
    '''
    CURRENTHOMELAND = LANDSCAPENUMS[LANDNUM]
    #OBJECTIVE: finds the rectangles of the two objects and sees if they overlap
    avatar1 = object1.avatar
    avatar2 = object2.avatar
    obj1tag = object1.tag
    obj2tag = object2.tag
    #print(obj2tag)
    HOMELAND1 = object1.homeland
    HOMELAND2 = object2.homeland
    #print("OBJ1 : " + HOMELAND1)
    #print("OBJ2 : " + HOMELAND2)
    #checks to see if they both are the same homeland:
    if HOMELAND1 != HOMELAND2:
        return False
    #Checks to see if both the homelands are the same as the current one
    #if not....the function stops.
    if HOMELAND1 and HOMELAND2 == CURRENTHOMELAND:
        #print("SAME")
        #grabs the object's position and checks to see if they overlap
        OBJ1 = WORLD.bbox(avatar1)
        OBJ2 = WORLD.bbox(avatar2)
        #bypasses the "NONETYPE ERROR"
        if OBJ1 == None:
            #reason for nonetype error is because the avatar does not exist at the
            #point of calling the function. 
            print("Nonetype, avatar does not exist")
        else:
            #grabs the overlapping objects and checks to see if OBJECT2 is in the overlap field
            overlap = WORLD.find_overlapping(OBJ1[0], OBJ1[1], OBJ1[2], OBJ1[3])
            #print("OBJ1: " + str(object1.ID))
            #print("OBJ2: " + str(object2.ID))
            #makes sure the first id in the tuple (object1) is not returned true
            if object2.ID in overlap:
                return True
       


#CANVAS PLAYER OBJECTS
LandscapeBar = WORLD.create_rectangle(400, 0, 100, 20, fill="white")
LandscapeName = WORLD.create_text(250, 10, text=LANDSCAPENUMS[0])
#makes the color of the landscape based upon the landscape color codes
WORLD.configure(bg=LANDSCAPE[LANDSCAPENUMS[0]])

#packing objects
#Creating the space in which all game objects will operate
WORLD.pack()

#creating operating game object classes
#defining the players of the game
class Player:
    def __init__(self, health, init_power, speed):
        self.health = health
        self.power = init_power
        self.speed = speed
        self.homeland = LANDSCAPENUMS[LANDNUM]
        self.draw(250, 250, 260, 260)
        self.walls = []
        self.tag = "player"
        self.photo = PhotoImage(file="Images/player/player_normal.gif")
        #for overlapping checking:
        OBJECTS["player"] = self
        print("PLAYER: " + str(WORLD.find_overlapping(250, 250, 260, 260)))
    #creating tangible, visible character
    def draw(self, x1, y1, x2, y2):
        self.avatar = WORLD.create_rectangle(x1, y1, x2, y2, fill="white", tag="player")
        self.x = x1
        self.y = y1
        self.width = x2-x1
        self.height = y2-y1
        overlap = WORLD.find_overlapping(250, 250, 260, 260)
        self.ID = overlap[0]
        #print(self.width)
        #print(self.height)
    #allowing player to control character movement
    def move(self, event):
        if event.keysym == "Right":
            WORLD.move(player.avatar, player.speed, 0)
        if event.keysym == "Left":
            WORLD.move(player.avatar, -player.speed, 0)
        if event.keysym == "Up":
            WORLD.move(player.avatar, 0, -player.speed)
        if event.keysym == "Down":
            WORLD.move(player.avatar, 0, player.speed)
        #calls world functions to check for neccessary landscape change
        ChangeLandscapeLEFT(self)
        ChangeLandscapeRIGHT(self)
        self.CHANGELAND()
        for x in range(0, len(self.walls)):
            self.walls[x].LANDCHECK()
        for x in range(0, len(BUILDINGS)):
            if DetectCollision(self, BUILDINGS[x]):
                print("PLAYER TOUCHING BUILDING")
            else:
                pass
    #attack to defend from enemies: flashes red for basic attack
    def attack(self, event):
        if event.keysym == "x":
            WORLD.itemconfigure(self.avatar, fill="red")
            #Tkinter After function: Delays command by certain miliseconds (500 in
            #this case
            WORLD.after(500, lambda: WORLD.itemconfigure(self.avatar, fill="white"))
    def build_wall(self, event):
        if event.keysym == "w":
            #print("BUILDING WALL")
            new_wall = Building("wall", self, LANDSCAPENUMS[LANDNUM])
            new_wall.build(self)
            self.walls.append(new_wall)
    def DEBUGrefresh(self):
        del self.avatar
        self.avatar = WORLD.create_rectangle(250, 250, 260, 260, fill="white", tag="player")
    def CHANGELAND(self):
        #changes the homeland so that the collision detection works.
        self.homeland = LANDSCAPENUMS[LANDNUM]
            
#defining the basic enemy class of the game------
class Enemy:
    def __init__(self, TYPE, player, homeland):
        self.player = player
        self.homeland = homeland
        self.tag = "E-%d" % id(self)
        OBJECTS[self.tag] = self
        self.ID = self.DefineID()
        if TYPE == "orc":
            self.TYPE = 1
        else:
            del self
    def DefineID(self):
        IDS = WORLD.find_all()
        SelfID = len(IDS) + 1
        return SelfID
    def SPAWN(self):
        pass
            
        
    
#----builds a building object, being either garrisons, villages, player built walls,-----
#NPC built walls, etc etc etc etc etc
#FUNCTIONS CAN BUILD:
    #walls
class Building:
    def __init__(self,TYPE, constructor, land):
        self.homeland = land
        self.constructor = constructor
        self.ID = self.DefineID()
        #print(self.ID)
        if TYPE == "wall":
            self.TYPE = 1
            self.photo = PhotoImage(file="Images/buildings/walls/BUILDING_newwall.gif")
            WALL_PHOTOS.append(self.photo)
            self.tag = "w-%d" % id(self)
            OBJECTS[self.tag] = self
        if TYPE == "village":
            self.TYPE = 2
            self.photo = PhotoImage(file="Images/buildings/villages/village_1.gif")
            VILLAGE_PHOTOS.append(self.photo)
            self.tag = "V-%d" % id(self)
            OBJECTS[self.tag] = self
        else:
            del self
    #places avatar based upon constructor vars
    def DefineID(self):
        IDS = WORLD.find_all()
        #defines itself a unique id for checking for overlap
        SelfID = len(IDS)+1
        return SelfID
    def build(self, constructor):
        ccoords = WORLD.coords(constructor.avatar)
        #print(ccoords)
        x = ccoords[0]+20
        y = ccoords[1]
        self.x = x
        self.y = y
        self.x1 = x+20
        self.y2 = x+20
        self.avatar = WORLD.create_image(x, y, image=self.photo, tags=("building", self.tag))
        self.width = self.photo.width()
        self.height = self.photo.height()
        print(self.homeland)
        #captures the building so we can detect collisions later
        BUILDINGS.append(self)
    #checks to see if the player is in the land that the object was built in.
    def LANDCHECK(self):
        if LANDSCAPENUMS[LANDNUM] != self.homeland:
            WORLD.itemconfigure(self.avatar, state=HIDDEN)
        if LANDSCAPENUMS[LANDNUM] == self.homeland:
            WORLD.itemconfigure(self.avatar, state=NORMAL)
        #print("X1, Y1, X2, Y2: " + str(self.x) + " " + str(self.y) + " " + str(self.x+20) + " " + str(self.y+20))
        #print("PLAYER: " + str(WORLD.coords(self.constructor.avatar)))
            
        if DetectCollision(self, self.constructor):
            print("BUILDING TOUCHING PLAYER")
        else:
            pass
    def DEFINEVILLAGES(self):
        self.VILLAGEID = "V-
                
        

#Defining Operating Objects
player = Player(10, 1, 10)

WORLD.bind_all("<KeyPress-Right>", player.move)
WORLD.bind_all("<KeyPress-Left>", player.move)
WORLD.bind_all("<KeyPress-Up>", player.move)
WORLD.bind_all("<KeyPress-Down>", player.move)
WORLD.bind_all("x", player.attack)
WORLD.bind_all("w", player.build_wall)

while True:
    try:
        root.mainloop()
        WORLD.update()
    except:
        pass

