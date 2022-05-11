'''
Mandarin Square Capturing
'''

import random
import copy
import pygame,sys
import math
import time
import concurrent.futures
import os

from User_Interface import User_Interface
from Computer_Brain import Computer_Brain
from CauHinh import *

def text_to_screen(screen , text , x ,y , fontsize , color): # Quy hoạch font chữ cho trò chơi
    try:
        pygame.font.init()
        myfont = pygame.font.SysFont('Arial' , fontsize)
        textsurface = myfont.render(text , True , color)
        screen.blit(textsurface , (x ,y))

    except Exception as e:
        print('Font Error\nPlease recheck this font which is call and ensure that it was exist in your system')
        raise e

class GamePlay:
    def __init__(self, algo_0= None , algo_1 = None): # Khởi tạo của sổ Window với các thông số được lấy từ module cấu hình
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.screen = pygame.display.set_mode((SCR_WIDTH , SCR_HEIGHT))
        pygame.display.set_caption(SCR_NAME)

        self.table = User_Interface(self.screen)
        self.Computer_Brain = [Computer_Brain(0 , algo_0 , self.screen , self.table), Computer_Brain(1 , algo_1 , self.screen , self.table)]
        self.move = None

    def redraw(self, turn): # cập nhập lại bảng game trên terminal
        self.table.redraw(turn)
    
    def finished(self): # Xuất Thông báo kết thúc và kết quả
        return self.table.finished()

    def Update(self , move): # Cập nhập trên cửa sổ
        self.table.play(move)

    def run(self): # Thiếp lập game
        
        excutor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        turn = 0 if TienPhong else 1
        running = True

        # Loop

        self.redraw(turn)
        while not self.finished():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            move = self.Computer_Brain[turn].execute(self.table.state , self.table.player_points)
            self.Update(move)

            print(f"USER_{turn}'s move: {move[0]} {move[1]}")
            text_to_screen(self.screen , "User", 0,0,30,(123,123,123))

            turn ^=1
            self.redraw(turn)
            print(self.table)
            time.sleep(1)
            excutor.submit(self.redraw)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()