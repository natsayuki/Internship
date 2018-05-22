# IMPORTS
import pygame
import random
from random import randint
import math
import PyCon

# INIT
pygame.init()
width = 320
height = 240
s = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption("Internship")

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

classPicked = ''
actionsToRun = []
enemies = {'Devil': {'h': 10, 'a': 5, 's': 5, 'm': 0, 'r': 0, 'l': 3}, 'Ghost': {'h': 10, 'a': 5, 's': 3, 'm': 5, 'r': 3, 'l': 3}, 'Goblin': {'h': 5, 'a': 7, 's': 7, 'm': 0, 'r': 0, 'l': 4},
 "Alligator": {'h': 50, 'a': 25, 's': 25, 'm': 0, 'r': 0, 'l': 35}, "Bat": {'h': 20, 'a': 5, 's': 15, 'm': 15, 'r': 5, 'l': 15}, "Bear": {'h': 45, 'a': 30, 's': 25, 'm': 0, 'r': 10, 'l': 40},
 "Bird": {'h': 20, 'a': 5, 's': 15, 'm': 0, 'r': 5, 'l': 10}, "Bomb": {'h': 5, 'a': 20, 's': 10, 'm': 10, 'r': 0, 'l': 25}, "Dino": {'h': 100, 'a': 75, 's': 50, 'm': 0, 'r': 0, 'l': 85},
 'Frog': {'h': 35, 'a': 15, 's': 25, 'm': 25, 'r': 0, 'l': 35}, "Horse": {'h': 50, 'a': 50, 's': 50, 'm': 0, 'r': 0, 'l': 65}, 'Jellyfish': {'h': 15, 'a': 10, 's': 5, 'm': 5, 'r': 0, 'l': 10},
 "Monkey": {'h': 20, 'a': 10, 's': 15, 'm': 0, 'r': 10, 'l': 15}, "Rat": {'h': 1, 'a': 1, 's': 5, 'm': 0, 'r': 0, 'l': 1}, "Robber": {'h': 30, 'a': 45, 's': 30, 'm': 0, 'r': 20, 'l': 65},
 "Slime": {'h': 5, 'a': 5, 's': 5, 'm': 10, 'r': 0, 'l': 8}, "Snake": {'h': 15,'a': 15, 's': 15, 'm': 0, 'r': 0, 'l': 20}, "Spider": {'h': 10, 'a': 5, 's': 5, 'm': 0, 'r': 5, 'l': 10}}

healthStat = 0
attackStat = 0
speedStat = 0
magicStat = 0
rangeStat = 0

waitAction = None


con = PyCon.PyCon(s,
                      (0,0,320,240 / 2),
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
    attack = random.randint(0, points)
    health = random.randint(0, points)
    speed = random.randint(0, points)
    magic = random.randint(0, points)
    range = random.randint(0, points)

    return [attack, health, speed, magic, range]
def genFloor(mapWidth, mapHeight, minRooms, maxRooms):
    mapArray = []
    for y in range(0, mapHeight):
        mapArray.append([])
        for x in range(0, mapWidth):
            mapArray[y].append('o')
    start = [random.randint(0, mapWidth-1), random.randint(0, mapHeight-1)]
    mapArray[start[0]][start[1]] = 'x'
    rooms = 0
    for y in range(0, mapHeight):
        for x in range(0, mapWidth):
            if y - 1 > -1 and mapArray[y - 1][x] == 'x':
                if random.randint(0, 1) == 0 and rooms < maxRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
                elif rooms < minRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
            if y + 1 < mapHeight and mapArray[y + 1][x] == 'x':
                if random.randint(0, 1) == 0 and rooms < maxRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
                elif rooms < minRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
            if x - 1 > -1 and mapArray[y][x-1] == 'x':
                if random.randint(0, 2) == 0 and rooms < maxRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
                elif rooms < minRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
            if x + 1 < mapWidth and mapArray[y][x+1] == 'x':
                if random.randint(0, 2) == 0 and rooms < maxRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
                elif rooms < minRooms:
                    mapArray[y][x] = 'x'
                    rooms += 1
    mapArray[start[0]][start[1]] = 'x'
    for y in range(0, mapHeight-1):
        for x in range(0, mapWidth-1):
            if mapArray[y][x] == 'x':
                start = [x, y]
                break
    return [start, mapArray, rooms]
def dist(n, start1, stop1, start2, stop2):
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2
def newTile(x, y, type='empty'):
    if type == 'empty':
        return base_sprite(width=10, height=10, image="images/roomTile.png", x=x, y=y)
    if type == 'in':
        return base_sprite(width=10, height=10, image="images/roomTileIn.png", x=x, y=y)
def drawMiniMap():
    for i in miniMap:
        mapGroup.add(newTile(i[0]*10 + indX, i[1]*10 + indY))
    roomsNumText = text(str(len(miniMap)) + '/' + str(rooms), 60, 10, font_size = 16)
    mapGroup.add(newTile(playerX*10 + indX, playerY*10 + indY, 'in'))
    mapGroup.add(roomsText)
    mapGroup.add(roomsNumText)
    mapGroup.add(roomsText)
    mapGroup.add(roomsNumText)
def actionTreasure():
    con.output("Found treasure!")
    chest = base_sprite(width=80, height=80, image="images/treasure.png", x=(width/2) - 40, y=(height/2) - 40)
    roomGroup.add(chest)
def actionEnemy():
    enemy = list(enemies.keys())[random.randint(0, len(enemies)-1)]
    enemySprite = base_sprite(width=80, height=80, image="images/enemies/"+enemy+".png", x=(width/2) - 40, y=(height/2) - 40)
    roomGroup.add(enemySprite)
    con.output("Found " + enemy + "!")
    waitAction = battle(enemy)
def actionNothing():
    actions = ["PictureOfPotato", "PictureOfChicken"]
    action = actions[random.randint(0, len(actions) -1)]
    actionSprite = base_sprite(width=80, height=80, image="images/"+action+".png", x=(width/2) - 40, y=(height/2) - 40)
    roomGroup.add(actionSprite)
    con.output("Found " + action + "!")
def battle(enemy):
    con.output("Encountered " + enemy + "!")



# CLASSES
class base_sprite(pygame.sprite.Sprite):
        def __init__(self, color=(0,0,0), width=0, height=0, image=None,x=0,y=0):
            pygame.sprite.Sprite.__init__(self)
            if "Surface" in type(image).__name__:
                self.image = image
            else:
                self.image = pygame.image.load(image)
            pygame.draw.rect(self.image, color, [5000000,5000000,width,height])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

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


# text = text("TEST", "Comic Sans MS",16,(0, 0, 0),15,15,255)
# SPRITES
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

stats = genStats(20)
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

inventoryGroup.add(back)






# MAIN
while running:
    events = pygame.event.get()
    for event in events:
        namePass = False
        classPick = False
        endGen = False
        move = False
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if inWait:
                waitAction()
            elif button.rect.collidepoint(event.pos) and inHome:
                inHome = False
                inLoad = True
            elif scanButton.rect.collidepoint(event.pos) and inLoad:
                print("Load Screen")
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
                stats = genStats(20)
                characterGenGroup2.remove(attackText)
                characterGenGroup2.remove(healthText)
                attackText = text(str(stats[0]), 200, 15)
                healthText = text(str(stats[1]), 200, 50)
                characterGenGroup2.add(attackText)
                characterGenGroup2.add(healthText)
            elif continueButton.rect.collidepoint(event.pos) and inCharacterGen2:
                inCharacterGen2 = False
                endGen = True
            elif NoButton.rect.collidepoint(event.pos) and inCharacterGenEnd:
                inCharacterGenEnd = False
                inLoad = True
            elif YesButton.rect.collidepoint(event.pos) and inCharacterGenEnd:
                inCharacterGenEnd = False
                inGame = True
            elif topDoor.rect.collidepoint(event.pos) and inGame and 'up' in directions and not inWait:
                playerY -= 1
                move = True
            elif bottomDoor.rect.collidepoint(event.pos) and inGame and 'down' in directions and not inWait:
                playerY += 1
                move = True
            elif leftDoor.rect.collidepoint(event.pos) and inGame and 'left' in directions and not inWait:
                playerX -= 1
                move = True
            elif rightDoor.rect.collidepoint(event.pos) and inGame and 'right' in directions and not inWait:
                playerX += 1
                move = True
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
            nameText = text(name, 0, 0, font_size=20)
            nameText.rerender(0, 35, center=True)
            classText = text(classPicked, 0, 0, font_size=20)
            classText.rerender(0, 55, center=True)
            attackText = text("Attack: " + str(stats[0]), 0, 0, font_size=20)
            attackText.rerender(0, 80, center=True)
            healthText = text("Health: " + str(stats[1]), 0, 0, font_size=20)
            healthText.rerender(0, 105, center=True)
            characterGenGroupEnd.add(nameText)
            characterGenGroupEnd.add(classText)
            characterGenGroupEnd.add(attackText)
            characterGenGroupEnd.add(healthText)
        if move:
            roomGroup.empty()
            if [playerX, playerY] not in miniMap:
                actions = [actionTreasure, actionEnemy, actionNothing, actionNothing]
                option = random.randint(0, len(actions) -1)
                actionsToRun.append(actions[option])
                miniMap.append([playerX, playerY])
            newMap = True
            move = False

    # END UPDATE
    homeScreenGroup.update()
    nameConfirmScreenGroup.update()
    if inHome:
        homeScreenGroup.draw(s)
    if inLoad:
        loadScreenGroup.draw(s)
    if inName:
        nameScreenGroup.draw(s)
    if inNameConfirm:
        nameConfirmScreenGroup.empty()
        nameConfirmScreenGroup.add(NameConfirmBackground)
        nameConfirmScreenGroup.add(YesButton)
        nameConfirmScreenGroup.add(NoButton)
        nameConfirmScreenGroup.add(nameText)
        nameConfirmScreenGroup.draw(s)
    if inCharacterGen:
        characterGenGroup.draw(s)
    if inCharacterGen1:
        characterGenGroup1.draw(s)
    if inCharacterGen2:
        characterGenGroup2.draw(s)
    if inCharacterGenEnd:
        characterGenGroupEnd.empty()
        characterGenGroupEnd.add(characterGenEndBackground)
        characterGenGroupEnd.add(YesButton)
        characterGenGroupEnd.add(NoButton)
        characterGenGroupEnd.add(nameText)
        characterGenGroupEnd.add(classText)
        characterGenGroupEnd.add(attackText)
        characterGenGroupEnd.add(healthText)
        characterGenGroupEnd.draw(s)
    if inGame:
        directions = []
        if genNewFloor:
            size = math.floor(dist(floorLevel, 1, 99, 3, 20))
            minRooms = math.floor(dist(floorLevel, 1, 99, 3, 300))
            maxRooms = math.floor(dist(floorLevel, 1, 99, 7, 350))
            mapArray = genFloor(size, size, minRooms, maxRooms)
            start = mapArray[0]
            rooms = mapArray[2]
            mapArray = mapArray[1]
            genNewFloor = False
            playerX = start[0]
            playerY = start[1]
            print(playerX, playerY)
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
        for i in actionsToRun:
            i()
        actionsToRun = []

        roomGroup.draw(s)
    if inMap:
        if newMap:
            mapGroup.empty()
            drawMiniMap()
            newMap = False
        mapGroup.draw(s)
    if inInventory:
        inventoryGroup.draw(s)
    if inCon:
        con.draw()
    pygame.display.flip()
    clock.tick(60)
