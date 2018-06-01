# if bossHealth <= 0:
#     bossHealth = 0
#     inBossEnd = True
#     inBoss = False
# bossGroup.empty()
# bossGroup.add(fightBackground)
# if bossTurn:
#     if bossNewTurn:
#         if bossHealth > (bosses[bossEncountered].health/3)*2:
#             exec(lowerCaseFirst(bossEncountered) + "Phase = 1")
#         elif bossHealth > (bosses[bossEncountered].health/3):
#             exec(lowerCaseFirst(bossEncountered) + "Phase = 2")
#         else:
#             exec(lowerCaseFirst(bossEncountered) + "Phase = 3")
#         bossNewTurn = False
# else:
#     healthBarOutlineBoss = base_sprite(width=104, height=24, image="images/HealthBarOutline.png", x=5, y=183)
#     healthBarWidthBoss = math.ceil(dist(currHealth, 0, healthStat, 0, 100))
#     healthBarBoss = base_sprite(width=100, height=20, image="images/HealthBar.png", x=7, y=185, scale=[healthBarWidthBoss, 20])
#     bossSprite = base_sprite(width=80, height=80, image="images/bosses/"+bossEncountered+".png", x=215, y=5)
#     bossHealthBarOutline = base_sprite(width=104, height=24, image="images/HealthBarOutline.png", x=40, y=20)
#     bossHealthBarWidth = math.ceil(dist(bossHealth, 0, bossMaxHealth, 0, 100))
#     bossHealthBar = base_sprite(width=100, height=20, image="images/HealthBar.png", x=42, y=22, scale=[bossHealthBarWidth, 20])
#     bossGroup.add(attackButton)
#     bossGroup.add(magicButton)
#     bossGroup.add(healthBarOutlineBoss)
#     bossGroup.add(healthBarBoss)
#     bossGroup.add(bossSprite)
#     bossGroup.add(bossHealthBarOutline)
#     bossGroup.add(bossHealthBar)
# if smolkPhase == 1:
#     if newPhase:
#         wavePos = [-80]
#         waves = []
#         smolkPlayerX = 130
#         smolkPlayerY = 160
#         newPhase = False
#         inLeft = False
#         inRight = False
#         inJump = False
#         jumpUp = True
#     waves = []
#     for x in wavePos:
#         print(x)
#         waves.append(base_sprite(width=40, height=20, image="images/bosses/smolk/wave.png", x=x, y=180))
#         bossGroup.add(waves[len(waves) -1])
#     for i in range(0, len(wavePos)):
#         wavePos[i] += 1
#         if wavePos[i] > width:
#             del wavePos[i]
#     if wavePos == []:
#         bossTurn = False
#         smolkPhase = 0
#     upArrow = base_sprite(width=60, height=80, image="images/bosses/smolk/upArrow.png", x=130, y=5)
#     leftArrow = base_sprite(width=80, height=60, image="images/bosses/smolk/leftArrow.png", x=5, y=90)
#     rightArrow = base_sprite(width=80, height=60, image="images/bosses/smolk/rightArrow.png", x=235, y=90)
#     player = base_sprite(width=60, height=80, image="images/bosses/smolk/player.png", x=smolkPlayerX, y=smolkPlayerY)
#     bossGroup.add(player)
#     bossGroup.add(upArrow)
#     bossGroup.add(leftArrow)
#     bossGroup.add(rightArrow)
#     print("smolkPhase1")
#     events = pygame.event.get()
#     for event in events:
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         if pygame.mouse.get_pressed()[0]:
#             if leftArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 inLeft = True
#             elif rightArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 inRight = True
#             elif upArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 if not inJump:
#                     inJump = True
#         elif not pygame.mouse.get_pressed()[0]:
#             inRight = False
#             inLeft = False
#     if inLeft:
#         smolkPlayerX -= 3
#     if inRight:
#         smolkPlayerX += 3
#     if inJump:
#         if jumpUp:
#             smolkPlayerY -= 3
#             if smolkPlayerY < 60:
#                 jumpUp = False
#         else:
#             smolkPlayerY += 3
#             if smolkPlayerY > 160:
#                 jumpUp = True
#                 inJump = False
#                 smolkPlayerY = 160
#     smolkPlayerX %= width
#     for i in waves:
#         if pygame.sprite.collide_rect(i, player) and hitTimer == 0:
#             currHealth -= (1/4) * bossAttack
#             hitTimer = 60
#         if currHealth <= 0:
#             currHealth = 0
#             inDead = True
#             currHealth = healthStat
#             genNewFloor = True
#             inBoss = False
#     if hitTimer > 0:
#         hitTimer -= 1
#     print(hitTimer)
#
# elif smolkPhase == 2:
#     if newPhase:
#         wavePos = []
#         for i in range(0, random.randint(6, 10)):
#             if random.randint(0, 2) == 0:
#                 wavePos.append([random.randint(-1500, -80), 0])
#             else:
#                 wavePos.append([random.randint(320, 1500), 1])
#         print(wavePos)
#         waves = []
#         smolkPlayerX = 130
#         smolkPlayerY = 160
#         newPhase = False
#         inLeft = False
#         inRight = False
#         inJump = False
#         jumpUp = True
#     waves = []
#     for x in wavePos:
#         x = x[0]
#         waves.append(base_sprite(width=40, height=20, image="images/bosses/smolk/wave.png", x=x, y=180))
#         bossGroup.add(waves[len(waves) -1])
#     for i in range(0, len(wavePos)-1):
#         if wavePos[i][1] == 0:
#             wavePos[i][0] += 2
#         elif wavePos[i][1] == 1:
#             wavePos[i][0] -= 2
#         if wavePos[i][0] > width and wavePos[i][1] == 0:
#             del wavePos[i]
#         elif wavePos[i][0] < -80 and wavePos[i][1] == 1:
#             del wavePos[i]
#     if len(wavePos) == 1:
#         bossTurn = False
#         smolkPhase = 0
#     upArrow = base_sprite(width=60, height=80, image="images/bosses/smolk/upArrow.png", x=130, y=5)
#     leftArrow = base_sprite(width=80, height=60, image="images/bosses/smolk/leftArrow.png", x=5, y=90)
#     rightArrow = base_sprite(width=80, height=60, image="images/bosses/smolk/rightArrow.png", x=235, y=90)
#     player = base_sprite(width=60, height=80, image="images/bosses/smolk/player.png", x=smolkPlayerX, y=smolkPlayerY)
#     bossGroup.add(player)
#     bossGroup.add(upArrow)
#     bossGroup.add(leftArrow)
#     bossGroup.add(rightArrow)
#     events = pygame.event.get()
#     for event in events:
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         if pygame.mouse.get_pressed()[0]:
#             if leftArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 inLeft = True
#             elif rightArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 inRight = True
#             elif upArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 if not inJump:
#                     inJump = True
#         elif not pygame.mouse.get_pressed()[0]:
#             inRight = False
#             inLeft = False
#     if inLeft:
#         smolkPlayerX -= 3
#     if inRight:
#         smolkPlayerX += 3
#     if inJump:
#         if jumpUp:
#             smolkPlayerY -= 3
#             if smolkPlayerY < 60:
#                 jumpUp = False
#         else:
#             smolkPlayerY += 3
#             if smolkPlayerY > 160:
#                 jumpUp = True
#                 inJump = False
#                 smolkPlayerY = 160
#     smolkPlayerX %= width
#     for i in waves:
#         if pygame.sprite.collide_rect(i, player) and hitTimer == 0:
#             currHealth -= (1/4) * bossAttack
#         if currHealth <= 0:
#             currHealth = 0
#             inDead = True
#             currHealth = healthStat
#             genNewFloor = True
#             inBoss = False
#         hitTimer = 60
#     if hitTimer > 0:
#         hitTimer -= 1
#     print("smolkPhase2")
# elif smolkPhase == 3:
#     if newPhase:
#         wavePos = []
#         for i in range(0, random.randint(3, 6)):
#             if random.randint(0, 2) == 0:
#                 wavePos.append([random.randint(-1000, -80), 0])
#             else:
#                 wavePos.append([random.randint(320, 1000), 1])
#         print(wavePos)
#         waves = []
#         smolkPlayerX = 130
#         smolkPlayerY = 160
#         newPhase = False
#         inLeft = False
#         inRight = False
#         inJump = False
#         jumpUp = True
#     waves = []
#     for x in wavePos:
#         x = x[0]
#         waves.append(base_sprite(width=40, height=20, image="images/bosses/smolk/wave.png", x=x, y=180))
#         bossGroup.add(waves[len(waves) -1])
#     for i in range(0, len(wavePos)-1):
#         if wavePos[i][1] == 0:
#             wavePos[i][0] += 3
#         elif wavePos[i][1] == 1:
#             wavePos[i][0] -= 3
#         if wavePos[i][0] > width and wavePos[i][1] == 0:
#             del wavePos[i]
#         elif wavePos[i][0] < -80 and wavePos[i][1] == 1:
#             del wavePos[i]
#     if len(wavePos) == 1:
#         bossTurn = False
#         smolkPhase = 0
#     upArrow = base_sprite(width=60, height=80, image="images/bosses/smolk/upArrow.png", x=130, y=5)
#     leftArrow = base_sprite(width=80, height=60, image="images/bosses/smolk/leftArrow.png", x=5, y=90)
#     rightArrow = base_sprite(width=80, height=60, image="images/bosses/smolk/rightArrow.png", x=235, y=90)
#     player = base_sprite(width=60, height=80, image="images/bosses/smolk/player.png", x=smolkPlayerX, y=smolkPlayerY)
#     bossGroup.add(player)
#     bossGroup.add(upArrow)
#     bossGroup.add(leftArrow)
#     bossGroup.add(rightArrow)
#     events = pygame.event.get()
#     for event in events:
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         if pygame.mouse.get_pressed()[0]:
#             if leftArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 inLeft = True
#             elif rightArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 inRight = True
#             elif upArrow.rect.collidepoint(pygame.mouse.get_pos()):
#                 if not inJump:
#                     inJump = True
#         elif not pygame.mouse.get_pressed()[0]:
#             inRight = False
#             inLeft = False
#     if inLeft:
#         smolkPlayerX -= 3
#     if inRight:
#         smolkPlayerX += 3
#     if inJump:
#         if jumpUp:
#             smolkPlayerY -= 3
#             if smolkPlayerY < 60:
#                 jumpUp = False
#         else:
#             smolkPlayerY += 3
#             if smolkPlayerY > 160:
#                 jumpUp = True
#                 inJump = False
#                 smolkPlayerY = 160
#     smolkPlayerX %= width
#     for i in waves:
#         if pygame.sprite.collide_rect(i, player) and hitTimer == 0:
#             currHealth -= (1/4) * bossAttack
#         if currHealth <= 0:
#             currHealth = 0
#             inDead = True
#             currHealth = healthStat
#             genNewFloor = True
#             inBoss = False
#         hitTimer = 60
#     if hitTimer > 0:
#         hitTimer -= 1
#
#     print("smolkPhase3")
