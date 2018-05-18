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

# FUNCTIONS
def randname(gender):
    if gender == 'male':
        name = ''
        with open ("names/maleFirst.txt", "r") as file:
            data = file.readlines()
        name += data[random.randint(0, len(data))].replace('\n', ' ')
        with open ("names/maleLast.txt", "r") as file:
            data = file.readlines()
        name += data[random.randint(0, len(data))].replace('\n', ' ')
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
nameText = text('', 0, 0)
nameText.rerender(0, 80, center=True)
YesButton =  base_sprite(width=70, height=50, image="images/YesButton.png", x=45, y=170)
NoButton =  base_sprite(width=70, height=50, image="images/NoButton.png", x=205, y=170)


nameConfirmScreenGroup.add(NameConfirmBackground)
nameConfirmScreenGroup.add(nameText)
nameConfirmScreenGroup.add(YesButton)
nameConfirmScreenGroup.add(NoButton)




# MAIN
while running:
    events = pygame.event.get()
    for event in events:
        namePass = False
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
            elif FemaleButton.rect.collidepoint(event.pos)and  inName:
                name = randname('female')
                namePass = True
            elif YesButton.rect.collidepoint(event.pos) and inNameConfirm:
                None
            elif NoButton.rect.collidepoint(event.pos) and inNameConfirm:
                nameConfirmScreenGroup.remove(nameText)
                inNameConfirm = False
                inName = True
        if namePass:
            inName = False
            inNameConfirm = True
            nameText = text(name, 0, 0)
            nameText.rerender(0, 30, center=True)
            nameConfirmScreenGroup.remove(nameText)
            nameConfirmScreenGroup.add(nameText)



    # END UPDATE
    homeScreenGroup.update()
    if inHome:
        homeScreenGroup.draw(s)
    if inLoad:
        loadScreenGroup.draw(s)
    if inName:
        nameScreenGroup.draw(s)
    if inNameConfirm:
        nameConfirmScreenGroup.draw(s)
    pygame.display.flip()
    clock.tick(60)
