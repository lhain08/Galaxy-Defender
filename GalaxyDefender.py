#!/usr/bin/python

import pygame, timeit, random, ButtonMod, pickle, sys, math, time
from random import randint as rand
from pygame.locals import *

pygame.init()

clock=pygame.time.Clock()

sound=pygame.mixer.Sound('Resources/Sound_Effects/shoot.wav')
GOsound = pygame.mixer.Sound('Resources/Sound_Effects/GameOver.wav')

global tbosskills, coins, totalkills, collateral, doubleh, doublec, perkselector

locked=pygame.image.load('Resources/Images/locked.png')
locked=pygame.transform.scale(locked,(70,70))

bossimg=pygame.image.load('Resources/Images/Boss.PNG')
bossimg=pygame.transform.scale(bossimg,(100,113))

arrow = pygame.image.load('Resources/Images/arrow.png')
arrow = pygame.transform.scale(arrow, (30,30))

shield = pygame.image.load('Resources/Images/Shield.png')

width=800
height=600
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
YELLOW=(255,225,0)
GREEN=(0,255,0)
PURPLE=(200,0,200)
BLUE=(0,0,200)

class preferences():
    def __init__(self, perk, sens):
        self.perk = perk
        self.sens = sens

plPref = preferences(0,100)

class pship():
    def __init__(self, image, price, purchased, damage, cooldown, movespeed):
        self.image=pygame.transform.scale(image, (75,75))
        self.price=price
        self.purchased=purchased
        self.srect=self.image.get_rect()
        self.damage = damage
        self.cooldown = cooldown
        self.movespeed = movespeed
    def draw(self,x):
        global coins, curship
        font=pygame.font.Font(None,25)
        self.srect.centerx=(width*((x+1)/float(len(ships)+1)))
        self.srect.centery=height/4
        if curship==x:
            pygame.draw.rect(screen,(100,0,0),self.srect)
        screen.blit(self.image,self.srect)
        if not self.purchased:
            screen.blit(locked,self.srect)
            t=font.render('Price: '+str(self.price),1,YELLOW)
            tp=t.get_rect()
            tp.centerx=self.srect.centerx
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
    def __init__(self, icon, function, reqrank, description, x):
        font=pygame.font.Font(None,50)
        self.icon=pygame.transform.scale(icon,(75,75))
        self.function=function
        self.reqrank=reqrank
        self.description=font.render(description,1,GREEN)
        self.descrect=self.description.get_rect()
        self.descrect.centerx=width/2
        self.descrect.centery=height-40
        self.prect=(self.icon.get_rect())
        self.prect.centerx=(width*((x+1)/float(5)))
        self.prect.centery=height*3/4
    def draw(self, x):
        global rank, curperk
        font=pygame.font.Font(None,30)
        screen.blit(self.icon,self.prect)
        if not rank>=self.reqrank:
            screen.blit(locked,self.prect)
            t=font.render('Rank: '+str(self.reqrank),1,GREEN)
            tp=t.get_rect()
            tp.centerx=self.prect.centerx
            tp.centery=height*3/4-60
            screen.blit(t,tp)
        
        a,b,c=pygame.mouse.get_pressed()
        if a and self.prect.collidepoint(pygame.mouse.get_pos()) and rank>=self.reqrank:
            self.function(self.prect.centerx, self.prect.centery)
        if self.prect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(self.description,self.descrect)

class Achievement():
    def __init__(self, description, reqkills, reqhealth, reqmulti, reqscore, reqdiff, reqtotalk, reqtbossk, rewcoins, rewxp, notice):
        self.desc=description
        self.reqkills=reqkills
        self.reqhealth=reqhealth
        self.reqmulti=reqmulti
        self.reqscore=reqscore
        self.reqdiff=reqdiff
        self.reqtotalk=reqtotalk
        self.reqtbossk=reqtbossk
        self.rewcoins=rewcoins
        self.rewxp=rewxp
        self.notice=notice
        self.achieved=False
        self.bantime=None
        font=pygame.font.Font(None, 40)
        self.a=font.render('Achievement Unlocked!',1,(YELLOW))
        self.n=font.render(str(self.notice),1,(GREEN))
        self.apos=self.a.get_rect()
        self.apos.centerx=width/2
        self.apos.centery=25
        self.npos=self.n.get_rect()
        self.npos.centerx=width/2
        self.npos.centery=50
        self.anrect=pygame.Rect.union(self.apos,self.npos)
    def check(self):
        global difficulty, kills, score, health, coins, xp
        if self.bantime:
            if self.bantime>timeit.default_timer():
                self.banner()
            else:
                self.achieved=True
        else:
            if self.cscore() and self.cmulti() and self.ckills() and self.cdiff() and self.chealth() and self.ctotalk() and self.ctbossk():
                self.bantime=timeit.default_timer()+3
                xp+=self.rewxp
                coins+=self.rewcoins
    def cscore(self):
        global score
        if self.reqscore:
            if self.reqscore<=score:
                return True
            else:
                return False
        else:
            return True
    def ckills(self):
        global kills
        if self.reqkills:
            if self.reqkills<=kills:
                return True
            else:
                return False
        else:
            return True
    def cdiff(self):
        global difficulty
        if self.reqdiff:
            if self.reqdiff==difficulty:
                return True
            else:
                return False
        else:
            return True
    def chealth(self):
        global health, doubleh
        if self.reqhealth:
            if self.reqhealth*(doubleh/100)<=health:
                return True
            else:
                return False
        else:
            return True
    def cmulti(self):
        if self.reqmulti:
            for i in pbullets:
                if i.hits>=self.reqmulti:
                    return True
                else:
                    return False
        else:
            return True
    def ctotalk(self):
        global totalkills
        if self.reqtotalk:
            if self.reqtotalk<=totalkills:
                return True
            else:
                return False
        else:
            return True
    def ctbossk(self):
        global tbosskills
        if self.reqtbossk:
            if self.reqtbossk<=tbosskills:
                return True
            else:
                return False
        else:
            return True
    def banner(self):
        pygame.draw.rect(screen,(155,10,10),self.anrect)
        screen.blit(self.a,self.apos)
        screen.blit(self.n,self.npos)
        

ship1=pship(pygame.image.load('Resources/Images/PlayerShip1.PNG'), 0, True, 10, .5, 12)
ship2=pship(pygame.image.load('Resources/Images/PlayerShip2.PNG'), 50, False, 15, .4, 14)
ship3=pship(pygame.image.load('Resources/Images/PlayerShip3.PNG'), 125, False, 25, .3, 16)
ship4=pship(pygame.image.load('Resources/Images/PlayerShip4.PNG'), 250, False, 40, .2, 18)
ship5=pship(pygame.image.load('Resources/Images/PlayerShip5.PNG'), 500, False, 75, .15, 19)
ship6=pship(pygame.image.load('Resources/Images/PlayerShip6.PNG'), 1000, False, 150, .1, 20)
ship7=pship(pygame.image.load('Resources/Images/PlayerShip7.PNG'), 2500, False, 350, .05, 22)

ships=[ship1,ship2,ship3,ship4,ship5,ship6,ship7]

def No_perk(cx, cy):
    global collateral, doublec, doubleh, perkselector, curperk
    collateral = False
    doublec = 1
    doubleh = 100
    perkselector.centerx = cx
    perkselector.centery = cy
    curperk = 0
def perk1_init(cx,cy):
    global collateral, doublec, doubleh, perkselector, curperk
    collateral=True
    doublec=1
    doubleh=100
    perkselector.centerx=cx
    perkselector.centery=cy
    curperk = 1
def perk2_init(cx,cy):
    global collateral, doublec, doubleh, perkselector, curperk
    collateral=False
    doublec=1
    doubleh=200
    perkselector.centerx=cx
    perkselector.centery=cy
    curperk = 2
def perk3_init(cx,cy):
    global collateral, doublec, doubleh, perkselector, curperk
    collateral=False
    doublec=2
    doubleh=100
    perkselector.centerx=cx
    perkselector.centery=cy
    curperk = 3

noPerk=perks(pygame.image.load('Resources/Images/EmptyIcon.png'),No_perk,0,'No Perks', 0)
perk1=perks(pygame.image.load('Resources/Images/perk1.PNG'),perk1_init,3,'Bullets May Pass Through Multiple Targets', 1)
perk2=perks(pygame.image.load('Resources/Images/perk2.PNG'),perk2_init,5,'Double Health. Does not affect direct hits', 2)
perk3=perks(pygame.image.load('Resources/Images/perk3.PNG'),perk3_init,7,'Coins are worth twice as much', 3)

allperks=[noPerk,perk1,perk2,perk3]

perkselector = pygame.Rect(0,0,90,90)

achv1=Achievement('Get ONE kill',None,None,None,None,None,1,None,5,10,'First Kill')
achv2=Achievement('Kill One Boss',None,None,None,None,None,None,1,6,15,'First Boss Kill')
achv3=Achievement('Kill TWENTY enemies in one game',20,None,None,None,None,None,None,5,30,'Killed 20 enemies in one game')
achv4=Achievement('Kill TWO or more enemies with the same bullet', None,None,2,None,None,None,None,15,40,'Kill 2 or more enemies with the same bullet')
achv5=Achievement('Kill FIFTY enemies in one game on EASY without taking damage',50,100,None,None,1,None,None,10,100,'Killed 50 enemies on Easy without taking damage')
achv6=Achievement('Kill FOURTY enemies in one game on MEDIUM without taking damage',40,100,None,None,2,None,None,15,120,'Killed 40 enemies on Medium without taking damage')
achv7=Achievement('Kill THIRTY enemies in one game on HARD without taking damage',30,100,None,None,3,None,None,25,150,'Killed 30 enemies on Hard without taking damage')
achv8=Achievement('Kill FOURTY enemies in one game on HARD without taking damage',40,100,None,None,3,None,None,30,200,'Killed 40 enemies on Hard without taking damage')
achv9=Achievement('Kill ONE THOUSAND enemies',None,None,None,None,None,1000,None,30,500,'1,000th Kill')
achv10=Achievement('Kill TEN THOUSAND enemies',None,None,None,None,None,10000,None,75,1000,'10,000th Kill')
achv11=Achievement('Kill 25 Bosses',None,None,None,None,None,None,25,30,150,"25th Boss Kill")
achv12=Achievement('Kill 100 Bosses',None,None,None,None,None,None,100,150,650,"100th Boss Kill")
achv13=Achievement('Score 10,000 points on Easy',None,None,None,10000,1,None,None,15,45,"Scored 10,000 points on Easy")
achv14=Achievement('Score 10,000 points on Medium',None,None,None,10000,2,None,None,25,60,"Scored 10,000 points on Medium")
achv15=Achievement('Score 10,000 points on Hard',None,None,None,10000,3,None,None,45,90,"Scored 10,000 points on Hard")

achievements = [achv1, achv2, achv3, achv4, achv5, achv6, achv7, achv8, achv9, achv10, achv11, achv12, achv13, achv14, achv15]
global highscore, curperk
try:
    f=open('Saves/GDstats.pickle')
    sdamages, scooldowns, smovespeeds, curperk, tbosskills, achv1.achieved, achv2.achieved, achv3.achieved, achv4.achieved, achv5.achieved, achv6.achieved, achv7.achieved, achv8.achieved, achv9.achieved, achv10.achieved, achv11.achieved, achv12.achieved, achv13.achieved, achv14.achieved, achv15.achieved, xp, totalkills, curship, coins, ship1.purchased, ship2.purchased, ship3.purchased, ship4.purchased, ship5.purchased, ship6.purchased, ship7.purchased, highscore = pickle.load(f)
    f.close()
    for i,x in enumerate(ships):
        x.damage = sdamages[i]
        x.cooldown = scooldowns[i]
        x.movespeed = smovespeeds[i]
except:
    print 'No previous stats'
    print "Unexpected error:", sys.exc_info()[0]
    tbosskills = 0
    coins = 0
    curship = 0
    totalkills = 0
    xp = 0
    highscore = [0, 0, 0]
    curperk = 0

allperks[curperk].function(allperks[curperk].prect.centerx, allperks[curperk].prect.centery)

enshipimg=pygame.image.load('Resources/Images/EnemyShip.PNG')
enbugimg=pygame.image.load('Resources/Images/EnemyBug.PNG')
enemyimgs=[enshipimg,enbugimg]
expsmall=pygame.image.load('Resources/Images/SmallExp.PNG')
expbig=pygame.image.load('Resources/Images/BigExp.PNG')
expbig=pygame.transform.scale(expbig,(75,75))
enspecks=pygame.image.load('Resources/Images/EnemySpecks.PNG')
enspecks=pygame.transform.scale(enspecks,(100,100))
expsmall=pygame.transform.scale(expsmall,(45,45))
coinimg=pygame.image.load('Resources/Images/CoinImage.PNG')

version=3.0

screen=pygame.display.set_mode((width, height))
pygame.display.set_caption('Galaxy Defender V'+str(version))

background=pygame.Surface(screen.get_size())
background=background.convert()
background.fill(BLACK)

backimg = pygame.image.load('Resources/Images/full-background.png')
w, h = backimg.get_size()
backimg = pygame.transform.scale(backimg, (width,int(h/(w/float(width)))))
backw, backh = backimg.get_size()

backheights = [height-backh, height-(backh*2), height-(backh*3)]

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
        if self.num>10:
            explosions.pop()
        else:
            if self.num>7:
                width=100
                height=100
                self.rect=enspecks.get_rect()
                self.rect.centerx=self.x
                self.rect.centery=self.y
                screen.blit(enspecks,self.rect)
            else:
                if self.num>4:
                    width=80
                    height=80
                    self.rect=expbig.get_rect()
                    self.rect.centerx=self.x
                    self.rect.centery=self.y
                    screen.blit(expbig,self.rect)
                else:
                    width=45
                    height=45
                    self.rect=expsmall.get_rect()
                    self.rect.centerx=self.x
                    self.rect.centery=self.y
                    screen.blit(expsmall,self.rect)

class enemy():
    def __init__(self, x, y, image, mhealth, sway=True):
        self.x=x
        self.image=image
        self.rect = self.image.get_rect()
        self.rect.centery = y
        self.active=True
        self.maxhealth = mhealth
        self.shealth = mhealth
        self.sway = sway
    def draw(self):
        global health, speed, kills, totalkills, score
        self.rect.centery+=speed
        if self.sway:
            self.rect.centerx=self.x+(60*math.sin(self.rect.centery/50.0))
        else:
            self.rect.centerx=self.x
        if self.rect.bottom > 0:
            if self.rect.centery>height:
                if self.active:
                    health-=10
                enemies.remove(self)
            if self.active==True:
                if not self.maxhealth == self.shealth:
                    pygame.draw.rect(screen,(175,175,175),(self.rect.centerx - 30, self.rect.top - 20, 60, 6))
                    pygame.draw.rect(screen,RED,(self.rect.centerx - 30, self.rect.top - 20, 60 * (float(self.shealth)/float(self.maxhealth)), 6))
                screen.blit(self.image,self.rect)
            else:
                enemies.remove(self)
                kills += 1
                totalkills += 1
                score += 100

class Boss():
    def __init__(self, x):
        global difficulty
        self.img=bossimg
        self.rect=self.img.get_rect()
        self.rect.centerx=x
        self.y=float(-60)
        self.rect.centery=self.y
        self.shealth=(400*difficulty/2)+(score/10)
        self.health=self.shealth
        self.sheild=False
        self.shieldimg = pygame.transform.scale(shield,(self.rect.height + 25, self.rect.height + 25))
        self.shieldrect = self.shieldimg.get_rect()
        self.sheilds=[]
        self.intervals=[]
        for i in range(1,5):
            self.intervals.append(self.health*i/5)
    def draw(self):
        global multiplier,score,xp,tbosskills,gameover,enhealth,spawnTimer
        self.y+=.7
        self.rect.centery=self.y
        if self.check_intervals() and not self.sheild:
            self.intervals.pop()
            self.sheild=True
            a=rand(0,360)
            self.sheilds=[Boss_sheild(a,0),Boss_sheild(a+(6.28/4),1),Boss_sheild(a+3.14,2),Boss_sheild(a-(3.14/2),3)]
            enhealth = score / 1000
            enhealth = (enhealth + 1) * 10
            enemies.insert(0,enemy(self.rect.right + 100, -30, enemyimgs[rand(0,len(enemyimgs)-1)], enhealth))
            enemies.insert(0,enemy(self.rect.left - 100, -30, enemyimgs[rand(0,len(enemyimgs)-1)], enhealth))
        if self.sheilds:
            self.shieldrect.centerx = self.rect.centerx
            self.shieldrect.centery = self.rect.centery - 5
            screen.blit(self.shieldimg,self.shieldrect)
            for i in self.sheilds:
                i.draw(self.rect.centerx,self.rect.centery)
        else:
            self.sheild=False
        if self.health<=0:
            bosses.remove(self)
            score+=500
            xp+=30*multiplier
            tbosskills+=1
            x = rand(1,2)
            if x == 1:
                enemies.insert(0, enemy(width / 2, -50, enemyimgs[0], enhealth, False))
                for i in range(1,5):
                    x = 50*i
                    enemies.insert(0,enemy(width/2-x,-1*(50+x),enemyimgs[0],enhealth, False))
                    enemies.insert(0,enemy(width/2+x,-1*(50+x),enemyimgs[0],enhealth, False))
            elif x == 2:
                for i in range(1,5):
                    enemies.insert(0,enemy(width/2,-50*i,enemyimgs[1],enhealth,False))
                    for x in range(1,3):
                        enemies.insert(0,enemy(width/2 + (50*x), -50*i, enemyimgs[1],enhealth,False))
                        enemies.insert(0,enemy(width/2 - (50*x), -50*i, enemyimgs[1],enhealth,False))
            spawnTimer = timeit.default_timer() +  5
            for i in range(0,2+int(score/3000)):
                coinslist.insert(0,coinob(-1*rand(15, 115),rand(0,height*3/5)))

        thr=pygame.Rect(self.rect.left,self.rect.top-5, self.rect.width,10)
        hr=pygame.Rect(self.rect.left,self.rect.top-5,(self.rect.width*self.health/self.shealth),10)
        pygame.draw.rect(screen,(100,100,100),thr)
        pygame.draw.rect(screen,GREEN,hr)
        screen.blit(self.img,self.rect)
        if self.rect.centery > height:
            gameover = True
    def check_intervals(self):
        for i in self.intervals:
            if self.health<i:
                return True

class Boss_sheild():
    def __init__(self,deg,lpos):
        self.deg=deg
        self.col=(50,150,255)
        self.lpos=lpos
        self.radius=10
        self.rect=pygame.Rect(1000,1000,self.radius*2,self.radius*2)
    def draw(self,Bx,By):
        self.deg+=0.07
        self.x=Bx+(100*(math.cos(float(self.deg))))
        self.y=By+(100*(math.sin(float(self.deg))))
        self.rect.centerx=self.x
        self.rect.centery=self.y
        pygame.draw.circle(screen,self.col,(int(self.x),int(self.y)),self.radius,0)
    

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
        self.hits=0
        self.speed = 25
        self.hitenemies = []
        self.damage = ships[curship].damage
    def run(self):
        global spawnrate, score, coins, kills, totalkills
        self.rect.centery-=self.speed
        if self.active:
            pygame.draw.rect(screen,(255,255,255),self.rect)
            for i in enemies:
                if not i in self.hitenemies:
                    if self.rect.colliderect(i.rect) and i.active:
                        if not collateral:
                            self.active = False
                        else:
                            self.hitenemies.append(i)
                            if len(self.hitenemies)>=2:
                                self.active = False
                        i.shealth -= self.damage
                        if i.shealth<=0:
                            i.active=False
                            explosions.insert(0,explosion(i.rect.centerx,i.rect.centery))
                        spawnrate=spawnrate*.95
                        if spawnrate<.3:
                            spawnrate=.15
                        self.hits+=1
            for i in coinslist:
                if self.rect.colliderect(i.rect) and i.active:
                    if not collateral:
                        self.active=False
                    i.active=False
                    coins+=doublec*(int(score/1000)+1)
            for i in bosses:
                if i.sheilds:
                    for x in i.sheilds:
                        if self.rect.colliderect(x.rect):
                            i.sheilds.pop(x.lpos)
                            for a,b in enumerate(i.sheilds):
                                b.lpos=a
                            break
                if self.rect.colliderect(i.rect):
                    self.active=False
                    if not i.sheild:
                        i.health-=self.damage
                        
        if self.rect.centery<=-15:
            pbullets.pop()
        

class player(): 
    def __init__(self,x,y,image):
        self.image=pygame.transform.scale(image,(60,60))
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.basey = y
        self.shootvar=True
        self.speed = ships[curship].movespeed
        self.cooldown = ships[curship].cooldown
        self.shoottimer = 0
    def draw(self):
        global gameover
        k=pygame.key.get_pressed()
        self.rect.centery = self.basey +(math.sin(timeit.default_timer()*5)*2)
        if k[pygame.K_RIGHT]:
            self.rect.centerx+=self.speed*plPref.sens/100
        if self.rect.centerx>width-30:
            self.rect.centerx=width-30
        if k[pygame.K_LEFT]:
            self.rect.centerx-=self.speed*plPref.sens/100
        if self.rect.centerx<30:
            self.rect.centerx=30
        if k[pygame.K_SPACE]:
            if self.shoottimer<timeit.default_timer():
                self.shoottimer=timeit.default_timer() + self.cooldown
                sound.play()
                pbullets.insert(0,playerbullet(self.rect.centerx,self.rect.centery-30))
        screen.blit(self.image,self.rect)
        for i in enemies:
            if self.rect.colliderect(i.rect) and i.active:
                gameover=True
        for i in bosses:
            if self.rect.colliderect(i.rect):
                gameover=True
            for x in i.sheilds:
                if self.rect.colliderect(x.rect):
                    gameover=True

def spawnEnemies():
    global spawnTimer, spawnrate, score
    if spawnrate<.6:
        spawnrate = .6
    enhealth = score/1000
    enhealth = (enhealth + difficulty) * 10
    if timeit.default_timer()-spawnTimer>0:
        enemies.insert(0,enemy(rand(60, width-60),-50, enemyimgs[rand(0,len(enemyimgs)-1)], enhealth))
        spawnTimer=timeit.default_timer()+spawnrate

def spawnCoins():
    global cspawnTimer, coinslist
    if timeit.default_timer()-cspawnTimer>0:
        coinslist.insert(0,coinob(-20,rand(0,height/2)))
        cspawnTimer=timeit.default_timer()+rand(5,12)

def Results():
    global kills, newcoins, score, totalkills, xp, multiplier, highscore
    newhs = False
    if score > highscore[difficulty - 1]:
        highscore[difficulty - 1] = score
        newhs = True
    xp+=(kills*multiplier)
    font=pygame.font.SysFont('droidserif', 120,bold = True, italic = True)
    stcolor = RED
    if newhs:
        stcolor = (0,255,0)
    st=font.render(str(score),1,stcolor)
    stp=st.get_rect()
    stp.centerx=width/2
    stp.bottom=height/2
    screen.blit(background,(0,0))
    screen.blit(st,stp)
    if newhs:
        font = pygame.font.SysFont("droidserif", 30)
        nhst = font.render("NEW HIGHSCORE!",1,RED)
        nhst = pygame.transform.rotate(nhst,-40)
        nhsrect = nhst.get_rect()
        nhsrect.centerx = stp.right
        nhsrect.centery = stp.top
        screen.blit(nhst,nhsrect)
    font=pygame.font.SysFont('droidserif',50)
    kt=font.render(('Kills: '+str(kills)),1,(255,255,255))
    ktp=kt.get_rect()
    ktp.centerx=width/2
    ktp.centery=height/2+75
    screen.blit(kt,ktp)
    contb=ButtonMod.button(width-120,height-50,None,'Continue',60,BLACK,YELLOW, breaker, screen, pygame)
    clickvar = False
    while True:
        x=contb.draw()
        if x and clickvar:
            break
        elif not pygame.mouse.get_pressed()[0]:
            clickvar = True
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

def draw_score():
    global coins, score, coinsicon, cirect
    font=pygame.font.Font(None,50)
    st=font.render(str(score),1,(250,250,250))
    ct=font.render(str(coins),1,YELLOW)
    stp=st.get_rect()
    ctp=ct.get_rect()
    stp.right=width-20
    ctp.left=50
    stp.top=20
    ctp.top=20
    screen.blit(background,(0,0))
    for i in backheights:
        screen.blit(backimg, (0, i))
    screen.blit(coinsicon,cirect)
    screen.blit(st,stp)
    screen.blit(ct,ctp)

def Paused():
    global escVar, gameover
    escVar = False
    breaker = False
    while True:
        draw_score()

        font = pygame.font.SysFont("droidserif", 75, bold=True)
        pt = font.render("PAUSED",1,RED)
        ptpos = pt.get_rect()
        ptpos.centerx = width/2
        ptpos.centery = 40
        screen.blit(pt, ptpos)

        font = pygame.font.SysFont("droidserif", 50)
        senst = font.render("Sensitivity",1,GREEN)
        senstpos = senst.get_rect()
        senstpos.left = 30
        senstpos.centery = 100
        screen.blit(senst, senstpos)

        k = pygame.key.get_pressed()

        if k[K_ESCAPE] and escVar:
            escVar = False
            break
        elif not k[K_ESCAPE]:
            escVar = True

        sliderect = pygame.Rect(((2*plPref.sens)+20,132.5,20,20))
        pygame.draw.rect(screen,BLACK,(10,125,250,40))
        pygame.draw.rect(screen, WHITE, (30, 138, 200, 9))
        pygame.draw.rect(screen, WHITE, (15, 130, 15, 25))
        pygame.draw.rect(screen, WHITE, (230, 130, 15, 25))
        pygame.draw.rect(screen, RED, sliderect)
        if pygame.mouse.get_pressed()[0]:
            if sliderect.collidepoint(pygame.mouse.get_pos()):
                while pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    sliderect.centerx = x
                    if sliderect.centerx>230:
                        sliderect.centerx = 230
                    elif sliderect.centerx < 30:
                        sliderect.centerx = 30

                    pygame.draw.rect(screen, BLACK, (10, 125, 250, 40))
                    pygame.draw.rect(screen, WHITE, (30, 138, 200, 9))
                    pygame.draw.rect(screen, WHITE, (15, 130, 15, 25))
                    pygame.draw.rect(screen, WHITE, (230, 130, 15, 25))
                    pygame.draw.rect(screen, RED, sliderect)
                    pygame.display.flip()

                    for i in pygame.event.get():
                        if i.type == QUIT:
                            pygame.display.quit()
                            quit()
                plPref.sens = (sliderect.centerx - 30)/2

        qt = font.render("Quit Game",1,GREEN)
        qtp = qt.get_rect()
        qtp.right = width - 30
        qtp.bottom = height - 30
        qtb = pygame.Rect(0,0,0,0)
        qtb.width = qtp.width + 10
        qtb.height = qtp.height + 10
        qtb.centerx = qtp.centerx
        qtb.centery = qtp.centery
        if qtb.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen,(100,0,0),qtb)
            if pygame.mouse.get_pressed()[0]:
                gameover = True
                breaker = True

        screen.blit(qt,qtp)

        pygame.display.flip()

        if breaker:
            break

        for i in pygame.event.get():
            if i.type == QUIT:
                pygame.display.quit()
                quit()

def Play():
    global escVar, bosses, coinsicon, cirect, doubleh, health, kills, newcoins, coinslist, cspawnTimer, player1, pbullets, enemies, explosions, spawnrate, spawnTimer, gameover, score
    bosses=[]
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
    escVar = False
    while True:
        for i in range(0, len(backheights)):
            backheights[i]+=3
            if backheights[i] > height:
                backheights[i] -= backh*len(backheights)
        draw_score()
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

        k = pygame.key.get_pressed()
        if k[K_ESCAPE] and escVar:
            Paused()
        elif not k[K_ESCAPE]:
            escVar = True

        if score in [1500,5000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
            while enemies:
                for i in range(0, len(backheights)):
                    backheights[i] += 3
                    if backheights[i] > height:
                        backheights[i] -= backh * len(backheights)
                draw_score()
                player1.draw()
                for i in coinslist:
                    i.draw()
                for i in pbullets:
                    i.run()
                for i in enemies:
                    i.draw()
                for i in explosions:
                    i.draw()
                health_bar()
                k = pygame.key.get_pressed()
                if k[K_ESCAPE] and escVar:
                    Paused()
                elif not k[K_ESCAPE]:
                    escVar = True
                for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.display.quit()

                pygame.display.flip()
                
                clock.tick(33)

                if gameover:
                    GOsound.play()
                    break
                for i in achievements:
                    if not i.achieved:
                        i.check()
            if score > 7500:
                bosses=[Boss(width/3),Boss(width*2/3)]
            else:
                bosses=[Boss(width/2)]
            while bosses:
                for i in range(0, len(backheights)):
                    backheights[i] += 3
                    if backheights[i] > height:
                        backheights[i] -= backh * len(backheights)
                draw_score()
                player1.draw()
                for i in pbullets:
                    i.run()
                for i in bosses:
                    i.draw()
                for i in enemies:
                    i.draw()
                for i in explosions:
                    i.draw()
                for i in coinslist:
                    i.draw()
                health_bar()
                for i in achievements:
                    if not i.achieved:
                        i.check()
                for i in achievements:
                    if not i.achieved:
                        i.check()

                k = pygame.key.get_pressed()
                if k[K_ESCAPE] and escVar:
                    Paused()
                elif not k[K_ESCAPE]:
                    escVar = True

                for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.display.quit()

                pygame.display.flip()
                
                clock.tick(33)

                if gameover:
                    GOsound.play()
                    break

        health_bar()

        for i in achievements:
            if not i.achieved:
                i.check()

        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.display.quit()

        pygame.display.flip()
        
        clock.tick(33)

        if gameover:
            GOsound.play()
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
    shipselect = None
    cvar = False
    while True:
        font=pygame.font.Font(None,60)
        ct=font.render(str(coins),1,YELLOW)
        ctp=ct.get_rect()
        ctp.top=10
        ctp.left=width-100
        screen.blit(background,(0,0))
        draw_Rank()
        st=font.render('Ships',1,WHITE)
        plt=font.render("Perks",1,WHITE)
        stp=st.get_rect()
        stp.left=25
        stp.centery=50
        pltp = plt.get_rect()
        pltp.left = 25
        pltp.centery = height*3/5
        screen.blit(plt,pltp)
        screen.blit(coinsicon,cirect)
        screen.blit(ct,ctp)
        screen.blit(st,stp)
        x=bbut.draw()
        if x:
            break
        for i,x in enumerate(ships):
            x.draw(i)
            if x.srect.collidepoint(pygame.mouse.get_pos()):
                shipselect = x
        if shipselect:
            arect = arrow.get_rect()
            arect.centerx = shipselect.srect.centerx
            arect.top = shipselect.srect.bottom
            screen.blit(arrow,arect)
            font = pygame.font.Font(None,35)
            dt = font.render("Damage: "+str(shipselect.damage),1,(RED))
            dtp = dt.get_rect()
            dtp.centerx = width/4
            dtp.centery = height*2/5
            screen.blit(dt,dtp)
            if shipselect.purchased:
                dut = font.render("UPGRADE",1,(RED))
                dutp = dut.get_rect()
                dutp.centerx = width/4
                dutp.centery = height/2-10
                pygame.draw.rect(screen,GREEN,dutp)
                screen.blit(dut,dutp)
                if dutp.collidepoint(pygame.mouse.get_pos()):
                    ut = font.render("+2 Damage   Cost: " + str(int(shipselect.damage * 1.2)),1,YELLOW)
                    utp = ut.get_rect()
                    utp.centerx = width/2
                    utp.centery = dutp.centery + 30
                    screen.blit(ut, utp)
                    if pygame.mouse.get_pressed()[0] and coins >= int(shipselect.damage*1.2) and not cvar:
                        cvar = True
                        coins -= int(shipselect.damage*1.2)
                        shipselect.damage += 2
            ct = font.render("Cooldown: "+str(round(shipselect.cooldown,3)),1,(RED))
            ctp = ct.get_rect()
            ctp.centerx = width/2
            ctp.centery = height*2/5
            screen.blit(ct,ctp)
            if shipselect.purchased:
                cut = font.render("UPGRADE",1,(RED))
                cutp = dut.get_rect()
                cutp.centerx = width/2
                cutp.centery = height/2-10
                pygame.draw.rect(screen,GREEN,cutp)
                screen.blit(cut,cutp)
                if cutp.collidepoint(pygame.mouse.get_pos()):
                    ut = font.render("15% Reduction   Cost: " + str(int(100 - ((float(shipselect.cooldown)/.57)*100))),1,YELLOW)
                    utp = ut.get_rect()
                    utp.centerx = width/2
                    utp.centery = dutp.centery + 30
                    screen.blit(ut, utp)
                    if pygame.mouse.get_pressed()[0] and coins >= int(100 - ((float(shipselect.cooldown)/.57)*100)) and not cvar:
                        cvar = True
                        coins -= int(100 - ((float(shipselect.cooldown)/.57)*100))
                        shipselect.cooldown = shipselect.cooldown * .85
            mt = font.render("Speed:"+str(shipselect.movespeed),1,(RED))
            mtp = mt.get_rect()
            mtp.centerx = width*3/4
            mtp.centery = height*2/5
            screen.blit(mt,mtp)
            if shipselect.purchased:
                mut = font.render("UPGRADE",1,(RED))
                mutp = dut.get_rect()
                mutp.centerx = width*3/4
                mutp.centery = height/2-10
                pygame.draw.rect(screen,GREEN,mutp)
                screen.blit(mut,mutp)
                if mutp.collidepoint(pygame.mouse.get_pos()):
                    ut = font.render("+1 Movement   Cost: " + str(int(shipselect.movespeed * 1.3)),1,YELLOW)
                    utp = ut.get_rect()
                    utp.centerx = width/2
                    utp.centery = dutp.centery + 30
                    screen.blit(ut, utp)
                    if pygame.mouse.get_pressed()[0] and coins >= int(shipselect.movespeed*1.3) and not cvar:
                        cvar = True
                        coins -= int(shipselect.movespeed*1.3)
                        shipselect.movespeed += 1
        pygame.draw.rect(screen,(100,0,0),perkselector)
        for i,x in enumerate(allperks):
            x.draw(i)
        for event in pygame.event.get():
            if event.type==QUIT:
                save()
                pygame.display.quit()
                sys.exit()
        pygame.display.flip()
        if cvar and not pygame.mouse.get_pressed()[0]:
            cvar = False

def Achv_Menu():
    yshift=0
    font=pygame.font.Font(None,32)
    checkmark=pygame.image.load('Resources/Images/Checkmark.PNG')
    checkmark=pygame.transform.scale(checkmark,(50,40))
    checkpos=checkmark.get_rect()
    checkpos.centerx=30
    bbut=ButtonMod.button(width-70,height-50,None,'Back',50,BLACK,YELLOW,breaker,screen,pygame)
    while True:
        screen.blit(background,(0,0))
        for i, x in enumerate(achievements):
            y=height*(i+1)/9-(yshift*height/9)
            if x.achieved:
                checkpos.centery=y
                screen.blit(checkmark,checkpos)
                t=font.render(x.desc,1,(YELLOW))
            else:
                t=font.render(x.desc,1,(RED))
            tpos=t.get_rect()
            tpos.left=60
            tpos.centery=y
            if tpos.width>width-65:
                tpos.width=width-65
            screen.blit(t,tpos)
        x=bbut.draw()
        if x:
            break
        for event in pygame.event.get():
            if event.type==QUIT:
                save()
                pygame.display.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_DOWN:
                    yshift+=1
                if event.key==K_UP:
                    yshift-=1
                if yshift<0:
                    yshift=0
                if yshift>len(achievements)-8:
                    yshift=len(achievements)-8
        pygame.display.flip()

def Stats_Menu():
    screen.blit(background,(0,0))
    global totalkills,tbosskills
    bbut=ButtonMod.button(width-70,height-50,None,'Back',50,BLACK,YELLOW,breaker,screen,pygame)
    font=pygame.font.Font(None,70)
    tkt=font.render('Total Kills: ',1,RED)
    tktp=tkt.get_rect()
    tktp.left=width/4
    tktp.centery=200
    tk=font.render(str(totalkills),1,GREEN)
    tkp=tk.get_rect()
    tkp.left=tktp.right
    tkp.centery=tktp.centery
    tbkt=font.render('Total Boss Kills: ',1,RED)
    tbktp=tbkt.get_rect()
    tbktp.left=width/4
    tbktp.centery=400
    tbk=font.render(str(tbosskills),1,GREEN)
    tbkp=tbk.get_rect()
    tbkp.left=tbktp.right
    tbkp.centery=400
    screen.blit(tkt,tktp)
    screen.blit(tk,tkp)
    screen.blit(tbkt,tbktp)
    screen.blit(tbk,tbkp)
    font = pygame.font.Font(None,50)
    hst = font.render("HIGHSCORES",1,PURPLE)
    hstp = hst.get_rect()
    hstp.top = 15
    hstp.left = 15
    screen.blit(hst,hstp)
    pygame.draw.line(screen,PURPLE,(hstp.left-5,hstp.bottom+5),(hstp.right+5,hstp.bottom +5),3)
    font = pygame.font.Font(None,35)
    et = font.render("EASY: ",1, GREEN)
    est = font.render(str(highscore[0]),1,BLUE)
    mt = font.render("MEDIUM: ",1, YELLOW)
    mst = font.render(str(highscore[1]),1,BLUE)
    ht = font.render("HARD: ",1,RED)
    hdst = font.render(str(highscore[2]),1,BLUE)
    etp = et.get_rect()
    etp.left = 15
    etp.top = hstp.bottom + 12
    screen.blit(et,etp)
    estp = est.get_rect()
    estp.left = etp.right
    estp.top = etp.top
    screen.blit(est,estp)
    mtp = mt.get_rect()
    mtp.top = etp.bottom + 5
    mtp.left = 15
    screen.blit(mt,mtp)
    mstp = mst.get_rect()
    mstp.top = mtp.top
    mstp.left = mtp.right
    screen.blit(mst,mstp)
    htp = ht.get_rect()
    htp.top = mtp.bottom + 5
    htp.left = 15
    screen.blit(ht,htp)
    hdstp = hdst.get_rect()
    hdstp.top = htp.top
    hdstp.left = htp.right
    screen.blit(hdst,hdstp)
    while True:
        x=bbut.draw()
        if x:
            break
        for event in pygame.event.get():
            if event.type==QUIT:
                save()
                pygame.display.quit()
                sys.exit()
        pygame.display.flip()

def save():
    global coins
    f=open('Saves/GDstats.pickle','w')
    sdamages = []
    scooldowns = []
    smovespeeds = []
    for i in ships:
        sdamages.append(i.damage)
        scooldowns.append(i.cooldown)
        smovespeeds.append(i.movespeed)
    pickle.dump([sdamages,scooldowns,smovespeeds,curperk,tbosskills,achv1.achieved,achv2.achieved,achv3.achieved,achv4.achieved,achv5.achieved,achv6.achieved,achv7.achieved,achv8.achieved,achv9.achieved,achv10.achieved,achv11.achieved,achv12.achieved,achv13.achieved,achv14.achieved,achv15.achieved,xp,totalkills,curship,coins,ship1.purchased,ship2.purchased,ship3.purchased,ship4.purchased,ship5.purchased,ship6.purchased, ship7.purchased, highscore], f)
    f.close()

def seteasy():
    global speed, multiplier, difficulty
    difficulty=1
    multiplier=1
    speed=4.5
    Play()

def setmed():
    global speed,multiplier, difficulty
    difficulty=2
    multiplier=2
    speed=6
    Play()

def sethard():
    global speed, multiplier, difficulty
    difficulty=3
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
    breakit = False
    playb=ButtonMod.button(width/2,120, "droidserif",'PLAY',75,BLACK,WHITE,difficultymenu,screen,pygame)
    shopb=ButtonMod.button(width/2,250, "droidserif",'SHOP',60,BLACK,WHITE,shop,screen,pygame)
    achvb=ButtonMod.button(width/2,380, "droidserif",'Achievements',60,BLACK,WHITE,Achv_Menu,screen,pygame)
    statb=ButtonMod.button(width/2,510, "droidserif",'Statistics',60,BLACK,WHITE,Stats_Menu,screen,pygame)
    while True:
        screen.blit(background,(0,0))
        draw_Rank()
        playb.draw()
        shopb.draw()
        achvb.draw()
        statb.draw()
        for event in pygame.event.get():
            if event.type==QUIT:
                save()
                breakit = True

        if breakit:
            break

        pygame.display.flip()

def OpenAnimation():
    fsize = 0
    angle = 0
    alpha = pygame.Surface((width, height))
    while angle<360:
        fsize += 5.5
        angle += 20
        alpha.blit(background,(0,0))
        font = pygame.font.SysFont("droidserif",int(fsize),bold = True, italic = True)
        gtext = font.render("GALAXY DEFENDER", 1, RED)
        gtext = pygame.transform.rotate(gtext, angle)
        gpos = gtext.get_rect()
        gpos.centerx = width/2
        gpos.centery = height/2
        alpha.blit(gtext,gpos)
        screen.blit(alpha, (0,0))
        pygame.display.flip()
    time.sleep(2)
    a = 252
    while a > 0:
        a -= 9
        alpha.set_alpha(a)
        screen.blit(background,(0,0))
        screen.blit(alpha,(0,0))
        pygame.display.flip()



OpenAnimation()
MainMenu()


pygame.display.quit()
