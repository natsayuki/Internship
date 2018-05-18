# IMPORTS
import pygame
import random

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

classPicked = ''

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
    health = points - attack
    return [attack, health]


# CLASSES
class base_sprite(pygame.sprite.Sprite): #turtle spawned in middle of screen
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

class text(pygame.sprite.Sprite): #helpful class for rendering text as a sprite
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
attackText = text(str(stats[0]), 200, 15)
healthText = text(str(stats[1]), 200, 50)
attackSayText = text("Attack: ", 100, 15)
healthSayText = text("Health: ", 100, 50)
rollButton = base_sprite(width=70, height=50, image="images/RollButton.png", x=45, y=170)
continueButton = base_sprite(width=70, height=50, image="images/ContinueButton.png", x=205, y=170)

characterGenGroup2.add(back)
characterGenGroup2.add(attackText)
characterGenGroup2.add(healthText)
characterGenGroup2.add(rollButton)
characterGenGroup2.add(continueButton)
characterGenGroup2.add(attackSayText)
characterGenGroup2.add(healthSayText)

characterGenEndBackground = base_sprite(width=320, height=240, image="images/CharacterGenEndBackground.png", x=0, y=0)
characterGenGroupEnd.add(characterGenEndBackground)
characterGenGroupEnd.add(YesButton)
characterGenGroupEnd.add(NoButton)





# MAIN
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button.rect.collidepoint(event.pos) and inHome:
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
                nameConfirmScreenGroup.remove(nameText)
                inLoad = True
        if namePass:
            inName = False
            inNameConfirm = True
            nameText = text(name, 0, 0)
            nameText.rerender(0, 30, center=True)
            nameConfirmScreenGroup.remove(nameText)
            nameConfirmScreenGroup.add(nameText)
        if classPick:
            print(classPicked)
            symbol = base_sprite(width=100, height=100, image="images/"+ classPicked +"Small.png", x=(width/2) - 50, y=80)
            characterGenGroup2.add(symbol)
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
        nameConfirmScreenGroup.draw(s)
    if inCharacterGen:
        characterGenGroup.draw(s)
    if inCharacterGen1:
        characterGenGroup1.draw(s)
    if inCharacterGen2:
        characterGenGroup2.draw(s)
    if inCharacterGenEnd:
        characterGenGroupEnd.draw(s)
    pygame.display.flip()
    clock.tick(60)
