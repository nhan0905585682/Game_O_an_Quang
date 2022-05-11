from CauHinh import *
import os
import pygame
import time
import sys
from CauHinh import PrintError
from GamePlay import GamePlay
import sys

def text_to_screen(screen , text , x ,y , fontsize , color ):
    try:
        pygame.font.init()
        myfont = pygame.font.SysFont('Arial' , fontsize)
        textsurface = myfont.render(text , True , color)
        screen.blit(textsurface, (x ,y ))
    except Exception as e:
        issues = PrintError()

class Menu_Choose:
    def __init__(): # Hàm khởi tạo Menu cho phép người chơi chọn chế độ chơi cũng như dừng trò chơi
        while True:
            print('\n _---------------------------------_')
            print('\n_    Mandaring Square Capturing     _')
            print('\n --________________________________--')
            print('\n')
            print('\n Hello and welcome every player to take part in this game')
            print('\n Let is me introduce a few a about this')
            print('\n[1]        Play with Computer Medium            ')
            print('\n[2]        Play with random mode                ')
            print('\n[3]        Play With Computer Hard              ')
            print('\n[4]        Play with another Player             ')
            print('\n[5]        Exit Game                            ')
            print('\n')
            Algorithms = input("Please choose mode which you want to play: ")
            if (Algorithms not in ('1' , '2' , '3' , '4' , '5')):
                print('Pleae choose again your selection is not suitable')
                continue
            
            if Algorithms == '1':
                game = GamePlay(algo_0=None , algo_1= 'alpha_beta')
                game.run()
            if Algorithms == '3':
                game = GamePlay(algo_0=None , algo_1= 'expectimax')
                game.run()
            if Algorithms == '2':
                game = GamePlay(algo_0=None , algo_1= 'random')
                game.run()
            if Algorithms == '4':
                game = GamePlay(algo_0=None , algo_1= 'human')
                game.run()
            if Algorithms == '5':
                break 
        print("\n GoodBye.")
        time.sleep(2)
        sys.exit()   
    
