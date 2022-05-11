# Module này chịu trách nhiệm cho việc cấu hình nên các giao diện của trò chơi cũng như số lượng quân và số điểm
# ngoài ra Module này còn chịu trách nhiệm cho việc cấu hình màu sắc và font của của trò chơi


SLQuan = 10
TienPhong = True
RES = 'res/' # đường dẫn background cho chương trình

SCR_WIDTH = 800 # Biểu thị chìêu rộng của cửa sổ game
SCR_HEIGHT = 480 # Biểu thị chiều cao của cửa sổ game
SCR_NAME = 'Report For Game Theory' # Tên của của sổ

def PrintError():
    print("This Font Doesn't exist in this system\nPlease ensure that you are right when type it")
    

class color(): #Định dạng màu Sắc 
    white = (255,255,255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    gray = (128, 128, 128)
    yellow = (255, 255, 0)
    green = (126, 202, 24)
    blue = (0, 0, 255)
    palegreen = (130, 224, 170)
    orange = (211, 84, 0)
    purple = (91, 44, 111)
    darkred = (202, 24, 24)
