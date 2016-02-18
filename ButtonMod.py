class button():
    def __init__(self,x,y,fontname,text,textsize,textcolor,rectcolor,function,displayname,pygamemodname):
        self.pygame=pygamemodname
        font=self.pygame.font.SysFont(fontname,textsize)
        self.text=font.render(text,1,textcolor)
        self.rect=self.text.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.rectcolor=rectcolor
        self.function=function
        self.dispname=displayname
    def draw(self):
        x=False
        self.pygame.draw.rect(self.dispname,self.rectcolor,self.rect)
        self.dispname.blit(self.text,self.rect)
        a,b,c=self.pygame.mouse.get_pressed()
        if self.rect.collidepoint(self.pygame.mouse.get_pos()) and a:
            x=self.function()
        return x
