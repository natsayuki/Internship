# IMPORTS
import pygame
import random
from random import randint
import math
import PyCon
import time
import Adafruit_PN532 as PN532
import json
import binascii
import os

# INIT
pygame.init()
width = 320
height = 240
s = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Internship")

# CLASSES
class base_sprite(pygame.sprite.Sprite):
        def __init__(self, color=(0,0,0), width=0, height=0, image=None,x=0,y=0, scale=None, surface=False):
            pygame.sprite.Sprite.__init__(self)
            if "Surface" in type(image).__name__ or surface:
                self.image = image
            else:
                self.image = pygame.image.load(image)
            if scale != None:
                self.image = pygame.transform.scale(self.image, (scale[0], scale[1]))
            pygame.draw.rect(self.image, color, [5000000,5000000,width,height])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        def blit(self, screen):
            self.image.blit(self.image, screen)

class text(pygame.sprite.Sprite):
        def __init__(self, text, x, y, font_path="Comic Sans MS", font_size=26, font_colour=(0, 0, 0), opacity=255,background=None):
                pygame.sprite.Sprite.__init__(self)
                self.font = pygame.font.SysFont(font_path, font_size)
                self.color = font_colour
                self.render_text = text
                self.rerender(x,y,opacity,background)
                self.pos = y
                self.text = text
                self.opacity = opacity
                self.background = background
        def update(self):
                pass
        def print_text(self, text_string, x, y):
                self.render_text = text_string
                self.rerender(x,y,self.opacity,self.background)
        def rerender(self, x, y, opacity=255,background=None, center=False):
                self.image = self.font.render(self.render_text, 0, self.color,background)
                self.image.set_alpha(opacity)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                if(center):
                    self.rect.x = (width/2)-(self.rect.width/2)
class enemy():
    def __init__(self, name, health, attack, speed, magic, range, level, weakness):
        self.name = name
        self.health = health
        self.attack = attack
        self.speed = speed
        self.magic = magic
        self.range = range
        self.level = level
        self.weakness = weakness
class item():
    def __init__(self, name, health, attack, speed, magic, range, level, itemClass, type, style, gap=4):
        self.name = name
        self.health = health
        self.attack = attack
        self.speed = speed
        self.magic = magic
        self.range = range
        self.level = level
        self.itemClass = itemClass
        self.type = type
        self.style = style
        self.gap = gap
class boss():
    def __init__(self, name, health, attack, speed, magic, range):
        self.name = name
        self.health = health
        self.attack = attack
        self.speed = speed
        self.magic = magic
        self.range = range


# INIT VARS
running = True
inHome = True
inLoad = False
inName = False
inNameConfirm = False
inCharacterGen = False
inCharacterGen1 = False
inCharacterGen2 = False
inCharacterGenEnd = False
inGame = False
genNewFloor = True
floorLevel = 1
inMap = False
miniMap = []
newMap = True
inCon = False
inInventory = False
inWait = False
newInventory = True
inSpell = False
inHead = False
inBody = False
inHand = False
inFeet = False
newSub = True
inSub = False
inFight = False
inDead = False
subFloor = False
inSwap = False
newSwap = False
treasureClicked = False
XPBonus = True
inInspect = False
inBoss = False
bossTurn = True
newPhase = True
bossNewTurn = True
inBossEnd = False
hitTimer = 0
newTurn = True
wait = 0
newRead = True
inFigureLoad = False
inBetween = False
inSave = False
newLoad = True


enemySprite = base_sprite(width=0, height=0, image="images/enemies/Devil.png", x=(width/2) - 40, y=(height/2) - 40)
stairsSprite = base_sprite(width=80, height=80, image="images/stairs.png", x=(width/2) - 40, y=(height/2) - 40)
chestSprite = base_sprite(width=80, height=80, image="images/treasure.png", x=(width/2) - 40, y=(height/2) - 40)


spells = ['BasicBook']
head = ['BasicHat']
body = ['BasicShirt']
hand = ['BasicThingToHitPeopleWith']
feet = ['BasicShoes']

spellsEq = 'BasicBook'
headEq = 'BasicHat'
bodyEq = 'BasicShirt'
handEq = 'BasicThingToHitPeopleWith'
feetEq = 'BasicShoes'

enemyEncountered = None
bossEncountered = "Smolk"
bossHealth = 150
bossAttack = 10
bossMaxHealth = 150

subSprites = None

delay = 0
delayAction = ''

stairs = None

classPicked = ''
actionsToRun = []
swapSprites = []

#name, health, attack, speed, magic, range, level, weakness
enemies = {'Devil': enemy("Devil", 30, 3, 5, 0, 0, 3, 'Range'), 'Ghost': enemy("Ghost", 30, 3, 3, 5, 3, 3, "Magic"), 'Goblin': enemy("Goblin", 15, 5, 7, 0, 0, 4, "Melee"),
"Alligator": enemy("Alligator", 150, 25, 25, 0, 0, 35, "Range"), "Bat": enemy("Bat", 60, 5, 15, 15, 5, 15, "Melee"), "Bear": enemy("Bear", 125, 30, 25, 0, 10, 40, "Magic"),
 "Bird": enemy("Bird", 40, 5, 15, 0, 5, 10, "Range"), "Bomb": enemy("Bomb", 45, 20, 10, 10, 0, 25, "Magic"), "Dino": enemy("Dino", 300, 75, 50, 0, 0, 85, "Range"),
 'Frog': enemy("Frog", 70, 15, 25, 25, 0, 35, "Melee"), "Horse": enemy("Horse", 150, 50, 50, 0, 0, 65, "Melee"), 'Jellyfish': enemy("Jellyfish", 50, 10, 5, 5, 0, 10, "Magic"),
 "Monkey": enemy("Monkey", 80, 10, 15, 0, 10, 15, None), "Rat": enemy("Rat", 10, 1, 5, 0, 0, 1, "Melee"), "Robber": enemy("Robber", 120, 45, 30, 0, 20, 65,"Range"),
 "Slime": enemy("Slime", 25, 5, 5, 10, 0, 8, "Magic"), "Snake": enemy("Snake", 50, 15, 15, 0, 0, 20, "Range"), "Spider": enemy("Spider", 30, 5, 5, 0, 5, 10, "Magic")}

#  name, health, attack, speed, magic, range, level, itemClass, type, style
items = {"HelmetOfStrength": item("HelmetOfStrength", 30,20,0,0,0,40, "Warrior", "head", None),
"AccuracyHelmet": item("AccuracyHelmet", 10,30,0,0,50,50,"Ranger","head", None),
"HelmetOfHexing": item("HelmetOfHexing", 20,0,0,30,0,30,"Mage","head", None),
"HelmetWithGoggles": item("HelmetWithGoggles", 30,10,25,0,25,35,"Ranger","head", None),
"MaskOfMasking": item("MaskOfMasking",10,15,30,0,10, 35,"Rouge", "head", None),
"RottonTomato": item("RottonTomato",0,100,30,10,100, 80,"Ranger", "hand", "Range"),
"SwordOfSwording": item("SwordOfSwording", 0, 5, 5, 0, 0, 1, 'Warrior', 'hand', "Melee"),
"BootsOfMovingAtADecentPace": item("BootsOfMovingAtADecentPace", 5, 0, 10, 0, 0, 1, 'Rogue', 'feet', None),
"BowOfShootingArrows": item("BowOfShootingArrows", 0, 15, 10, 0, 20, 15, 'Ranger', 'hand', "Range"),
"ClubOfCrushing": item("ClubOfCrushing", 5, 15, -5, -5, 0, 8, 'Warrior', 'hand',"Melee" ),
"Crossbow": item("Crossbow", 0, 5, 5, 0, 35, 35, 'Ranger', 'hand', "Range"),
"DaggerOfDagging": item("DaggerOfDagging", 0, 10, 10, 0, 0, 15, 'Rogue', 'hand', "Melee"),
"DaggerOfDemocracy": item("DaggerOfDemocracy", 0, 25, 20, 0, -10, 25, "Rogue", 'hand' , "Melee"),
"DecapiTater": item("DecapiTater", 0, 10, 5, -5, 0, 8, "Warrior", 'hand', "Melee"),
"FakeID": item("FakeID", 5, 3, 5, 0, 0, 5, "Rogue", 'hand', "Melee"),
"FlashlightOfFrying": item("FlashlightOfFrying", 0, 0, 0, 35, 0, 28, "Mage", 'hand', "Magic"),
"FleshRipper": item("FleshRipper", 15, 15, 5, -10, 0, 20, 'Warrior', 'hand', "Melee"),
"Gun": item("Gun", 0, 5, 20, -5, 10, 25, "Ranger", 'hand', "Range"),
"HiddenButterKnife": item("HiddenButterKnife", 0, 5, 10, 0, -5, 10, "Rogue", 'hand',"Melee"),
"HolyHobnail": item("HolyHobnail", 0, 15, 0, 0, 0, 8, "Warrior", 'hand', "Range"),
"LighterFullOfSuperMagicFluid": item("LighterFullOfSuperMagicFluid", 0, 0, 5, 25, 0, 25, "Mage", 'hand', "Magic"),
"MagicBanana": item("MagicBanana", 0, 5, 5, 10, -5, 10, "Mage", 'hand', "Magic"),
"PotOfScaldingMagicWater": item("PotOfScaldingMagicWater", -5, -5, -5, 50, -5, 30, "Mage", 'hand', "Magic"),
"QuiverForArrows": item("QuiverForArrows", 0, 0, 5, 0, 10, 10, "Ranger", 'spells', None),
"ReallyHeavyHandBag": item("ReallyHeavyHandBag", 1, 15, 5, 0, 0, 16, "Rogue", 'hand', "Melee" ),
"ReallyLongPoker": item("ReallyLongPoker", 0, 15, 5, 0, 15, 10, "Ranger", 'hand', "Range"),
"ReallySharpNeedle": item("ReallySharpNeedle", 0, 5, 10, 0, 0, 10, "Rogue", 'hand', "Melee"),
"Rock": item("Rock", 0, 5, 0, 0, 0, 5, "Warrior", 'hand', "Melee"),
"ScrollOfFreezing": item("ScrollOfFreezing", 0, 0, 15, 15, 0, 20, "Mage", 'spells', None),
"ShootingStar": item("ShootingStar", 0, 5, 10, 0, 10, 8, "Rogue", 'hand', "Range"),
"Shotput": item("Shotput", 0, 20, 20, 0, 10, 15, "Ranger", 'hand', "Range"),
"SkullBasher": item("SkullBasher", 5, 10, 0, 0, 0, 8, "Warrior", 'hand', "Melee"),
"Slingshot": item("Slingshot", 0, 0, 10, 0, 5, 5, "Ranger", 'hand', "Range"),
"Spear": item("Spear", 0, 5, 5, 0, 10, 10, "Ranger", 'hand', "Range"),
"SuperBallOfZapping": item("SuperBallOfZapping", 10, 0, 5, 20, 0, 25, "Mage", 'hand', "Magic"),
"Trebuchet": item("Trebuchet", 0, 0, 0, 0, 300, 99, "Ranger", 'hand', "Range", gap = 1),
"TrickCard": item("TrickCard", 0, 0, 10, 15, 0, 10, "Mage", 'hand', "Magic"),
"WandOfCastingSpells": item("WandOfCastingSpells", 0, 0, 5, 10, 0, 5, "Mage", 'hand','Magic'),
"BasicBook": item("BasicBook", 0, 0, 0, 0, 0, 1, "All", 'spells', None),
"BasicHat": item("BasicHat", 0, 0, 0, 0, 0, 1, "All", 'head', None),
"BasicShirt": item("BasicHat", 0, 0, 0, 0, 0, 1, "All", 'body', None),
"BasicShoes": item("BasicShoes", 0, 0, 0, 0, 0, 1, "All", 'feet', None),
"BasicThingToHitPeopleWith": item("BasicThingToHitPeopleWith", 0, 0, 0, 0, 0, 1, "All", 'hand', "Melee")
}

angryRockBossPhase = 0
angryWindUpRobotBossPhase = 0
atoplocrastPhase = 0
calipatusPhase = 0
daplomesPhase = 0
datastricreaverPhase = 0
dauremiPhase = 0
dragonPhase = 0
evilOctopusPhase = 0
hexagonamalitPhase = 0
koplerPhase = 0
krempPhase = 0
sharkBossPhase = 0
smolkPhase = 0
zedoreptPhase = 0

#name, health, attack, speed, magic, range, phase1, phase2, phase3
bosses ={
"AngryRockBoss": boss("AngryRockBoss", 150, 10, 15, 0, 0),
"AngryWindUpRobotBoss": boss("AngryWindUpRobotBoss", 200, 5, 5, 10, 10),
"Atoplocrast": boss("Atoplocrast", 180, 8, 15, 0, 0),
"Calipatus": boss("Calipatus", 200, 3, 10, 20, 5),
"Daplomes": boss("Daplomes", 150, 0, 5, 25, 5),
"Datastricreaver": boss("Datastricreaver", 250, 8, 5, 0, 0),
"Dauremi": boss("Dauremi", 100, 5, 5, 5, 5),
"Dragon": boss("Dragon", 200, 10, 10, 10, 0),
"EvilOctopus": boss("EvilOctopus", 200, 10, 5, 0, 5),
"Hexagonamalit": boss("Hexagonamalit", 150, 8, 8, 0, 0),
"Kopler": boss("Kopler", 100, 5, 5, 0, 0),
"Kremp": boss("Kremp", 150, 15, 15, 0, 0),
"SharkBoss": boss("SharkBoss", 200, 15, 15, 0, 0),
"Smolk": boss("Smolk", 150, 0, 0, 25, 0),
"Zedorept": boss("Zedorept", 150, 15, 15, 5, 5)
}

healthStat = 50
attackStat = 50
speedStat = 50
magicStat = 50
rangeStat = 50
currHealth = 50
currXP = 0
currLevel = 1

waitAction = None

enemyMaxHealth = 0

con = PyCon.PyCon(s,
                      (0,0,320,240),
                      functions = {},
                      key_calls = {},
                      vari={"A":100,"B":200,"C":300}#,
                     # syntax={re_function:console_func}
)
con.set_active()

# FUNCTIONS
def randname(gender):
    if gender == 'male':
        name = ''
        with open ("names/maleFirst.txt", "r") as file:
            data = file.readlines()
        name += data[random.randint(0, len(data)-1)].replace('\n', ' ')
        with open ("names/maleLast.txt", "r") as file:
            data = file.readlines()
        name += data[random.randint(0, len(data)-1)].replace('\n', ' ')
        return name
    elif gender == 'female':
        name = ''
        with open ("names/femaleFirst.txt", "r") as file:
            data = file.readlines()
        name += data[random.randint(0, len(data))].replace('\n', ' ')
        with open ("names/femaleLast.txt", "r") as file:
            data = file.readlines()
        name += data[random.randint(0, len(data))].replace('\n', ' ')
        return name
def genStats(points):
    attack = random.randint(5, points)
    health = random.randint(5, points)
    speed = random.randint(5, points)
    magic = random.randint(5, points)
    range = random.randint(5, points)

    return [attack, health, speed, magic, range]
def genFloor(mapWidth, mapHeight, minRooms, maxRooms):
    print("Gen New Floor")
    mapArray = []
    for y in range(0, mapHeight):
        mapArray.append([])
        for x in range(0, mapWidth):
            mapArray[y].append('o')
    start = [random.randint(0, mapWidth-1), random.randint(0, mapHeight-1)]
    mapArray[start[0]][start[1]] = 'x'
    rooms = 0
    def populate(rooms):
        print("Populate")
        for y in range(0, mapHeight):
            for x in range(0, mapWidth):
                if y - 1 > -1 and mapArray[y - 1][x] == 'x' and mapArray[y][x] != 'x':
                    if random.randint(0, 2) == 0 and rooms < maxRooms:
                        mapArray[y][x] = 'x'
                        rooms += 1
                if y + 1 < mapHeight and mapArray[y + 1][x] == 'x' and mapArray[y][x] != 'x':
                    if random.randint(0, 1) == 0 and rooms < maxRooms:
                        mapArray[y][x] = 'x'
                        rooms += 1
                if x - 1 > -1 and mapArray[y][x-1] == 'x' and mapArray[y][x] != 'x':
                    if random.randint(0, 2) == 0 and rooms < maxRooms:
                        mapArray[y][x] = 'x'
                        rooms += 1
                if x + 1 < mapWidth and mapArray[y][x+1] == 'x' and mapArray[y][x] != 'x':
                    if random.randint(0, 2) == 0 and rooms < maxRooms:
                        mapArray[y][x] = 'x'
                        rooms += 1
        return rooms
    while rooms < minRooms and rooms < (mapWidth * mapHeight)-1:
        rooms = populate(rooms)
    mapArray[start[0]][start[1]] = 'x'
    for y in range(0, mapHeight-1):
        for x in range(0, mapWidth-1):
            if mapArray[y][x] == 'x':
                start = [x, y]
                break
    return [start, mapArray, rooms + 1]
def dist(n, start1, stop1, start2, stop2):
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2
def newTile(x, y, type='empty'):
    if type == 'empty':
        return base_sprite(width=10, height=10, image="images/roomTile.png", x=x, y=y)
    if type == 'in':
        return base_sprite(width=10, height=10, image="images/roomTileIn.png", x=x, y=y)
    if type == 'stairs':
        return base_sprite(width=10, height=10, image="images/stairsTile.png", x=x, y=y)
def drawMiniMap():
    for i in miniMap:
        mapGroup.add(newTile(i[0]*10 + indX, i[1]*10 + indY))
    roomsNumText = text("rooms: " + str(len(miniMap)) + '/' + str(rooms), 10, 5, font_size = 16)
    floorText = text("floor: " + str(floorLevel), 10, 20, font_size = 16)
    if stairs != None:
        mapGroup.add(newTile(stairs[0]*10 + indX, stairs[1]*10 + indY, 'stairs'))
    mapGroup.add(newTile(playerX*10 + indX, playerY*10 + indY, 'in'))
    mapGroup.add(floorText)
    mapGroup.add(roomsNumText)
    mapGroup.add(roomsNumText)
def actionTreasure():
    global treasureClicked #no judge
    treasureClicked = False
    con.output("Found treasure!")
    chestSprite = base_sprite(width=80, height=80, image="images/treasure.png", x=(width/2) - 40, y=(height/2) - 40)
    roomGroup.add(chestSprite)
def actionEnemy():
    # Globals are still bad mkay
    global enemyEncountered, waitAction
    def pick():
        return  list(enemies.keys())[random.randint(0, len(enemies)-1)]
    enemyEncountered = pick()
    while enemies[enemyEncountered].level < floorLevel - 5 or enemies[enemyEncountered].level > floorLevel + 5:
        enemyEncountered = pick()
    enemySprite = base_sprite(width=80, height=80, image="images/enemies/"+enemyEncountered+".png", x=(width/2) - 40, y=(height/2) - 40)
    roomGroup.add(enemySprite)
    con.output("Found " + enemyEncountered + "!")
    waitAction = battle
def actionNothing():
    global stairs #Do not judge globals
    actions = ["PictureOfPotato", "PictureOfChicken", "Stairs"]
    action = actions[random.randint(0, len(actions) -1)]
    if action == "Stairs":
        if random.randint(0, 8) < 8:
            action = "PictureOfPotato"
    if len(miniMap) >= rooms-1:
        action = "Stairs"
    if action == "Stairs" and stairs != None:
        action = "PictureOfPotato"
    elif action == "Stairs":
        stairsSprite = base_sprite(width=80, height=80, image="images/stairs.png", x=(width/2) - 40, y=(height/2) - 40)
        roomGroup.add(stairsSprite)
        stairs = [playerX, playerY]
    else:
        actionSprite = base_sprite(width=80, height=80, image="images/"+action+".png", x=(width/2) - 40, y=(height/2) - 40)
        roomGroup.add(actionSprite)
    con.output("Found " + action + "!")
def battle(enemyEncountered):
    # We know it's really bad to use globals but we have just 'cause. Don't question it.
    global enemyHealth, playerTurn, inFight, floorLevel, enemyMaxHealth
    con.output("Encountered " + enemyEncountered + "!")
    enemyHealth = random.randint(enemies[enemyEncountered].health, enemies[enemyEncountered].health + (floorLevel * 2))
    enemyMaxHealth = enemyHealth
    playerTurn = speedStat >= enemies[enemyEncountered].speed
    inFight = True
def handleXP():
    global currXP, currLevel, healthStat, attackStat, speedStat, magicStat, rangeStat, currHealth # globals are bad but it makes it okay if we acknowldge it.  No questions
    cap = (2 * currLevel * (1 + currLevel))
    if currXP >= cap:
        currXP -= cap
        currLevel += 1
        con.output("Congratulations! Reached level "+str(currLevel)+"!")
        healthUp = currLevel - math.floor(currLevel/5)
        attackUp = currLevel - math.floor(currLevel/5)
        speedUp = currLevel - math.floor(currLevel/5)
        magicUp = currLevel - math.floor(currLevel/5)
        rangeUp = currLevel - math.floor(currLevel/5)
        if classPicked == "mage":
            magicUp = (currLevel * 2) - math.floor(currLevel/5)
        elif classPicked == "warrior":
            attackUp = math.floor(currLevel * 1.75) - math.floor(currLevel/5)
            healthUp = math.floor(currLevel * 1.25) - math.floor(currLevel/5)
        elif classPicked == 'ranger':
            rangeUp = math.floor(currLevel * 1.75) - math.floor(currLevel/5)
            speedUp = math.floor(currLevel * 1.25) - math.floor(currLevel/5)
        elif classPicked == "rogue":
            attackUp = (currLevel * 1.25) - math.floor(currLevel/3)
            rangeUp = (currLevel * 1.25) - math.floor(currLevel/3)
            speedUp = (currLevel * 1.25) - math.floor(currLevel/3)
            magicUp = (currLevel * 1.25) - math.floor(currLevel/3)
        con.output("Health: " + str(healthStat) + " + " + str(healthUp) + " -> " + str(healthStat + healthUp))
        healthStat += healthUp
        con.output("Attack: " + str(attackStat) + " + " + str(attackUp) + " -> " + str(attackStat + attackUp))
        attackStat += attackUp
        con.output("Speed: " + str(speedStat) + " + " + str(speedUp) + " -> " + str(speedStat + speedUp))
        speedStat += speedUp
        con.output("Magic: " + str(magicStat) + " + " + str(magicUp) + " -> " + str(magicStat + magicUp))
        magicStat += magicUp
        con.output("Range: " + str(rangeStat) + " + " + str(rangeUp) + " -> " + str(rangeStat + rangeUp))
        rangeStat += rangeUp
        currHealth += healthUp
        handleXP()
def genBoss():
    # just dont even bother judging spaghetti globals at this point
    global floorLevel, bosses, inBoss, bossEncountered, bossHealth, floorLevel, bossAttack, bossMaxHealth
    bossEncountered = list(bosses.keys())[random.randint(0, len(bosses) -1)]
    con.output("A very angry " + bossEncountered + " has caught you!")
    inBoss = True
    bossHealth = bosses[bossEncountered].health + floorLevel
    bossAttack = bosses[bossEncountered].attack + floorLevel
    bossMaxHealth = bosses[bossEncountered].health + floorLevel
lowerCaseFirst = lambda s: s[:1].lower() + s[1:] if s else ''
def bigBlit(group):
    global s #still lazy ok
    surface = pygame.image.load("images/back.png")
    for i in group:
        surface.blit(i.image, (i.rect.x, i.rect.y))
    group = pygame.sprite.Group()
    group.add(base_sprite(image=surface, width=320, height=240, x=0, y=0, surface=True))
    group.draw(s)
def rfRead():
    global healthStat, attackStat, rangeStat, magicStat, speedStat, currHealth, currXP, currLevel, floorLevel
    global spellsEq, headEq, bodyEq, handEq, feetEq, spells, head, body, hand, feet, genNewFloor, inGame, inLoad, classPicked
    # 5, 6, 16, 26
    CS = 7
    MOSI = 20
    MISO = 19
    SCLK = 21
    pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
    pn532.begin()
    pn532.SAM_configuration()
    con.output("Place figure on reader.")
    uid = pn532.read_passive_target()
    while uid is None:
        uid = pn532.read_passive_target()
    with open("saves/" + str(binascii.hexlify(uid)).replace("'", '') + '.json') as file:
        stuffToLoad = json.loads(file.readlines()[0])
        for i in stuffToLoad:
            if isinstance(stuffToLoad[i], str):
                exec(i + " = '" + stuffToLoad[i] + "'")
            else:
                exec(i + " = " + str(stuffToLoad[i]))
    print(classPicked + ' class')
    genNewFloor = True
    inGame = True
    inLoad = False
    con.output("Load complete. It save safe to remove figure.")



def rfWrite():
    stuffToSave = ['healthStat', 'attackStat', 'rangeStat', 'magicStat', 'speedStat', 'currHealth', 'currXP', 'currLevel', 'floorLevel',
    'spellsEq', 'headEq', 'bodyEq', 'handEq', 'feetEq', 'spells', 'head', 'body', 'hand', 'feet', 'classPicked']
    stuffToSave = dict  ( (name,eval(name)) for name in stuffToSave )

    # 5, 6, 16, 26
    CS = 7
    MOSI = 20
    MISO = 19
    SCLK = 21
    pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
    pn532.begin()
    pn532.SAM_configuration()
    con.output("Place figure on reader.")
    uid = pn532.read_passive_target()
    while uid is None:
        uid = pn532.read_passive_target()
    with open("saves/" + str(binascii.hexlify(uid)).replace("'", '') + '.json', 'w') as file:
        print(json.dumps(stuffToSave))
        file.write(json.dumps(stuffToSave))
    con.output("Save complete! It is safe to remove figure.")








# text = text("TEST", "Comic Sans MS",16,(0, 0, 0),15,15,255)
# SPRITES
# rfRead()

homeScreenGroup = pygame.sprite.Group()
loadScreenGroup = pygame.sprite.Group()
nameScreenGroup = pygame.sprite.Group()
nameConfirmScreenGroup = pygame.sprite.Group()
characterGenGroup = pygame.sprite.Group()
characterGenGroup1 = pygame.sprite.Group()
characterGenGroup2 = pygame.sprite.Group()
characterGenGroupEnd = pygame.sprite.Group()
roomGroup = pygame.sprite.Group()
mapGroup = pygame.sprite.Group()
inventoryGroup = pygame.sprite.Group()
subGroup = pygame.sprite.Group()
fightGroup = pygame.sprite.Group()
deadGroup = pygame.sprite.Group()
swapGroup = pygame.sprite.Group()
inspectGroup = pygame.sprite.Group()
bossGroup = pygame.sprite.Group()
loadFigureGroup = pygame.sprite.Group()
betweenGroup = pygame.sprite.Group()

button = base_sprite(width=70, height=50, image="images/HomeScreenStartButton.png", x=(width/2) - (70/2), y=120)
homeScreen = base_sprite(width=320, height=240, image="images/back.png", x=0, y=0)

homeScreenGroup.add(homeScreen)
homeScreenGroup.add(button)

scanButton = base_sprite(width=70, height=50, image="images/ScanButton.png", x=45, y=100)
newButton = base_sprite(width=70, height=50, image="images/NewButton.png", x=205, y=100)
back = base_sprite(width=320, height=240, image="images/back.png", x=0, y=0)

loadScreenGroup.add(back)
loadScreenGroup.add(scanButton)
loadScreenGroup.add(newButton)

NameBackground = base_sprite(width=320, height=240, image="images/NameBackground.png", x=0, y=0)
MaleButton = base_sprite(width=70, height=50, image="images/MaleButton.png", x=45, y=120)
FemaleButton = base_sprite(width=70, height=50, image="images/FemaleButton.png", x=205, y=120)
nameText = text("test", 15, 15)
# nameText.rerender(0, 80, center=True)

nameScreenGroup.add(NameBackground)
nameScreenGroup.add(MaleButton)
nameScreenGroup.add(FemaleButton)
# nameScreenGroup.add(nameText)

NameConfirmBackground = base_sprite(width=320, height=240, image="images/NameConfirmBackground.png", x=0, y=0)
nameText.rerender(0, 80, center=True)
YesButton =  base_sprite(width=70, height=50, image="images/YesButton.png", x=45, y=170)
NoButton =  base_sprite(width=70, height=50, image="images/NoButton.png", x=205, y=170)

nameConfirmScreenGroup.add(NameConfirmBackground)
nameConfirmScreenGroup.add(YesButton)
nameConfirmScreenGroup.add(NoButton)

CharacterGenBackground = base_sprite(width=320, height=240, image="images/CharacterGenBackground.png", x=0, y=0)
customButton = base_sprite(width=70, height=50, image="images/CustomButton.png", x=45, y=170)
randomButton = base_sprite(width=70, height=50, image="images/RandomButton.png", x=205, y=170)

characterGenGroup.add(CharacterGenBackground)
characterGenGroup.add(customButton)
characterGenGroup.add(randomButton)

characterGen1Background = base_sprite(width=320, height=240, image="images/CharacterGen1Background.png", x=0, y=0)
mageButton = base_sprite(width=70, height=50, image="images/MageButton.png", x=45, y=80)
rogueButton = base_sprite(width=70, height=50, image="images/RogueButton.png", x=205, y=80)
warriorButton = base_sprite(width=70, height=50, image="images/WarriorButton.png", x=45, y=170)
rangerButton = base_sprite(width=70, height=50, image="images/RangerButton.png", x=205, y=170)

characterGenGroup1.add(characterGen1Background)
characterGenGroup1.add(mageButton)
characterGenGroup1.add(rogueButton)
characterGenGroup1.add(warriorButton)
characterGenGroup1.add(rangerButton)

stats = genStats(10)
healthText = text(str(stats[1]), 200, 0, font_size=20)
attackText = text(str(stats[0]), 200, 25, font_size=20)
speedText = text(str(stats[2]), 200, 50, font_size=20)
magicText = text(str(stats[3]), 200, 75, font_size=20)
rangeText = text(str(stats[4]), 200, 100, font_size=20)
healthSayText = text("Health: ", 100, 0, font_size=20)
attackSayText = text("Attack: ", 100, 25, font_size=20)
speedSayText = text("Speed: ", 100, 50, font_size=20)
magicSayText = text("Magic: ", 100, 75, font_size=20)
rangeSayText = text("Range: ", 100, 100, font_size=20)
rollButton = base_sprite(width=70, height=50, image="images/RollButton.png", x=45, y=170)
continueButton = base_sprite(width=70, height=50, image="images/ContinueButton.png", x=205, y=170)

characterGenGroup2.add(back)
characterGenGroup2.add(attackText)
characterGenGroup2.add(healthText)
characterGenGroup2.add(speedText)
characterGenGroup2.add(magicText)
characterGenGroup2.add(rangeText)
characterGenGroup2.add(rollButton)
characterGenGroup2.add(continueButton)
characterGenGroup2.add(healthSayText)
characterGenGroup2.add(attackSayText)
characterGenGroup2.add(speedSayText)
characterGenGroup2.add(magicSayText)
characterGenGroup2.add(rangeSayText)



characterGenEndBackground = base_sprite(width=320, height=240, image="images/CharacterGenEndBackground.png", x=0, y=0)
characterGenGroupEnd.add(characterGenEndBackground)
characterGenGroupEnd.add(YesButton)
characterGenGroupEnd.add(NoButton)

floor = base_sprite(width=320, height=240, image="images/roomFloor.png", x=0, y=0)
leftDoor = base_sprite(width=20, height=80, image="images/vertDoor.png", x=0, y=80)
rightDoor = base_sprite(width=20, height=80, image="images/vertDoor.png", x=300, y=80)
topDoor = base_sprite(width=80, height=20, image="images/horDoor.png", x=120, y=0)
bottomDoor = base_sprite(width=80, height=20, image="images/horDoor.png", x=120, y=220)
roomsText = text('rooms: ', 10, 10, font_size = 16)
roomsNumText = text('0/0', 60, 10, font_size = 16)
roomGroup.add(floor)

headBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=180, y=10, scale=[50, 50])
handBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=250, y=94, scale=[50, 50])
bodyBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=180, y=94, scale=[50, 50])
feetBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=180, y=178, scale=[50, 50])
spellBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=110, y=10, scale=[50, 50])
inventoryGroup.add(back)

xButton = base_sprite(width=25, height=25, image="images/X.png", x=5, y=5, scale=[25, 25])

subGroup.add(back)

runButton = base_sprite(width=70, height=50, image="images/RunButton.png", x=30, y=170)
attackButton = base_sprite(width=70, height=50, image="images/AttackButton.png", x=130, y=170)
magicButton = base_sprite(width=70, height=50, image="images/MagicButton.png", x=230, y=170)
healthBarOutline = base_sprite(width=104, height=24, image="images/HealthBarOutline.png", x=200, y=5)
playerHealthBarOutline = base_sprite(width=104, height=24, image="images/HealthBarOutline.png", x=10, y=140)
fightBackground = base_sprite(width=320, height=240, image="images/FightBackground.png", x=0, y=0)

deadText = text("You have died", 0, 0, font_size=36)
deadText.rerender(0, 5, center=True)
deadMessageText = text("You will be returned to the previous floor", 0, 0, font_size=16)
deadMessageText.rerender(0, 65, center=True)
deadContinueButton = base_sprite(width=70, height=50, image="images/ContinueButton.png", x=125, y=170)

deadGroup.add(back)
deadGroup.add(deadContinueButton)
deadGroup.add(deadText)
deadGroup.add(deadMessageText)


dontSwapButton = base_sprite(width=100, height=50, image="images/DontSwapButton.png", x=(width/2)-50, y=180)
swapText = text("Pick an item to swap.", 0, 0, font_size=20)
swapText.rerender(0, 5, center=True)
swapGroup.add(back)
swapGroup.add(dontSwapButton)
swapGroup.add(swapText)


inspectGroup.add(back)
inspectGroup.add(xButton)

bossGroup.add(fightBackground)

loadFigureGroup.add(back)
loadFigureText = text("Place figure on reader", 0, 0)
loadFigureText.rerender(0, 10, center=True)

saveButton = base_sprite(width=70, height=50, image="images/SaveButton.png", x=45, y=170)

betweenGroup.add(back)
betweenGroup.add(saveButton)
betweenGroup.add(continueButton)


# MAIN
move = False
while running:
    events = pygame.event.get()
    for event in events:
        namePass = False
        classPick = False
        endGen = False
        if event.type == pygame.QUIT:
            running = False;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                print("test")
            elif event.key == pygame.K_m and inGame:
                print('map')
                inMap = not inMap
                if inMap:
                    newMap = True
            elif event.key == pygame.K_c:
                print("con")
                inCon = not inCon
            elif event.key == pygame.K_i and inGame:
                print("inventory")
                inInventory = not inInventory
                if inInventory:
                    newInventory = True
                else:
                    inSub = False
                    inSpell = False
                    inHead = False
                    inHand = False
                    inBody = False
                    inFeet = False
                    inInspect = False
            elif event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(event.pos) and inHome:
                inHome = False
                inLoad = True
            elif scanButton.rect.collidepoint(event.pos) and inLoad:
                inFigureLoad = True
            elif newButton.rect.collidepoint(event.pos) and inLoad:
                inLoad = False
                inName = True
            elif MaleButton.rect.collidepoint(event.pos) and inName:
                name = randname('male')
                namePass = True
            elif FemaleButton.rect.collidepoint(event.pos) and  inName:
                name = randname('female')
                namePass = True
            elif YesButton.rect.collidepoint(event.pos) and inNameConfirm:
                inNameConfirm = False
                inCharacterGen = True
            elif NoButton.rect.collidepoint(event.pos) and inNameConfirm:
                nameConfirmScreenGroup.remove(nameText)
                inNameConfirm = False
                inName = True
            elif customButton.rect.collidepoint(event.pos) and inCharacterGen:
                inCharacterGen1 = True
                inCharacterGen = False
            elif randomButton.rect.collidepoint(event.pos) and inCharacterGen:
                inCharacterGen = False
                randint = random.randint(1, 4)
                if randint == 1:
                    classPicked = 'mage'
                elif randint == 2:
                    classPicked = 'ranger'
                elif randint == 3:
                    classPicked = 'rogue'
                elif randint == 4:
                    classPicked = 'warrior'
                endGen = True
            elif mageButton.rect.collidepoint(event.pos) and inCharacterGen1:
                classPick = True
                classPicked = 'mage'
            elif rogueButton.rect.collidepoint(event.pos) and inCharacterGen1:
                classPick = True
                classPicked = 'rogue'
            elif warriorButton.rect.collidepoint(event.pos) and inCharacterGen1:
                classPick = True
                classPicked = 'warrior'
            elif rangerButton.rect.collidepoint(event.pos) and inCharacterGen1:
                classPick = True
                classPicked = 'ranger'
            elif rollButton.rect.collidepoint(event.pos) and inCharacterGen2:
                characterGenGroup2.empty()
                stats = genStats(20)
                healthText = text(str(stats[1]), 200, 0, font_size=20)
                attackText = text(str(stats[0]), 200, 25, font_size=20)
                speedText = text(str(stats[2]), 200, 50, font_size=20)
                magicText = text(str(stats[3]), 200, 75, font_size=20)
                rangeText = text(str(stats[4]), 200, 100, font_size=20)
                characterGenGroup2.add(back)
                characterGenGroup2.add(attackText)
                characterGenGroup2.add(healthText)
                characterGenGroup2.add(speedText)
                characterGenGroup2.add(magicText)
                characterGenGroup2.add(rangeText)
                characterGenGroup2.add(rollButton)
                characterGenGroup2.add(continueButton)
                characterGenGroup2.add(healthSayText)
                characterGenGroup2.add(attackSayText)
                characterGenGroup2.add(speedSayText)
                characterGenGroup2.add(magicSayText)
                characterGenGroup2.add(rangeSayText)
            elif continueButton.rect.collidepoint(event.pos) and inCharacterGen2:
                inCharacterGen2 = False
                endGen = True
            elif NoButton.rect.collidepoint(event.pos) and inCharacterGenEnd:
                inCharacterGenEnd = False
                inLoad = True
            elif YesButton.rect.collidepoint(event.pos) and inCharacterGenEnd:
                inCharacterGenEnd = False
                healthStat = stats[1]
                attackStat = stats[0]
                speedStat = stats[2]
                magicStat = stats[3]
                rangeStat = stats[4]
                currHealth = stats[1]
                inGame = True
            elif topDoor.rect.collidepoint(event.pos) and inGame and 'up' in directions and waitAction == None and not inFight and not inSwap:
                playerY -= 1
                move = True
            elif bottomDoor.rect.collidepoint(event.pos) and inGame and 'down' in directions and waitAction == None and not inFight and not inSwap:
                playerY += 1
                move = True
            elif leftDoor.rect.collidepoint(event.pos) and inGame and 'left' in directions and waitAction == None and not inFight and not inSwap:
                playerX -= 1
                move = True
            elif rightDoor.rect.collidepoint(event.pos) and inGame and 'right' in directions and waitAction == None and not inFight and not inSwap:
                playerX += 1
                move = True
            elif topDoor.rect.collidepoint(event.pos) and waitAction != None:
                con.output("The enemy won't let you leave the room")
            elif bottomDoor.rect.collidepoint(event.pos) and waitAction != None:
                con.output("The enemy won't let you leave the room")
            elif leftDoor.rect.collidepoint(event.pos) and waitAction != None:
                con.output("The enemy won't let you leave the room")
            elif rightDoor.rect.collidepoint(event.pos) and waitAction != None:
                con.output("The enemy won't let you leave the room")
            elif spellBorder.rect.collidepoint(event.pos) and inInventory and not inSub:
                inSub = True
                newSub = True
                inSpell = True
            elif headBorder.rect.collidepoint(event.pos) and inInventory and not inSub:
                inSub = True
                newSub = True
                inHead = True
            elif bodyBorder.rect.collidepoint(event.pos) and inInventory and not inSub:
                inSub = True
                newSub = True
                inBody = True
            elif handBorder.rect.collidepoint(event.pos) and inInventory and not inSub:
                inSub = True
                newSub = True
                inHand = True
            elif feetBorder.rect.collidepoint(event.pos) and inInventory and not inSub:
                inSub = True
                newSub = True
                inFeet = True
            elif xButton.rect.collidepoint(event.pos) and inSub and not inInspect:
                inSub = False
                inSpell = False
                inHead = False
                inHand = False
                inBody = False
                inFeet = False
                newInventory = True
            elif enemySprite.rect.collidepoint(event.pos) and inGame and waitAction != None and not inInventory:
                print('oh you clicked me')
                waitAction(enemyEncountered)
                waitAction = None
            elif runButton.rect.collidepoint(event.pos) and inFight:
                if random.randint(0, math.ceil(speedStat/4)) == 0:
                    con.output("Failed to run away!")
                    playerTurn = False
                else:
                    con.output("Managed to escape!")
                    inFight = False
                    move = True
            elif attackButton.rect.collidepoint(event.pos) and inFight and playerTurn:
                gap = items[handEq].gap
                if items[handEq].style == 'Melee':
                    damage = attackStat + items[handEq].attack
                elif items[handEq].style == 'Range':
                    damage = rangeStat + items[handEq].range
                elif items[handEq].style == 'Magic':
                    damage = magicStat + items[handEq].magic
                if items[handEq].itemClass == classPicked:
                    damage *= 2

                damage = random.randint(int(damage - math.floor((damage/gap))), int(damage + math.floor((damage/gap))))
                if random.randint(0, math.floor(speedStat/2)) == 0:
                    con.output("Uh oh! You missed!")
                else:
                    con.output("Hit enemy for " + str(damage) + " damage!")
                    enemyHealth -= damage
                    if enemyHealth < 0:
                        enemyHealth = 0
                playerTurn = False
            elif deadContinueButton.rect.collidepoint(event.pos) and inDead:
                inDead = False
                genNewFloor = True
            elif stairsSprite.rect.collidepoint(event.pos) and inGame and [playerX, playerY] == stairs and not inInventory:
                # if str(floorLevel)[len(str(floorLevel)) -1] == '9':
                #     genBoss()
                # else:
                #     genNewFloor = True
                #     floorLevel += 1
                inBetween = True
            elif saveButton.rect.collidepoint(event.pos) and inBetween:
                inSave = True
            elif continueButton.rect.collidepoint(event.pos) and inBetween:
                if str(floorLevel)[len(str(floorLevel)) -1] == '9':
                    genBoss()
                else:
                    genNewFloor = True
                    floorLevel += 1
                inBetween = False
            elif chestSprite.rect.collidepoint(event.pos) and inGame and  not treasureClicked and not inInventory:
                treasureClicked = True
                itemFound = list(items.keys())[random.randint(0, len(items) -1)]
                while items[itemFound].level > floorLevel + 5 or items[itemFound].level < floorLevel -5:
                    itemFound = list(items.keys())[random.randint(0, len(items) -1)]
                con.output("Obtained " + itemFound + "!")
                itemSprite = base_sprite(width=80, height=80, image="images/items/"+ itemFound +".png", x=(width/2)-40, y=(height/2)-40)
                roomGroup.remove(chestSprite)
                roomGroup.add(itemSprite)

                if eval("'" + itemFound + "' in " + items[itemFound].type):
                    None
                elif len(eval(items[itemFound].type)) >= 6:
                    inSwap = True
                    newSwap = True
                    con.output("You are carying too many " + items[itemFound].type.replace('s', '') + ' items.')
                else:
                    exec(items[itemFound].type + ".append('"+itemFound+"')")
            elif dontSwapButton.rect.collidepoint(event.pos) and inSwap:
                inSwap = False
            elif xButton.rect.collidepoint(event.pos) and inInspect:
                inInspect = False
            elif attackButton.rect.collidepoint(event.pos) and inBoss and not bossTurn:
                gap = items[handEq].gap
                if items[handEq].style == 'Melee':
                    damage = attackStat + items[handEq].attack
                elif items[handEq].style == 'Range':
                    damage = rangeStat + items[handEq].range
                elif items[handEq].style == 'Magic':
                    damage = magicStat + items[handEq].magic
                if items[handEq].itemClass == classPicked:
                    damage *= 2

                damage = random.randint(int(damage - math.floor((damage/gap))), int(damage + math.floor((damage/gap))))
                con.output("You hit " + bossEncountered + " for " + str(damage) + "!")
                bossHealth -= damage
                bossTurn =True
                bossNewTurn = True
                newPhase = True
                newTurn = True
            elif xButton.rect.collidepoint(event.pos) and inInspect:
                inInspect = False
            if subSprites != None:
                for i in subSprites:
                    if i[1].rect.collidepoint(event.pos) and i[0] in [spellsEq, headEq, handEq, bodyEq, feetEq] and inSub:
                        inInspect = True
                        inspecting = i[0]
                    elif i[1].rect.collidepoint(event.pos) and inSub and not inInspect:
                        con.output("Equipped " + i[0] + "!")
                        exec(items[i[0]].type + 'Eq = "' + i[0] + '"')
                        newSub = True
            if len(swapSprites) >  0:
                for i in swapSprites:
                    if i[1].rect.collidepoint(event.pos) and inSwap:
                        try:
                            con.output("Swapped" + i[0] + " for " + itemFound + '.')
                            print(i[0])
                            eval(items[itemFound].type).remove(i[0])
                            eval(items[itemFound].type).append(itemFound)
                            exec(items[itemFound].type + 'Eq = "' + itemFound + '"')
                        except:
                            None
                        inSwap = False

        if namePass:
            inName = False
            inNameConfirm = True
            nameText = text(name, 0, 0)
            nameText.rerender(0, 30, center=True)
            nameConfirmScreenGroup.remove(nameText)
            nameConfirmScreenGroup.add(nameText)
        if classPick:
            print(classPicked)
            # symbol = base_sprite(width=100, height=100, image="images/"+ classPicked +"Small.png", x=(width/2) - 50, y=80)
            # characterGenGroup2.add(symbol)
            inCharacterGen1 = False
            inCharacterGen2 = True
        if endGen:
            inCharacterGenEnd = True
            nameText = text(name, 0, 0, font_size=16)
            nameText.rerender(0, 25, center=True)
            classText = text(classPicked, 0, 0, font_size=16)
            classText.rerender(0, 45, center=True)
            attackText = text("Attack: " + str(stats[0]), 0, 0, font_size=16)
            attackText.rerender(0, 85, center=True)
            healthText = text("Health: " + str(stats[1]), 0, 0, font_size=16)
            healthText.rerender(0, 65, center=True)
            speedText = text("Speed: " + str(stats[2]), 0, 0, font_size=16)
            speedText.rerender(0, 105, center=True)
            magicText = text("Magic: " + str(stats[3]), 0, 0, font_size=16)
            magicText.rerender(0, 125, center=True)
            rangeText = text("Range: " + str(stats[4]), 0, 0, font_size=16)
            rangeText.rerender(0, 145, center=True)
            characterGenGroupEnd.add(nameText)
            characterGenGroupEnd.add(classText)
            characterGenGroupEnd.add(attackText)
            characterGenGroupEnd.add(healthText)
            characterGenGroupEnd.add(speedText)
            characterGenGroupEnd.add(magicText)
            characterGenGroupEnd.add(rangeText)
        if move:
            roomGroup.empty()
            if [playerX, playerY] not in miniMap:
                actions = [actionTreasure, actionNothing, actionNothing, actionNothing, actionEnemy, actionEnemy]
                option = random.randint(0, len(actions) -1)
                if stairs == None and len(miniMap) >= rooms-1:
                    actionsToRun.append(actionNothing)
                else:
                    actionsToRun.append(actions[option])
                miniMap.append([playerX, playerY])
            elif [playerX, playerY] == stairs:
                print("Stairs here")
                roomGroup.add(stairsSprite)
            newMap = True
            move = False
            if rooms == len(miniMap) and XPBonus:
                con.output("Discovered all rooms! Received " + str(rooms) + " XP bonus")
                currXP += rooms
                handleXP()
                XPBonus = False

    # END UPDATE
    homeScreenGroup.update()
    nameConfirmScreenGroup.update()
    pygame.display.update()
    if inHome:
        homeScreenGroup.update()
        homeScreenGroup.draw(s)
        #bigBlit(homeScreenGroup)
    if inLoad:
        loadScreenGroup.update()
        loadScreenGroup.draw(s)
        #bigBlit(loadScreenGroup)
    if inName:
        nameScreenGroup.update()
        nameScreenGroup.draw(s)
        #bigBlit(nameScreenGroup)
    if inNameConfirm:
        nameConfirmScreenGroup.empty()
        nameConfirmScreenGroup.add(NameConfirmBackground)
        nameConfirmScreenGroup.add(YesButton)
        nameConfirmScreenGroup.add(NoButton)
        nameConfirmScreenGroup.add(nameText)
        nameConfirmScreenGroup.update()
        nameConfirmScreenGroup.draw(s)
        #bigBlit(nameConfirmScreenGroup)
    if inCharacterGen:
        characterGenGroup.update()
        characterGenGroup.draw(s)
        #bigBlit(characterGenGroup)
    if inCharacterGen1:
        characterGenGroup1.update()
        characterGenGroup1.draw(s)
        #bigBlit(characterGenGroup1)
    if inCharacterGen2:
        characterGenGroup2.update()
        characterGenGroup2.draw(s)
        #bigBlit(characterGenGroup2)
    if inCharacterGenEnd:
        characterGenGroupEnd.empty()
        characterGenGroupEnd.add(characterGenEndBackground)
        characterGenGroupEnd.add(YesButton)
        characterGenGroupEnd.add(NoButton)
        characterGenGroupEnd.add(nameText)
        characterGenGroupEnd.add(classText)
        characterGenGroupEnd.add(attackText)
        characterGenGroupEnd.add(healthText)
        characterGenGroupEnd.add(speedText)
        characterGenGroupEnd.add(magicText)
        characterGenGroupEnd.add(rangeText)
        characterGenGroupEnd.update()
        characterGenGroupEnd.draw(s)
        #bigBlit(characterGenGroupEnd)
    if inGame:
        directions = []
        if genNewFloor:
            roomGroup.empty()
            miniMap = []
            newMap = True
            stairs = None
            XPBonus = True
            size = math.floor(dist(floorLevel, 1, 99, 3, 25))
            minRooms = math.floor(dist(floorLevel, 1, 99, 3, 200))
            maxRooms = math.floor(dist(floorLevel, 1, 99, 7, 250))
            mapArray = genFloor(size, size, minRooms, maxRooms)
            start = mapArray[0]
            rooms = mapArray[2]
            mapArray = mapArray[1]
            genNewFloor = False
            playerX = start[0]
            playerY = start[1]
            for i in mapArray:
                print(i)
            indX = ((width/2) - ((size*10)/2))
            indY = (height/2) - ((size*10)/2)
            miniMap.append([playerX, playerY])
            mapGroup.add(newTile(start[0]*10 + indX, start[1]*10 + indY))
        roomGroup.add(floor)
        if playerY != 0 and mapArray[playerY-1][playerX] == 'x':
            roomGroup.add(topDoor)
            directions.append('up')
        if playerY != size-1 and mapArray[playerY+1][playerX] == 'x':
            roomGroup.add(bottomDoor)
            directions.append('down')
        if playerX != 0 and mapArray[playerY][playerX-1] == 'x':
            roomGroup.add(leftDoor)
            directions.append('left')
        if playerX != size-1 and mapArray[playerY][playerX+1] =='x':
            roomGroup.add(rightDoor)
            directions.append('right')
        if [playerX, playerY] == stairs:
            stairsSprite = base_sprite(width=80, height=80, image="images/stairs.png", x=(width/2) - 40, y=(height/2) - 40)
            roomGroup.add(stairsSprite)
        # for i in actionsToRun:
        #     i()
        if len(actionsToRun) >= 1:
            actionsToRun[len(actionsToRun)-1]()
        actionsToRun = []
        roomGroup.update()
        roomGroup.draw(s)
        #bigBlit(roomGroup)
    if inMap:
        if newMap:
            mapGroup.empty()
            drawMiniMap()
            newMap = False
        mapGroup.update()
        mapGroup.draw(s)
        #bigBlit(mapGroup)
    if inInventory:
        if newInventory:
            newInventory = False
            inventoryGroup.empty()

            symbol =  base_sprite(width=100, height=100, image="images/"+ classPicked +"Small.png", x=5, y=(height/2)-50)

            inventoryGroup.add(back)
            inventoryGroup.add(symbol)
            inventoryGroup.add(headBorder)
            inventoryGroup.add(handBorder)
            inventoryGroup.add(bodyBorder)
            inventoryGroup.add(feetBorder)
            inventoryGroup.add(spellBorder)
            inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/" + headEq + ".png", x=180, y=10, scale=[50, 50]))
            inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/" + handEq + ".png", x=250, y=94, scale=[50, 50]))
            inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/" + bodyEq + ".png", x=180, y=94, scale=[50, 50]))
            inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/" + feetEq + ".png", x=180, y=178, scale=[50, 50]))
            inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/" + spellsEq + ".png", x=110, y=10, scale=[50, 50]))
        inventoryGroup.update()
        inventoryGroup.draw(s)
        #bigBlit(inventoryGroup)
    if inSub:
        if newSub:
            newSub = False
            subSprites = []
            subGroup.empty()
            subGroup.add(back)
            subGroup.add(xButton)
            if inSpell:
                inventoryPicked = 'spells'
            elif inHead:
                inventoryPicked = 'head'
            elif inBody:
                inventoryPicked = 'body'
            elif inHand:
                inventoryPicked = 'hand'
            elif inFeet:
                inventoryPicked = 'feet'
            for index, i in enumerate(eval(inventoryPicked)):
                if index <= 2:
                    tempY = 1
                else:
                    tempY = 2
                subSprites.append([i, base_sprite(width=50, height=50, image="images/items/"+ i +".png", x=55 + ((70*index)%210), y=0 + (70*tempY), scale=[50, 50])])
                if eval(inventoryPicked + "Eq") == i:
                    border = base_sprite(width=54, height=54, image="images/ItemBorder.png", x=53 + ((70*index)%210), y=-2 + (70*tempY), scale=[54, 54])
                    subGroup.add(border)
                subGroup.add(subSprites[len(subSprites) - 1][1])
        subGroup.update()
        subGroup.draw(s)
        #bigBlit(subGroup)
    if inFight:
        fightGroup.empty()
        enemyBattleSprite = base_sprite(width=54, height=54, image="images/enemies/"+ enemyEncountered +".png", x=220, y=34, scale=[60, 60])
        healthBarWidth = math.ceil(dist(enemyHealth, 0, enemyMaxHealth, 0, 100))
        healthBar = base_sprite(width=100, height=20, image="images/HealthBar.png", x=202, y=7, scale=[healthBarWidth, 20])
        playerHealthBarWidth = math.ceil(dist(currHealth, 0, healthStat, 0, 100))
        playerHealthBar = base_sprite(width=100, height=20, image="images/HealthBar.png", x=12, y=142, scale=[playerHealthBarWidth, 20])
        fightGroup.add(fightBackground)
        fightGroup.add(enemyBattleSprite)
        fightGroup.add(healthBarOutline)
        fightGroup.add(healthBar)
        fightGroup.add(playerHealthBarOutline)
        fightGroup.add(playerHealthBar)
        if enemyHealth <= 0:
            inFight = False
            enemyLevel = enemies[enemyEncountered].level
            expObtained = (random.randint(3, 4) * enemyLevel) - (enemyLevel - math.floor((enemyLevel / (random.randint(5, 6)))))
            con.output("You defeated " + enemyEncountered + " and gained "+ str(expObtained) +" XP!")
            if random.randint(0, 1) == 0:
                healthGained = math.floor(enemies[enemyEncountered].health / 3)
                con.output("Gained " + str(healthGained) + " health!")
                currHealth += healthGained
                if currHealth > healthStat:
                    currHealth = healthStat
            currXP += expObtained
            handleXP()
            move = True
        if playerTurn:
            yourTurnText = text("Your Turn", 5, 5, font_size=20)
            fightGroup.add(yourTurnText)
            fightGroup.add(runButton)
            fightGroup.add(attackButton)
            fightGroup.add(magicButton)
        else:
            enemyTurnText = text("Enemy's Turn", 5, 5, font_size=20)
            fightGroup.add(enemyTurnText)
            if delay == 0:
                delayAction = 'attack'
                delay = 60
            if delay == 1:
                if delayAction == "pass":
                    con.output("The enemy passes their turn")
                    playerTurn = True
                elif delayAction == "attack":
                    damage = enemies[enemyEncountered].attack
                    damage = random.randint(damage - math.floor((damage/4)), damage + math.floor((damage/4)))
                    damage += random.randint(0, floorLevel)
                    armorList = [spellsEq, headEq, bodyEq, handEq, feetEq]
                    for i in armorList:
                        damage -= items[i].health
                        if damage < 0:
                            damage = 0
                    con.output(enemyEncountered + " hit you for " + str(damage) + " damage!")
                    currHealth -= damage
                    if currHealth < 0:
                        currHealth = 0
                        inFight = False
                        inDead = True
                        subFloor = True
                    playerTurn = True
            if delay >= 1:
                delay -= 1
        fightGroup.update()
        fightGroup.draw(s)
        #bigBlit(fightGroup)
    if inDead:
        if subFloor:
            floorLevel -= 1
            if floorLevel < 1:
                floorLevel = 1
            genNewFloor = True
            currHealth = healthStat
            subFloor = False
            con.output("Oh dear, you are dead!")
        deadGroup.update()
        deadGroup.draw(s)
        #bigBlit(deadGroup)
    if inSwap:
        if newSwap:
            newSwap = False
            swapGroup.empty()
            swapGroup.add(back)
            swapGroup.add(swapText)
            swapGroup.add(dontSwapButton)
            swapSprites = []
            for index, i in enumerate(eval(items[itemFound].type)):
                if index <= 2:
                    tempY = 1
                else:
                    tempY = 2
                swapSprites.append([i, base_sprite(width=50, height=50, image="images/items/"+ i +".png", x=55 + ((70*index)%210), y=-30 + (70*tempY), scale=[50, 50])])
                swapGroup.add(swapSprites[len(swapSprites)-1][1])
        swapGroup.update()
        swapGroup.draw(s)
        #bigBlit(swapGroup)
    if inInspect:
        inspectGroup.empty()
        inspectGroup.add(back)
        inspectGroup.add(xButton)
        inspectGroup.add(base_sprite(width=80, height=80, image="images/items/"+inspecting+".png", x=(width/2) - 40, y=5))
        classTextInspect = text("Class: " + items[inspecting].itemClass, 0, 0, font_size=20)
        classTextInspect.rerender(0, 90, center=True)
        inspectGroup.add(classTextInspect)
        healthTextInspect = text("Health: " + str(items[inspecting].health), 0, 0, font_size=20)
        healthTextInspect.rerender(0, 115, center=True)
        inspectGroup.add(healthTextInspect)
        attackTextInspect = text("Attack: " + str(items[inspecting].attack), 0, 0, font_size=20)
        attackTextInspect.rerender(0, 140, center=True)
        inspectGroup.add(attackTextInspect)
        rangeTextInspect = text("Range: " + str(items[inspecting].range), 0, 0, font_size=20)
        rangeTextInspect.rerender(0, 165, center=True)
        inspectGroup.add(rangeTextInspect)
        magicTextInspect = text("Magic: " + str(items[inspecting].magic), 0, 0, font_size=20)
        magicTextInspect.rerender(0, 190, center=True)
        inspectGroup.add(magicTextInspect)
        speedTextInspect = text("Speed: " + str(items[inspecting].speed), 0, 0, font_size=20)
        speedTextInspect.rerender(0, 215, center=True)
        inspectGroup.add(speedTextInspect)
        inspectGroup.update()
        inspectGroup.draw(s)
        #bigBlit(inspectGroup)
    if inBoss:
        bossGroup.empty()
        bossGroup.add(fightBackground)
        if bossHealth <= 0:
            bossHealth = 1
            XPGained = random.randint(4 * floorLevel, 5 * floorLevel)
            con.output("You defeated " + bossEncountered + " for " + str(XPGained) + " XP!")
            currXP += XPGained
            handleXP()
            inBoss = False
            floorLevel += 1
            genNewFloor = True
        if bossTurn:
            if newTurn:
                wait = 60
                waitAction = "attack"
                newTurn = False
            turnText = text(bossEncountered + "'s turn", 50, 50, font_size=16)
        else:
            turnText = text("Your turn", 50, 50, font_size=16)
        turnText.rerender(0, 50, center=True)
        turnText.rerender(turnText.rect.x - 68, 50)
        bossGroup.add(turnText)
        healthBarOutlineBoss = base_sprite(width=104, height=24, image="images/HealthBarOutline.png", x=5, y=183)
        healthBarWidthBoss = math.ceil(dist(currHealth, 0, healthStat, 0, 100))
        healthBarBoss = base_sprite(width=100, height=20, image="images/HealthBar.png", x=7, y=185, scale=[healthBarWidthBoss, 20])
        bossSprite = base_sprite(width=80, height=80, image="images/bosses/"+bossEncountered+".png", x=215, y=5)
        bossHealthBarOutline = base_sprite(width=104, height=24, image="images/HealthBarOutline.png", x=40, y=20)
        bossHealthBarWidth = math.ceil(dist(bossHealth, 0, bossMaxHealth, 0, 100))
        bossHealthBar = base_sprite(width=100, height=20, image="images/HealthBar.png", x=42, y=22, scale=[bossHealthBarWidth, 20])
        bossGroup.add(attackButton)
        bossGroup.add(magicButton)
        bossGroup.add(healthBarOutlineBoss)
        bossGroup.add(healthBarBoss)
        bossGroup.add(bossSprite)
        bossGroup.add(bossHealthBarOutline)
        bossGroup.add(bossHealthBar)
        if wait > 0:
            wait -= 1
        if wait == 1:
            if waitAction == "attack":
                damage = random.randint(bossAttack - math.floor(bossAttack/4), bossAttack + math.floor(bossAttack/4))
                for i in [spellsEq, headEq, bodyEq, handEq, feetEq]:
                    damage -= items[i].health

                con.output(bossEncountered + " hits you for " + str(damage) + "!")
                currHealth -= damage
                bossTurn = False
        if currHealth <= 0:
            bossHealth = 0
            inDead = True
            inBoss = False
            currHealth = healthStat
            floorLevel -= 2

        bossGroup.draw(s)
        #bigBlit(bossGroup)
    if inFigureLoad:
        if newLoad:
            rfRead()
            newLoad = False
            inGame = True
            genNewFloor = True
            inFigureLoad = False
        loadFigureGroup.draw(s)
    if inBetween:
        betweenGroup.empty()
        betweenGroup.add(back)
        if not inSave:
            betweenFloorText = text("Completed floor " + str(floorLevel) +"!", 0, 0)
            betweenFloorText.rerender(0, 10, center=True)
            betweenGroup.add(betweenFloorText)
            betweenGroup.add(saveButton)
            betweenGroup.add(continueButton)
        else:
            betweenFloorText = text("Place figurine on reader", 0, 0)
            betweenFloorText.rerender(0, 10, center=True)
            betweenGroup.add(betweenFloorText)
            rfWrite()
            inSave = False
        betweenGroup.draw(s)
    if inCon:
        con.draw()
    pygame.display.update()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
