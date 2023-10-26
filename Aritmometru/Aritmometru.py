from posixpath import isabs
import sys
import pygame
import pygame_widgets
import math
import os

from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


pygame.init()
pygame.font.init()
pygame.mixer.init()
fps = 60
fpsClock = pygame.time.Clock()
w, h = 1300, 600
screen = pygame.display.set_mode((w, h))
font = pygame.font.SysFont('Arial', 20)
sound = 'sound'
btnClickedAudio = pygame.mixer.Sound(os.path.join(sound, 'btn_click.ogg'))
accMoveAudio = pygame.mixer.Sound(os.path.join(sound, 'accumulator_slide.ogg'))
playSound = False

objects = []

class Button():
    def __init__(self, x, y, width, height,audio, buttonText = 'Button', onClickFunction = None, onePress = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.flipped = False
        self.audio = audio
        self.textImg = pygame.image.load('images/add.png')

        self.fillColors = {
            'normal' : '#ffffff',
            'hover': '#666666',
            'pressed' : '#333333'
            }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20,20,20))


    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onClickFunction()
                elif not self.alreadyPressed:
                    pygame.mixer.Sound.play(self.audio)
                    self.onClickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
        screen.blit(self.buttonSurface, self.buttonRect)


    

class Aritmometru():
    def __init__ (self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.count = 0
        self.fillColors = {
            'normal': '#232d3d'
            }
        self.surface = pygame.Surface((self.width, self.height))
        self.textImg = pygame.image.load('images/add.png')
        
        #self.img = pygame.image.load().convert()

        self.isAdd = True
        self.playSound = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.btnMoveLeft = Button(200,460,100,50,accMoveAudio,'<<',self.shiftLeft)
        self.btnMoveRight = Button(730,460,100,50,accMoveAudio,'>>', self.shiftRight)
        self.btnOperation = Button(200,260,100,50,btnClickedAudio,"Operation", self.operation )
        self.btnComputeOp = Button(200,360,100,50,btnClickedAudio,"Compute", self.compute)
        self.btnResetOp = Button(730,320,100,50,btnClickedAudio, "Reset Op", self.resetOp)
        self.btnResetAcc = Button(730,250,100,50,btnClickedAudio, "Reset Acc", self.resetAcc)
        self.displayValue = 0
        self.currentValue = 0
        self.opValue = 0
        self.execCnt = 0

        self.accPos = [180,150]

        self.opSign = TextBox(screen, 100, 270, 40, 30, fontSize=30, radius = 14)

        self.accumulator = []
        for i in range(0,7):
            self.accumulator.append(TextBox(screen, self.accPos[0] , self.accPos[1] , 40, 30, fontSize=30, radius = 14))
            if i > 0:
                self.accumulator[i].setX(self.accPos[0] + i*(self.accumulator[i].getWidth()+30))
            self.accumulator[i].disable()



        self.opPos = [677,400]
        self.opDisplay = []
        for i in range(0,4):
            self.opDisplay.append(TextBox(screen, self.opPos[0] , self.opPos[1] , 40, 30, fontSize=30, radius = 14))
            if i > 0: self.opDisplay[i].setX(self.opPos[0] + i*(self.opDisplay[i].getWidth()+15))
            self.opDisplay[i].disable()
        
        self.slider1 = Slider(screen, 400, 300, 20,200, min=0, max=9, step=1, vertical = True, initial = 0)
        
        self.output1 = TextBox(screen, self.slider1.getX() - 10, self.slider1.getY() - 60 , 40, 30, fontSize=30, radius = 14)

        self.slider2 = Slider(screen, 470, 300, 20,200, min=0, max=9, step=1, vertical = True, initial = 0)
        self.output2 = TextBox(screen, self.slider2.getX() - 10, self.slider2.getY() - 60 , 40, 30, fontSize=30, radius = 14)

        self.slider3 = Slider(screen, 540, 300, 20,200, min=0, max=9, step=1, vertical = True, initial = 0)
        self.output3 = TextBox(screen, self.slider3.getX() - 10, self.slider3.getY() - 60 , 40, 30, fontSize=30, radius = 14)
        
        self.slider4 = Slider(screen, 610, 300, 20,200, min=0, max=9, step=1, vertical = True, initial = 0)
        self.output4 = TextBox(screen, self.slider4.getX() - 10, self.slider4.getY() - 60 , 40, 30, fontSize=30, radius = 14)
        
        self.output1.disable()
        self.output2.disable()
        self.output3.disable()
        self.output4.disable()
        self.opSign.disable()
        
        objects.append(self)

    def add(self):
        self.displayValue += self.currentValue*pow(10, self.count)
        #print(self.displayValue)

    def subtract(self):
        self.displayValue -= self.currentValue*pow(10, self.count)

    def compute(self):
        self.opValue += pow(10,self.count)
        if self.isAdd :
            self.add()
        else:
            self.subtract()

    def operation(self):
        self.isAdd = not self.isAdd
        if self.isAdd == True:
            self.textImg = pygame.image.load('images/add.png')
        else:
            self.textImg = pygame.image.load('images/subtract.png')
    
    def shiftLeft(self):
        if self.count > 0:
            self.count -=1
            self.accPos[0] -= 70
            for i in range(0,7):
                    self.accumulator[i].setX(self.accPos[0] + i*(self.accumulator[i].getWidth()+30))
         
    def resetOp(self):
        self.opValue = 0

    def resetAcc(self):
        self.displayValue = 0

    def shiftRight(self):
        if self.count < 3:
            self.count +=1
            self.accPos[0] += 70
            for i in range(0,7):
                    self.accumulator[i].setX(self.accPos[0] + i*(self.accumulator[i].getWidth()+30))
 

    def process(self):
        
        pygame.draw.rect(screen, self.fillColors['normal'], self.rect, 0, 20)
        #screen.blit(self.surface, self.rect)
        if self.playSound and self.output1.getText() != str(self.slider1.getValue()):  
            pygame.mixer.Sound.play(btnClickedAudio)
        if self.playSound and self.output2.getText() != str(self.slider2.getValue()):  
            pygame.mixer.Sound.play(btnClickedAudio)
        if self.playSound and self.output3.getText() != str(self.slider3.getValue()):  
            pygame.mixer.Sound.play(btnClickedAudio)
        if self.playSound and self.output4.getText() != str(self.slider4.getValue()):  
            pygame.mixer.Sound.play(btnClickedAudio)
        self.output1.setText(self.slider1.getValue())
        self.output2.setText(self.slider2.getValue())
        self.output3.setText(self.slider3.getValue())
        self.output4.setText(self.slider4.getValue())
        self.currentValue=self.slider1.getValue()*1000+self.slider2.getValue()*100+self.slider3.getValue()*10+self.slider4.getValue()
        if self.isAdd:
            self.opSign.setText('+|x')
        else:
            self.opSign.setText('-|/')

        if self.displayValue < 0:
            self.displayValue = 0
        self.displayValue=self.displayValue % 10000000
       
        self.aux = self.displayValue
        for i in range(6,-1,-1):
            self.accumulator[i].setText(math.floor(self.aux % 10))
            self.aux /= 10;

        self.aux = self.opValue
        for i in range(3,-1,-1):
            self.opDisplay[i].setText(math.floor(self.aux%10))
            self.aux /= 10

        self.btnMoveLeft.process()
        self.btnMoveRight.process()
        self.btnOperation.process()
        self.btnComputeOp.process()
        self.btnResetOp.process()
        self.btnResetAcc.process()
        self.surface.blit(self.btnMoveLeft.buttonSurface,self.btnMoveLeft.buttonRect)
        self.surface.blit(self.btnMoveRight.buttonSurface,self.btnMoveRight.buttonRect)
        self.surface.blit(self.btnOperation.buttonSurface,self.btnOperation.buttonRect)
        self.surface.blit(self.btnComputeOp.buttonSurface,self.btnComputeOp.buttonRect)
        self.surface.blit(self.btnResetOp.buttonSurface, self.btnResetOp.buttonRect)
        self.surface.blit(self.btnResetAcc.buttonSurface, self.btnResetAcc.buttonRect)
        
        self.playSound = True
        
        if self.isAdd==True:
            screen.blit(self.textImg,(900,140))
        else:
            screen.blit(self.textImg,(900,50))

run = True
Aritmometru(30, 30, 1240, 540)  

while run:
    screen.fill((20, 20, 20))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
    for object in objects:
        object.process()
    
    pygame_widgets.update(events)
    pygame.display.update()
    pygame.display.flip()
    fpsClock.tick(fps)