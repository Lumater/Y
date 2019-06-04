#---UPDATES FOR NEXT WORK TIME---

#prepare to build landscapes
    #Player can pick up different projectiles, adding health and damage to their own projectiles

        #NPC soldiers if enemies are near. To attack orcs.
        #Builder NPCS build farms, camps, etc.
        #Priest NPCS build shrines from camps

#SOLDIER NPCS: Fight enemies
#WANDERER NPCS: wander a few lands and then build a village, and immediately
    #become elders
#FADES: teleport around the map. Turn invisible randomly and reappear later
    #ONLY if the player is in the land.
    #when orcs die, they have the potential to become fades
    #fades will eat NPCS and become stronger and bigger.

#NPCS when they run out of purpose:
    #I.E. they become a elder NPC

#Y.py
from tkinter import *
import random
import math

#creating objects
root = Tk()
root.title("Y")
WORLD = Canvas(root, width=500, height=500)


#Garbage Collection Prevention Lists (can be used to store other images, etc etc)
WALL_PHOTOS = []
VILLAGE_PHOTOS = []
ENEMYPHOTOS = []
GARRISION_PHOTOS = []
NPC_PHOTOS = []
CONSTRUCTION_PHOTOS = []
SHRINE_PHOTOS = []
FARM_PHOTOS = []

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
             "Bloodlands" : "#7D2D2D", "Fly you fools": "#788351"}

LANDSCAPENUMS = ["The Fields", "The Forest", "The Shirelands",
                 "The BorderLands", "High Feet of the Mountain",
                 "Crown Mountains", "Low Feet of the Mountain",
                 "The Desert", "Snowdin", "Tundra", "Isle Point",
                 "Islelands", "Dark Desert", "Bloodlands", "Fly you fools"]
LANDNUM = 0
FixVar = [0, len(LANDSCAPENUMS)-1]

#COLLISION VARIABLES - For detecting collisions
BUILDINGS = []
ENEMIES = []
LANDSCAPE_ITEMS = []
PROJECTILES = []
NPCS = []
CONSTRUCTIONS = []


#object tracking variables:
OBJECTS = {} #keeps track of objects and their unique ids

#SPAWN VARIABLES
EnemyNum = 1
EnemyWaveSecs = 500
#number of enemy types
Ntype = 1

#PLAYER ATTACK VARS:
PLAYERATTACKING = False
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
    try:
        Coords = WORLD.coords(player.avatar)
        WORLD.itemconfigure(LandscapeName, text=LANDSCAPENUMS[LANDNUM])
        #print(Coords)
        x1 = Coords[0]
        x2 = Coords[2]
        if x1 <= -10 and x2 <= 0:
            #print("NEXTLANDSCAPELEFT")
            if LANDNUM <= 0:
                WORLD.itemconfigure(LandscapeName, text="You cannot pass")
            else:
                try:
                    LANDNUM -= 1
                    WORLD.configure(bg=LANDSCAPE[LANDSCAPENUMS[LANDNUM]])
                    WORLD.itemconfigure(LandscapeName, text=LANDSCAPENUMS[LANDNUM])
                    del player.avatar
                    #places player on the right side of the world
                    player.draw(420, 250, 430, 260)
                    player.homeland = LANDSCAPENUMS[LANDNUM]
                except:
                    FIXVAR()
    except:
        pass
def ChangeLandscapeRIGHT(player):
    global LANDNUM
    try:
        Coords = WORLD.coords(player.avatar)
        WORLD.itemconfigure(LandscapeName, text=LANDSCAPENUMS[LANDNUM])
        #print(Coords)
        x1 = Coords[0]
        x2 = Coords[2]
        if x1 >= 510 and x2 >= 520:
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
                    #places player on the left side of the world
                    player.draw(10, 250, 20, 260)
                    player.homeland = LANDSCAPENUMS[LANDNUM]
                except:
                    #print("Index out of range")
                    FIXVAR()
    except:
        pass
                
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
    obj1 = str(obj1tag)
    obj2 = str(obj2tag)
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
        #print(obj1 + " SAME " + obj2)
        #grabs the object's position and checks to see if they overlap
        OBJ1 = WORLD.bbox(avatar1)
        OBJ2 = WORLD.bbox(avatar2)
        #print(obj1 + ":" + str(OBJ1))
        #print(obj2 + ":" + str(OBJ2))
        #bypasses the "NONETYPE ERROR"
        if OBJ1 == None or OBJ2 == None:
            #reason for nonetype error is because the avatar does not exist at the
            #point of calling the function. 
            #print("Nonetype, avatar does not exist")
            return False
        else:
            #grabs the overlapping objects and checks to see if OBJECT2 is in the overlap field
            overlap = WORLD.find_overlapping(OBJ1[0], OBJ1[1], OBJ1[2], OBJ1[3])
            overlap2 = WORLD.find_overlapping(OBJ2[0], OBJ2[1], OBJ2[2], OBJ2[3])
            #print(obj1 + ":" + str(overlap))
            #print(obj1 + ":" + str(object1.ID))
            #print(obj2 + ":" + str(object2.ID))
            #makes sure the first id in the tuple (object1) is not returned true
            if object2.avatar in overlap:
                return True
            else:
                return False
            
#----VILLAGE FUNCTIONS----
def SpawnVillages():
    global player
    #finds number of lands, picks the number of potential villages
    #and creates villages in random spots in those lands.
    Landnumber = len(LANDSCAPENUMS)
    Numofvillages = random.randint(1, 16)
    for x in range(0, Numofvillages):
        land = random.randint(0, (Landnumber-2))
        Hland = LANDSCAPENUMS[land]
        VILLAGE = Building("village", player, Hland)
        VILLAGE.spawn()
        VILLAGE.LANDCHECK()

#----Enemy functions----
def SpawnEnemies():
    global EnemyNum
    global Ntype
    global player
    for x in range(0, random.randint(0, 20)):
        #False is specifing they are spawning normally. NOT from a garrison.
        newenemy = Enemy(random.randint(1, Ntype), False)
        
#----CLEAN FUNCTIONS----
def Clean():
    print("cleaning")
    for x in range(0, len(PROJECTILES)-1):
        PROJECTILES[x].implode()
        
    #for x in range(0, len(ENEMIES)-1):
        #ENEMIES[x].DIE()

#----Random Math Functions-----

#rounds up the number to the 10ths place if Decimals is a negative value of -1
#why? Well, cause it's moving <- past the decimal value
def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

#---NPC CONSTRUCTION FUNCTION----
def BuildConstruction(constructor):
    Construct = Building("construction", constructor, constructor.homeland)
    Construct.build(constructor)

#--BUILDINGS CONSTRUCTION -> actual Building FUNCTION----
def makeBuilding(TYPE, OBJECT):
    #Tier THREE - Construction update 
    if TYPE == "shrine":
        SHRINE = Building("shrine", OBJECT, OBJECT.homeland)
        #print("SHRINE OBJECT MADE " + str(OBJECT.homeland))
        SHRINE.build(OBJECT)
        #print("SHRINE OBJECT BEING BUILT " + str(OBJECT.homeland))
        #print("CONSTRUCTION OBJECT DELETED " + str(OBJECT.homeland))
        #OBJECT.ended = True
        
    elif TYPE == "village":
        VILLAGE = Building("village", OBJECT, OBJECT.homeland)
        VILLAGE.FromConstructionBuild(OBJECT)
        OBJECT.ended = True

    elif TYPE == "farm":
        FARM = Building("farm", OBJECT, OBJECT.homeland)
        FARM.FromConstructionBuild(OBJECT)
        OBJECT.ended = True
    

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
    def __init__(self, health, init_power, speed, projectileNum):
        self.health = health
        self.power = init_power
        self.speed = speed
        self.homeland = LANDSCAPENUMS[LANDNUM]
        self.pos = [250, 250, 260, 260]
        self.draw(250, 250, 260, 260)
        self.walls = []
        self.tag = "player"
        self.photo = PhotoImage(file="Images/player/player_normal.gif")
        #for overlapping checking:
        OBJECTS["player"] = self
        #print("PLAYER: " + str(WORLD.find_overlapping(250, 250, 260, 260)))
        self.direct = "R"
        self.Num_Of_Projectiles = projectileNum

    #creating tangible, visible character
    def draw(self, x1, y1, x2, y2):
        self.avatar = WORLD.create_rectangle(x1, y1, x2, y2, fill="white", tag="player")
        self.x = x1
        self.y = y1
        self.width = x2-x1
        self.height = y2-y1
        overlap = WORLD.find_overlapping(250, 250, 260, 260)
        self.ID = overlap[0]

    #allowing player to control character movement
        
    def move(self, event):
        try:
            if event.keysym == "Right":
                WORLD.move(player.avatar, player.speed, 0)
                self.direct = "R"
            if event.keysym == "Left":
                WORLD.move(player.avatar, -player.speed, 0)
                self.direct = "L"
            if event.keysym == "Up":
                WORLD.move(player.avatar, 0, -player.speed)
                self.direct = "U"
            if event.keysym == "Down":
                WORLD.move(player.avatar, 0, player.speed)
                self.direct = "D"
            #calls world functions to check for neccessary landscape change
            ChangeLandscapeLEFT(self)
            ChangeLandscapeRIGHT(self)
            self.CHANGELAND()
            #checks for collisions and tells each object to "recheck" where
            #they are on the map
            for x in range(0, len(self.walls)):
                self.walls[x].LANDCHECK()
                
            for x in range(0, len(BUILDINGS)):
                BUILDINGS[x].LANDCHECK()
                if DetectCollision(self, BUILDINGS[x]):
                    print("PLAYER TOUCHING BUILDING")
                else:
                    pass
                
            for x in range(0, len(CONSTRUCTIONS)):
                CONSTRUCTIONS[x].LANDCHECK()
                
            for x in range(0, len(ENEMIES)):
                ENEMIES[x].LANDCHECK()
                if DetectCollision(self, ENEMIES[x]):
                    print("PLAYER TOUCHING ENEMY")
                else:
                    pass

            for x in range(0, len(PROJECTILES)):
                #the player will only recognize enemy projectiles as dangerous
                if "E" in PROJECTILES[x].orgin.tag:
                    if DetectCollision(self, PROJECTILES[x]):
                        #subtracts health from itself if hit by ENEMY projectiles
                        if self.health > 0:
                            self.health -= PROJECTILES[x].attack
                            WORLD.itemconfigure(HealthBar, text="HP: " + str(self.health))
                            PROJECTILES[x].implode()
                        if self.health <= 0:
                            player.GAMEOVER()
                            PROJECTILES[x].implode()
                else:
                    pass

            for x in range(0, len(NPCS)):
                #The player can interact with NPCS like enemies, except NPCS
                #are benevolent.
                NPCS[x].RUN()
                if DetectCollision(self, NPCS[x]):
                    print("TOUCHING NPC")
        except:
            pass
    #attack to defend from enemies: flashes red for basic attack
    def attack(self, event):
        global PLAYERATTACKING
        
        if event.keysym == "x":
            #limits the potential number of projectiles a player can make
            if self.Num_Of_Projectiles > 0:
                PROJECTILE = Projectile(self, "red", 10)
                self.Num_Of_Projectiles -= 1
                print(self.Num_Of_Projectiles)
            elif self.Num_Of_Projectiles <= 0:
                pass
            '''
            WORLD.itemconfigure(self.avatar, fill="red")
            PLAYERATTACKING = True
            #Tkinter After function: Delays command by certain miliseconds (500 in
            #this case
            WORLD.after(6000, lambda: WORLD.itemconfigure(self.avatar, fill="white"))
            PLAYERATTACKING = False
            '''           
            
        elif event.keysym == "z":
            #imits the potential number of projectiles a player can make
            if self.Num_Of_Projectiles > 0:
                PROJECTILE = Projectile(self, "red", 10)
                self.Num_Of_Projectiles -= 1
                #print(self.Num_Of_Projectiles)
            elif self.Num_Of_Projectiles <= 0:
                pass
            elif self.Num_Of_Projectiles > 15:
                self.Num_Of_Projectiles = 15

        elif event.keysym == "c":
            makeBuilding("shrine", self)

        elif event.keysym == "v":
            #the player can call an NPC from a village on command.
            #Randomly assigned a class by the NPC itself
            for x in range(0, len(BUILDINGS)):
                if "V" in BUILDINGS[x].tag:
                    if DetectCollision(self, BUILDINGS[x]):
                        CalledNPC = NPC(BUILDINGS[x])
                else:
                    pass

        elif event.keysym == "e":
            #checks for the player touching a farm.
            #if the player is touching a farm and e is pressed
            #the player will "eat" and regain 1 health point, but use
            #up the farm's crops. Then the farm will decline.
            
            for x in range(0, len(BUILDINGS)): 
                if BUILDINGS[x].TYPE == 6:
                    if DetectCollision(self, BUILDINGS[x]):
                        #adds health to player by one:
                        BUILDINGS[x].FarmAddPlayerHealth()

        elif event.keysym == "q":
            #checks for the player touching a shrine
            #if the player touches a farm and q is pressed
            #the player may or may not get 1 extra power to it's variable.
            #Then the shrine will get stronger if q is used often
            #But the shrine will decline if q is not used.

            for x in range(0, len(BUILDINGS)):
                if BUILDINGS[x].TYPE == 5:
                    if DetectCollision(self, BUILDINGS[x]):
                        #adds power to player maybe.
                        n = random.randint(0, 50)
                        BUILDINGS[x].ShrineRENEW()
                        WORLD.itemconfigure(self.avatar, fill="#07F0EC")
                        WORLD.after(500, lambda: WORLD.itemconfigure(self.avatar, fill="white"))
                        if n == 20 or 30 and BUILDINGS[x].cangivepower == True:
                            n = random.randint(0, 1)
                            self.addpower(n)
                            BUILDINGS[x].cangivepower = False
            
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

    def addhealth(self, h):
        self.health += h
        WORLD.itemconfigure(HealthBar, text="HP: " + str(self.health))

    def losehealth(self, h):
        self.health -= h
        WORLD.itemconfigure(HealthBar, text="HP: " + str(self.health))

    def addpower(self, p):
        self.power += p
        WORLD.itemconfigure(PowerBar, text="PW: " + str(self.power))

    def losepower(self, p):
        self.power -= p
        WORLD.itemconfigure(PowerBar, text="PW: " + str(self.power))

    def GAMEOVER(self):
        WORLD.delete(self.avatar)
        print("DEAD")
        GAMEOVER = WORLD.create_text(250, 250,text="YOU DIED", fill="red")
        
#defining the basic enemy class of the game------
class Enemy:
    def __init__(self, TYPE, garrison=False):
        #so the enemy can reference the player in various
        #functions
        self.player = player
        #basic stuff to make sure that the
        #object has a place in space,
        #as well as making it discernable from other
        #enemy objects
        self.homeland = "Fly you fools"
        self.landn = len(LANDSCAPENUMS)
        self.tag = "E-%d" % id(self)
        OBJECTS[self.tag] = self
        self.ID = self.DefineID()
        ENEMIES.append(self)
        self.collision = False
        #Death Boolean Variable
        self.DEAD = False
        #direction var for projectiles
        self.direct = "L"

        #ORC CLASS OF ENEMY
        if TYPE == "orc" or 1:
            self.TYPE = 1
            self.photo = PhotoImage(file="Images/enemies/orc/orc_1.gif")
            self.attack_photo = PhotoImage(file="Images/enemies/orc/orc_attack.gif")
            ENEMYPHOTOS.append(self.photo)
            OBJECTS[self.tag] = self
            #specific to orc class:
            self.health = 2
            self.attack = 1
            self.speed = 5
            #specific to orc class but MUST be defined:
            self.canspawn = True
            self.garrison = garrison

            #Spawning from Garrison
            if garrison != False:
                self.garrison = garrison
                #refrenced later to check if the object can spawn a garrison.
                #If false, they cannot.
                self.canspawn = False
                GCoords = WORLD.coords(garrison.avatar)
                if GCoords == None:
                    pass
                else:
                    #Creates it's coords based upon garrison coords
                    n = random.randint(0, 3)
                    if n == 0:
                        self.x = GCoords[0] - 30
                        self.y = GCoords[1]
                    if n == 1:
                        self.x = GCoords[0] + 30
                        self.y = GCoords[1]
                    if n == 2:
                        self.x = GCoords[0]
                        self.y = GCoords[1] - 30
                    if n == 3:
                        self.x = GCoords[0]
                        self.y = GCoords[1] + 30
                        
                    self.homeland = self.garrison.homeland
                    self.SPAWNBYGARRISON()
                    print("SPAWNING BY GARRISON: " + str(self.garrison.homeland))
            elif garrison == False:

                #Normal spawning
                self.x = random.randint(20, 480)
                self.y = random.randint(20, 480)
            
                self.SPAWN()
            else:
                del self

        if TYPE == "fade" or 2:
            self.TYPE = 2
            self.photo = PhotoImage(file="Images/enemies/basicfade/basic_fade1.gif")
            ENEMYPHOTOS.append(self.photo)
            OBJECTS[self.tag] = self
            #specific to FADE class
            self.health = 2
            self.attack = 2
            self.speed = 10
            #super specific to FADE class
            self.hidden = False
            
            
    def DefineID(self):
        IDS = WORLD.find_all()
        SelfID = len(IDS) + 1
        return SelfID
    def SPAWN(self):
        self.homeland = "Fly you fools"
        self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tags=("enemy", self.tag))
        self.LANDCHECK()

    def SPAWNBYGARRISON(self):
        #For spawning by a garrison
        self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tags=("enemy", self.tag))
        self.LANDCHECK()
        
    def ATTACK(self, obj):
        #sees if it's touching anything.
        #if so, checks if it's a player or a building
        #print(obj)
        if DetectCollision(self, obj):
            if obj == player:
                #FAILED PLAYER ATTACK CODE:
                #fix for projectiles.
                '''
                    color = WORLD.itemcget(player.avatar, "fill")
                    if color == "red":
                        print("ENEMY HEALTH LOST")
                        #if the player has an attack color:
                        #enemy takes it's health.
                        self.health - player.power
                        if self.health <= 0:
                            WORLD.delete(self.avatar)
                            del self
                            '''
            elif obj in BUILDINGS:
                #checks the building types. If it's a village
                #or a wall
                if obj.TYPE == 1:
                    #tells the object to check if it's being attacked.
                    WORLD.itemconfigure(self.avatar, image=self.attack_photo)
                    root.after(4000, lambda: obj.checkattack(self))
                    root.after(500, lambda: WORLD.itemconfigure(self.avatar, image=self.photo))
                if obj.TYPE == 2:
                    pass
            
    def LANDCHECK(self):
        #if statement to check if the enemy is existent:
        #if self.avatar != None:
        #if statement to check if the enemy is dead:
        if self.DEAD == True:
            self.DIE()
        else:
            #checks to see if the player is in the land that the object was built in.
            if LANDSCAPENUMS[LANDNUM] != self.homeland:
                WORLD.itemconfigure(self.avatar, state=HIDDEN)
            if LANDSCAPENUMS[LANDNUM] == self.homeland:
                WORLD.itemconfigure(self.avatar, state=NORMAL)
            #print("X1, Y1, X2, Y2: " + str(self.x) + " " + str(self.y) + " " + str(self.x+20) + " " + str(self.y+20))
            #print("PLAYER: " + str(WORLD.coords(self.constructor.avatar)))

            #for enemies tries to detect whether it (at any point)
            #is touching a building (i.e. walls, villages)
            #is touching a player
            #dies if touching a projectile
            #Enemies can overlap however.

            #if statement to check if they are dead. self.DEAD boolean
            for x in range(0, len(BUILDINGS)):
                if DetectCollision(self, BUILDINGS[x]):
                    #print("ENEMY TOUCHING BUILDING - Not moving")
                    self.collision = True
                    self.ATTACK(BUILDINGS[x])
                
            if DetectCollision(self, self.player):
                #print("ENEMY TOUCHING PLAYER")
                self.collision = True
                self.ATTACK(self.player)

            for x in range(0, len(PROJECTILES)):
                if DetectCollision(self, PROJECTILES[x]):
                    self.collision = True
                    #This code compares the power of a projectile to it's health
                    #and subtracts health from itself based upon that.
                    if PROJECTILES[x].enemy == True:
                        pass
                    else:
                        if self.health <= 0:
                            PROJECTILES[x].implode()
                            self.DIE()
                        else:
                            self.health -= PROJECTILES[x].attack
                            PROJECTILES[x].implode()
            
            if self.collision == False:
                Coords = WORLD.coords(self.avatar)
                CURRENTLAND = LANDSCAPENUMS[LANDNUM]
                EnemyLands = {}
                #builds a little map of which it can dictate where it is in
                #relation to the player.
                for x in range(0, len(LANDSCAPENUMS)):
                    EnemyLands[x] = LANDSCAPENUMS[x]
                #print(Coords)
                x1 = Coords[0]
                #checks to see if the enemy has left the land it was in,
                if x1 >= 520:
                    if self.landn == len(LANDSCAPENUMS):
                        WORLD.move(self.avatar, -self.speed, 0)
                    else:
                        #moves it to the next land on the right.
                        self.landn += 1
                        self.homeland = EnemyLands[self.landn]
                        del self.avatar
                        self.avatar = WORLD.create_image(470, self.y, image=self.photo, tags=("enemy", self.tag))
                        self.LANDCHECK()
                elif x1 <= -20:
                    if self.landn == 1:
                        print("EVOLVING")
                        #makes the enemy go back to where it started
                        self.landn = 14
                        #makes the enemy randomly stronger or healthier
                        #or faster
                        SHSN = random.randint(0, 2)
                        if SHSN == 0:
                            self.attack += 1
                        elif SHSN == 1:
                            self.health += 1
                        elif SHSN == 2:
                            self.speed += 1
                        #---
                        self.homeland = EnemyLands[self.landn]
                        del self.avatar
                        #randomly places the enemy somewhere on the y axis
                        self.y = random.randint(40, 360)
                        self.avatar = WORLD.create_image(470, self.y, image=self.photo, tags=("enemy", self.tag))
                        self.LANDCHECK()
                    else:
                        #moves it to the next land on the left.
                        self.landn -= 1
                        self.homeland = EnemyLands[self.landn]
                        del self.avatar
                        self.avatar = WORLD.create_image(470, self.y, image=self.photo, tags=("enemy", self.tag))
                        self.LANDCHECK()
                else:
                    WORLD.move(self.avatar, -self.speed, 0)
                
                #Compares Y coords to see if enemies and player is on the same plane.
                #will allow for enemies to shoot projectiles at the player
                if self.CompareYCoords() and self.homeland == LANDSCAPENUMS[LANDNUM]:
                    if self.TYPE == 1:
                        proj = Projectile(self, "grey", self.speed+1)
                
            elif self.collision == True:
                #Checks collisions again, just to see if the enemy is still being touched
                for x in range(0, len(BUILDINGS)):
                    if DetectCollision(self, BUILDINGS[x]):
                    
                        #moves around villages
                        if BUILDINGS[x].TYPE == 2 or BUILDINGS[x].TYPE == 3:
                            xoy = random.randint(1, 2)
                            if xoy == 1:
                                WORLD.move(self.avatar, 0, -self.speed)
                            if xoy == 2:
                                WORLD.move(self.avatar, 0, self.speed)
                        else:
                        
                            #print("ENEMY TOUCHING BUILDING - Not moving")
                            self.collision = True
                            self.ATTACK(BUILDINGS[x])
                
                if DetectCollision(self, self.player):
                    #if touching player, enemy attacks player.
                    print("ENEMY TOUCHING PLAYER")
                    self.collision = True
                    self.ATTACK(self.player)
            
                else:
                    self.collision = False

                    #Double random coords for garrison spawning.
                    #CURRENTLY DEBUG SMALL RATIOS
                    #Checks to see if the self.canspawn is false or true
                    #To check if the object can propagate.
                    if self.canspawn == True: 
                        num1 = random.randint(0, 30)
                        num2 = random.randint(0, 30)
                    
                        if num1 == 2 and num2 == 2:
                            #print("GARRISON CONSTRUCTED IN: " + str(self.homeland))
                            GARRISON = Building("orc_garrison", self, self.homeland)
                            GARRISON.build(self)
                            self.DIE()
                    elif self.canspawn == False:
                        pass
    def DIE(self):
        self.DEAD = True
        WORLD.delete(self.avatar)
        try:
            ENEMIES.remove(self)
        except:
            pass

    def CompareYCoords(self):
        SELFCOORDS = WORLD.coords(self.avatar)
        PLAYERCOORDS = WORLD.coords(player.avatar)
        selfy = SELFCOORDS[1]
        playery = PLAYERCOORDS[1]
        #rounds up the number so that it can be even to the player's
        if round_up(selfy, -1) == playery:
            return True
        else:
            return False
            
    
        
    
#----builds a building object, being either garrisons, villages, player built walls,-----
#NPC built walls, etc etc etc etc etc
#FUNCTIONS CAN BUILD:
    #walls
class Building:
    def __init__(self,TYPE, constructor, land):
        self.homeland = land
        self.constructor = constructor
        self.ID = self.DefineID()

        #general buildings variable
        self.ended = False
        
        if TYPE == "wall":
            self.TYPE = 1
            self.photo = PhotoImage(file="Images/buildings/walls/BUILDING_newwall.gif")
            WALL_PHOTOS.append(self.photo)
            self.tag = "w-%d" % id(self)
            OBJECTS[self.tag] = self
            self.HEALTH = 5
            self.Hmax = 5
            
        if TYPE == "village":
            self.TYPE = 2
            self.photo = PhotoImage(file="Images/buildings/villages/village_1.gif")
            VILLAGE_PHOTOS.append(self.photo)
            self.tag = "V-%d" % id(self)
            OBJECTS[self.tag] = self
            self.HEALTH = 30
            self.Hmax = 30
            #specific to villages
            self.MAXSPAWNNPCS = 3
            self.burn = False
            self.stage = 0

        if TYPE == "orc_garrison":
            self.TYPE = 3
            self.photo = PhotoImage(file="Images/buildings/garrisons/orc_garrison.gif")
            GARRISION_PHOTOS.append(self.photo)
            self.tag = "o_g-%d" % id(self)
            OBJECTS[self.tag] = self
            self.HEALTH = 40
            self.Hmax = 40
            #specific to orc garrison
            self.MAXSPAWN = 10
            self.time = 20000

        if TYPE == "construction":
            self.TYPE = 4
            self.photo = PhotoImage(file="Images/buildings/constructions/Construction.gif")
            CONSTRUCTION_PHOTOS.append(self.photo)
            self.tag = "construction-%d" % id(self)
            OBJECTS[self.tag] = self
            self.HEALTH = 10
            self.Hmax = 10
            #specifics to construction
            self.typechosen = False
            self.newTYPE = ""
            self.ended = False

        if TYPE == "shrine":
            self.TYPE = 5  
            self.photo = PhotoImage(file="Images/buildings/shrines/Shrine.gif")
            SHRINE_PHOTOS.append(self.photo)
            self.tag = "shrine-%d" % id(self)
            OBJECTS[self.tag] = self
            self.HEALTH = 50
            self.Hmax = 50
            #specifics to shrine
            self.decline = False
            self.growing = True
            self.stage = 0
            self.cangivepower = True

            #photos
            PHOTOS = []
            self.mainphoto = self.photo
            self.decline4photo = PhotoImage(file="Images/buildings/shrines/Shrine_decline4.gif")
            self.decline3photo = PhotoImage(file="Images/buildings/shrines/Shrine_decline3.gif")
            self.decline2photo = PhotoImage(file="Images/buildings/shrines/Shrine_decline2.gif")
            self.decline1photo = PhotoImage(file="Images/buildings/shrines/Shrine_decline1.gif")
            self.evolve1photo = PhotoImage(file="Images/buildings/shrines/ShrineEvolve1.gif")
            self.evolve2photo = PhotoImage(file="Images/buildings/shrines/ShrineEvolve2.gif")
            self.evolve3photo = PhotoImage(file="Images/buildings/shrines/ShrineEvolve3.gif")
            PHOTOS.append(self.decline4photo)
            PHOTOS.append(self.decline3photo)
            PHOTOS.append(self.decline2photo)
            PHOTOS.append(self.decline1photo)
            PHOTOS.append(self.evolve1photo)
            PHOTOS.append(self.evolve2photo)
            PHOTOS.append(self.evolve3photo)  
                                            
        if TYPE == "farm":
            self.TYPE = 6
            self.photo = PhotoImage(file="Images/buildings/farms/Farm.gif")
            FARM_PHOTOS.append(self.photo)
            self.tag = "farm-%d" % id(self)
            OBJECTS[self.tag] = self
            self.HEALTH = 20
            self.Hmax = 20
            #specifics to farm
            self.crops = True
            self.decline = 0
                 
        else:
            del self
    #places avatar based upon constructor vars
    def DefineID(self):
        IDS = WORLD.find_all()
        #defines itself a unique id for checking for overlap
        SelfID = len(IDS)+1
        return SelfID
    
    def build(self, constructor):
        #Builds a building based upon a constructor.
        ccoords = WORLD.coords(constructor.avatar)
        #print(ccoords)
        x = ccoords[0]+20
        y = ccoords[1]
        self.x = x
        self.y = y
        self.x1 = x+20
        self.y2 = x+20
        self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tags=("building", self.tag))
        self.width = self.photo.width()
        self.height = self.photo.height()
        #print(self.homeland)
        #captures the building so we can detect collisions later
        BUILDINGS.append(self)
        self.LANDCHECK()

    def ConstructBuild(self, constructor):
        #adds constructions to CONSTRUCTIONS list to avoid choking up NPCS
        ccoords = WORLD.coords(constructor.avatar)
        #print(ccoords)
        x = ccoords[0]+50
        y = ccoords[1]
        self.x = x
        self.y = y
        self.x1 = x+20
        self.y2 = x+20
        self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tags=("building", self.tag))
        self.width = self.photo.width()
        self.height = self.photo.height()
        #print(self.homeland)
        #captures the building so we can detect collisions later
        CONSTRUCTIONS.append(self)
        self.LANDCHECK()

    def FromConstructionBuild(self, constructor):
        #Constructs the building right on top of the construction
        ccoords = WORLD.coords(constructor.avatar)
        #print(ccoords)
        
        if len(ccoords) == 0:
            pass
        elif len(ccoords) != 0:
            ccoords = WORLD.coords(constructor.avatar)
            if len(ccoords) == 0:
                WORLD.delete(constructor.avatar)
                del constructor
            else:
                #print("calcoords " + str(ccoords))

                x = ccoords[0]
                y = ccoords[1]
                self.x = x
                self.y = y
                self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tags=("building", self.tag))
                self.width = self.photo.width()
                self.height = self.photo.height()
                #print(self.homeland)
                #captures the building so we can detect collisions later
                BUILDINGS.append(self)
                self.LANDCHECK()

        #DELETES CONSTRUCTOR
        WORLD.delete(constructor.avatar)
        del constructor
        
        
    def spawn(self):
        #does a random spawn for the more randomly created buildings.
        x = random.randint(20, 480)
        y = random.randint(20, 480)
        self.avatar = WORLD.create_image(x, y, image=self.photo, tags=("building", self.tag))
        BUILDINGS.append(self)
        
    def LANDCHECK(self):
        #checks to see if the player is in the land that the object was built in.
        if LANDSCAPENUMS[LANDNUM] != self.homeland:
            WORLD.itemconfigure(self.avatar, state=HIDDEN)
        if LANDSCAPENUMS[LANDNUM] == self.homeland:
            WORLD.itemconfigure(self.avatar, state=NORMAL)
        #print("X1, Y1, X2, Y2: " + str(self.x) + " " + str(self.y) + " " + str(self.x+20) + " " + str(self.y+20))
        #print("PLAYER: " + str(WORLD.coords(self.constructor.avatar)))
        #print(str(self.tag) + " " + str(DetectCollision(self, self.constructor)))
        if DetectCollision(self, self.constructor):
            if "NPC" in self.constructor.tag:
                pass
            elif "construction" in self.constructor.tag:
                pass
            else:
                pass
                #print("BUILDING TOUCHING CONSTRUCTOR")
        else:
            pass
        if DetectCollision(self, player):
            pass
            #print("BUILDING TOUCHING PLAYER")
        else:
            pass

        #ONLY RUNS IF THE BUILDING IS GOING TO SPAWN ANYTHING
        self.SpawnFrom()

    def checkattack(self,attacker):
        #Activates the defense/attack function of the object.
        #Mostly just harms the object if needed to be called.
        if self.HEALTH <= 0:
            if self.TYPE == 2 and self.ended == False:
                self.burn = True
            else:
                self.ended = True
        else:
            self.HEALTH -= attacker.attack
            #print(self.HEALTH)

    def MakeEnemy(self, TYPE):
        e = Enemy(TYPE, self)
        e.LANDCHECK()
    
    def SpawnFrom(self):
        #Makes a garrison form a time loop that will continually spawn
        #enemies until destroyed. An enemy every: DEBUG 4000 ms
        if self.TYPE == 3:
            if self.MAXSPAWN > 0:
                try:
                    n1 = random.randint(0, 4)
                    n2 = random.randint(0, 4)
                    if n1 == n2:
                        WORLD.after(self.time, lambda: self.MakeEnemy("orc"))
                        self.MAXSPAWN -= 1
                    else:
                        pass
                except:
                    pass
            else:
                pass
        #Makes NPCS if it's a village that is spawns from.
        elif self.TYPE == 2 and self.ended == False:
            if self.burn == False:
                #makes the BUILDER NPC spawn randomly if all three numbers are the same.
                n1 = random.randint(0, 500)
                n2 = random.randint(0, 500)
                n3 = random.randint(0, 500)
                if n1 and n2 == n3:
                    if self.MAXSPAWNNPCS > 0:
                        try:
                            #print("NPCS COMING FROM: " + str(self.homeland))
                            BUILDER = NPC(self)
                            self.MAXSPAWNNPCS -= 1
                        except:
                            pass
                        
            elif self.burn == True and self.ended == False:
                #this is for when the village is burning. It's its sortof "last view"
                #rather than just disappearing.
                if self.stage == 0 and self.ended == False:
                    self.stage = 1
                    self.photo = PhotoImage(file="Images/buildings/villages/village_burn1.gif")
                    VILLAGE_PHOTOS.append(self.photo)
                    WORLD.itemconfigure(self.avatar, image=self.photo)
                    self.LANDCHECK()
                
                if self.stage == 1 and self.ended == False:
                    #keeps stage changes random so time goes inbetween changes
                    n1 = random.randint(0, 5)
                    n2 = random.randint(0, 5)
                    if n1 == n2 and self.ended == False:
                        self.stage = 2
                        self.photo = PhotoImage(file="Images/buildings/villages/village_burn2.gif")
                        VILLAGE_PHOTOS.append(self.photo)
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                        self.LANDCHECK()
                elif self.stage == 2 and self.ended == False:
                    #keeps stage changes random so time goes inbetween changes
                    n1 = random.randint(0, 5)
                    n2 = random.randint(0, 5)
                    if n1 == n2 and self.ended == False:
                        self.stage = 3
                        self.photo = PhotoImage(file="Images/buildings/villages/village_burn3.gif")
                        VILLAGE_PHOTOS.append(self.photo)
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                        self.LANDCHECK()
                elif self.stage == 3 and self.ended == False:
                    #keeps stage changes random so time goes inbetween changes
                    n1 = random.randint(0, 5)
                    n2 = random.randint(0, 5)
                    if n1 == n2 and self.ended == False:
                        self.stage = 4
                        self.photo = PhotoImage(file="Images/buildings/villages/village_burn4.gif")
                        VILLAGE_PHOTOS.append(self.photo)
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                        self.LANDCHECK()
                elif self.stage == 4 and self.ended == False:
                    #keeps stage changes random so time goes inbetween changes
                    n1 = random.randint(0, 5)
                    n2 = random.randint(0, 5)
                    if n1 == n2 and self.ended == False:
                        self.ended = True
                        
                    
        #Makes constructions build whatever they are going to be.
        elif self.TYPE == 4 and self.ended == False:
            if self.ended == False:
                if self.typechosen == False and self.ended == False:
                    nFarm1 = random.randint(0, 50)
                    nFarm2 = random.randint(0, 50)
                    nVillage1 = random.randint(0, 100)
                    nVillage2 = random.randint(0, 100)
                    nShrine1 = random.randint(0, 200)
                    nShrine2 = random.randint(0, 200)

                    if nShrine1 == nShrine2 and self.ended == False:
                        #shrine is first because they get built more rarely, and if
                        #the chances are just right, they will get built                        
                        #print("Shrine Building " + str(self.homeland))
                        self.photo = PhotoImage(file="Images/buildings/constructions/ShrineConstruction2.gif")
                        CONSTRUCTION_PHOTOS.append(self.photo)
                        self.typechosen = True
                        self.newTYPE = "shrine"
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                        self.LANDCHECK()
                        
                    elif nVillage1 == nVillage2 and self.ended == False:
                        #the village is next, because it is also kinda rare
                        #print("Village Building " + str(self.homeland))
                        self.photo = PhotoImage(file="Images/buildings/constructions/ConstructionVillage2.gif")
                        CONSTRUCTION_PHOTOS.append(self.photo)
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                        self.typechosen = True
                        self.newTYPE = "village"
                        self.LANDCHECK()
                        
                    elif nFarm1 == nFarm2 and self.ended == False:
                        #the farm is next because it is the most common
                        #print("Farm Building " + str(self.homeland))
                        self.photo = PhotoImage(file="Images/buildings/constructions/ConstructionFarm2.gif")
                        CONSTRUCTION_PHOTOS.append(self.photo)
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                        self.typechosen = True
                        self.newTYPE = "farm"
                        self.LANDCHECK()
                        
                    else:
                        pass
                if self.typechosen == True and self.ended == False:
                    #Tier TWO - Construction Update
                    if self.newTYPE == "shrine" and self.ended == False:
                        n1 = random.randint(0, 5)
                        n2 = random.randint(0, 5)

                        if n1 == n2 and self.ended == False:
                            #print("MAKE BUILD")
                            makeBuilding("shrine", self)
                            try:
                                CONSTRUCTION_PHOTOS.remove(self.photo)
                            except:
                                pass
                            self.LANDCHECK()
                            self.ended = True
                            #print("MAKE BUILD")
                        else:
                            #print("NOT MAKING BUILDINGS")
                            self.LANDCHECK()
                            
                    elif self.newTYPE == "village" and self.ended == False:
                        n1 = random.randint(0, 5)
                        n2 = random.randint(0, 5)

                        if n1 == n2 and self.ended == False:
                            makeBuilding("village", self)
                            try:
                                CONSTRUCTION_PHOTOS.remove(self.photo)
                            except:
                                pass
                            self.LANDCHECK()
                            self.ended = True
                        else:
                            self.LANDCHECK()
                            
                    elif self.newTYPE == "farm" and self.ended == False:
                        n1 = random.randint(0, 5)
                        n2 = random.randint(0, 5)

                        if n1 == n2 and self.ended == False:
                            makeBuilding("farm", self)
                            try:
                                CONSTRUCTION_PHOTOS.remove(self.photo)
                            except:
                                pass
                            self.LANDCHECK()
                            self.ended = True
                        else:
                            self.LANDCHECK()
                            
        elif self.TYPE == 6 and self.ended == False:
            if self.crops == False and self.ended == False:
                #if farms' crops are used up, the farm will go into steady
                #decline till it dies.
                #the decline variable is basically the stage. At 0 it is just a farm
                if self.decline == 0:
                    n1 = random.randint(0, 10)
                    n2 = random.randint(0, 10)
                    if n1 == n2:
                        self.decline = 1
                        self.photo = PhotoImage(file="Images/buildings/farms/Farm_decline1.gif")
                        FARM_PHOTOS.append(self.photo)
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                if self.decline == 1:
                    n1 = random.randint(0, 10)
                    n2 = random.randint(0, 10)
                    if n1 == n2:
                        self.decline = 2
                        self.photo = PhotoImage(file="Images/buildings/farms/Farm_decline2.gif")
                        FARM_PHOTOS.append(self.photo)
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                if self.decline == 2:
                    n1 = random.randint(0, 10)
                    n2 = random.randint(0, 10)
                    if n1 == n2:
                        self.decline = 3
                        self.photo = PhotoImage(file="Images/buildings/farms/Farm_decline3.gif")
                        FARM_PHOTOS.append(self.photo)
                        WORLD.itemconfigure(self.avatar, image=self.photo)
                if self.decline == 3:
                    n1 = random.randint(0, 10)
                    n2 = random.randint(0, 10)
                    if n1 == n2:
                        self.ended == True
                        WORLD.delete(self.avatar)
                        try:
                            BUILDINGS.remove(self)
                        except:
                            pass
                        del self

        elif self.TYPE == 5 and self.ended == False:

##            print("shrine funcs: " + str(self.homeland) + "----+")
##            print("shrine growing: " + str(self.growing))
##            print("shrine declining: " + str(self.decline))
            
            if self.decline == True and self.growing == False and self.ended == False:
                #The decline mechnanism is much rarer than the
                #growing mechanism
                n1 = random.randint(0, 40)
                n2 = random.randint(0, 40)
                n3 = random.randint(0, 40)
                n4 = random.randint(0, 40)
                
                ONE = True
                TWO = False
                if n1 == n2 and self.ended == False:
                    ONE = False
                if n3 == n4 and self.ended == False:
                    TWO = True            
                if ONE == TWO and self.ended == False:
                    change = 5
##                    print("SHRINE CHANGING "+ str(self.homeland))
##                    print(self.stage)
##                    print(self.growing)
                    #Based upon the stage the shrine is at
                    if self.stage == -5:
                        self.ended = True
                        
                    elif self.stage == -4:
                        WORLD.itemconfigure(self.avatar, image=self.decline4photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = -5
                        self.LANDCHECK()
                        
                    elif self.stage == -3:
                        WORLD.itemconfigure(self.avatar, image=self.decline3photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = -4
                        self.LANDCHECK()
                        
                    elif self.stage == -2:
                        WORLD.itemconfigure(self.avatar, image=self.decline2photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = -3
                        self.LANDCHECK()
                        
                    elif self.stage == -1:
                        WORLD.itemconfigure(self.avatar, image=self.decline1photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = -2
                            self.cangivepower = False
                        self.LANDCHECK()
                        
                    elif self.stage == 0:
                        WORLD.itemconfigure(self.avatar, image=self.mainphoto)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = -1
                        self.LANDCHECK()

                    elif self.stage == 1:
                        WORLD.itemconfigure(self.avatar, image=self.evolve1photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = 0
                        self.LANDCHECK()
                        
                    elif self.stage == 2:
                        WORLD.itemconfigure(self.avatar, image=self.evolve2photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = 1
                        self.LANDCHECK()
                        
                    elif self.stage == 3:
                        WORLD.itemconfigure(self.avatar, image=self.evolve3photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = 2
                        self.LANDCHECK()

                                                    
            elif self.growing == True and self.decline == False and self.ended == False:
                n1 = random.randint(0, 40)
                n2 = random.randint(0, 40)
                n3 = random.randint(0, 40)
                n4 = random.randint(0, 40)
                ONE = True
                TWO = False
                if n1 == n2 and self.ended == False:
                    ONE = False
                if n3 == n4 and self.ended == False:
                    TWO = True            
                if ONE == TWO and self.ended == False:
                    
                    change = 5
                    
                    if self.stage == -4:
                        WORLD.itemconfigure(self.avatar, image=self.decline4photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = -3
                        self.LANDCHECK()
                        
                    elif self.stage == -3:
                        WORLD.itemconfigure(self.avatar, image=self.decline3photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = -2
                        self.LANDCHECK()
                        
                    elif self.stage == -2:
                        WORLD.itemconfigure(self.avatar, image=self.decline2photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = -1
                        self.LANDCHECK()
                        
                    elif self.stage == -1:
                        WORLD.itemconfigure(self.avatar, image=self.decline1photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = 0
                        self.LANDCHECK()
                        
                    elif self.stage == 0:
                        WORLD.itemconfigure(self.avatar, image=self.mainphoto)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = 1
                        self.LANDCHECK()
                        
                    elif self.stage == 1:
                        WORLD.itemconfigure(self.avatar, image=self.evolve1photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = 2
                        self.LANDCHECK()
                        
                    elif self.stage == 2:
                        WORLD.itemconfigure(self.avatar, image=self.evolve2photo)
                        n1 = random.randint(0, change)
                        n2 = random.randint(0, change)
                        if n1 == n2:
                            self.stage = 3
                        self.LANDCHECK()
                        
                    elif self.stage == 3:
                        WORLD.itemconfigure(self.avatar, image=self.evolve3photo)
                        self.growing = False
                        self.decline = True
                        self.cangivepower = True
                        self.LANDCHECK()

                                  
        elif self.ended == True:
                WORLD.delete(self.avatar)
                try:
                    BUILDINGS.remove(self)
                except:
                    pass
                del self
                    
        else:
            self.ended == True
            
    #--Farm specific functions
    def FarmAddPlayerHealth(self):
        if self.crops == True:
            #adds one health to player if the farm's crops aren't used
            player.addhealth(1)
            self.photo = PhotoImage(file="Images/buildings/farms/Farm_used.gif")
            FARM_PHOTOS.append(self.photo)
            WORLD.itemconfigure(self.avatar, image=self.photo)
            #then says the crops are used up so that they can't be used again.
            self.crops = False
        else:
            pass

    #--Shrine specific functions
    def ShrineRENEW(self):
        self.growing = True
        self.decline = False
        
        
#PROJECTILE CLASS:
class Projectile():
    
    def __init__(self, orgin, color, speed):
        self.orgin = orgin
        #grabs direction of orgin objects
        self.direction = orgin.direct
        self.color = color
        self.speed = speed
        self.ID = self.DefineID()
        self.tag = "Proj-%d" % id(self)
        OBJECTS[self.tag] = self
        #sets homeland to the homeland of the orgin object
        #The "firer"
        self.homeland = self.orgin.homeland
        self.DEAD = False
        #Collision is automatically false
        self.collision = False
        #self.player var. To find if the object is made by the player
        #self.enemy var. To find if the object is made by an enemy
        self.player = False
        self.enemy = False
        self.NPC = False
        
        #attack variable. The amount of damage a projectile inflicts
        #Making a attack variable based upon the player or enemy's strength
        #Universalizes the variable to an "attack" variable rather than a "power" variable specific to the player.
        if "player" == self.orgin.tag:
            self.attack = self.orgin.power
            self.player = True
            self.draw()
        elif "E" in self.orgin.tag:
            self.attack = self.orgin.attack
            self.enemy = True
            self.Edraw()
        elif "NPC" in self.orgin.tag:
            #save for later
            pass
        
    def DefineID(self):
        IDS = WORLD.find_all()
        #defines itself a unique id for checking for overlap
        SelfID = len(IDS)+1
        return SelfID

    def Edraw(self):
        COORDS = WORLD.coords(self.orgin.avatar)
        #FOR ENEMIES. They run with IMAGE avatars, which only have x and y
        #So we need to build the x2 and y2 from x1 and y1

        if self.direction == "R":
            self.x1 = COORDS[0] + 10
            self.y1 = COORDS[1]
            
        if self.direction == "L":
            self.x1 = COORDS[0] - 10
            self.y1 = COORDS[1]
            
        if self.direction == "U":
            self.x1 = COORDS[0]
            self.y1 = COORDS[1] - 10
            
        if self.direction == "D":
            self.x1 = COORDS[0]
            self.y1 = COORDS[1] + 10

        self.x2 = self.x1 + 10
        self.y2 = self.y1 + 10
        self.avatar = WORLD.create_rectangle(self.x1, self.y1, self.x2, self.y2)
        PROJECTILES.append(self)
        self.FIRE()
    
    def draw(self):
        COORDS = WORLD.coords(self.orgin.avatar)
        #places the projectile in the direction the
        #firer moved last
        
        if self.direction == "R":
            
            self.x1 = COORDS[0] + 10
            self.y1 = COORDS[1]
            self.x2 = COORDS[2] + 10
            self.y2 = COORDS[3]
            
        if self.direction == "L":

            self.x1 = COORDS[0] - 10
            self.y1 = COORDS[1]
            self.x2 = COORDS[2] - 10
            self.y2 = COORDS[3]
            
        if self.direction == "U":

            self.x1 = COORDS[0]
            self.y1 = COORDS[1] - 10 
            self.x2 = COORDS[2]
            self.y2 = COORDS[3] - 10
            
        if self.direction == "D":

            self.x1 = COORDS[0]
            self.y1 = COORDS[1] + 10
            self.x2 = COORDS[2]
            self.y2 = COORDS[3] + 10

        self.avatar = WORLD.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=str(self.color))
        PROJECTILES.append(self)
        #and then moves the projectile along
        #starts the loop of it moving and checking.
        self.FIRE()
        
    def FIRE(self):
        #checks the self.DEAD variable. It's important to kill itself if
        #it's not in the right place
        self.LANDCHECK()
        
        if self.DEAD == True:
            self.implode()
        else:
                #moves itself based upon the direction it was fired in.
                if self.direction == "R":
                    WORLD.move(self.avatar, self.speed, 0)
                    self.LANDCHECK()
                if self.direction == "L":
                    WORLD.move(self.avatar, -self.speed, 0)
                    self.LANDCHECK()
                if self.direction == "D":
                    WORLD.move(self.avatar, 0, self.speed)
                    self.LANDCHECK()
                if self.direction == "U":
                    WORLD.move(self.avatar, 0, -self.speed)
                    self.LANDCHECK()

                #The lambda after program makes the loop go and not
                #interrupt the gameflow.

                WORLD.after(1000, lambda: self.checkhit())
                #LANDCHECK in the form of checkhit
                
    def checkhit(self):    
        #checks every time it moves for enemies/walls
        for x in range(0, len(ENEMIES)):
            if DetectCollision(self, ENEMIES[x]):
                #print("TOUCHING ENEMY")
                if self.enemy == True:
                    pass
                else:
                    self.collision = True
                
        for y in range(0, len(BUILDINGS)):
            if DetectCollision(self, BUILDINGS[y]):
                self.collision = True
                BUILDINGS[y].checkattack(self)
                self.DEAD = True

        for j in range(0, len(NPCS)):
            if DetectCollision(self, NPCS[j]):
                print("TOUCHING NPC")
                if self.NPC == True:
                    pass
                else:
                    self.collision = True

        #checks for the self.DEAD variable, deciding if it's dead.
        if self.DEAD == True:
            self.implode()

        if self.collision == False:
            #ALSO CODE FOR MOVING THROUGH LANDS -- KEEP HANDY FOR NEW UPDATES
            #uses the FindNewCoords function to redefine the x and y values
            #makes it more functional and having the ability to CHANGE
            #the values now adapt.
            x1 = self.FindNewCoords("x")
            y1 = self.FindNewCoords("y")

            #in case the FindNewCoords function returns none:
            if x1 == None:
                x1 = -20
            if y1 == None:
                y1 = -20
                
            #checks to see if the projectile has left the land it was in,
            

            #CURRENT CODE LIMITS PROJECTILES TO ONE SECTION
                    #Commented code is for allowing the projectile to move to
                    #different lands
            
            if x1 >= 520:
                #print("X520")
                self.implode()

            #CURRENT CODE LIMITS PROJECTILES TO ONE SECTION
                    #Commented code is for allowing the projectile to move to
                    #different lands
                    
            if x1 <= -20:
                #print("X-20")
                self.implode()

            #This code makes it so the projectile destroys itself if it
            #goes up too far to the upper regions of the map
            #or the lower regions
            if y1 >= 520:
                #print("DEADy1520")
                self.DEAD = True
                self.implode()


            if y1 <= -20:
                #print("DEADy1-20")
                self.DEAD = True
                self.implode()
                
            else:
                self.FIRE()
                
        if self.collision == True:
            pass

    def LANDCHECK(self):
        #Basic Landcheck
        #the try expression keeps the errors away, because
        #of when the avatar gets deleted so often in the code above:
        
            if LANDSCAPENUMS[LANDNUM] != self.homeland:
                WORLD.itemconfigure(self.avatar, state=HIDDEN)
            if LANDSCAPENUMS[LANDNUM] == self.homeland:
                WORLD.itemconfigure(self.avatar, state=NORMAL)

    def implode(self):
        WORLD.delete(self.avatar)
        #checks to see if the player made it. If so, it adds the projectile back
        #to potential projectiles of the player. Capping the player's projectile
        #number starts at 15
        if self.player == True:
            if self.orgin.Num_Of_Projectiles > 15:
                pass
            else:
                self.orgin.Num_Of_Projectiles += 1
        else:
            pass
        del self
        try:
            PROJECTILES.remove(self)
        except:
            pass

    def FindNewCoords(self, var):
        #use this function to redefine the coords in use
        #So the other functions function.
        C = WORLD.coords(self.avatar)
        if C == []:
            pass
        else:
            if var == "x":
                return C[0]
            if var == "y":
                return C[1]

#---------------------------
#Village NPCS MAIN class
class NPC():
    def __init__(self, homevillage):
        self.homevillage = homevillage
        
        #since the NPC starts out randomly as a NORMAL NPC (No class)
        self.photo = PhotoImage(file="Images/NPC/NPC.gif")
        NPC_PHOTOS.append(self.photo)
        self.tag = "NPC-%d" % id(self)
        OBJECTS[self.tag] = self
        self.homeland = self.homevillage.homeland
        self.type = 0
        self.speed = 5

        #Life functions
        self.DEAD = False

        #interaction functions - landn, collision
        self.collision = False
        self.direction = "R"
        self.moves = 10
        #--Elder variable
        self.elder = False

        #NPC CLASS VARS - specific to class. Only called upon if it is a class
        self.maxbuild = 1

        #NPC CLASS REGULATION VARS
        self.CLASSESBEEN = []
        
        #building x and y coords (randomly based upon the homevillage)
        #either above, below, or to the left or the right
        C = WORLD.coords(self.homevillage.avatar)
        n1 = random.randint(0, 3)
        if n1 == 0:
            self.x = C[0] + 30
            self.y = C[1]
        elif n1 == 1:
            self.x = C[0] - 30
            self.y = C[1]
        elif n1 == 2:
            self.x = C[0]
            self.y = C[1] + 30
        elif n1 == 3:
            self.x = C[0]
            self.y = C[1] - 30

        #NPC HEALTH and POWER variables
        self.health = 10
        self.power = 1

        self.draw()

    def draw(self):
        self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tag=("NPC", self.tag))
        NPCS.append(self)
        self.RUN()
        
    def DefineID(self):
        IDS = WORLD.find_all()
        #defines itself a unique id for checking for overlap
        SelfID = len(IDS)+1
        return SelfID

    def LANDCHECK(self):
        #Basic Landcheck
        #the try expression keeps the errors away, because
        #of when the avatar gets deleted so often in the code above:

        #print("LANDCHECKING: " + str(LANDSCAPENUMS[LANDNUM]) + " " + str(self.homeland))
        
        if LANDSCAPENUMS[LANDNUM] != self.homeland:
            WORLD.itemconfigure(self.avatar, state=HIDDEN)
        if LANDSCAPENUMS[LANDNUM] == self.homeland:
            WORLD.itemconfigure(self.avatar, state=NORMAL)

    def CLASSACTIONS(self):
        self.LANDCHECK()

        #PreMovement FUNCTIONS - control things like class definement
        #Anything not to do with Movement.

        #randomly becomes Builder NPC
        numB1 = random.randint(0, 5)
        numB2 = random.randint(0, 5)

        #if statement below to turn a NORMAL NPC into either a
        #Builder NPC
        #Normal NPC again

        if self.type != 0 and self.elder == False:
            self.LANDCHECK()
            #If an BUILDER NPC cannot build anymore buildings, it becomes an normal NPC
            if self.type == 1 and self.MAXSPAWN <= 0:
                self.type = 0
                self.photo = PhotoImage(file="Images/NPC/NPC.gif")
                C = WORLD.coords(self.avatar)
                self.x = C[0]
                self.y = C[1]
                WORLD.delete(self.avatar)
                self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tag=("NPC", self.tag))
            
             
        if self.type == 0 and self.elder == False:
            self.LANDCHECK()
            #normal NPCS can become BUILDER NPCS
            if numB1 == numB2 and "builder" not in self.CLASSESBEEN:
                self.type = 1
                self.photo = PhotoImage(file="Images/NPC/BuilderNPC.gif")
                C = WORLD.coords(self.avatar)
                self.x = C[0]
                self.y = C[1]
                WORLD.delete(self.avatar)
                self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tag=("NPC", self.tag))
                self.MAXSPAWN = 2
                self.CLASSESBEEN.append("builder")
                
            if len(self.CLASSESBEEN) >= 3:
                self.LANDCHECK()
                #If the number of classes the Normal NPC has been exceeds 3:
                #It will indefinitely become an Elder NPC
                self.type = 2
                self.photo = PhotoImage(file="Images/NPC/Elder_NPC_Design_1.gif")
                C = WORLD.coords(self.avatar)
                self.x = C[0]
                self.y = C[1]
                WORLD.delete(self.avatar)
                self.avatar = WORLD.create_image(self.x, self.y, image=self.photo, tag=("NPC", self.tag))
                #This variable makes the NPC unable to change classes again.
                self.elder = True
                     

        #--NPC TYPE SPECIALTY FUNCTIONS---Based on class
        if self.type == 0:
            #NORMAL NPC, so pass
            self.LANDCHECK()
        elif self.type == 1:
            #BUILDER NPC ---can build:
            #Constructions (they can randomly become a shrine or farm)
            numC1 = random.randint(0, 50)
            numC2 = random.randint(0, 50)

            self.LANDCHECK()

            if numC1 == numC2:
                if self.MAXSPAWN <= 0:
                    #returns the NPC to a normal NPC status
                    self.type = 0
                    #print("returning to normal NPC")
                else:
                    #to keep the NPCs building within a precise square
                    C = WORLD.coords(self.avatar)
                    x = C[0]
                    y = C[1]
                    if x <= 450 and x >= 50 and y <= 450 and y >= 50:
                        Construct = Building("construction", self, self.homeland)
                        Construct.ConstructBuild(self)
                        self.MAXSPAWN -= 1


    def RUN(self):
        self.CLASSACTIONS()
        
        if self.DEAD == True:
            WORLD.delete(self.avatar)
            try:
                NPCS.remove(self)
            except:
                pass
            del self
        else:

            #COLLISION DETECTION FOR PROJECTILES AND ENEMIES AND PLAYER:
            #detecting collisions with projectiles
            for x in range(0, len(PROJECTILES)):
                if DetectCollision(self, PROJECTILES[x]):
                    self.collision = True
                    #This code compares the power of a projectile to it's health
                    #and subtracts health from itself based upon that.
                    if PROJECTILES[x].NPC == True:
                        pass
                    else:
                        if self.health <= 0:
                            PROJECTILES[x].implode()
                            self.DIE()
                        else:
                            self.health -= PROJECTILES[x].attack
                            PROJECTILES[x].implode()

            if DetectCollision(self, player):
                    #checks if the NPC is touching the player
                    print("NPC TOUCHING PLAYER")
                    self.collision = True

            for x in range(0, len(CONSTRUCTIONS)):
                CONSTRUCTIONS[x].LANDCHECK()

            #MOVEMENT FUNCTIONS
            #NPCS can travel lands just like Enemies and the player.
            NPCLands = {}
            #builds a little map of which it can dictate where it is in
            #relation to the player.
            for x in range(0, len(LANDSCAPENUMS)):
                NPCLands[x] = LANDSCAPENUMS[x]

            self.landn = 0

            for y in range(0, len(NPCLands)-1):
                if self.homeland == NPCLands[y]:
                    self.landn = y
                else:
                    pass
                
            Coordinates = WORLD.coords(self.avatar)
            x1 = self.FindNewCoords("x")
            y1 = self.FindNewCoords("y")

            #collision detection
            for x in range(0, len(BUILDINGS)):
                if DetectCollision(self, BUILDINGS[x]):
                    self.collision = True

            for x in range(0, len(PROJECTILES)):
                if DetectCollision(self, PROJECTILES[x]):
                    self.collision = True
                    #This code compares the power of a projectile to it's health
                    #and subtracts health from itself based upon that.
                    if self.health <= 0:
                        PROJECTILES[x].implode()
                        self.DIE()
                    else:
                        self.health -= PROJECTILES[x].attack
                        PROJECTILES[x].implode()

            #checks to see if the NPC hasn't touched anything.
            if self.collision == False:

                #checking for NPC to be either to the left or to the right
                #or up or down.
                if x1 >= 520:
                    if self.landn == len(LANDSCAPENUMS)-1:
                        WORLD.move(self.avatar, -self.speed, 0)
                        self.landn = 0
                        
                    if self.landn != len(LANDSCAPENUMS)-1:
                        #moves it to the next land on the right.
                        self.landn += 1
                        self.homeland = NPCLands[self.landn]
                        WORLD.delete(self.avatar)
                        self.avatar = WORLD.create_image(20, self.y, image=self.photo, tags=("NPC", self.tag))
                        self.LANDCHECK()
                
                if x1 <= -20:
                    if self.landn == 0:
                        #NPC returns to Fly you Fools, after going -20 X Fields.
                        self.landn = 14
                        self.homeland = NPCLands[self.landn]
##                        print(self.homeland)
##                        print(self.landn)
                        WORLD.delete(self.avatar)
                        #randomly places the NPC somewhere on the y axis
                        self.y = random.randint(40, 360)
                        self.avatar = WORLD.create_image(470, self.y, image=self.photo, tags=("NPC", self.tag))
                        self.LANDCHECK()
                        
                    if self.landn != 0:
                        #moves it to the next land on the left.
                        self.landn -= 1
                        self.homeland = NPCLands[self.landn]
                        WORLD.delete(self.avatar)
                        self.avatar = WORLD.create_image(470, self.y, image=self.photo, tags=("NPC", self.tag))
                        self.LANDCHECK()     
                
                if y1 >= 520:
                    #if the NPC goes off the map in the up or down directions:
                    self.x = self.FindNewCoords("x")
                    WORLD.delete(self.avatar)
                    self.avatar = WORLD.create_image(self.x, 10, image=self.photo, tags=("NPC", self.tag))
                    self.LANDCHECK()
                
                if y1 <= -20:
                    self.x = self.FindNewCoords("x")
                    WORLD.delete(self.avatar)
                    self.avatar = WORLD.create_image(self.x, 490, image=self.photo, tags=("NPC", self.tag))
                    self.LANDCHECK()

                else:
                    #moves the NPC around
                    if self.moves > 0:
                        C = WORLD.coords(self.avatar)
                        #number of times the NPC can move in a certain direction
                        if self.direction == "R":
                            WORLD.move(self.avatar, self.speed, 0)
                            self.moves -= 1
                        if self.direction == "L":
                            WORLD.move(self.avatar, -self.speed, 0)
                            self.moves -= 1
                        if self.direction == "U":
                            WORLD.move(self.avatar, 0, -self.speed)
                            self.moves -= 1
                        if self.direction == "D":
                            WORLD.move(self.avatar, 0, self.speed)
                            self.moves -= 1
                        
                    elif self.moves <= 0:
                        #if self.moves == 0, then it randomly picks a new direction and resets
                        #self.moves
                        n = random.randint(0, 3)
                        if n == 0:
                            self.direction = "R"
                            self.moves = 10
                        if n == 1:
                            self.direction = "L"
                            self.moves = 10
                        if n == 2:
                            self.direction = "U"
                            self.moves = 10
                        if n == 3:
                            self.direction = "D"
                            self.moves = 10

                    
        #if the NPC is touching something
            elif self.collision == True:
                #checks buildings again for collision and gets around them.
                for x in range(0, len(BUILDINGS)):
                    if DetectCollision(self, BUILDINGS[x]):
                    
                        TRIES = 0
                    
                        #moves around villages, or garrisons, or walls
                        #or shrines
                        if BUILDINGS[x].TYPE == 2 or BUILDINGS[x].TYPE == 3 or BUILDINGS[x].TYPE == 5:

                            if TRIES >= 20:
                                print("NOT MOVING. OBSTACLE IN THE WAY")
                                WORLD.after(4000)
                                TRIES = 0
                            else:
                                #if the NPC tries to get around a building 20 times
                                #it will turn around and go the opposite direction
                                xoy = random.randint(1, 2)
                                if xoy == 1:
                                    WORLD.move(self.avatar, 0, -self.speed)
                                    TRIES += 1
                                if xoy == 2:
                                    WORLD.move(self.avatar, 0, self.speed)
                                    TRIES += 1
                        else:
                        
                            self.collision = False
                    else:
                        self.collision = False
                self.collison = False
            

    def DIE(self):
        WORLD.delete(self.avatar)
        try:
            NPCS.remove(self)
            NPC_PHOTOS.remove(self.photo)
        except:
            pass
        del self

    def FindNewCoords(self, var):
        #use this function to redefine the coords in use
        #So the other functions function.
        C = WORLD.coords(self.avatar)
        if C == []:
            pass
        else:
            if var == "x":
                return C[0]
            if var == "y":
                return C[1]
        

#Defining Operating Objects
player = Player(10, 1, 10, 15)

#Player Specific Objects (Health bar, etc)
PlayerHealthDisplay = WORLD.create_rectangle(0, 0, 60, 30, fill="grey")
HealthBar = WORLD.create_text(30, 20, text="HP: " + str(player.health), fill="blue")

PlayerPowerDisplay = WORLD.create_rectangle(500, 0, 440, 30, fill="black")
PowerBar = WORLD.create_text(470, 20, text="PW: " + str(player.power), fill="red")

#WORLD-Building operations
SpawnVillages()

#ENEMY SPAWNING
WORLD.after(500, SpawnEnemies)

WORLD.bind_all("<KeyPress-Right>", player.move)
WORLD.bind_all("<KeyPress-Left>", player.move)
WORLD.bind_all("<KeyPress-Up>", player.move)
WORLD.bind_all("<KeyPress-Down>", player.move)
WORLD.bind_all("x", player.attack)
WORLD.bind_all("c", player.attack)
WORLD.bind_all("z", player.attack)
WORLD.bind_all("w", player.build_wall)
WORLD.bind_all("v", player.attack)
WORLD.bind_all("e", player.attack)
WORLD.bind_all("q", player.attack)

while True:
    try:
        root.mainloop()
        WORLD.update()
        WORLD.after(EnemyWaveSecs, lambda: SpawnEnemies)
        EnemyWaveSecs += 31.25
    except:
        pass

