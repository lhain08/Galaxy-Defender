import pygame, timeit, random, ButtonMod, pickle, sys, math, time
from random import randint as rand
from pygame.locals import *

pygame.init()

global coins, totalkills, collateral, doubleh, doublec, perkselector

locked=pygame.image.load('locked.png')
locked=pygame.transform.scale(locked,(70,70))

width=800
height=600
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
YELLOW=(255,225,0)
GREEN=(0,255,0)
perkselector=pygame.Rect(-100,-100,90,90)

class pship():
    def __init__(self, image, price, purchased):
        self.image=pygame.transform.scale(image, (75,75))
        self.price=price
        self.purchased=purchased
        self.srect=self.image.get_rect()
    def draw(self,x):
        global coins, curship
        font=pygame.font.Font(None,30)
        self.srect.centerx=(width*((x+1)/7.0))
        self.srect.centery=height/4
        if curship==x:
            pygame.draw.rect(screen,(100,0,0),self.srect)
        screen.blit(self.image,self.srect)
        if not self.purchased:
            screen.blit(locked,self.srect)
            t=font.render('Price: '+str(self.price),1,YELLOW)
            tp=t.get_rect()
            tp.centerx=(width*((x+1)/7.0))
            tp.centery=height/4-60
            screen.blit(t,tp)
        a,b,c=pygame.mouse.get_pressed()
        if a and self.srect.collidepoint(pygame.mouse.get_pos()):
            if not self.purchased and self.price<=coins:
                coins-=self.price
                self.purchased=True
                curship=x
            elif self.purchased:
                curship=x

class perks():
    def __init__(self, icon, function, reqrank, description):
        font=pygame.font.Font(None,50)
        self.icon=pygame.transform.scale(icon,(75,75))
        self.function=function
        self.reqrank=reqrank
        self.description=font.render(description,1,GREEN)
        self.descrect=self.description.get_rect()
        self.descrect.centerx=width/2
        self.descrect.centery=height-40
        self.prect=(self.icon.get_rect())
    def draw(self, x):
        global rank, curperk
        font=pygame.font.Font(None,30)
        self.prect.centerx=(width*((x+1)/4.0))
        self.prect.centery=height*3/4
        screen.blit(self.icon,self.prect)
        if not rank>=self.reqrank:
            screen.blit(locked,self.prect)
            t=font.render('Rank: '+str(self.reqrank),1,GREEN)
            tp=t.get_rect()
            tp.centerx=(width*((x+1)/4.0))
            tp.centery=height*3/4-60
            screen.blit(t,tp)
        
        a,b,c=pygame.mouse.get_pressed()
        if a and self.prect.collidepoint(pygame.mouse.get_pos()) and rank>=self.reqrank:
            self.function(self.prect.centerx, self.prect.centery)
        if self.prect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.description,self.descrect)

ship1=pship(pygame.image.load('PlayerShip1.PNG'), 0, True)
ship2=pship(pygame.image.load('PlayerShip2.PNG'), 25, False)
ship3=pship(pygame.image.load('PlayerShip3.PNG'), 50, False)
ship4=pship(pygame.image.load('PlayerShip4.PNG'), 100, False)
ship5=pship(pygame.image.load('PlayerShip5.PNG'), 150, False)
ship6=pship(pygame.image.load('PlayerShip6.PNG'), 200, False)

ships=[ship1,ship2,ship3,ship4,ship5,ship6]

def perk1_init(cx,cy):
    global collateral, doublec, doubleh, perkselector
    collateral=True
    doublec=1
    doubleh=100
    perkselector.centerx=cx
    perkselector.centery=cy
def perk2_init(cx,cy):
    global collateral, doublec, doubleh, perkselector
    collateral=False
    doublec=1
    doubleh=200
    perkselector.centerx=cx
    perkselector.centery=cy
def perk3_init(cx,cy):
    global collateral, doublec, doubleh, perkselector
    collateral=False
    doublec=2
    doubleh=100
    perkselector.centerx=cx
    perkselector.centery=cy

perk1=perks(pygame.image.load('perk1.PNG'),perk1_init,3,'Bullets May Pass Through Multiple Targets')
perk2=perks(pygame.image.load('perk2.PNG'),perk2_init,5,'Double Health. Does not affect direct hits')
perk3=perks(pygame.image.load('perk3.PNG'),perk3_init,7,'Coins are worth twice as much')

allperks=[perk1,perk2,perk3]

collateral=False
doubleh=100
doublec=1

try:
    f=open('GDstats.pickle')
    xp,totalkills,curship,coins,ship1.purchased,ship2.purchased,ship3.purchased,ship4.purchased,ship5.purchased,ship6.purchased=pickle.load(f)
    f.close()
except:
    print 'No previous stats'
    coins=0
    curship=0
    totalkills=0
    xp=0

enshipimg=pygame.image.load('EnemyShip.PNG')
enbugimg=pygame.image.load('EnemyBug.PNG')
enemyimgs=[enshipimg,enbugimg]
expsmall=pygame.image.load('SmallExp.PNG')
expbig=pygame.image.load('BigExp.PNG')
expbig=pygame.transform.scale(expbig,(75,75))
enspecks=pygame.image.load('EnemySpecks.PNG')
enspecks=pygame.transform.scale(enspecks,(100,100))
expsmall=pygame.transform.scale(expsmall,(45,45))
coinimg=pygame.image.load('CoinImage.PNG')

version=2

screen=pygame.display.set_mode((width, height))
pygame.display.set_caption('Galaxy Defender V'+str(version))

background=pygame.Surface(screen.get_size())
background=background.convert()
background.fill(BLACK)

pygame.mixer.music.load('shoot.wav')

def breaker():
    return True

class explosion():
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.num=0
        self.rect=pygame.Rect(x-15,y-15,30,30)
        self.rect.centerx=x
        self.rect.centery=y
    def draw(self):
        self.num+=1
        if self.num>50:
            explosions.pop()
        else:
            if self.num>30:
                width=100
                height=100
                self.rect.centerx=self.x
                self.rect.centery=self.y
                screen.blit(enspecks,self.rect)
            else:
                if self.num>10:
                    width=80
                    height=80
                    self.rect.centerx=self.x
                    self.rect.centery=self.y
                    screen.blit(expbig,self.rect)
                else:
                    width=45
                    height=45
                    self.rect.centerx=self.x
                    self.rect.centery=self.y
                    screen.blit(expsmall,self.rect)

class enemy():
    def __init__(self, x, y, image):
        self.rect=pygame.Rect(x-25,y-25,50,50)
        self.image=image
        self.active=True
    def draw(self):
        global health, speed
        self.rect.centery+=speed
        if self.rect.centery>height+25:
            if self.active:
                health-=10
            enemies.pop()
        if self.active==True:
            screen.blit(self.image,self.rect)

class coinob():
    def __init__(self, x, y):
        self.img=pygame.transform.scale(coinimg,(35,35))
        self.rect=self.img.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.active=True
    def draw(self):
        self.rect.centerx+=5
        if self.active:
            screen.blit(self.img,self.rect)
        if self.rect.centerx>width+20:
            coinslist.pop()

class playerbullet():
    def __init__(self,x,y):
        self.rect=pygame.Rect(x-5,y-15,10,30)
        self.active=True
    def run(self):
        global spawnrate, score, coins,kills
        self.rect.centery-=15
        if self.active:
            pygame.draw.rect(screen,(255,255,255),self.rect)
            for i in enemies:
                if self.rect.colliderect(i.rect) and i.active:
                    if not collateral:
                        self.active=False
                    i.active=False
                    spawnrate=spawnrate*.95
                    if spawnrate<.1:
                        spawnrate=.15
                    score+=100
                    kills+=1
                    explosions.insert(0,explosion(i.rect.centerx,i.rect.centery))
            for i in coinslist:
                if self.rect.colliderect(i.rect) and i.active:
                    if not collateral:
                        self.active=False
                    i.active=False
                    coins+=doublec*(int(score/1000)+1)
        if self.rect.centery<=-15:
            pbullets.pop()
        

class player(): 
    def __init__(self,x,y,image):
        self.image=pygame.transform.scale(image,(60,60))
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.shootvar=True
    def draw(self):
        global gameover
        k=pygame.key.get_pressed()
        if k[pygame.K_RIGHT]:
            self.rect.centerx+=14
        if self.rect.centerx>width-30:
            self.rect.centerx=width-30
        if k[pygame.K_LEFT]:
            self.rect.centerx-=14
        if self.rect.centerx<30:
            self.rect.centerx=30
        if k[pygame.K_SPACE]:
            if self.shootvar:
                self.shootvar=False
                pygame.mixer.music.play(-1, 0.0)
                pbullets.insert(0,playerbullet(self.rect.centerx,self.rect.centery-30))
        else:
            self.shootvar=True
        screen.blit(self.image,self.rect)
        for i in enemies:
            if self.rect.colliderect(i.rect) and i.active:
                gameover=True

def spawnEnemies():
    global spawnTimer
    if timeit.default_timer()-spawnTimer>0:
        enemies.insert(0,enemy(rand(25, width-25),-30, enemyimgs[rand(0,len(enemyimgs)-1)]))
        spawnTimer=timeit.default_timer()+spawnrate

def spawnCoins():
    global cspawnTimer, coinslist
    if timeit.default_timer()-cspawnTimer>0:
        coinslist.insert(0,coinob(-20,rand(0,height/2)))
        cspawnTimer=timeit.default_timer()+rand(15,25)

def Results():
    global kills, newcoins, score, totalkills, xp, multiplier
    totalkills+=kills
    xp+=(kills*multiplier)
    font=pygame.font.SysFont('droidserif', 120)
    st=font.render(str(score),1,(255,0,0))
    stp=st.get_rect()
    stp.centerx=width/2
    stp.bottom=height/2
    screen.blit(background,(0,0))
    screen.blit(st,stp)
    font=pygame.font.SysFont('droidserif',50)
    kt=font.render(('Kills: '+str(kills)),1,(255,255,255))
    ktp=kt.get_rect()
    ktp.centerx=width/2
    ktp.centery=height/2+75
    screen.blit(kt,ktp)
    contb=ButtonMod.button(width-120,height-50,None,'Continue',60,BLACK,YELLOW, breaker, screen, pygame)
    while True:
        x=contb.draw()
        if x:
            break
        for event in pygame.event.get():
            if event.type==QUIT:
                save()
                pygame.display.quit()
        pygame.display.flip()
    save()

def health_bar():
    global health, gameover, doubleh
    if health>0:
        pygame.draw.rect(screen, GREEN, (0,height-15,(width*health/doubleh),15))
    else:
        gameover=True

def Play():
    global doubleh, health, kills, newcoins, coinslist, cspawnTimer, player1, pbullets, enemies, explosions, spawnrate, spawnTimer, gameover, score
    health=doubleh
    kills=0
    newcoins=0
    player1=player(width/2,height-50,ships[curship].image)
    pbullets=[]
    enemies=[]
    explosions=[]
    spawnrate=3.5
    spawnTimer=timeit.default_timer()+2
    cspawnTimer=timeit.default_timer()+rand(15,25)
    score=0
    coinslist=[]
    font=pygame.font.Font(None,50)
    coinsicon=pygame.transform.scale(coinimg,(30,30))
    cirect=coinsicon.get_rect()
    cirect.top=20
    cirect.left=10
    while True:
        st=font.render(str(score),1,(250,250,250))
        ct=font.render(str(coins),1,YELLOW)
        stp=st.get_rect()
        ctp=ct.get_rect()
        stp.right=width-20
        ctp.left=50
        stp.top=20
        ctp.top=20
        screen.blit(background,(0,0))
        screen.blit(coinsicon,cirect)
        screen.blit(st,stp)
        screen.blit(ct,ctp)
        player1.draw()
        spawnEnemies()
        spawnCoins()
        for i in coinslist:
            i.draw()
        for i in pbullets:
            i.run()
        for i in enemies:
            i.draw()
        for i in explosions:
            i.draw()

        health_bar()

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.display.quit()

        pygame.display.flip()

        if gameover:
            break
    Results()

def draw_Rank():
    global xp, rank
    rvar=1+(0.1*math.sqrt(2*xp))
    rank=int(rvar)
    font=pygame.font.Font(None,40)
    rt=font.render(('RANK '+str(rank)),1,(0,130,0))
    rtpos=rt.get_rect()
    rtpos.centerx=width/2
    rtpos.centery=25
    pygame.draw.rect(screen,(100,100,100),(rtpos.left,rtpos.bottom,rtpos.width,10))
    pygame.draw.rect(screen,GREEN,(rtpos.left,rtpos.bottom,(rvar-rank)*(rtpos.width),10))
    screen.blit(rt,rtpos)

def shop():
    global coins, perkselector
    coinsicon=pygame.transform.scale(coinimg,(30,30))
    cirect=coinsicon.get_rect()
    cirect.top=20
    cirect.left=width-150
    bbut=ButtonMod.button(width-70,height-50,None,'Back',50,BLACK,YELLOW,breaker,screen,pygame)
    while True:
        font=pygame.font.Font(None,60)
        ct=font.render(str(coins),1,YELLOW)
        ctp=ct.get_rect()
        ctp.top=10
        ctp.left=width-100
        screen.blit(background,(0,0))
        draw_Rank()
        st=font.render('Ships',1,WHITE)
        stp=st.get_rect()
        stp.centerx=75
        stp.centery=50
        screen.blit(coinsicon,cirect)
        screen.blit(ct,ctp)
        screen.blit(st,stp)
        x=bbut.draw()
        if x:
            break
        for i,x in enumerate(ships):
            x.draw(i)
        pygame.draw.rect(screen,(100,0,0),perkselector)
        for i,x in enumerate(allperks):
            x.draw(i)
        for event in pygame.event.get():
            if event.type==QUIT:
                save()
                pygame.display.quit()
                sys.exit()
        pygame.display.flip()

def save():
    global coins
    f=open('GDstats.pickle','w')
    pickle.dump([xp,totalkills,curship,coins,ship1.purchased,ship2.purchased,ship3.purchased,ship4.purchased,ship5.purchased,ship6.purchased], f)
    f.close()

def seteasy():
    global speed, multiplier
    multiplier=1
    speed=4.5
    Play()

def setmed():
    global speed,multiplier
    multiplier=2
    speed=6
    Play()

def sethard():
    global speed, multiplier
    multiplier=4
    speed=8
    Play()

def difficultymenu():
    global gameover
    gameover=False
    aa,bb,cc=pygame.mouse.get_pressed()
    while aa==True:
        aa,bb,cc=pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.display.quit()
    easyb=ButtonMod.button(width/2,height/4,"droidserif",'EASY',75, GREEN, BLACK, seteasy, screen, pygame)
    medb=ButtonMod.button(width/2,height/2,"droidserif",'MEDIUM',75, YELLOW, BLACK, setmed, screen, pygame)
    hardb=ButtonMod.button(width/2,height*3/4,"droidserif",'HARD',75, RED, BLACK, sethard, screen, pygame)
    while True:
        screen.blit(background,(0,0))
        easyb.draw()
        medb.draw()
        hardb.draw()
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.display.quit()
        if gameover:
            break
        pygame.display.flip()
        

def MainMenu():
    playb=ButtonMod.button(width/2,120, "droidserif",'PLAY',75,BLACK,WHITE,difficultymenu,screen,pygame)
    shopb=ButtonMod.button(width/2,270, "droidserif",'SHOP',60,BLACK,WHITE,shop,screen,pygame)
    while True:
        screen.blit(background,(0,0))
        draw_Rank()
        playb.draw()
        shopb.draw()
        for event in pygame.event.get():
            if event.type==QUIT:
                save()
                pygame.display.quit()
                sys.exit()

        pygame.display.flip()


MainMenu()


pygame.display.quit()
