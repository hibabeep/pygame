import pygame
import sys
import random
import math 
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("mi.mp3")  
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
fenetre = pygame.display.set_mode( (600,187) ) 
pygame.display.set_caption("Art Robbery")
imgmap=pygame.image.load("map.jpg")
imgthief=pygame.image.load("thief.png")
imgpolice=pygame.image.load("police.png")
imggold=pygame.image.load("go.png")
imglady=pygame.image.load("la.jpg")
imgsphinx=pygame.image.load("sps.png")
imgmetal=pygame.image.load("ms.png")
imgmona=pygame.image.load("ml.jpg")
imgafra=pygame.image.load("af.jpg")
imgstarry=pygame.image.load("sn.jpg")
imgguy=pygame.image.load("ss.png")
imgbroken=pygame.image.load("brj.png")
imgroman=pygame.image.load("bj.png")
imgjar=pygame.image.load("gj.png")
imgmus=pygame.image.load("museum.png")
rectgold = pygame.Rect(220, 95, 54, 54)
rectlady = pygame.Rect(215, 15, 64, 64)
rectsphinx = pygame.Rect(525, 110, 64, 64)
rectmetal = pygame.Rect(220, 140, 54, 54)
rectmona = pygame.Rect(295, 15, 64, 64)
rectafra = pygame.Rect(450, 15, 64, 64)
rectstarry = pygame.Rect(525, 15, 64, 64)
rectguy = pygame.Rect(295, 95, 64, 64)
rectbroken = pygame.Rect(305, 145, 44, 44)
rectroman = pygame.Rect(455, 95, 54, 54)
rectjar = pygame.Rect(455, 140, 54, 54)
homescreen = 0
diffscreen = 1
gamescreen = 2
jeu=homescreen
difficulte = "facile"
alert_triggered = False
alert_start_time = 0
alert_duration = 40000  

imgpolice = pygame.transform.scale(imgpolice, (64, 64))
imgthief = pygame.transform.scale(imgthief, (42, 42))
imggold = pygame.transform.scale(imggold, (54, 54))
imglady = pygame.transform.scale(imglady, (64, 64))
imgsphinx = pygame.transform.scale(imgsphinx, (64, 64))
imgsphinx = pygame.transform.rotate(imgsphinx,90)
imgmetal = pygame.transform.scale(imgmetal, (54, 54))
imgmona = pygame.transform.scale(imgmona, (64, 64))
imgafra = pygame.transform.scale(imgafra, (64, 64))
imgstarry = pygame.transform.scale(imgstarry, (64, 64))
imgguy = pygame.transform.scale(imgguy, (64, 64))
imgbroken = pygame.transform.scale(imgbroken, (44, 44))
imgroman = pygame.transform.scale(imgroman, (54, 54))
imgjar = pygame.transform.scale(imgjar, (54, 54))
positionthief = pygame.Rect(125, 75, 42, 42)
positionpolice = pygame.Rect(75, 25, 42, 42)
police_direction = random.choice(['up', 'down', 'left', 'right'])
police_speed = 2
change_direction_counter = 0
positions_police = []
stolenrect = []

def dessiner():
    global imgthief, imgpolice
    fenetre.blit(imgmap,(0,0))    
    if rectgold in rectt:
        fenetre.blit(imggold, rectgold)
    if rectlady in rectt:
        fenetre.blit(imglady, rectlady)
    if rectsphinx in rectt:
        fenetre.blit(imgsphinx, rectsphinx)
    if rectmetal in rectt:
        fenetre.blit(imgmetal, rectmetal)
    if rectmona in rectt:
        fenetre.blit(imgmona, rectmona)
    if rectafra in rectt:
        fenetre.blit(imgafra, rectafra)
    if rectstarry in rectt:
        fenetre.blit(imgstarry, rectstarry)
    if rectguy in rectt:
        fenetre.blit(imgguy, rectguy)
    if rectbroken in rectt:
        fenetre.blit(imgbroken, rectbroken)
    if rectroman in rectt:
        fenetre.blit(imgroman, rectroman)
    if rectjar in rectt:
        fenetre.blit(imgjar, rectjar)
    fenetre.blit(imgthief, positionthief)
    fenetre.blit(imgpolice, positionpolice)
    for pos in positions_police:
        fenetre.blit(imgpolice, pos)
        
def draw_vision_cone():
    cone_surface = pygame.Surface((600, 187), pygame.SRCALPHA)
    cx, cy = positionpolice.center
    length = 100
    angle_width = 60 
    direction_angles = {'up': -90,'down': 90,'left': 180,'right': 0}
    base_angle = direction_angles.get(police_direction, 0)
    left_angle = math.radians(base_angle - angle_width / 2)
    right_angle = math.radians(base_angle + angle_width / 2)
    x1 = cx + length * math.cos(left_angle)
    y1 = cy + length * math.sin(left_angle)
    x2 = cx + length * math.cos(right_angle)
    y2 = cy + length * math.sin(right_angle)
    pygame.draw.polygon(cone_surface,(255, 255, 150, 100),  [(cx, cy), (x1, y1), (x2, y2)])
    fenetre.blit(cone_surface, (0, 0))
    
def check_vision_cone_collision():
    global alert_triggered, alert_start_time
    cx, cy = positionpolice.center
    length = 100
    angle_width = 60
    direction_angles = {'up': -90, 'down': 90, 'left': 180, 'right': 0}
    base_angle = direction_angles.get(police_direction, 0)
    left_angle = math.radians(base_angle - angle_width / 2)
    right_angle = math.radians(base_angle + angle_width / 2)
    x1 = cx + length * math.cos(left_angle)
    y1 = cy + length * math.sin(left_angle)
    x2 = cx + length * math.cos(right_angle)
    y2 = cy + length * math.sin(right_angle)
    cone_polygon = [(cx, cy), (x1, y1), (x2, y2)]
    def point_in_triangle(p, a, b, c):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
            b1 = sign(p, a, b) < 0.0
            b2 = sign(p, b, c) < 0.0
            b3 = sign(p, c, a) < 0.0
            return ((b1 == b2) and (b2 == b3))
    thief_center = positionthief.center
    if point_in_triangle(thief_center, cone_polygon[0], cone_polygon[1], cone_polygon[2]):
        if not alert_triggered:
            alert_triggered = True
            alert_start_time = pygame.time.get_ticks()
            
def dotransition(toscreen):
    global jeu
    fade(600, 187) 
    jeu = toscreen
    dessiner()
    pygame.display.update()
    
def claviersouris():
    global cont, positionthief
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = False
    touchesPressees = pygame.key.get_pressed()
    if touchesPressees[pygame.K_RIGHT] == True and positionthief[0]<536:
        positionthief.x += 1
    if touchesPressees[pygame.K_LEFT] == True and positionthief[0]>0:
        positionthief.x -= 1
    if touchesPressees[pygame.K_UP] and positionthief[1] > 0:
        positionthief.y -= 1
    if touchesPressees[pygame.K_DOWN] and positionthief[1] < 150:
        positionthief.y += 1
        
def deplacer_police():
    global police_direction, change_direction_counter, police_speed, positionpolice, alert_triggered    
    change_direction_counter += 1
    if change_direction_counter >= 120:
        police_direction = random.choice(['up', 'down', 'left', 'right'])
        change_direction_counter = 0     
    current_time = pygame.time.get_ticks()
    if alert_triggered:
        if current_time - alert_start_time < alert_duration:
            current_speed = 4            
            dx = positionthief.centerx - positionpolice.centerx
            dy = positionthief.centery - positionpolice.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                dx, dy = dx / dist, dy / dist
                positionpolice.x += int(dx * current_speed)
                positionpolice.y += int(dy * current_speed)
            return
        else:
            alert_triggered = False  
    moved = False
    attempts = 0
    while not moved and attempts < 4:
        new_pos = positionpolice.copy()
        if police_direction == 'up' and positionpolice.y > 0:
            new_pos.y -= police_speed
        elif police_direction == 'down' and positionpolice.y < 145:
            new_pos.y += police_speed
        elif police_direction == 'left' and positionpolice.x > 0:
            new_pos.x -= police_speed
        elif police_direction == 'right' and positionpolice.x < 536:
            new_pos.x += police_speed
        collision = False
        for rect in rectt:
            if new_pos.colliderect(rect):
                collision = True
                break        
        if not collision:
            positionpolice = new_pos
            moved = True
        else:
            police_direction = random.choice(['up', 'down', 'left', 'right'])
            attempts += 1
    
    if difficulte == "difficile":
        police_speed = 10
def draw_spotlight():
    overlay = pygame.Surface((600, 187), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 240)) 
    spotlight_radius = 25
    spotlight_pos = (positionthief.centerx, positionthief.centery)
    pygame.draw.circle(overlay, (0, 0, 0, 0), spotlight_pos, spotlight_radius)
    fenetre.blit(overlay, (0, 0))

       
       
rectt= [rectgold , rectlady ,rectsphinx , rectmetal , rectmona , rectafra , rectstarry , rectguy , rectbroken , rectroman , rectjar]
gameover = False
def stealing():
    global rectt, positionpolice, gameover
    if gameover:
        return
    for rect in rectt: 
        if positionthief.colliderect(rect):
            stolenrect.append(rectt.remove(rect))
            if rectt==[]:
                fenetre.fill((0, 153, 0))
                arial24 = pygame.font.SysFont("arial",30)
                surfacegagne = arial24.render("GAGNÉ",True,pygame.Color(0, 102, 0))
                surfacegagnee = arial24.render("Tu es un vrai criminel!",True,pygame.Color(0, 102, 0))
                fenetre.blit(surfacegagne,(230,50))
                fenetre.blit(surfacegagnee,(120,100))
                pygame.display.flip()
                pygame.time.delay(2000)
                dotransition(homescreen)
                break
    if positionthief.colliderect(positionpolice):
        gameover = True
        fenetre.fill((204, 102, 0))
        arial24 = pygame.font.SysFont("arial",30)
        surfaceperdu = arial24.render("PERDU!",True,pygame.Color(102, 51, 0))
        surfaceperduu = arial24.render("Direction la prison haha!",True,pygame.Color(102, 51, 0))
        fenetre.blit(surfaceperdu,(230,50))
        fenetre.blit(surfaceperduu,(120,100))
        pygame.display.flip()
        pygame.time.delay(2000)
        dotransition(homescreen)
    
def fade(width, height): 
    fade = pygame.Surface((width,height))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        fenetre.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(3)          
        
def reset_artworks():
    global rectt, positionthief, positionpolice, stolenrect, gameover, police_direction, change_direction_counter
    rectt = [rectgold, rectlady, rectsphinx, rectmetal, rectmona, rectafra, rectstarry, rectguy, rectbroken, rectroman, rectjar]
    stolenrect = []
    positionthief.x, positionthief.y = 125, 75
    positionpolice.x, positionpolice.y = 75, 25
    police_direction = random.choice(['up', 'down', 'left', 'right'])
    change_direction_counter = 0
    gameover = False

def ecrandepart():
    touches = pygame.key.get_pressed()
    while touches[pygame.K_SPACE] == True:
        dotransition(diffscreen)
        break
clock = pygame.time.Clock()
cont= True
while cont :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cont = False
    if jeu == homescreen:
        fenetre.blit(imgmus,(0,0))
        font = pygame.font.SysFont(None, 24)
        texte = font.render("Appuie sur ESPACE pour commencer", True, (131, 96, 73))
        text_rect = texte.get_rect(topleft=(160, 157))        
        bg_rect = pygame.Rect(text_rect.x - 5, text_rect.y - 5, text_rect.width + 10, text_rect.height + 10)
        pygame.draw.rect(fenetre, (0, 0, 0), bg_rect)         
        fenetre.blit(texte, text_rect)            
    elif jeu == diffscreen:
        fenetre.fill((204, 102, 0))
        font = pygame.font.SysFont(None, 36)        
        b1 = pygame.Rect(150, 60, 300, 40)
        b2 = pygame.Rect(150, 110, 300, 40)
        text = font.render("Choisie ton niveau de difficulté", True, (102, 51, 0))
        pygame.draw.rect(fenetre, (3, 71, 50), b1)
        pygame.draw.rect(fenetre, (0, 129, 72), b2)
        fenetre.blit(text,(110, 18))
        fenetre.blit(font.render("Facile", True, (255, 255, 255)), (270, 68))
        fenetre.blit(font.render("Difficile", True, (255, 255, 255)), (260, 118))        
        pos_souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()
        if clic[0]: 
            if b1.collidepoint(pos_souris):
                difficulte = "facile"
                reset_artworks()
                dotransition(gamescreen)
            elif b2.collidepoint(pos_souris):
                difficulte = "difficile"
                reset_artworks()
                dotransition(gamescreen)            
    elif jeu == gamescreen:
        dessiner()
        claviersouris()
        stealing()
        deplacer_police()
        if difficulte == "facile":
            draw_vision_cone()
        elif difficulte == "difficile":
            draw_spotlight()          
    check_vision_cone_collision()   
    ecrandepart()       
    clock.tick(60)
    pygame.display.flip()
   
pygame.quit()
sys.exit()