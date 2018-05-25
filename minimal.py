import pygame
class base_sprite(pygame.sprite.Sprite):
        def __init__(self, color=(0,0,0), width=0, height=0, image=None,x=0,y=0, scale=None):
            pygame.sprite.Sprite.__init__(self)
            if "Surface" in type(image).__name__:
                self.image = image
            else:
                self.image = pygame.image.load(image)
            if scale != None:
                self.image = pygame.transform.scale(self.image, (scale[0], scale[1]))
            pygame.draw.rect(self.image, color, [5000000,5000000,width,height])
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

pygame.init()
width = 320
height = 240
s = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

gameGroup = pygame.sprite.Group()
inventoryGroup = pygame.sprite.Group()

back = base_sprite(width=320, height=240, image="images/back.png", x=0, y=0)

headBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=180, y=10, scale=[50, 50])
handBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=250, y=94, scale=[50, 50])
bodyBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=180, y=94, scale=[50, 50])
feetBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=180, y=178, scale=[50, 50])
spellBorder = base_sprite(width=64, height=64, image="images/ItemBorder.png", x=110, y=10, scale=[50, 50])
symbol =  base_sprite(width=100, height=100, image="images/mageSmall.png", x=5, y=(height/2)-50)

gameGroup.add(back)

inInventory = False
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                inInventory = not inInventory

    gameGroup.draw(s)
    if inInventory:
        inventoryGroup.add(back)
        inventoryGroup.add(symbol)
        inventoryGroup.add(headBorder)
        inventoryGroup.add(handBorder)
        inventoryGroup.add(bodyBorder)
        inventoryGroup.add(feetBorder)
        inventoryGroup.add(spellBorder)
        inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/BasicHat.png", x=180, y=10, scale=[50, 50]))
        inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/BasicThingToHitPeopleWith.png", x=250, y=94, scale=[50, 50]))
        inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/BasicShirt.png", x=180, y=94, scale=[50, 50]))
        inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/BasicShoes.png", x=180, y=178, scale=[50, 50]))
        inventoryGroup.add(base_sprite(width=64, height=64, image="images/items/BasicBook.png", x=110, y=10, scale=[50, 50]))
        inventoryGroup.draw(s)
    clock.tick(60)
    pygame.display.flip()
