import copy
import sys
import pygame
import random

# khởi tạo
pygame.init()

# khai báo
scrWidth = 1000
scrHeight = 600
insWidth = 400
insHeight = 300
cellSize = 40

state = "mainMenu"
backToMainMenu = backToSelectMenu = False   # menu1
hoverStart = False
hoverIns = False
showIns = False

showPvPMode = False         # menu2
hoverPVP = False
hoverPVE = False
hoverEasy = False
hoverNormal = False
hoverHard = False

modeGame = 1        # menu3
playerPrepare = 1
nextPlayer = False
prevPlayer = True
hoverNext = False
hoverStartGame = False
checkPick = False
wantToAdd = False
putShip = False
alert1 = False
curClickPrep = ()
pick_P1_6_1 = pick_P1_6_2 = pick_P1_6_3 = pick_P1_6_4 = False
pick_P1_5_1 = pick_P1_5_2 = pick_P1_5_3 = False
pick_P1_4_1 = pick_P1_4_2 = pick_P1_4_3 = False
pick_P1_3_1 = pick_P1_3_2 = False
pick_P1_2_1 = pick_P1_2_2 = False
selectedCells = [[0] * 10 for _ in range(10)]   # khởi tạo mảng 10x10 = False
shipPrep = []
shipPrep1 = []
shipPrep2 = []
shipBotPrep = []

turn = 'player'
pts_pl = pts_bot = 0
show_pl = show_bot = False
winner = ''

showEnd = False


# các hàm
def draw_mini_sqr(left = 0, top = 0, size = 0, count = 0):
    for i in range(0, count):
        pygame.draw.rect(screen, (90, 180, 45), (left + i*size + 4*i, top, size, size), 0)

def draw_ship(L = 0, W = 0, O = "", X = 0, Y = 0):
    if O == 'v':
        rectangle = pygame.Rect(80 + X*cellSize + cellSize/4, 120 + Y*cellSize + cellSize/4, (L/W)*cellSize - cellSize/2, W*cellSize - cellSize/2)
        pygame.draw.rect(screen, (255, 137, 0), rectangle, border_radius = 10)
    elif O == 'h':    
        rectangle = pygame.Rect(80 + X*cellSize + cellSize/4, 120 + Y*cellSize + cellSize/4, W*cellSize - cellSize/2, (L/W)*cellSize - cellSize/2)
        pygame.draw.rect(screen, (255, 137, 0), rectangle, border_radius = 10)
    else:
        if L == 5:
            rectangle = pygame.Rect(80 + X*cellSize + cellSize/4, 120 + Y*cellSize + cellSize/4, 3*cellSize - cellSize/2, cellSize - cellSize/2)
            pygame.draw.rect(screen, (255, 137, 0), rectangle, border_radius = 10)
            rectangle = pygame.Rect(80 + (X+1)*cellSize + cellSize/4, 120 + (Y-1)*cellSize + cellSize/4, cellSize - cellSize/2, 3*cellSize - cellSize/2)
            pygame.draw.rect(screen, (255, 137, 0), rectangle, border_radius = 10)
        else:
            rectangle = pygame.Rect(80 + X*cellSize + cellSize/4, 120 + Y*cellSize + cellSize/4, W*cellSize - cellSize/2, (L/W)*cellSize - cellSize/2)
            pygame.draw.rect(screen, (255, 137, 0), rectangle, border_radius = 10)    
                       
def addShip(L = 0, W = 0, O = "", X = 0, Y = 0):
    shipPrep.append(
        {
            'box' : L,
            'width' : W,
            'orient' : O,
            'x' : X,
            'y' : Y 
        }
    )
    if O == 'v':
        if W == 2:
            for iTick in range(X, X+3):
                selectedCells[iTick][Y] = 1
                selectedCells[iTick][Y+1] = 1
        else:
            for iTick in range(X, X+L):  
                selectedCells[iTick][Y] = 1    
    elif O == 'h':
        if W == 2:
            for iTick in range(Y, Y+3):
                selectedCells[X][iTick] = 1
                selectedCells[X+1][iTick] = 1
        else:
            for iTick in range(Y, Y+L):
                selectedCells[X][iTick] = 1  
    elif O == 'r':
        if L == 5:
            selectedCells[X][Y] = 1
            selectedCells[X+1][Y] = 1
            selectedCells[X+2][Y] = 1
            selectedCells[X+1][Y-1] = 1
            selectedCells[X+1][Y+1] = 1
        else:
            for iTick in range(X, X+2):
                selectedCells[iTick][Y] = 1
                selectedCells[iTick][Y+1] = 1
                          
def delShip(L = 0):
    iDel = 0
    while iDel < len(shipPrep):
        if shipPrep[iDel]['box'] == L:  
            W = shipPrep[iDel]['width']
            O = shipPrep[iDel]['orient']
            X = shipPrep[iDel]['x']
            Y = shipPrep[iDel]['y']
            if O == 'v':
                if W == 2:
                    for iTick in range(X, X+3):
                        selectedCells[iTick][Y] = 0
                        selectedCells[iTick][Y+1] = 0
                else:
                    for iTick in range(X, X+L):  
                        selectedCells[iTick][Y] = 0    
            elif O == 'h':
                if W == 2:
                    for iTick in range(Y, Y+3):
                        selectedCells[X][iTick] = 0
                        selectedCells[X+1][iTick] = 0
                else:
                    for iTick in range(Y, Y+L):
                        selectedCells[X][iTick] = 0  
            elif O == 'r':
                if L == 5:
                    selectedCells[X][Y] = 0
                    selectedCells[X+1][Y] = 0
                    selectedCells[X+2][Y] = 0
                    selectedCells[X+1][Y-1] = 0
                    selectedCells[X+1][Y+1] = 0
                else:
                    for iTick in range(X, X+2):
                        selectedCells[iTick][Y] = 0
                        selectedCells[iTick][Y+1] = 0                    
            del shipPrep[iDel]
        else:
            iDel += 1   
            
def checkShipPrep(L = 0, W = 0, O = "", X = 0, Y = 0):
    if O == 'v':
        if W == 2:  # L = 6 va W = 2
            if Y > 8:
                return False
            for iCheck in range(X, X+3):
                if iCheck > 9:
                    return False
                if selectedCells[iCheck][Y] == 1:
                    return False
                if selectedCells[iCheck][Y+1] == 1:
                    return False
            return True    
        else:    
            for iCheck in range(X, X+L):
                if iCheck > 9:
                    return False
                if selectedCells[iCheck][Y] == 1:
                    return False    
            return True    
    elif O == 'h':
        if W == 2 :
            if X > 8:
                return False
            for iCheck in range(Y, Y+3):
                if iCheck > 9:
                    return False
                if selectedCells[X][iCheck] == 1:
                    return False
                if selectedCells[X+1][iCheck] == 1:
                    return False
            return True 
        else:    
            for iCheck in range(Y, Y+L):
                if iCheck > 9:
                    return False 
                if selectedCells[X][iCheck] == 1:
                    return False
            return True        
    elif O == 'r':
        if L == 5:
            if X > 7 or Y > 8 or Y < 1:
                return False
            if selectedCells[X][Y] == 1 or selectedCells[X+1][Y] == 1 or selectedCells[X+2][Y] == 1 or selectedCells[X+1][Y-1] == 1 or selectedCells[X+1][Y+1] == 1:
                return False
            return True
        else:
            if X > 8 or Y > 8:
                return False
            for iCheck in range(X, X+2):
                if iCheck > 9:
                    return False
                if selectedCells[iCheck][Y] == 1:
                    return False
                if selectedCells[iCheck][Y+1] == 1:
                    return False
            return True     

def createShipBot():
    i = 2  
    while i < 7:
        if i == 6:
            W = random.choice([1, 2]) 
            O = random.choice(['v', 'h'])
        elif i == 5:
            W = random.choice([1, 3]) 
            if W == 1:
                O = random.choice(['v', 'h'])
            else:
                O = 'r'    
        elif i == 4:
            W = random.choice([1, 2])     
            if W == 1:
                O = random.choice(['v', 'h'])
            else:
                O = 'r'      
        else:
            W = 1
            O = random.choice(['v', 'h'])
        
        X = random.randint(0, 9)
        Y = random.randint(0, 9)              
        
        if checkShipPrep(i, W, O, X, Y):
            addShip(i, W, O, X, Y)
            shipPrep.append({
                'box' : i,
                'width' : W,
                'orient' : O,    
                'x' : X,
                'y' : Y            
            })  
            i = i + 1  
        else:
            continue    
  
def draw_Box(xC = 0, yC = 0):
    rectangle = pygame.Rect(80 + xC*cellSize + cellSize/4, 120 + yC*cellSize + cellSize/4, cellSize - cellSize/2, cellSize - cellSize/2)
    pygame.draw.rect(screen, (255, 137, 0), rectangle, border_radius = 20)                

def draw_Sea(xC = 0, yC = 0):
    rectangle = pygame.Rect(80 + xC*cellSize+1, 120 + yC*cellSize+1, cellSize-2, cellSize-2)
    pygame.draw.rect(screen, (114, 241, 250), rectangle)
    
def clr_Box():
    for idg in range(100):
        x = idg % 10 * cellSize + 80
        y = idg // 10 * cellSize + 120
        pygame.draw.rect(screen, (255, 255, 255), (x+1, y+1, cellSize-2, cellSize-2), 0)

def draw_pl():
    for iCheck in range(len(sl_2)):
        for jCheck in range(len(sl_2[iCheck])):
            if sl_2[iCheck][jCheck] == 2:
                draw_Sea(iCheck, jCheck) 
            elif sl_2[iCheck][jCheck] == 3:
                draw_Box(iCheck, jCheck)
            
                
def draw_bot():
    for iCheck in range(len(sl_1)):
        for jCheck in range(len(sl_1[iCheck])):
            if sl_1[iCheck][jCheck] == 3:
                draw_Box(iCheck, jCheck)
            elif sl_1[iCheck][jCheck] == 2:
                draw_Sea(iCheck, jCheck)                 
                        

# hiển thị menu
screen = pygame.display.set_mode((scrWidth, scrHeight))
pygame.display.set_caption("BATTLESHIP - TEAM 5")

# chỉnh font
titleFont = pygame.font.SysFont("Helvetica", 103)
selectFont = pygame.font.SysFont("Helvetica", 30)
pageInsFont = pygame.font.SysFont("Helvetica", 48)
insFont = pygame.font.SysFont("Helvetica", 20)
modeFont = pygame.font.SysFont("Helvetica", 56)
modeDFont = pygame.font.SysFont("Helvetica", 16)
miniFont = pygame.font.SysFont("Helvetica", 12)
testFont = pygame.font.SysFont("Helvetica", 15)

title = titleFont.render("BATTLESHIP", 1, (115, 205, 134), (255,255,255))
start = selectFont.render("START", 1, (128, 235, 134), (255, 255, 255))
nonStart = selectFont.render("START", 1, (255, 255, 255), (128, 235, 134))
ins = selectFont.render("INSTRUCTION", 1, (128, 235, 134), (255, 255, 255))
nonIns = selectFont.render("INSTRUCTION", 1, (255, 255, 255), (128, 235, 134))
pageIns = pageInsFont.render("INSTRUCTION", 1, (48, 165, 105), (225, 248, 234))
click = insFont.render("Click anywhere to continue >>", 1, (5, 88, 53), (225, 248, 234))
insText = [
    "Mỗi người chơi sẽ có một bảng lưới các ô vuông được đánh toạ độ.",
    "Người chơi sau đó sẽ bố trí vị trí các tàu của mình theo chiều ngang hoặc chiều dọc trên bảng lưới đã cho,",
    "đối thủ sẽ không được biết vị trí của các con tàu đã được xếp.",
    "Các tàu trong hạm đội sẽ không thể xếp chồng lên nhau.",
    "Sau khi chuẩn bị xong, trò chơi sẽ bắt đầu.",
    "Nếu bắn trúng, người chơi sẽ được thông báo là đã bắn trúng tàu của địch và sẽ được bắn tiếp.",
    "Nếu trượt, lượt sẽ được chuyển cho người còn lại và cứ thế tiếp tục đến khi hạm đội của 1 trong 2 người ",
    "bị đánh chìm hoàn toàn."
]

modeText = modeFont.render("SELECT MODE", 1, (48, 165, 105), (255, 255, 255))
pvpMode = selectFont.render("PVP", 1, (128, 235, 134), (255, 255, 255))
pveMode = selectFont.render("PVE", 1, (128, 235, 134), (255, 255, 255))
easyMode = selectFont.render("Easy", 1, (217, 236, 28), (255, 255, 255))
normalMode = selectFont.render("Normal", 1, (255, 188, 1), (255, 255, 255))
hardMode = selectFont.render("Hard", 1, (248, 45, 11), (255, 255, 255))
nonPvPMode = selectFont.render("PVP", 1, (255, 255, 255), (128, 235, 134))
nonPvEMode = selectFont.render("PVE", 1, (255, 255, 255), (128, 235, 134))
nonEasyMode = selectFont.render("Easy", 1, (255, 255, 255), (217, 236, 28))
nonNormalMode = selectFont.render("Normal", 1, (255, 255, 255), (255, 188, 1))
nonHardMode = selectFont.render("Hard", 1, (255, 255, 255), (248, 45, 11))

preparingText = modeFont.render("PREPARING", 1, (48, 165, 105), (255, 255, 255))
playerText = selectFont.render("PLAYER", 1, (48, 165, 105), (255, 255, 255))
yourText = selectFont.render("YOUR TEAM", 1, (48, 165, 105), (255, 255, 255))
oneText = selectFont.render("1", 1, (48, 165, 105), (255, 255, 255))
twoText = selectFont.render("2", 1, (48, 165, 105), (255, 255, 255))
nextText = insFont.render("Next", 1, (15, 85, 13), (255, 255, 255))
startText = insFont.render("Start", 1, (15, 85, 13), (255, 255, 255))
nonNextText = insFont.render("Next", 1, (255, 255, 255), (15, 85, 13))
nonStartText = insFont.render("Start", 1, (255, 255, 255), (15, 85, 13))
easyText = insFont.render("<Mode: Easy>", 1, (221, 226, 18), (255, 255, 255))
normalText = insFont.render("<Mode: Normal>", 1, (255, 188, 1), (255, 255, 255))
hardText = insFont.render("<Mode: Hard>", 1, (248, 45, 11), (255, 255, 255))
twoShipText = miniFont.render("2", 1, (0, 0, 0))
threeShipText = miniFont.render("3", 1, (0, 0, 0))
fourShipText = miniFont.render("4", 1, (0, 0, 0))
fiveShipText = miniFont.render("5", 1, (0, 0, 0))
sixShipText = miniFont.render("6", 1, (0, 0, 0))
vText = miniFont.render("v", 1, (0, 0, 0))
hText = miniFont.render("h", 1, (0, 0, 0))
rText = miniFont.render("r", 1, (0, 0, 0))
putText = modeDFont.render("[Mời đặt tàu chiến vào vị trí]", 1, (8, 114, 43))
alert1Text = modeDFont.render("(*)[Vị trí tàu không hợp lệ]", 1, (255, 94, 0))
alert2Text = modeDFont.render("(**)[Số lượng tàu chưa đủ (=5, bao gồm 2, 3, 4, 5, 6)]", 1, (255, 94, 0))

playingText = modeFont.render("BATTLING", 1, (48, 165, 105), (255, 255, 255))
botText = selectFont.render("BOT", 1, (48, 165, 105), (255, 255, 255))
yourTurnText = selectFont.render("YOUR TURN", 1, (48, 165, 105), (255, 255, 255))
botTurnText = selectFont.render("BOT'S TURN", 1, (48, 165, 105), (255, 255, 255))
pointText = insFont.render("Pts : ", 1, (48, 165, 105), (255, 255, 255))
remainingText = insFont.render("Remaining ship : ", 1, (48, 165, 105), (255, 255, 255))
twosText = selectFont.render("2", 1, (48, 165, 105), (255, 255, 255))
threesText = selectFont.render("3", 1, (48, 165, 105), (255, 255, 255))
foursText = selectFont.render("4", 1, (48, 165, 105), (255, 255, 255))
fivesText = selectFont.render("5", 1, (48, 165, 105), (255, 255, 255))
sixsText = selectFont.render("6", 1, (48, 165, 105), (255, 255, 255))
ptsText = ''

winnerTitleText = selectFont.render("WINNER:", 1, (48, 165, 105), (255, 255, 255))
winnerText = ''

# cập nhật ảnh
bgImage = pygame.image.load("bg_scr3.png") 
bgImage = pygame.transform.scale(bgImage, (240, 50))
i = 0

backImage = pygame.image.load("back_arrow.png")
backImage = pygame.transform.scale(backImage, (50, 40))

winnerImage = pygame.image.load("winner.jpg")
winnerImage = pygame.transform.scale(winnerImage, (200, 200))

# run
while 1:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()    
            
            if state == "mainMenu":
                if showIns:
                    showIns = False
                elif hoverIns:
                    showIns = True
                elif hoverStart:
                    state = "menuSelect"
                    backToMainMenu = False
            
            if state == "menuSelect":
                if backToMainMenu:
                    state = "mainMenu"
                if hoverPVP:
                    state = "pvpSelect"  
                    backToSelectMenu = False  
                elif hoverEasy or hoverNormal or hoverHard:
                    backToSelectMenu = False
                    state = "pveSelect" 
                    if hoverEasy:
                        modeGame = 1
                    elif hoverNormal:
                        modeGame = 2
                    else:
                        modeGame = 3  
            
            if state == "pvpSelect":
                testText = testFont.render(f"toa do : {mouse[0]},{mouse[1]}", True, (0,0,0))
                DText = testFont.render(str(len(shipPrep1)), True, (0,0,0))
                checkText = testFont.render("0", True, (0,0,0))
                curClickText = testFont.render(str(curClickPrep), True, (0,0,0))
                if 80 <= mouse[0] <= 480 and 120 <= mouse[1] <= 520:
                    testXYText = testFont.render(f"toa do (x, y): {int((mouse[0]-80)/40)},{int((mouse[1]-120)/40)}", True, (0,0,0))
                    if wantToAdd == True:
                        if checkShipPrep(curClickPrep[0], curClickPrep[1], curClickPrep[2], int((mouse[0]-80)/40), int((mouse[1]-120)/40)):
                            addShip(curClickPrep[0], curClickPrep[1], curClickPrep[2], int((mouse[0]-80)/40), int((mouse[1]-120)/40))  
                            wantToAdd = False  
                            putShip = False
                            alert1 = False
                        else:
                            alert1 = True    
                else:
                    testXYText = testFont.render(f"toa do (x, y): #,#", True, (0,0,0))    
                if backToSelectMenu:
                    state = "menuSelect" 
                    shipPrep = [] 
                if nextPlayer:
                    playerPrepare = 2 
                if prevPlayer:
                    playerPrepare = 1   
                    backToSelectMenu = False  
                if playerPrepare == 1:                         
                    
                    if 526 <= mouse[0] <= 737 and 200 <= mouse[1] <= 263 and checkPick == True and putShip == False: # check 6     
                        if pick_P1_6_1 == False:
                            pick_P1_6_1 = True
                            pick_P1_6_2 = pick_P1_6_3 = pick_P1_6_4 = False 
                            wantToAdd = True   
                            putShip = True 
                            delShip(6)
                            curClickPrep = (6,1,'v')    
                        else:
                            pick_P1_6_1 = False
                            wantToAdd = False
                            putShip = False
                            delShip(6)
                            curClickPrep = ()
                    elif 738 <= mouse[0] <= 950 and 200 <= mouse[1] <= 263 and checkPick == True and putShip == False:
                        if pick_P1_6_2 == False:
                            pick_P1_6_2 = True
                            pick_P1_6_1 = pick_P1_6_3 = pick_P1_6_4 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(6)
                            curClickPrep = (6,1,'h')
                        else:
                            pick_P1_6_2 = False
                            wantToAdd = False  
                            putShip = False
                            delShip(6)
                            curClickPrep = () 
                    elif 526 <= mouse[0] <= 737 and 264 <= mouse[1] <= 328 and checkPick == True and putShip == False:
                        if pick_P1_6_3 == False:
                            pick_P1_6_3 = True
                            pick_P1_6_1 = pick_P1_6_2 = pick_P1_6_4 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(6)
                            curClickPrep = (6,2,'v')
                        else:
                            pick_P1_6_3 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(6)
                            curClickPrep = ()
                    elif 738 <= mouse[0] <= 950 and 264 <= mouse[1] <= 328 and checkPick == True and putShip == False:
                        if pick_P1_6_4 == False:
                            pick_P1_6_4 = True
                            pick_P1_6_1 = pick_P1_6_2 = pick_P1_6_3 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(6)
                            curClickPrep = (6,2,'h')
                        else:
                            pick_P1_6_4 = False    
                            wantToAdd = False  
                            putShip = False
                            delShip(6)
                            curClickPrep = ()       
                    
                    if 526 <= mouse[0] <= 666 and 329 <= mouse[1] <= 392 and checkPick == True and putShip == False: # check 5
                        if pick_P1_5_1 == False:
                            pick_P1_5_1 = True
                            pick_P1_5_2 = pick_P1_5_3 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(5)
                            curClickPrep = (5,1,'v')     
                        else:
                            pick_P1_5_1 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(5)
                            curClickPrep = ()
                    elif 667 <= mouse[0] <= 808 and 329 <= mouse[1] <= 392 and checkPick == True and putShip == False: 
                        if pick_P1_5_2 == False:
                            pick_P1_5_2 = True
                            pick_P1_5_1 = pick_P1_5_3 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(5)
                            curClickPrep = (5,1,'h') 
                        else:
                            pick_P1_5_2 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(5)
                            curClickPrep = () 
                    elif 809 <= mouse[0] <= 950 and 329 <= mouse[1] <= 392 and checkPick == True and putShip == False:
                        if pick_P1_5_3 == False:
                            pick_P1_5_3 = True
                            pick_P1_5_1 = pick_P1_5_2 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(5)
                            curClickPrep = (5,3,'r') 
                        else:
                            pick_P1_5_3 = False    
                            wantToAdd = False 
                            putShip = False
                            delShip(5)
                            curClickPrep = ()             
                        
                    if 526 <= mouse[0] <= 666 and 393 <= mouse[1] <= 456 and checkPick == True and putShip == False: # check 4
                        if pick_P1_4_1 == False:
                            pick_P1_4_1 = True
                            pick_P1_4_2 = pick_P1_4_3 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(4)
                            curClickPrep = (4,1,'v') 
                        else:
                            pick_P1_4_1 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(4)
                            curClickPrep = () 
                    elif 667 <= mouse[0] <= 808 and 393 <= mouse[1] <= 456 and checkPick == True and putShip == False: 
                        if pick_P1_4_2 == False:
                            pick_P1_4_2 = True
                            pick_P1_4_1 = pick_P1_4_3 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(4)
                            curClickPrep = (4,1,'h') 
                        else:
                            pick_P1_4_2 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(4)
                            curClickPrep = ()
                    elif 809 <= mouse[0] <= 950 and 393 <= mouse[1] <= 456 and checkPick == True and putShip == False:
                        if pick_P1_4_3 == False:
                            pick_P1_4_3 = True
                            pick_P1_4_1 = pick_P1_4_2 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(4)
                            curClickPrep = (4,2,'r') 
                        else:
                            pick_P1_4_3 = False   
                            wantToAdd = False
                            putShip = False
                            delShip(4)
                            curClickPrep = () 
                     
                    if 526 <= mouse[0] <= 630 and 457 <= mouse[1] <= 520 and checkPick == True and putShip == False: # check 3
                        if pick_P1_3_1 == False:
                            pick_P1_3_1 = True
                            pick_P1_3_2 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(3)
                            curClickPrep = (3,1,'v') 
                        else:
                            pick_P1_3_1 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(3)
                            curClickPrep = () 
                    elif 631 <= mouse[0] <= 736 and 457 <= mouse[1] <= 520 and checkPick == True and putShip == False: 
                        if pick_P1_3_2 == False:
                            pick_P1_3_2 = True
                            pick_P1_3_1 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(3)
                            curClickPrep = (3,1,'h') 
                        else:
                            pick_P1_3_2 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(3)
                            curClickPrep = () 
                    
                    if 737 <= mouse[0] <= 841 and 457 <= mouse[1] <= 520 and checkPick == True and putShip == False: # check 2
                        if pick_P1_2_1 == False:
                            pick_P1_2_1 = True
                            pick_P1_2_2 = False 
                            wantToAdd = True
                            putShip = True
                            delShip(2)
                            curClickPrep = (2,1,'v') 
                        else:
                            pick_P1_2_1 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(2)
                            curClickPrep = () 
                    elif 842 <= mouse[0] <= 945 and 457 <= mouse[1] <= 520 and checkPick == True and putShip == False: 
                        if pick_P1_2_2 == False:
                            pick_P1_2_2 = True
                            pick_P1_2_1 = False
                            wantToAdd = True 
                            putShip = True
                            delShip(2)
                            curClickPrep = (2,1,'h') 
                        else:
                            pick_P1_2_2 = False 
                            wantToAdd = False
                            putShip = False
                            delShip(2)
                            curClickPrep = () 
                
                
                    # if 850 <= mouseClk[0] < 950 and 535 <= mouseClk[1] < 575:
                    #     if len(shipPrep1) == 5:
                    #         checkPick = False     
                    #         checkText = testFont.render("1", True, (0,0,0))   
                    #         curClickPrep = ()
                    #         pick_P1_6_1 = pick_P1_6_2 = pick_P1_6_3 = pick_P1_6_4 = False
                    #         pick_P1_5_1 = pick_P1_5_2 = pick_P1_5_3 = False
                    #         pick_P1_4_1 = pick_P1_4_2 = pick_P1_4_3 = False
                    #         pick_P1_3_1 = pick_P1_3_2 = False
                    #         pick_P1_2_1 = pick_P1_2_2 = False
                    #         selectedCells = [[False] * 10 for _ in range(10)]                           
                        
                
                # if playerPrepare == 2:
                #     shipPrep = [] 
                               
            if state == "pveSelect":
                if backToSelectMenu:
                    state = "menuSelect" 
                testText = testFont.render(f"toa do : {mouse[0]},{mouse[1]}", True, (0,0,0))
                DText = testFont.render(str(len(shipPrep)), True, (0,0,0))
                checkText = testFont.render("0", True, (0,0,0))
                curClickText = testFont.render(str(curClickPrep), True, (0,0,0))
                if 80 <= mouse[0] <= 480 and 120 <= mouse[1] <= 520:
                    testXYText = testFont.render(f"toa do (x, y): {int((mouse[0]-80)/40)},{int((mouse[1]-120)/40)}", True, (0,0,0))
                    if wantToAdd == True:
                        if checkShipPrep(curClickPrep[0], curClickPrep[1], curClickPrep[2], int((mouse[0]-80)/40), int((mouse[1]-120)/40)):
                            addShip(curClickPrep[0], curClickPrep[1], curClickPrep[2], int((mouse[0]-80)/40), int((mouse[1]-120)/40))  
                            wantToAdd = False  
                            putShip = False
                            alert1 = False
                        else:
                            alert1 = True    
                else:
                    testXYText = testFont.render(f"toa do (x, y): #,#", True, (0,0,0))        
                if 526 <= mouse[0] <= 737 and 200 <= mouse[1] <= 263 and checkPick == True and putShip == False: # check 6     
                    if pick_P1_6_1 == False:
                        pick_P1_6_1 = True
                        pick_P1_6_2 = pick_P1_6_3 = pick_P1_6_4 = False 
                        wantToAdd = True   
                        putShip = True 
                        delShip(6)
                        curClickPrep = (6,1,'v')    
                    else:
                        pick_P1_6_1 = False
                        wantToAdd = False
                        putShip = False
                        delShip(6)
                        curClickPrep = ()
                elif 738 <= mouse[0] <= 950 and 200 <= mouse[1] <= 263 and checkPick == True and putShip == False:
                    if pick_P1_6_2 == False:
                        pick_P1_6_2 = True
                        pick_P1_6_1 = pick_P1_6_3 = pick_P1_6_4 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(6)
                        curClickPrep = (6,1,'h')
                    else:
                        pick_P1_6_2 = False
                        wantToAdd = False  
                        putShip = False
                        delShip(6)
                        curClickPrep = () 
                elif 526 <= mouse[0] <= 737 and 264 <= mouse[1] <= 328 and checkPick == True and putShip == False:
                    if pick_P1_6_3 == False:
                        pick_P1_6_3 = True
                        pick_P1_6_1 = pick_P1_6_2 = pick_P1_6_4 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(6)
                        curClickPrep = (6,2,'v')
                    else:
                        pick_P1_6_3 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(6)
                        curClickPrep = ()
                elif 738 <= mouse[0] <= 950 and 264 <= mouse[1] <= 328 and checkPick == True and putShip == False:
                    if pick_P1_6_4 == False:
                        pick_P1_6_4 = True
                        pick_P1_6_1 = pick_P1_6_2 = pick_P1_6_3 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(6)
                        curClickPrep = (6,2,'h')
                    else:
                        pick_P1_6_4 = False    
                        wantToAdd = False  
                        putShip = False
                        delShip(6)
                        curClickPrep = ()       
                
                if 526 <= mouse[0] <= 666 and 329 <= mouse[1] <= 392 and checkPick == True and putShip == False: # check 5
                    if pick_P1_5_1 == False:
                        pick_P1_5_1 = True
                        pick_P1_5_2 = pick_P1_5_3 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(5)
                        curClickPrep = (5,1,'v')     
                    else:
                        pick_P1_5_1 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(5)
                        curClickPrep = ()
                elif 667 <= mouse[0] <= 808 and 329 <= mouse[1] <= 392 and checkPick == True and putShip == False: 
                    if pick_P1_5_2 == False:
                        pick_P1_5_2 = True
                        pick_P1_5_1 = pick_P1_5_3 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(5)
                        curClickPrep = (5,1,'h') 
                    else:
                        pick_P1_5_2 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(5)
                        curClickPrep = () 
                elif 809 <= mouse[0] <= 950 and 329 <= mouse[1] <= 392 and checkPick == True and putShip == False:
                    if pick_P1_5_3 == False:
                        pick_P1_5_3 = True
                        pick_P1_5_1 = pick_P1_5_2 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(5)
                        curClickPrep = (5,3,'r') 
                    else:
                        pick_P1_5_3 = False    
                        wantToAdd = False 
                        putShip = False
                        delShip(5)
                        curClickPrep = ()             
                    
                if 526 <= mouse[0] <= 666 and 393 <= mouse[1] <= 456 and checkPick == True and putShip == False: # check 4
                    if pick_P1_4_1 == False:
                        pick_P1_4_1 = True
                        pick_P1_4_2 = pick_P1_4_3 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(4)
                        curClickPrep = (4,1,'v') 
                    else:
                        pick_P1_4_1 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(4)
                        curClickPrep = () 
                elif 667 <= mouse[0] <= 808 and 393 <= mouse[1] <= 456 and checkPick == True and putShip == False: 
                    if pick_P1_4_2 == False:
                        pick_P1_4_2 = True
                        pick_P1_4_1 = pick_P1_4_3 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(4)
                        curClickPrep = (4,1,'h') 
                    else:
                        pick_P1_4_2 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(4)
                        curClickPrep = ()
                elif 809 <= mouse[0] <= 950 and 393 <= mouse[1] <= 456 and checkPick == True and putShip == False:
                    if pick_P1_4_3 == False:
                        pick_P1_4_3 = True
                        pick_P1_4_1 = pick_P1_4_2 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(4)
                        curClickPrep = (4,2,'r') 
                    else:
                        pick_P1_4_3 = False   
                        wantToAdd = False
                        putShip = False
                        delShip(4)
                        curClickPrep = () 
                    
                if 526 <= mouse[0] <= 630 and 457 <= mouse[1] <= 520 and checkPick == True and putShip == False: # check 3
                    if pick_P1_3_1 == False:
                        pick_P1_3_1 = True
                        pick_P1_3_2 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(3)
                        curClickPrep = (3,1,'v') 
                    else:
                        pick_P1_3_1 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(3)
                        curClickPrep = () 
                elif 631 <= mouse[0] <= 736 and 457 <= mouse[1] <= 520 and checkPick == True and putShip == False: 
                    if pick_P1_3_2 == False:
                        pick_P1_3_2 = True
                        pick_P1_3_1 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(3)
                        curClickPrep = (3,1,'h') 
                    else:
                        pick_P1_3_2 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(3)
                        curClickPrep = () 
                
                if 737 <= mouse[0] <= 841 and 457 <= mouse[1] <= 520 and checkPick == True and putShip == False: # check 2
                    if pick_P1_2_1 == False:
                        pick_P1_2_1 = True
                        pick_P1_2_2 = False 
                        wantToAdd = True
                        putShip = True
                        delShip(2)
                        curClickPrep = (2,1,'v') 
                    else:
                        pick_P1_2_1 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(2)
                        curClickPrep = () 
                elif 842 <= mouse[0] <= 945 and 457 <= mouse[1] <= 520 and checkPick == True and putShip == False: 
                    if pick_P1_2_2 == False:
                        pick_P1_2_2 = True
                        pick_P1_2_1 = False
                        wantToAdd = True 
                        putShip = True
                        delShip(2)
                        curClickPrep = (2,1,'h') 
                    else:
                        pick_P1_2_2 = False 
                        wantToAdd = False
                        putShip = False
                        delShip(2)
                        curClickPrep = () 
                
                if 850 <= mouseClk[0] < 950 and 535 <= mouseClk[1] < 575:
                    if len(shipPrep1) == 5:           
                        state = "playing"  
            
            if state == 'playing':
                if pts_pl == 20 or pts_bot == 20:
                    if (pts_pl > pts_bot):
                        winner = 'PLAYER'
                    else:
                        winner = 'BOT'    
                    state = 'end'
                elif 80 <= mouse[0] <= 480 and 120 <= mouse[1] <= 520 and pts_pl < 20 and pts_bot < 20:
                    xC = int((mouse[0]-80)/40)
                    yC = int((mouse[1]-120)/40)
                      
                    if turn == 'player':
                        if 80 <= mouse[0] <= 480 and 120 <= mouse[1] <= 520:
                            if sl_2[xC][yC] == 0:
                                sl_2[xC][yC] = 2
                                pygame.time.delay(200)
                                show_pl = True
                                turn = 'bot'
                            elif sl_2[xC][yC] == 1:
                                sl_2[xC][yC] = 3   
                                pts_pl += 1 
                                show_pl = True
                    else:
                        if modeGame == 1:
                            while turn != 'player':
                                xC = random.randint(0, 9)
                                yC = random.randint(0, 9)
                                while sl_1[xC][yC] in [2, 3]:  
                                    xC = random.randint(0, 9)
                                    yC = random.randint(0, 9)  
                                if sl_1[xC][yC] == 0:
                                    sl_1[xC][yC] = 2
                                    turn = 'player'
                                elif sl_1[xC][yC] == 1:
                                    sl_1[xC][yC] = 3   
                                    pts_bot += 1 
                                    pygame.time.delay(200)   
                                    
            
                  
                                        
    if state == "mainMenu":
        if showIns == False:
            if (i > 990):
                i = -300
            i += 0.18
            screen.fill([255, 255, 255])
            screen.blit(title, (scrWidth/2 - title.get_width()/2, 80))
            screen.blit(bgImage, (10 + i, 220))

        mouse = pygame.mouse.get_pos()
        if 0 < mouse[0] < scrWidth and 330 < mouse[1] < 425:
            hoverStart = True
            hoverIns = False
        elif 0 < mouse[0] < scrWidth and 425 <= mouse[1] < 520:
            hoverStart = False
            hoverIns = True
        else:
            hoverStart = False
            hoverIns = False

        if hoverStart == True:
            pygame.draw.rect(screen, (128, 235, 134), (0, 330, scrWidth, start.get_height()+60))
            screen.blit(nonStart, (scrWidth/2 - start.get_width()/2, 360))
        if hoverStart == False:
            pygame.draw.rect(screen, (255, 255, 255), (0, 330, scrWidth, start.get_height()+60))
            screen.blit(start, (scrWidth/2 - start.get_width()/2, 360))
        if hoverIns == True:
            pygame.draw.rect(screen, (128, 235, 134), (0, 425, scrWidth, ins.get_height()+60))
            screen.blit(nonIns, (scrWidth/2 - ins.get_width()/2, 455))
        if hoverIns == False:
            pygame.draw.rect(screen, (255, 255, 255), (0, 425, scrWidth, ins.get_height()+60))
            screen.blit(ins, (scrWidth/2 - ins.get_width()/2, 455))
        if showIns ==  True:
            pygame.draw.rect(screen, (225, 248, 234), (0, 0, scrWidth, scrHeight))
            screen.blit(pageIns, (25, 40))
            screen.blit(click, (670, 525))
            space = 140
            for ln in insText:
                text = insFont.render(ln, True, (38, 155, 100))
                screen.blit(text, (25, space))
                space += 30

    if state == "menuSelect":
        screen.fill([255, 255, 255])
        screen.blit(backImage, (25, 25))
        screen.blit(modeText, ((scrWidth - modeText.get_width())/2, 25))
        screen.blit(pvpMode, ((scrWidth - pvpMode.get_width())/2, 175))
        screen.blit(pveMode, ((scrWidth - pveMode.get_width())/2, 265))
        pygame.draw.line(screen, (88, 252, 100), (0,235), (1200,235), 1)
        
        checkPick = False
        pick_P1_6_1 = pick_P1_6_2 = pick_P1_6_3 = pick_P1_6_4 = False
        pick_P1_5_1 = pick_P1_5_2 = pick_P1_5_3 = False
        pick_P1_4_1 = pick_P1_4_2 = pick_P1_4_3 = False
        pick_P1_3_1 = pick_P1_3_2 = False
        pick_P1_2_1 = pick_P1_2_2 = False  

        mouseClk = pygame.mouse.get_pos()
        if 15 <= mouseClk[0] < 75 and 15 <= mouseClk[1] <= 75:
            backToMainMenu = True
        else:
            backToMainMenu = False      
        if 0 < mouseClk[0] < scrWidth and 0 < mouseClk[1] < 235:
            showPvEMode = hoverPVE = hoverEasy = hoverNormal = hoverHard = False
            if (149 <= mouseClk[1] < 235):
                hoverPVP = True
                backToMainMenu = False
            else:
                hoverPVP = False
        if 0 < mouseClk[0] < scrWidth and 235 <= mouseClk[1] < scrHeight:
            hoverPVP = False
            showPvEMode = True
            hoverPVE = True
            if 235 <= mouseClk[1] < 325 or 520 <= mouseClk[1]:
                hoverEasy = hoverNormal = hoverHard = False
            elif 325 <= mouseClk[1] < 390:
                hoverEasy = True
                hoverNormal = hoverHard = False
            elif 390 <= mouseClk[1] < 455:
                hoverNormal = True
                hoverEasy = hoverHard = False
            elif 455 <= mouseClk[1] < 520:
                hoverHard = True
                hoverEasy = hoverNormal = False

        if hoverPVP == True:
            pygame.draw.rect(screen, (128, 235, 134), (0, 148, scrWidth, 87))
            screen.blit(nonPvPMode, (scrWidth/2 - pvpMode.get_width()/2, 175))
        if hoverPVP == False:
            pygame.draw.rect(screen, (255, 255, 255), (0, 148, scrWidth, 87))
            screen.blit(pvpMode, (scrWidth/2 - pvpMode.get_width()/2, 175))
        if hoverPVE == True:
            pygame.draw.rect(screen, (128, 235, 134), (0, 236, scrWidth, 89))
            screen.blit(nonPvEMode, (scrWidth/2 - pveMode.get_width()/2, 265))
        if hoverPVE == False:
            pygame.draw.rect(screen, (255, 255, 255), (0, 236, scrWidth, 89))
            screen.blit(pveMode, (scrWidth/2 - pveMode.get_width()/2, 265))
        if hoverEasy == True:
            pygame.draw.rect(screen, (217, 236, 28), (0, 325, scrWidth, 65))
            screen.blit(nonEasyMode, (scrWidth/2 - easyMode.get_width()/2, 340))
        if hoverEasy == False:
            pygame.draw.rect(screen, (255, 255, 255), (0, 325, scrWidth, 65))
            screen.blit(easyMode, (scrWidth/2 - easyMode.get_width()/2, 340))
        if hoverNormal == True:
            pygame.draw.rect(screen, (255, 188, 1), (0, 390, scrWidth, 65))
            screen.blit(nonNormalMode, (scrWidth/2 - normalMode.get_width()/2, 405))
        if hoverNormal == False:
            pygame.draw.rect(screen, (255, 255, 255), (0, 390, scrWidth, 65))
            screen.blit(normalMode, (scrWidth/2 - normalMode.get_width()/2, 405))
        if hoverHard == True:
            pygame.draw.rect(screen, (248, 45, 11), (0, 455, scrWidth, 65))
            screen.blit(nonHardMode, (scrWidth/2 - hardMode.get_width()/2, 470))
        if hoverHard == False:
            pygame.draw.rect(screen, (255, 255, 255), (0, 455, scrWidth, 65))
            screen.blit(hardMode, (scrWidth/2 - hardMode.get_width()/2, 470))        
        if showPvEMode == True:
            pygame.draw.line(screen, (154, 242, 54), (0,325), (1200,325), 1)
            pygame.draw.line(screen, (225, 218, 33), (0,390), (1200,390), 1)
            pygame.draw.line(screen, (232, 159, 21), (0,455), (1200,455), 1)
        if showPvEMode == False:
            pygame.draw.rect(screen, (255, 255, 255), (0, 325, scrWidth, scrHeight-325))

    if state == "pvpSelect":
        screen.fill([255, 255, 255])
        screen.blit(backImage, (25, 25))
        screen.blit(preparingText, ((scrWidth - preparingText.get_width())/2, 25))
        screen.blit(playerText, (810, 120))
        screen.blit(testText, (800, 40))  # test click
        screen.blit(testXYText, (800, 60))
        screen.blit(DText, (800, 80))
        screen.blit(curClickText, (800, 100))
        
        if putShip == True:
            pygame.draw.rect(screen, (255, 255, 255), (524, 170, 600, 20), 0)  
            screen.blit(putText, (524, 170))
        if alert1 == True:
            pygame.draw.rect(screen, (255, 255, 255), (524, 170, 600, 20), 0)  
            screen.blit(alert1Text, (524, 170))    
        for iShow in shipPrep:
            draw_ship(iShow['box'], iShow['width'], iShow['orient'], iShow['x'], iShow['y'])
        # for i in range(len(selectedCells)):
        #     for j in range(len(selectedCells[i])):
        #         if selectedCells[i][j]:
        #             pygame.draw.rect(screen, (100, 215, 5), (i*40+80, j*40+120, cellSize, cellSize), 0)  
        checkPick = True
        pygame.draw.rect(screen, (15, 85, 13), (850, 535, 100, 40), 1)   
        if (playerPrepare == 1):
            screen.blit(oneText, (818 + playerText.get_width(), 120))
            screen.blit(nextText, (880, 545))
        elif (playerPrepare == 2):
            screen.blit(twoText, (818 + playerText.get_width(), 120)) 
            screen.blit(startText, (878, 545))  
        for idg in range(100):
            x = idg % 10 * cellSize + 80
            y = idg // 10 * cellSize + 120
            pygame.draw.rect(screen, (15, 85, 13), (x, y, cellSize, cellSize), 1)
        pygame.draw.rect(screen, (41, 185, 43), (525, 200, 425, 320), 1)    # bảng chọn tàu
        pygame.draw.line(screen, (41, 185, 43), (525, 264), (949, 264), 1)  # phân chia các tàu
        pygame.draw.line(screen, (41, 185, 43), (525, 328), (949, 328), 1)  
        pygame.draw.line(screen, (41, 185, 43), (525, 392), (949, 392), 1)  
        pygame.draw.line(screen, (41, 185, 43), (525, 456), (949, 456), 1)  
        pygame.draw.line(screen, (41, 185, 43), (737, 200), (737, 327), 1)
        pygame.draw.line(screen, (41, 185, 43), (666, 328), (666, 455), 1)
        pygame.draw.line(screen, (41, 185, 43), (808, 328), (808, 455), 1)
        pygame.draw.line(screen, (41, 185, 43), (737, 456), (737, 519), 1)
        pygame.draw.line(screen, (41, 185, 43), (631, 456), (631, 519), 1)
        pygame.draw.line(screen, (41, 185, 43), (843, 456), (843, 519), 1)
        screen.blit(sixShipText, (722, 206))
        screen.blit(sixShipText, (935, 206))
        screen.blit(sixShipText, (722, 270))
        screen.blit(sixShipText, (935, 270))
        screen.blit(fiveShipText, (651, 334))
        screen.blit(fiveShipText, (793, 334))
        screen.blit(fiveShipText, (935, 334))
        screen.blit(fourShipText, (651, 398))
        screen.blit(fourShipText, (793, 398))
        screen.blit(fourShipText, (935, 398))
        screen.blit(threeShipText, (616, 462))
        screen.blit(threeShipText, (722, 462))
        screen.blit(twoShipText, (828, 462))
        screen.blit(twoShipText, (935, 462))
        draw_mini_sqr(580, 225, 14, 6)  # chọn 6
        draw_mini_sqr(792, 225, 14, 6)
        draw_mini_sqr(607, 280, 14, 3)
        draw_mini_sqr(607, 299, 14, 3)
        draw_mini_sqr(819, 280, 14, 3)
        draw_mini_sqr(819, 299, 14, 3)
        draw_mini_sqr(553, 353, 14, 5)  # chọn 5
        draw_mini_sqr(695, 353, 14, 5)
        draw_mini_sqr(871, 335, 14, 1)
        draw_mini_sqr(853, 353, 14, 3)
        draw_mini_sqr(871, 371, 14, 1)
        draw_mini_sqr(562, 417, 14, 4)  # chọn 4
        draw_mini_sqr(703, 417, 14, 4)
        draw_mini_sqr(862, 410, 14, 2)
        draw_mini_sqr(862, 428, 14, 2)
        draw_mini_sqr(554, 481, 14, 3)  # chọn 3
        draw_mini_sqr(659, 481, 14, 3)
        draw_mini_sqr(774, 481, 14, 2)  # chọn 2
        draw_mini_sqr(880, 481, 14, 2)
        
        
        mouseClk = pygame.mouse.get_pos()
        if 15 <= mouseClk[0] < 75 and 15 <= mouseClk[1] <= 75:
            if playerPrepare == 1:
                backToSelectMenu = True
            if playerPrepare == 2:
                prevPlayer = True   
                nextPlayer = False  
        else:
            backToSelectMenu = False    
        if 850 <= mouseClk[0] < 950 and 535 <= mouseClk[1] < 575:
            if playerPrepare == 1:
                if len(shipPrep) == 5:
                    shipPrep1 = shipPrep.copy()
                    nextPlayer = True      
                    prevPlayer = False
                    hoverNext = True
                    hoverStartGame = False           
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (524, 170, 600, 20), 0)  
                    screen.blit(alert2Text, (524, 170))     
            elif playerPrepare == 2:
                hoverStartGame = True    
                hoverNext = False
        else:
            hoverNext = hoverStartGame = False        
                
        if hoverNext == True and playerPrepare == 1:
            pygame.draw.rect(screen, (15, 85, 13), (850, 535, 100, 40), 0)    
            screen.blit(nonNextText, (880, 545))
        if hoverNext == False and playerPrepare == 1:
            pygame.draw.rect(screen, (15, 85, 13), (850, 535, 100, 40), 1)  
            pygame.draw.rect(screen, (255, 255, 255), (851, 536, 98, 38), 1)  
            screen.blit(nextText, (880, 545))
        if hoverStartGame == True and playerPrepare == 2:
            pygame.draw.rect(screen, (15, 85, 13), (850, 535, 100, 40), 0)    
            screen.blit(nonStartText, (878, 545))
        if hoverStartGame == False and playerPrepare == 2:
            pygame.draw.rect(screen, (15, 85, 13), (850, 535, 100, 40), 1)  
            pygame.draw.rect(screen, (255, 255, 255), (851, 536, 98, 38), 1)  
            screen.blit(startText, (878, 545))    
        if pick_P1_6_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 201, 211, 63)) 
            draw_mini_sqr(580, 225, 14, 6) 
            screen.blit(sixShipText, (722, 206))   
            screen.blit(vText, (535, 206))   
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 201, 211, 63))    
            screen.blit(sixShipText, (722, 206))   
            screen.blit(vText, (535, 206))     
            draw_mini_sqr(580, 225, 14, 6)   
        if pick_P1_6_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (738, 201, 211, 63)) 
            draw_mini_sqr(792, 225, 14, 6)         
            screen.blit(hText, (747, 206))  
            screen.blit(sixShipText, (935, 206))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (738, 201, 211, 63))    
            screen.blit(sixShipText, (935, 206))    
            screen.blit(hText, (747, 206))   
            draw_mini_sqr(792, 225, 14, 6)     
        if pick_P1_6_3 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 265, 211, 63)) 
            screen.blit(vText, (535, 206))   
            draw_mini_sqr(607, 280, 14, 3)
            draw_mini_sqr(607, 299, 14, 3)       
            screen.blit(sixShipText, (722, 270))
            screen.blit(vText, (535, 270))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 265, 211, 63))    
            screen.blit(sixShipText, (722, 270))     
            screen.blit(vText, (535, 270))  
            draw_mini_sqr(607, 280, 14, 3)
            draw_mini_sqr(607, 299, 14, 3)
        if pick_P1_6_4 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (738, 265, 211, 63)) 
            screen.blit(hText, (747, 270))
            draw_mini_sqr(819, 280, 14, 3)
            draw_mini_sqr(819, 299, 14, 3)  
            screen.blit(sixShipText, (935, 270))      
        else:
            pygame.draw.rect(screen, (255, 255, 255), (738, 265, 211, 63))    
            screen.blit(sixShipText, (935, 270))   
            screen.blit(hText, (747, 270))  
            draw_mini_sqr(819, 280, 14, 3)
            draw_mini_sqr(819, 299, 14, 3)     
            
        if pick_P1_5_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 329, 140, 63)) 
            draw_mini_sqr(553, 353, 14, 5)   
            screen.blit(fiveShipText, (651, 334))    
            screen.blit(vText, (535, 334))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 329, 140, 63))    
            screen.blit(fiveShipText, (651, 334))    
            screen.blit(vText, (535, 334))
            draw_mini_sqr(553, 353, 14, 5) 
        if pick_P1_5_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (667, 329, 141, 63)) 
            draw_mini_sqr(695, 353, 14, 5)   
            screen.blit(fiveShipText, (793, 334))  
            screen.blit(hText, (676, 334))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (667, 329, 141, 63))    
            screen.blit(fiveShipText, (793, 334))    
            screen.blit(hText, (676, 334))
            draw_mini_sqr(695, 353, 14, 5)
        if pick_P1_5_3 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (809, 329, 140, 63)) 
            draw_mini_sqr(871, 335, 14, 1)
            draw_mini_sqr(853, 353, 14, 3)
            draw_mini_sqr(871, 371, 14, 1)     
            screen.blit(fiveShipText, (935, 334))
            screen.blit(rText, (818, 334))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (809, 329, 140, 63))    
            screen.blit(fiveShipText, (935, 334))  
            screen.blit(rText, (818, 334))  
            draw_mini_sqr(871, 335, 14, 1)
            draw_mini_sqr(853, 353, 14, 3)
            draw_mini_sqr(871, 371, 14, 1)                         
                
        if pick_P1_4_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 393, 140, 63)) 
            draw_mini_sqr(562, 417, 14, 4) 
            screen.blit(fourShipText, (651, 398)) 
            screen.blit(vText, (535, 398))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 393, 140, 63))    
            screen.blit(fourShipText, (651, 398))   
            screen.blit(vText, (535, 398))
            draw_mini_sqr(562, 417, 14, 4)    
        if pick_P1_4_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (667, 393, 141, 63)) 
            draw_mini_sqr(703, 417, 14, 4)
            screen.blit(fourShipText, (793, 398))
            screen.blit(hText, (676, 398))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (667, 393, 141, 63))    
            screen.blit(fourShipText, (793, 398)) 
            screen.blit(hText, (676, 398))
            draw_mini_sqr(703, 417, 14, 4)       
        if pick_P1_4_3 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (809, 393, 140, 63)) 
            draw_mini_sqr(862, 410, 14, 2)
            draw_mini_sqr(862, 428, 14, 2)
            screen.blit(fourShipText, (935, 398))
            screen.blit(rText, (818, 398))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (809, 393, 140, 63))    
            screen.blit(fourShipText, (935, 398))  
            screen.blit(rText, (818, 398))
            draw_mini_sqr(862, 410, 14, 2)
            draw_mini_sqr(862, 428, 14, 2)        
        
        if pick_P1_3_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 457, 105, 62)) 
            draw_mini_sqr(554, 481, 14, 3)
            screen.blit(threeShipText, (616, 462))
            screen.blit(vText, (535, 462))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 457, 105, 62))    
            screen.blit(threeShipText, (616, 462))
            screen.blit(vText, (535, 462))
            draw_mini_sqr(554, 481, 14, 3) 
        if pick_P1_3_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (632, 457, 105, 62)) 
            draw_mini_sqr(659, 481, 14, 3)
            screen.blit(threeShipText, (722, 462))
            screen.blit(hText, (639, 462))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (632, 457, 105, 62))    
            screen.blit(threeShipText, (722, 462)) 
            screen.blit(hText, (639, 462))
            draw_mini_sqr(659, 481, 14, 3)           
            
        if pick_P1_2_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (738, 457, 105, 62)) 
            draw_mini_sqr(774, 481, 14, 2)
            screen.blit(twoShipText, (828, 462))
            screen.blit(vText, (747, 462))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (738, 457, 105, 62))    
            screen.blit(twoShipText, (828, 462))
            screen.blit(vText, (747, 462))
            draw_mini_sqr(774, 481, 14, 2) 
        if pick_P1_2_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (844, 457, 105, 62)) 
            draw_mini_sqr(880, 481, 14, 2)
            screen.blit(twoShipText, (935, 462))
            screen.blit(hText, (853, 462))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (844, 457, 105, 62))    
            screen.blit(twoShipText, (935, 462)) 
            screen.blit(hText, (853, 462))
            draw_mini_sqr(880, 481, 14, 2)              
    
    if state == "pveSelect":
        screen.fill([255, 255, 255])
        screen.blit(backImage, (25, 25))
        screen.blit(preparingText, ((scrWidth - preparingText.get_width())/2, 25))
        screen.blit(yourText, (772, 120))    
        pygame.draw.rect(screen, (15, 85, 13), (850, 535, 100, 40), 1) 
        screen.blit(startText, (878, 545)) 
        
        if putShip == True:
            pygame.draw.rect(screen, (255, 255, 255), (524, 170, 600, 20), 0)  
            screen.blit(putText, (524, 170))
        if alert1 == True:
            pygame.draw.rect(screen, (255, 255, 255), (524, 170, 600, 20), 0)  
            screen.blit(alert1Text, (524, 170))    
        for iShow in shipPrep:
            draw_ship(iShow['box'], iShow['width'], iShow['orient'], iShow['x'], iShow['y'])        
        checkPick = True    
        
        for idg in range(100):
            x = idg % 10 * cellSize + 80
            y = idg // 10 * cellSize + 120
            pygame.draw.rect(screen, (15, 85, 13), (x, y, cellSize, cellSize), 1)
        pygame.draw.rect(screen, (41, 185, 43), (525, 200, 425, 320), 1)    # bảng chọn tàu
        pygame.draw.line(screen, (41, 185, 43), (525, 264), (949, 264), 1)  # phân chia các tàu
        pygame.draw.line(screen, (41, 185, 43), (525, 328), (949, 328), 1)  
        pygame.draw.line(screen, (41, 185, 43), (525, 392), (949, 392), 1)  
        pygame.draw.line(screen, (41, 185, 43), (525, 456), (949, 456), 1)  
        pygame.draw.line(screen, (41, 185, 43), (737, 200), (737, 327), 1)
        pygame.draw.line(screen, (41, 185, 43), (666, 328), (666, 455), 1)
        pygame.draw.line(screen, (41, 185, 43), (808, 328), (808, 455), 1)
        pygame.draw.line(screen, (41, 185, 43), (737, 456), (737, 519), 1)
        pygame.draw.line(screen, (41, 185, 43), (631, 456), (631, 519), 1)
        pygame.draw.line(screen, (41, 185, 43), (843, 456), (843, 519), 1)
        screen.blit(sixShipText, (722, 206))
        screen.blit(sixShipText, (935, 206))
        screen.blit(sixShipText, (722, 270))
        screen.blit(sixShipText, (935, 270))
        screen.blit(fiveShipText, (651, 334))
        screen.blit(fiveShipText, (793, 334))
        screen.blit(fiveShipText, (935, 334))
        screen.blit(fourShipText, (651, 398))
        screen.blit(fourShipText, (793, 398))
        screen.blit(fourShipText, (935, 398))
        screen.blit(threeShipText, (616, 462))
        screen.blit(threeShipText, (722, 462))
        screen.blit(twoShipText, (828, 462))
        screen.blit(twoShipText, (935, 462))
        draw_mini_sqr(580, 225, 14, 6)  # chọn 6
        draw_mini_sqr(792, 225, 14, 6)
        draw_mini_sqr(607, 280, 14, 3)
        draw_mini_sqr(607, 299, 14, 3)
        draw_mini_sqr(819, 280, 14, 3)
        draw_mini_sqr(819, 299, 14, 3)
        draw_mini_sqr(553, 353, 14, 5)  # chọn 5
        draw_mini_sqr(695, 353, 14, 5)
        draw_mini_sqr(871, 335, 14, 1)
        draw_mini_sqr(853, 353, 14, 3)
        draw_mini_sqr(871, 371, 14, 1)
        draw_mini_sqr(562, 417, 14, 4)  # chọn 4
        draw_mini_sqr(703, 417, 14, 4)
        draw_mini_sqr(862, 410, 14, 2)
        draw_mini_sqr(862, 428, 14, 2)
        draw_mini_sqr(554, 481, 14, 3)  # chọn 3
        draw_mini_sqr(659, 481, 14, 3)
        draw_mini_sqr(774, 481, 14, 2)  # chọn 2
        draw_mini_sqr(880, 481, 14, 2)
        
        if hoverStartGame == True:
            pygame.draw.rect(screen, (15, 85, 13), (850, 535, 100, 40), 0)    
            screen.blit(nonStartText, (878, 545))
        if hoverStartGame == False:
            pygame.draw.rect(screen, (15, 85, 13), (850, 535, 100, 40), 1)  
            pygame.draw.rect(screen, (255, 255, 255), (851, 536, 98, 38), 1)  
            screen.blit(startText, (878, 545))  
        if pick_P1_6_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 201, 211, 63)) 
            draw_mini_sqr(580, 225, 14, 6) 
            screen.blit(sixShipText, (722, 206))   
            screen.blit(vText, (535, 206))   
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 201, 211, 63))    
            screen.blit(sixShipText, (722, 206))   
            screen.blit(vText, (535, 206))     
            draw_mini_sqr(580, 225, 14, 6)   
        if pick_P1_6_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (738, 201, 211, 63)) 
            draw_mini_sqr(792, 225, 14, 6)         
            screen.blit(hText, (747, 206))  
            screen.blit(sixShipText, (935, 206))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (738, 201, 211, 63))    
            screen.blit(sixShipText, (935, 206))    
            screen.blit(hText, (747, 206))   
            draw_mini_sqr(792, 225, 14, 6)     
        if pick_P1_6_3 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 265, 211, 63)) 
            screen.blit(vText, (535, 206))   
            draw_mini_sqr(607, 280, 14, 3)
            draw_mini_sqr(607, 299, 14, 3)       
            screen.blit(sixShipText, (722, 270))
            screen.blit(vText, (535, 270))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 265, 211, 63))    
            screen.blit(sixShipText, (722, 270))     
            screen.blit(vText, (535, 270))  
            draw_mini_sqr(607, 280, 14, 3)
            draw_mini_sqr(607, 299, 14, 3)
        if pick_P1_6_4 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (738, 265, 211, 63)) 
            screen.blit(hText, (747, 270))
            draw_mini_sqr(819, 280, 14, 3)
            draw_mini_sqr(819, 299, 14, 3)  
            screen.blit(sixShipText, (935, 270))      
        else:
            pygame.draw.rect(screen, (255, 255, 255), (738, 265, 211, 63))    
            screen.blit(sixShipText, (935, 270))   
            screen.blit(hText, (747, 270))  
            draw_mini_sqr(819, 280, 14, 3)
            draw_mini_sqr(819, 299, 14, 3)     
            
        if pick_P1_5_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 329, 140, 63)) 
            draw_mini_sqr(553, 353, 14, 5)   
            screen.blit(fiveShipText, (651, 334))    
            screen.blit(vText, (535, 334))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 329, 140, 63))    
            screen.blit(fiveShipText, (651, 334))    
            screen.blit(vText, (535, 334))
            draw_mini_sqr(553, 353, 14, 5) 
        if pick_P1_5_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (667, 329, 141, 63)) 
            draw_mini_sqr(695, 353, 14, 5)   
            screen.blit(fiveShipText, (793, 334))  
            screen.blit(hText, (676, 334))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (667, 329, 141, 63))    
            screen.blit(fiveShipText, (793, 334))    
            screen.blit(hText, (676, 334))
            draw_mini_sqr(695, 353, 14, 5)
        if pick_P1_5_3 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (809, 329, 140, 63)) 
            draw_mini_sqr(871, 335, 14, 1)
            draw_mini_sqr(853, 353, 14, 3)
            draw_mini_sqr(871, 371, 14, 1)     
            screen.blit(fiveShipText, (935, 334))
            screen.blit(rText, (818, 334))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (809, 329, 140, 63))    
            screen.blit(fiveShipText, (935, 334))  
            screen.blit(rText, (818, 334))  
            draw_mini_sqr(871, 335, 14, 1)
            draw_mini_sqr(853, 353, 14, 3)
            draw_mini_sqr(871, 371, 14, 1)                         
                
        if pick_P1_4_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 393, 140, 63)) 
            draw_mini_sqr(562, 417, 14, 4) 
            screen.blit(fourShipText, (651, 398)) 
            screen.blit(vText, (535, 398))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 393, 140, 63))    
            screen.blit(fourShipText, (651, 398))   
            screen.blit(vText, (535, 398))
            draw_mini_sqr(562, 417, 14, 4)    
        if pick_P1_4_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (667, 393, 141, 63)) 
            draw_mini_sqr(703, 417, 14, 4)
            screen.blit(fourShipText, (793, 398))
            screen.blit(hText, (676, 398))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (667, 393, 141, 63))    
            screen.blit(fourShipText, (793, 398)) 
            screen.blit(hText, (676, 398))
            draw_mini_sqr(703, 417, 14, 4)       
        if pick_P1_4_3 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (809, 393, 140, 63)) 
            draw_mini_sqr(862, 410, 14, 2)
            draw_mini_sqr(862, 428, 14, 2)
            screen.blit(fourShipText, (935, 398))
            screen.blit(rText, (818, 398))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (809, 393, 140, 63))    
            screen.blit(fourShipText, (935, 398))  
            screen.blit(rText, (818, 398))
            draw_mini_sqr(862, 410, 14, 2)
            draw_mini_sqr(862, 428, 14, 2)        
        
        if pick_P1_3_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (526, 457, 105, 62)) 
            draw_mini_sqr(554, 481, 14, 3)
            screen.blit(threeShipText, (616, 462))
            screen.blit(vText, (535, 462))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (526, 457, 105, 62))    
            screen.blit(threeShipText, (616, 462))
            screen.blit(vText, (535, 462))
            draw_mini_sqr(554, 481, 14, 3) 
        if pick_P1_3_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (632, 457, 105, 62)) 
            draw_mini_sqr(659, 481, 14, 3)
            screen.blit(threeShipText, (722, 462))
            screen.blit(hText, (639, 462))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (632, 457, 105, 62))    
            screen.blit(threeShipText, (722, 462)) 
            screen.blit(hText, (639, 462))
            draw_mini_sqr(659, 481, 14, 3)           
            
        if pick_P1_2_1 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (738, 457, 105, 62)) 
            draw_mini_sqr(774, 481, 14, 2)
            screen.blit(twoShipText, (828, 462))
            screen.blit(vText, (747, 462))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (738, 457, 105, 62))    
            screen.blit(twoShipText, (828, 462))
            screen.blit(vText, (747, 462))
            draw_mini_sqr(774, 481, 14, 2) 
        if pick_P1_2_2 == True:  
            pygame.draw.rect(screen, (63, 255, 21), (844, 457, 105, 62)) 
            draw_mini_sqr(880, 481, 14, 2)
            screen.blit(twoShipText, (935, 462))
            screen.blit(hText, (853, 462))
        else:
            pygame.draw.rect(screen, (255, 255, 255), (844, 457, 105, 62))    
            screen.blit(twoShipText, (935, 462)) 
            screen.blit(hText, (853, 462))
            draw_mini_sqr(880, 481, 14, 2)              
    
        
        if modeGame == 1:
            screen.blit(easyText, (517, 125)) 
        elif modeGame == 2:
            screen.blit(normalText, (517, 125))
        elif modeGame == 3:
            screen.blit(hardText, (517, 125))        
        
        mouseClk = pygame.mouse.get_pos()
        if 15 <= mouseClk[0] < 75 and 15 <= mouseClk[1] <= 75:
            backToSelectMenu = True
            shipPrep = shipPrep1 = []
        else:
            backToSelectMenu = False             
        if 850 <= mouseClk[0] < 950 and 535 <= mouseClk[1] < 575:
            if len(shipPrep) == 5:
                shipPrep1 = shipPrep.copy()
                hoverStartGame = True           
            else:
                pygame.draw.rect(screen, (255, 255, 255), (524, 170, 600, 20), 0)  
                screen.blit(alert2Text, (524, 170))  
        else:
            hoverStartGame = False
    
    if state == "playing":
        screen.fill([255, 255, 255])
        screen.blit(backImage, (25, 25))
        screen.blit(playingText, ((scrWidth - playingText.get_width())/2, 25))  
        screen.blit(pointText, (773, 160))
        if modeGame == 1:
            screen.blit(easyText, (517, 125)) 
        elif modeGame == 2:
            screen.blit(normalText, (517, 125))
        elif modeGame == 3:
            screen.blit(hardText, (517, 125))     
        if len(shipBotPrep) == 0:
            sl_1 = copy.deepcopy(selectedCells)
            selectedCells = [[0] * 10 for _ in range(10)]
            shipPrep = []
            createShipBot()
            shipBotPrep = shipPrep.copy()
            sl_2 = copy.deepcopy(selectedCells)
        # for iShow in shipBotPrep:
        #     draw_ship(iShow['box'], iShow['width'], iShow['orient'], iShow['x'], iShow['y'])
        for idg in range(100):
            x = idg % 10 * cellSize + 80
            y = idg // 10 * cellSize + 120
            pygame.draw.rect(screen, (15, 85, 13), (x, y, cellSize, cellSize), 1)
        pygame.draw.rect(screen, (41, 185, 43), (525, 200, 425, 320), 1)   
        pygame.draw.rect(screen, (41, 185, 43), (525, 200, 425, 320), 1)    # bảng chọn tàu
        pygame.draw.line(screen, (41, 185, 43), (525, 264), (949, 264), 1)  # phân chia các tàu
        pygame.draw.line(screen, (41, 185, 43), (525, 328), (949, 328), 1)  
        pygame.draw.line(screen, (41, 185, 43), (525, 392), (949, 392), 1)  
        pygame.draw.line(screen, (41, 185, 43), (525, 456), (949, 456), 1)   
        screen.blit(twosText, (550, 217))
        screen.blit(threesText, (550, 281))
        screen.blit(foursText, (550, 345))
        screen.blit(fivesText, (550, 409))
        screen.blit(sixsText, (550, 473))
        # strText = miniFont.render(str(sl_2), True, (0,0,0))  
        # screen.blit(strText, (10,50))     
        
        # if show_pl == True:
        #     pygame.time.delay(500)
        #     clr_Box()
        #     draw_pl()
        #     show_pl = False
        
        if turn == 'player':
            ptsText1 = insFont.render(str(pts_pl), True, (48, 165, 105))
            screen.blit(ptsText1, (822, 160))
            pygame.draw.rect(screen, (255, 255, 255), (760, 106, yourTurnText.get_width(), yourTurnText.get_height()), 0)  
            screen.blit(yourTurnText, (773, 120))
            draw_pl()
            if show_pl == True:  
                draw_pl()
                pygame.time.delay(200)
                show_pl = False
                
                
        elif turn == 'bot':
            if modeGame == 1:
                clr_Box()
                ptsText2 = insFont.render(str(pts_bot), True, (48, 165, 105))
                screen.blit(ptsText2, (822, 160))
                pygame.draw.rect(screen, (255, 255, 255), (760, 106, botTurnText.get_width(), botTurnText.get_height()), 0)  
                screen.blit(botTurnText, (773, 120))
                draw_bot()
                                            
    if state == "end":
        if showEnd == False:
            for i in range(0,256):
                pygame.time.delay(5)
                screen.fill([i, i, i])         
                pygame.display.flip()
                showEnd = True 
        winnerText = titleFont.render(str(winner), 1, (48, 165, 105), (255, 255, 255))        
        screen.blit(winnerTitleText, ((scrWidth-winnerTitleText.get_width())/2, 30))        
        screen.blit(winnerText, ((scrWidth-winnerText.get_width())/2, 80))  
        screen.blit(winnerImage, ((scrWidth-winnerImage.get_width())/2, 190))
        screen.blit(playerText, (120, 320))
        screen.blit(botText, (790, 320))
        screen.blit(ptsText1, (70, 390))
        screen.blit(ptsText2, (740, 390))
        screen.blit(remainingText, (70, 440))
        screen.blit(remainingText, (740, 440))
                         
    pygame.display.update()
