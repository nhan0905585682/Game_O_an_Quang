from math import trunc
import pygame
import os
from pygame import mouse
from CauHinh import *
from copy import deepcopy
from random import shuffle, choice, randint
from BangGame import fill_if_empty, finished , play_turn
import time
import sys
# module này chủ yếu thể hiện về quy tắc vận hành của một bàn cờ và cách thức xử lý của máy tính khi gặp trường hợp
# đặc biệt chủ yếu viết về cách xử lý trong bàn cờ


LNavigation = pygame.image.load(os.path.join(RES, 'left.png')) # Di chuyển quân sang trái
RNavigation = pygame.image.load(os.path.join(RES, 'right.png')) # Di chuyển quân sang phải

class Computer_Brain:
    def __init__(self , player_id , algo = None, screen = None , table = None): # Khởi tạo trò chơi
        self.INF = 70 # tổng sô điểm tối đa của trò chơi
        self.SLQUAN = SLQuan # số quân được lấy từ CauHinh = 5
        self.player_id = player_id # ID của người chơi thường là Player 0 và Player 1
        self.algo = algo # Thuật toán được thi triển trong trò chơi nếu None là người chơi
        self.screen = screen # Khởi tạo cửa sổ window
        self.table = table # hiển thị bảng chi tiết trò chơi dưới dạng terminal

    def Condition_Ending(self, state_, cur_point_): # Điều kiện để đưa ra kết luận rằng người chơi đã thắng hòa hay thua
        state, player_point = deepcopy(state_), deepcopy(cur_point_)

        if finished(state):
            player_point[0] += sum([i[0] for i in state[1:6]])
            player_point[1] += sum([i[0] for i in state[7:12]])

            if player_point[0] > player_point[1]:
                return (True, -self.INF if self.player_id else self.INF)
            elif player_point[0] < player_point[1]:
                return (True ,self.INF if self.player_id else -self.INF)
            else:
                return(True,0)
        return (False, player_point[1] if self.player_id else player_point[0])

    def get_available_move(self, state , player_id): #Kiểm tra những bước đi có thể đi trên bàn cờ
        list_of_action = []

        inc = 6 if player_id else 0
        for i in range(1 + inc, 6 + inc):
            if state[i][0]:
                list_of_action.extend([(i,'l'), (i,'r')])

        shuffle(list_of_action)
        return list_of_action
    
    def evaluation(self, state , cur_point , is_end): # Kiểm tra điều kiện dừng việc di chuyển trong một lượt hay còn gọi là kết thúc lượt
        if is_end[0]:
            return is_end[1] + cur_point[1] - cur_point[0] if self.player_id else is_end[1] + cur_point[0] - cur_point[1]
        return cur_point[1] - cur_point[0] if self.player_id else cur_point[0] - cur_point[1]

    def generate_next_move(self , state__, move , cur_point_ , id): # Khởi tạo bước đi trong bàn cờ
        state , cur_point = deepcopy(state__), deepcopy(cur_point_)
        inc = 1 if move[1] == 'r' else -1
        cur_pos = move[0]
        next_pos = (cur_pos + inc) % 12

        for _ in range(state[cur_pos][0]):
            state[next_pos][0] += 1
            next_pos = (next_pos + inc) % 12
        state[cur_pos][0] //= 12

        while True:
            if state[next_pos][1] or (state[next_pos][0] == 0 and state[(next_pos + inc) % 12][0] == 0 and
                                    state[(next_pos + inc) % 12][1] != 1):
                                    return state , cur_point
            elif state[next_pos][0] == 0 and (
                state[(next_pos + inc) % 12][0] or state[(next_pos + inc) % 12][1] ==1
            ):
                cur_point[id], state[(next_pos + inc) % 12][0] = cur_point[id] + state[(next_pos + inc) % 12][0], 0
                if state[(next_pos + inc) % 12][1] == 1:
                    cur_point[id] += self.SLQUAN
                    state[(next_pos + inc) % 12][1] = 2

                if state[(next_pos + inc*2) % 12][0] == 0 and state[(next_pos + inc * 2) % 12][1] != 1:
                    next_pos = (next_pos + inc * 2) % 12

            else:
                cur_pos = next_pos
                for _ in range(state[cur_pos][0]):
                    state[next_pos][0] += 1 
                    next_pos = (next_pos + inc) % 12
                state[cur_pos][0] //= 12

    def alpha_beta(self , state_game , cur_point , depth = 3): # Alpha_Beta Algorithms
        #Depth Limit search
        alpha, beta = -self.INF, self.INF

        def max_value(curstate, cur_point, curDepth , alpha , beta):
            is_end = self.Condition_Ending(curstate, cur_point)
            if is_end[0] or curDepth == 0 :
                return self.evaluation(curstate, cur_point, is_end)
            v = -self.INF

            curstate ,cur_point = fill_if_empty(curstate, cur_point)

            for move in self.get_available_move(curstate, self.player_id):
                next_state, next_point = self.generate_next_move(curstate, move , cur_point ,self.player_id)
                v = max(v, min_value(next_state, next_point, curDepth, alpha , beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v



        def min_value(curState, cur_point, curDepth, alpha, beta):
            is_end = self.Condition_Ending(curState, cur_point)
            if is_end[0] or curDepth == 0 :
                return self.evaluation(curState, cur_point , is_end)

            v = self.INF

            curState , cur_point = fill_if_empty(curState , cur_point)
            for move in self.get_available_move(curState, self.player_id ^ 1):
                next_state , next_point = self.generate_next_move(curState, move ,cur_point, self.player_id ^ 1)
                v = min(v , max_value(next_state, next_point, curDepth - 1 , alpha , beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        opt_action , score = None , -self.INF - 20
        curstate , cur_point = fill_if_empty(state_game, cur_point)
        for move in self.get_available_move(state_game, self.player_id):
            next_state, next_point = self.generate_next_move(curstate, move,cur_point,self.player_id)
            cur_score = min_value(next_state, next_point, depth , alpha , beta)

            if cur_score > score:
                score = cur_score
                opt_action = move
            alpha = max(alpha,score)
        return self.get_available_move(state_game , self.player_id)[0] if opt_action == None else opt_action

    def expectimax(self ,state_game, cur_point, depth=  3): # Expectimax Algorithm
        
        def generate_agent(state_game , cur_point, depth, idx_agent = 0):
            is_end = self.Condition_Ending(state_game, cur_point)
            if is_end[0] or depth == 0:
                return "", self.evaluation(state_game,cur_point ,is_end)
            else:
                maxAlpha = -self.INF-20 if idx_agent == 0 else 0
                curstate, cur_point = fill_if_empty(state_game, cur_point)
                list_valid_mode = self.get_available_move(curstate, self.player_id ^ idx_agent)
                if idx_agent:
                    depth -= 1
                best_move, next_agent = "" , idx_agent ^ 1
                for move in list_valid_mode:
                    next_state, next_point = self.generate_next_move(curstate, move , cur_point, self.player_id ^ idx_agent)
                    result = generate_agent(next_state, next_point, depth , next_agent)
                    if idx_agent == 0:
                        if result[1] > maxAlpha:
                            maxAlpha = result[1]
                            best_move = move
                    else:
                        maxAlpha += 1 / len(list_valid_mode) * result[1]
                        best_move = move
                best_move = list_valid_mode[0] if best_move == "" else best_move
                return (best_move , maxAlpha)

        return generate_agent(state_game , cur_point , depth)[0]
    
    def random_algo(self , state_game): # sẽ chạy ngẫu nhiên trong 2 thuật toán Alphal beta và Expectimax để đấu với người chơi
        pos = 0
        if self.player_id:
            while True:
                pos = randint(7, 11)
                if state_game[pos][0] != 0:
                    break
        else:
            while True:
                pos = randint(1 , 5)
                if state_game[pos][0] != 0:
                    break
        return pos, choice(['l', 'r'])

    def human_2(self , state_game , cur_point): # Người chơi 2 theo hình thức đối kháng (Chưa hoàn thiện)
        move = [None , None]
        old_box = 0
        self.table.redraw(0)
        x, y = 0 , 0
        isClick = False

        availabel_box = []
        for i in range(1 , 6):
            if state_game[i][0] > 0:
                availabel_box.append(i)
        while True:
            isClick = False
            time.sleep(0.2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    x = mouse[0]
                    y = mouse[1]
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        isClick = True

    def human(self, state_game , cur_point): # Người chơi 1 theo hình thức đối kháng sẽ là lựa chọn mặc đinh nếu algo bên trên là None
        move = [None ,  None]
        old_box = 0
        self.table.redraw(0)
        x , y = 0 , 0
        isClick = False

        availabel_box = []
        for i in range(1 , 6):
            if state_game[i][0] > 0:
                availabel_box.append(i)

        while True:
            isClick = False
            time.sleep(0.2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    x = mouse[0]
                    y = mouse[1]

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        isClick = True
            if 240 < y < 340:
                if 160 < x < 260:
                    move[0] = 1 
                    if move[0] not in availabel_box:
                        continue

                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(LNavigation, (165 , 315))
                        self.screen.blit(RNavigation, (233, 315))
                        old_box = move[0]

                    if isClick:
                        move[1] = 'l' if x < 210 else 'r'

                elif 260 < x < 360:
                    move[0] = 2
                    if move[0] not in availabel_box:
                        continue
                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(LNavigation , (265,315))
                        self.screen.blit(RNavigation , (333, 315))
                        old_box = move[0]

                    if isClick:
                        move[1] = 'l' if x < 310 else 'r'
                elif 360 < x < 460:
                    move[0] = 3
                    if move[0] not in availabel_box:
                        continue

                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(LNavigation , (360 , 315))
                        self.screen.blit(RNavigation , (428 , 315))
                        old_box = move[0]

                    if isClick:
                        move[1] = 'l' if x < 410 else 'r'
                elif 460 < x < 560:
                    move[0] = 4
                    if move[0] not in availabel_box:
                        continue
                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(LNavigation , (460 , 315))
                        self.screen.blit(RNavigation , (528 , 315))
                        old_box = move[0]

                    if isClick:
                        move[1] = 'l' if x < 510 else 'r'
                elif 560 < x < 660:
                    move[0] = 5
                    if move[0] not in availabel_box:
                        continue

                    if move[0] != old_box:
                        self.table.redraw(0)
                        self.screen.blit(LNavigation , (560 , 315))
                        self.screen.blit(RNavigation , (628 , 315))
                        old_box = move[0]

                    if isClick:
                        move[1] = 'l' if x < 610 else 'r'
                else:
                    self.table.redraw(0)
                    old_box = 0
            else:
                self.table.redraw(0)
                old_box = 0

            pygame.display.flip()
            if move[0] is not None and move[1] is not None:
                break
        return move[0], move[1]

    def execute(self, state_game_, cur_point_, depth = 3): # Thực thi và xử lý input của người nhập từ đó thể hiện kết quả của người chơi
        state_game , cur_point = deepcopy(state_game_), deepcopy(cur_point_)
        
        if self.algo is None:
            return self.human(state_game , cur_point)
        elif self.algo == "random":
            return self.random_algo(state_game)

        elif self.algo == "human":
            return self.human(state_game , cur_point)

        elif self.algo == "alpha_beta":
            depth= 5 if len(self.get_available_move(state_game, self.player_id)) < 5 else depth
            return self.alpha_beta(state_game , cur_point , depth)

        elif self.algo == "expectimax":
            return self.expectimax(state_game ,cur_point ,depth=2)