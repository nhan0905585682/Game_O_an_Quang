import pygame
import os
from math import gamma, pi as PI
from Computer_Brain import *
from pygame import mouse
from CauHinh import *
from BangGame import Table
from BangGame import *

background = pygame.image.load(os.path.join(RES,'background.png'))


#Định dạng thuộc tính của các quân cờ 
O_Thuong = (50, 50)
O_Quan = (100 , 100) # Vẽ hình vòng cung , (x,y)

Norm = pygame.image.load(os.path.join(RES , 'dan.png')) # Load ảnh Dân
Boss = pygame.image.load(os.path.join(RES , 'quan1.png')) # Load ảnh quan
Boss2 = pygame.image.load(os.path.join(RES , 'quan.png'))
SLQuan = 10 # Số lượng quân cho mỗi ô
statistic = [0 ,0 ,0]
Total_score = [0,0]
Highest = [0,0]

COLOR= color()

def text_to_screen(screen , text ,x ,y,fontsize, color):
    try:
        pygame.font.init()

        myfont = pygame.font.SysFont('Arial' , fontsize)

        textsurface = myfont.render(text , True, color)

        screen.blit(textsurface, (x, y))
    except Exception as e:
        PrintError()
    
def buttonpress(marginleft , screen , marginright , marginup , margindown , xbuttonleft , ybuttonleft , xbuttonright , ybuttonright , flag , move1, move0 , point): # Check stabilization of left and righ button i may be check event mouse hover of pointer
    if point:
        mouse = pygame.mouse.get_pos()
        move0 = (marginleft - 60)/100

        if marginleft < mouse[0] < marginright and marginup < mouse[1] < margindown:
            flag = True

        if flag:
            screen.blit(RNavigation, (xbuttonright, ybuttonright))
            screen.blit(LNavigation, (xbuttonleft , ybuttonleft))
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and xbuttonright < mouse[0] < xbuttonright + 20 and ybuttonright < mouse[1] < ybuttonright + 20:
                print("Right Clicked!")
                move1 = 'r'
            elif e.type == pygame.MOUSEBUTTONDOWN and xbuttonleft < mouse[0] < xbuttonleft + 20 and ybuttonleft < mouse[1] < ybuttonleft + 20:
                print("Left Clicked !")
                move1 = 'l'
    flag = False
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.QUIT()
            sys.exit()

    move = (move0 ,move1)
    return move


class User_Interface(Table):

    def __init__(self , screen  = None):
        super().__init__()
        self.screen = screen
        if screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
            pygame.display.set_caption(SCR_NAME)

    def __draw_table(self,  turn): # hiển thị tên người chơi và điểm
        self.screen.fill((255,255,255))
        self.screen.blit(background, (0,0))
        text_to_screen(self.screen, "Player 1 " , 200, 60, 25, COLOR.darkred)
        text_to_screen(self.screen ,str(self.player_points[1]), 370 , 40 , 50 , COLOR.darkred)
        text_to_screen(self.screen , "Player 0 " , 470 , 380 , 25 , COLOR.purple)
        text_to_screen(self.screen , str(self.player_points[0]), 370 , 365 , 50 , COLOR.purple)
        
        if turn == 0:
            text_to_screen(self.screen , "Player " + str(turn) + " is thinking ..." , 300, 450 , 20 , COLOR.purple)
        else:
            text_to_screen(self.screen , "Player " + str(turn) + " is thinking ..." , 300 , 10 , 20 , COLOR.red)


        # So quan trong cac o thuong
        text_to_screen(self.screen, str(self.state[11][0]), 170, 150, 20, COLOR.orange) #No. 11
        text_to_screen(self.screen, str(self.state[10][0]), 270, 150, 20, COLOR.orange) #No. 10
        text_to_screen(self.screen, str(self.state[9][0]), 370, 150, 20, COLOR.orange) #No. 9
        text_to_screen(self.screen, str(self.state[8][0]), 470, 150, 20, COLOR.orange) #No. 8
        text_to_screen(self.screen, str(self.state[7][0]), 570, 150, 20, COLOR.orange) #No. 7
        text_to_screen(self.screen, str(self.state[1][0]), 170, 250, 20, COLOR.orange) #No. 1
        text_to_screen(self.screen, str(self.state[2][0]), 270, 250, 20, COLOR.orange) #No. 2
        text_to_screen(self.screen, str(self.state[3][0]), 370, 250, 20, COLOR.orange) #No. 3
        text_to_screen(self.screen, str(self.state[4][0]), 470, 250, 20, COLOR.orange) #No. 4
        text_to_screen(self.screen, str(self.state[5][0]), 570, 250, 20, COLOR.orange) #No. 5 

        #bang co theo thu tu tu trai sang phai theo moi voi 5 o quan co thuong se xuat hien mot o quan nhung vay
        #co the thay duoc neu bat dau la o quan o vi tri thu 0 thi theo chu ky o o thu 6 cua chung ta se tiep xuat
        #mot o quan nua

        # so quan trong trong cac o quan
        text_to_screen(self.screen, str(abs(self.state[0][1] - 2)), 120, 170, 30, COLOR.orange)
        text_to_screen(self.screen, str(self.state[0][0]), 120, 230, 20, COLOR.orange) #No. 0

        text_to_screen(self.screen, str(abs(self.state[6][1] - 2)), 670, 170, 30, COLOR.orange)
        text_to_screen(self.screen, str(self.state[6][0]), 670, 230, 20, COLOR.orange) #No. 6

        # Drawing the soldiers and Commander
        if (self.state[0][1] == 1):
            self.screen.blit(Boss , (80 , 200))
            self.screen.blit(Boss2, (685 , 200))
            
           # Dat soi quan tren o ben trai
        if (self.state[0][0] >= 1): self.screen.blit(Norm, (130, 260))
        if (self.state[0][0] >= 2): self.screen.blit(Norm, (130, 275))
        if (self.state[0][0] >= 3): self.screen.blit(Norm, (115, 260))
        if (self.state[0][0] >= 4): self.screen.blit(Norm, (115, 275))
        if (self.state[0][0] >= 5): self.screen.blit(Norm, (100, 260))
        if (self.state[0][0] >= 6): self.screen.blit(Norm, (100, 275))
        if (self.state[0][0] >= 7): self.screen.blit(Norm, (85, 260))
        if (self.state[0][0] >= 8): self.screen.blit(Norm, (85, 275))

        # Dat soi quan tren o ben phai
        if (self.state[6][0] >= 1): self.screen.blit(Norm, (660, 260))
        if (self.state[6][0] >= 2): self.screen.blit(Norm, (660, 275))
        if (self.state[6][0] >= 3): self.screen.blit(Norm, (675, 260))
        if (self.state[6][0] >= 4): self.screen.blit(Norm, (675, 275))
        if (self.state[6][0] >= 5): self.screen.blit(Norm, (690, 260))
        if (self.state[6][0] >= 6): self.screen.blit(Norm, (690, 275))
        if (self.state[6][0] >= 7): self.screen.blit(Norm, (705, 260))
        if (self.state[6][0] >= 8): self.screen.blit(Norm, (705, 275))

        #Set Ways to User_0
        for i in range(1,6):
            if (self.state[i][0] >= 1):
                self.screen.blit(Norm , (75 + 100*i , 285))
            if (self.state[i][0] >= 2):
                self.screen.blit(Norm, (75 + 100*i , 300))
            if (self.state[i][0] >= 3):
                self.screen.blit(Norm, (90 + 100*i , 285))
            if (self.state[i][0] >= 4):
                self.screen.blit(Norm, (90 + 100*i , 300))
            if (self.state[i][0] >= 5):
                self.screen.blit(Norm, (105 + 100*i , 285))
            if (self.state[i][0] >= 6):
                self.screen.blit(Norm, (105 + 100*i , 300))
            if (self.state[i][0] >= 7):
                self.screen.blit(Norm, (120 + 100*i , 285))
            if (self.state[i][0] >=7 ):
                self.screen.blit(Norm, (120 + 100*i , 300))
            
        #Set ways For Player 1

        for i in range (7 , 12):
            if (self.state[i][0] >= 1 ):
                self.screen.blit(Norm, (75 + 100*(12-i) , 185))
            if (self.state[i][0] >= 2):
                self.screen.blit(Norm, (75 + 100*(12-i) , 200))
            if (self.state[i][0] >= 3):
                self.screen.blit(Norm, (90 + 100*(12-i) , 185))
            if (self.state[i][0] >= 4):
                self.screen.blit(Norm, (90 + 100*(12-i) , 200))
            if (self.state[i][0] >= 5):
                self.screen.blit (Norm, (105 + 100*(12-i) , 185))
            if (self.state[i][0] >= 6):
                self.screen.blit (Norm , (105 + 100*(12-i) , 200))
            if (self.state[i][0] >= 7):
                self.screen.blit (Norm , (120 + 100*(12-i) , 185))
            if (self.state[i][0] >= 8 ):
                self.screen.blit (Norm , (120 + 100*(12-i) , 200))

        pygame.display.flip()

    def redraw(self , turn): # tái tạo lại bảng game
        self.__draw_table(turn)

if __name__ == '__main__':
    table = User_Interface()
    table.redraw()
    print(table)