#!/usr/bin/python

import pygame, timeit, random, ButtonMod, pickle, sys, math, time
from random import randint as rand
from pygame.locals import *

pygame.init()

clock=pygame.time.Clock()

sound=pygame.mixer.Sound('Resources/Sound_Effects/shoot.wav')

global tbosskills, coins, totalkills, collateral, doubleh, doublec, perkselector

locked=pygame.image.load('Resources/Images/locked.png')
locked=pygame.transform.scale(locked,(70,70))

bossimg=pygame.image.load('Resources/Images/Boss.PNG')
bossimg=pygame.transform.scale(bossimg,(100,113))

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
            if self.cmulti() and self.ckills() and self.cdiff() and self.chealth() and self.ctotalk() and self.ctbossk():
                self.bantime=timeit.default_timer()+3
                xp+=self.rewxp
                coins+=self.rewcoins
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
        

ship1=pship(pygame.image.load('Resources/Images/PlayerShip1.PNG'), 0, True)
ship2=pship(pygame.image.load('Resources/Images/PlayerShip2.PNG'), 25, False)
ship3=pship(pygame.image.load('Resources/Images/PlayerShip3.PNG'), 50, False)
ship4=pship(pygame.image.load('Resources/Images/PlayerShip4.PNG'), 100, False)
ship5=pship(pygame.image.load('Resources/Images/PlayerShip5.PNG'), 150, False)
ship6=pship(pygame.image.load('Resources/Images/PlayerShip6.PNG'), 200, False)

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

perk1=perks(pygame.image.load('Resources/Images/perk1.PNG'),perk1_init,3,'Bullets May Pass Through Multiple Targets')
perk2=perks(pygame.image.load('Resources/Images/perk2.PNG'),perk2_init,5,'Double Health. Does not affect direct hits')
perk3=perks(pygame.image.load('Resources/Images/perk3.PNG'),perk3_init,7,'Coins are worth twice as much')

allperks=[perk1,perk2,perk3]

collateral=False
doubleh=100
doublec=1

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

achievements=[achv1,achv2,achv3,achv4,achv5,achv6,achv7,achv8,achv9,achv10]

try:
    f=open('Saves/GDstats.pickle')
    tbosskills,achv1.achieved,achv2.achieved,achv3.achieved,achv4.achieved,achv5.achieved,achv6.achieved,achv7.achieved,achv8.achieved,achv9.achieved,achv10.achieved,xp,totalkills,curship,coins,ship1.purchased,ship2.purchased,ship3.purchased,ship4.purchased,ship5.purchased,ship6.purchased=pickle.load(f)
    f.close()
except:
    print 'No previous stats'
    tbosskills=0
    coins=0
    curship=0
    totalkills=0
    xp=0

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

version=1

screen=pygame.display.set_mode((width, height))
pygame.display.set_caption('Galaxy Defender V'+str(version))

background=pygame.Surface(screen.get_size())
background=background.convert()
background.fill(BLACK)

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
                self.rect=enspecks.get_rect()
                self.rect.centerx=self.x
                self.rect.centery=self.y
                screen.blit(enspecks,self.rect)
            else:
                if self.num>10:
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
    def __init__(self, x, y, image):
        self.x=x
        self.rect=pygame.Rect(x-25,y-25,50,50)
        self.image=image
        self.active=True
    def draw(self):
        global health, speed
        self.rect.centery+=speed
        self.rect.centerx=self.x+(60*math.sin(self.rect.centery/50.0))
        if self.rect.centery>height+25:
            if self.active:
                health-=10
            enemies.pop()
        if self.active==True:
            screen.blit(self.image,self.rect)

class Boss():
    def __init__(self):
        global difficulty
        self.img=bossimg
        self.rect=self.img.get_rect()
        self.rect.centerx=width/2
        self.y=float(-60)
        self.rect.centery=self.y
        self.shealth=400*difficulty/2
        self.health=self.shealth
        self.sheild=False
        self.sheilds=[]
        self.intervals=[]
        for i in range(1,5):
            self.intervals.append(self.health*i/5)
    def draw(self):
        global multiplier,score,xp,tbosskills
        self.y+=.7
        self.rect.centery=self.y
        if self.check_intervals() and not self.sheild:
            self.intervals.pop()
            self.sheild=True
            a=rand(0,360)
            self.sheilds=[Boss_sheild(a,0),Boss_sheild(a+(6.28/4),1),Boss_sheild(a+3.14,2),Boss_sheild(a-(3.14/2),3)]
            enemies.insert(0,enemy(width/4,-30, enemyimgs[rand(0,len(enemyimgs)-1)]))
            enemies.insert(0,enemy(width*3/4,-30, enemyimgs[rand(0,len(enemyimgs)-1)]))
        if self.sheilds:
            for i in self.sheilds:
                i.draw(self.rect.centerx,self.rect.centery)
        else:
            self.sheild=False
        if self.health<=0:
            bosses.pop()
            score+=500
            xp+=30*multiplier
            tbosskills+=1
        thr=pygame.Rect(self.rect.left,self.rect.top-5, self.rect.width,10)
        hr=pygame.Rect(self.rect.left,self.rect.top-5,(self.rect.width*self.health/self.shealth),10)
        pygame.draw.rect(screen,(100,100,100),thr)
        pygame.draw.rect(screen,GREEN,hr)
        screen.blit(self.img,self.rect)
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
        self.deg+=0.08
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
    def run(self):
        global spawnrate, score, coins,kills,totalkills
        self.rect.centery-=15
        if self.active:
            pygame.draw.rect(screen,(255,255,255),self.rect)
            for i in enemies:
                if self.rect.colliderect(i.rect) and i.active:
                    if not collateral:
                        self.active=False
                    i.active=False
                    spawnrate=spawnrate*.95
                    if spawnrate<.3:
                        spawnrate=.15
                    score+=100
                    kills+=1
                    self.hits+=1
                    totalkills+=1
                    explosions.insert(0,explosion(i.rect.centerx,i.rect.centery))
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
                        i.health-=20
                        
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
            self.rect.centerx+=15
        if self.rect.centerx>width-30:
            self.rect.centerx=width-30
        if k[pygame.K_LEFT]:
            self.rect.centerx-=15
        if self.rect.centerx<30:
            self.rect.centerx=30
        if k[pygame.K_SPACE]:
            if self.shootvar:
                self.shootvar=False
                sound.play()
                pbullets.insert(0,playerbullet(self.rect.centerx,self.rect.centery-30))
        else:
            self.shootvar=True
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
    global spawnTimer
    if timeit.default_timer()-spawnTimer>0:
        enemies.insert(0,enemy(rand(60, width-60),-30, enemyimgs[rand(0,len(enemyimgs)-1)]))
        spawnTimer=timeit.default_timer()+spawnrate

def spawnCoins():
    global cspawnTimer, coinslist
    if timeit.default_timer()-cspawnTimer>0:
        coinslist.insert(0,coinob(-20,rand(0,height/2)))
        cspawnTimer=timeit.default_timer()+rand(10,20)

def Results():
    global kills, newcoins, score, totalkills, xp, multiplier
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
    screen.blit(coinsicon,cirect)
    screen.blit(st,stp)
    screen.blit(ct,ctp)

def Play():
    global bosses, coinsicon, cirect, doubleh, health, kills, newcoins, coinslist, cspawnTimer, player1, pbullets, enemies, explosions, spawnrate, spawnTimer, gameover, score
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
    while True:
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

        if score in [1500,5000,10000,20000,30000,40000,50000,60000,70000,80000,90000,100000]:
            while enemies:
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
                for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.display.quit()

                pygame.display.flip()
                
                clock.tick(33)

                if gameover:
                    break
                for i in achievements:
                    if not i.achieved:
                        i.check()

            bosses=[Boss()]
            while bosses:
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
                health_bar()
                for i in achievements:
                    if not i.achieved:
                        i.check()
                for i in achievements:
                    if not i.achieved:
                        i.check()

                for event in pygame.event.get():
                    if event.type==QUIT:
                        pygame.display.quit()

                pygame.display.flip()
                
                clock.tick(33)

                if gameover:
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
    pickle.dump([tbosskills,achv1.achieved,achv2.achieved,achv3.achieved,achv4.achieved,achv5.achieved,achv6.achieved,achv7.achieved,achv8.achieved,achv9.achieved,achv10.achieved,xp,totalkills,curship,coins,ship1.purchased,ship2.purchased,ship3.purchased,ship4.purchased,ship5.purchased,ship6.purchased], f)
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
                pygame.display.quit()
                sys.exit()

        pygame.display.flip()


MainMenu()


pygame.display.quit()
