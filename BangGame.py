from math import trunc
from sys import winver
from CauHinh import *
import os
from copy import deepcopy
import pygame
from tkinter import *
from tkinter import messagebox
import time

# Module này khởi tạo bàn cờ với số lượng quân việc xử lý phân bố cờ của người chơi


COLOR = color()

def text_to_screen(screen , text , x , y, fontsize ,color): #Print Notification to your screen
    try:
        pygame.font.init()
        myfont = pygame.font.Sys('Arial', fontsize)
        textsurface = myfont.render(text, True, color)
        screen.blit(textsurface, (x, y))

    except Exception as e:
        PrintError()
    
def ipos(pos, inc = 1 ):
    ''''''
    return (pos + inc) % 12
    
def fill_if_empty(_state, _player_point):
    state, player_point = deepcopy(_state), deepcopy(_player_point)

    if not any([i[0] for i in state[1:6]]):
        player_point[0] -= 5

        for i in range(1,6):
            state[i][0] = 1
    
    if not any([i[0] for i in state[7:12]]):
        player_point[1] -= 5

        for i in range(7,12):
            state[i][0] = 1
    return state, player_point

def finished(_state):
    return _state[0] == [0, 2] and _state[6] == [0, 2]

def play_turn(_state , _player_point, _move , SLQuan = 5):
    state , player_point  = deepcopy(_state), deepcopy(_player_point)
    move = _move

    player = 0 if 0 < move[0] < 6 else 1

    inc = 1 if move[1] == 'r' else -1

    cur_pos = move[0]
    next_pos = ipos(cur_pos, inc)

    for _ in range (state[cur_pos][0]):
        state[next_pos][0] += 1
        next_pos = ipos(next_pos,inc)
    state[cur_pos][0] //= 12

    while True:
        state, player_point = fill_if_empty(state, player_point)

        if state[next_pos][1] or (state[next_pos][0] == 0 and state[ipos(next_pos, inc)][0] == 0 and state[ipos(next_pos,inc)][1] != 1):
            #Kết thúc lượt chơi
            break
        elif state[next_pos][0] == 0 and (state[ipos(next_pos, inc)][0] or state[ipos(next_pos, inc)][1] == 1):
            #Ghi điểm
            if state[ipos(next_pos , inc)][1] == 1:
                player_point[player] += SLQuan
                state[ipos(next_pos ,inc)][1] = 2

            player_point[player] += state[ipos(next_pos , inc)][0]
            state[ipos(next_pos,inc)][0] = 0

            temp_pos = ipos(ipos(next_pos , inc) , inc)
            if state[temp_pos][0] == 0 and state[temp_pos][1] != 1: # Kiểm tra ô trên bàn cờ đang trống hay không
                next_pos = temp_pos
            else:
                break
        else:
            #Tiếp tục phân phối sỏi tới các ô khác trên bàn cờ
            cur_pos = next_pos
            next_pos = ipos(cur_pos,inc)

            for _ in range(state[cur_pos][0]):
                state[next_pos][0] += 1
                next_pos = ipos(next_pos, inc)
            state[cur_pos][0] //= 12
    return state , player_point

class Table:
    def __init__(self) : #Khơi tạo bảng game 2 Chiều
        self.state = [[0, 1], [5, 0],[5, 0],[5, 0],[5, 0],[5, 0],
                      [0, 1], [5, 0],[5, 0],[5, 0],[5, 0],[5, 0]]
        self.player_points = [0, 0]
        self.SLquan = SLQuan

    def __str__(self): #định dạng bảng game
        return '''
            11 10  9  8  7  6 
        +--+--------------+--+
        |{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|{:2}|
        |{:2}|--------------|{:2}|
        |  |{:2}|{:2}|{:2}|{:2}|{:2}|  |
        +--+--------------+--+
          0  1  2  3  4  5

        USER_0: {} USER_1: {}
        '''.format(
            " *" if self.state[0][1] == 1 else " ",
                self.state[11][0] if self.state[11][0] else '',
                self.state[10][0] if self.state[10][0] else '',
                self.state[9][0] if self.state[9][0] else '',
                self.state[8][0] if self.state[8][0] else '',
                self.state[7][0] if self.state[7][0] else '',
                " *" if self.state[6][1] == 1 else " ",  
                self.state[0][0] if self.state[0][0] else '',
                self.state[6][0] if self.state[6][0] else '',
                self.state[1][0] if self.state[1][0] else '',
                self.state[2][0] if self.state[2][0] else '',
                self.state[3][0] if self.state[3][0] else '',
                self.state[4][0] if self.state[4][0] else '',
                self.state[5][0] if self.state[5][0] else '',
                self.player_points[0], self.player_points[1]
        )

    def finished(self): # Điền Kiện và Thông Báo kết trò chơi
        '''This Definitation will use whenever this game finished'''
        if finished(self.state):
            if self.player_points[0] > self.player_points[1]:
                result = "You Win"
            elif self.player_points[0] < self.player_points[1]:
                result = "Computer has win"
            else:
                result = "This game was draw"
            print("End!!!")

            # endscreen = pygame.display.set_mode((400, 300))
            # text_to_screen(endscreen, 'Winner is ' + winner)

            while True:
                Tk().wm_withdraw()
                messagebox.showinfo('GAME HAS OVER', 'RESULT: ' +  result)
                time.sleep(2)
                break;
            return True
        else:
            return False

    def play(self , move): #Rải sỏi
        self.state, self.player_points = play_turn(self.state, self.player_points , move)
        if finished(self.state):
            self.player_points[0] += sum([self.state[i][0] for i in range(1 , 6)])
            self.player_points[1] += sum([self.state[i][0] for i in range(7 ,12)])
            for i in range(0, 12):
                self.state[i][0] = 0
        self.redraw(1)

if __name__ == '__main__':
    table = Table()
    print(table)
    table.play((2,'r'))
    print(table)