import pygame as py


def pmain():
  x = PlayerVsPlayer()
  x.playGame()

class PlayerVsPlayer:
  def __init__(self):
    #Render Variavles
    self.framerate = 60
    self.width = self.height = 800
    self.rows = self.columns = 8
    self.squareSize = self.height // self.rows
    self.kingmarker = py.transform.scale(py.image.load("images/marker.png"), (60, 56))
    self.classText = Text()
    
    #Board variables
    self.moveCounter = 0
    self.board = []
    self.redMen = self.whiteMen = 12
    self.redKings = self.whiteKings = 0
    self.chosenPiece = None
    
    #Misc
    self.leftClick = 1
    self.rightClick = 3


  #==================================================
  # Creating the Interface
  #==================================================

  def createWindow(self):
    self.window = py.display.set_mode((self.width,self.height))
    py.display.set_caption("Draughts")


  def playGame(self):
    '''
    Waits for an input from the user in order to call a function in the code
    '''
    self.createWindow()
    self.drawBoard()
    self.drawSquares()

    classLogic = Logic(self.window)
    self.classText.createTextFile()
    self.drawBoard()
    self.run = True
    clock = py.time.Clock()

    while self.run:
      # Updates the window 1/(self.framemate) second
      clock.tick(self.framerate)

      # Iterates until the event queue is empty
      # Take first item in the queue, checks the type and button
      for event in py.event.get():
        if event.type == py.QUIT:
          # Stop the program
          self.run = False
        if event.type == py.MOUSEBUTTONDOWN and event.button == self.leftClick:
          # Calls mousePosition function and returns value into choose function
          position = py.mouse.get_pos()
          r , c = self.mousePosition(position)
          classLogic.choose(r,c)
          break
        if event.type == py.MOUSEBUTTONDOWN and event.button == self.rightClick:
          #Calls mousePosition function and returns value into drawHelp function
          position = py.mouse.get_pos()
          r , c = self.mousePosition(position)
          self.drawHelp(r,c)
          break
        if event.type == py.KEYDOWN and event.key == py.K_r:
          #Calls resignGame function for Red
          resignColour = "red"
          self.resignGame(resignColour)
        if event.type == py.KEYDOWN and event.key == py.K_w:
          #Calls resignGame function for White
          resignColour = "white"
          self.resignGame(resignColour)
        if event.type == py.KEYDOWN and event.key == py.K_d:
          #Calls jointDraw function
          self.jointDraw()
  

      classLogic.refreshScreen()
      
    py.quit()
    return

  #==================================================
  # Tracking Mouse Position & Drawing Guidance Lines
  #==================================================

  def mousePosition(self,position):
    # Uses the position to find the row and column of the mouse on the board
    x , y= position
    column = x // self.squareSize
    row = y // self.squareSize
    return row , column


  def drawHelp(self,r,c):
    ''' 
    Uses the values returned from mousePosition function to draw the guidance lines
    '''
    r2 = c2 = -1
    #Keeps looping until another position is clicked
    while r2 == -1 and c2 == -1:
      for event2 in py.event.get():
        if event2.type == py.MOUSEBUTTONDOWN and event2.button == self.rightClick:
          position2 = py.mouse.get_pos()
          r2 , c2 = self.mousePosition(position2)
    #Calculate the position of the screen where the line is drawn
    rPosition = self.squareSize * r + self.squareSize // 2
    cPosition = self.squareSize * c + self.squareSize // 2
    firstPosition = [ cPosition , rPosition ]
    r2Position = self.squareSize * r2 + self.squareSize // 2
    c2Position = self.squareSize * c2 + self.squareSize // 2
    secondPosition = [ c2Position , r2Position ]
    #Draws the line with it starting at firstPosition and ending at secondPosition
    py.draw.circle(self.window, py.Color("black"), firstPosition, 17)
    py.draw.line(self.window, py.Color("black"), firstPosition, secondPosition, 20)
    py.draw.circle(self.window, py.Color("black"), secondPosition, 17)
    py.draw.circle(self.window, py.Color("darkseagreen"), firstPosition, 15)
    py.draw.line(self.window, py.Color("darkseagreen"), firstPosition, secondPosition, 15)
    py.draw.circle(self.window, py.Color("darkseagreen"), secondPosition, 15)
    py.display.update()
    #RightClick will recursively repeat the drawHelp function
    #until a leftClick which will delete all the lines
    self.stop = 0
    while self.stop == 0:
      for event in py.event.get():
        if event.type == py.MOUSEBUTTONDOWN and event.button == self.leftClick:
          self.stop = 1
        if event.type == py.MOUSEBUTTONDOWN and event.button == self.rightClick:
          position = py.mouse.get_pos()
          r , c = self.mousePosition(position)
          #Recursive Algorithm
          self.drawHelp(r,c)

          
  #==================================================
  # Drawing the Board
  #==================================================

  def renderBoard(self):
    '''
    Checks if piece at (row,col) is empty and draws appropriately
    '''
    self.drawSquares()
    for row in range(self.rows):
      for column in range(self.columns):
        piece = self.board[row][column]
        if piece != "//":
          piece.drawPiece()
  
  def drawSquares(self):
    '''
    Draw alternating coloured squares as the board and calls DrawCoordinates
    '''
    boardColours = [py.Color("antiquewhite"), py.Color("antiquewhite4")]
    for i in range(self.rows):
        for k in range(self.columns):
            boardColour = boardColours[((i + k) % 2)]  # Even squares = Light // Odd Squares = Dark
            py.draw.rect(self.window, boardColour, py.Rect(k * self.squareSize, i * self.squareSize, self.squareSize, self.squareSize))
    self.drawCoordinates()

  def drawCoordinates(self):
    '''
    #Renders numbers acting as a x and y axis on the board
    '''
    py.font.init()
    font = py.font.SysFont("arial",15)
    for row in range(self.rows):
      for column in range(self.columns):
        if row == 0: 
          #Renders increasing numbers in ascending rowson the leftmost column
          text = font.render(str(8-column), True, py.Color("black"))
          position = (5,(column*100 + 80))
          self.window.blit(text,position)
        if column == 0: 
          #Renders increasing numbers in ascending columns on the bottom row
          text = font.render(str(row+1), True, py.Color("black"))
          position = ((row*100 + 5), 780)
          self.window.blit(text,position)


  def drawBoard(self):
    '''
    Adds a piece or empty space into the list self.board
    '''
    for r in range(self.rows):
      self.board.append([])
      for c in range(self.columns):
        if c % 2 == ((r + 1) % 2):
          #On every other square
          if r < 3:
            #Top 3 rows will have white Pieces
            self.board[r].append(Piece(r,c,py.Color("white"),self.window))
          elif r > 4:
            #Bottom 3 rows will have red Pieces
            self.board[r].append(Piece(r,c,py.Color("red"),self.window))
          else:
            self.board[r].append("//")
        else:
          self.board[r].append("//")

  #==================================================
  # Checking, Moving, Removing Pieces
  #==================================================

  def checkPiece(self,r,c):
    return(self.board[r][c])


  def movePiece(self, p, r, c):
    '''
    Moves piece in the array and check if it is upgraded to a king
    '''
    self.classText.pieceMoveText(p,r,c)
    self.board[p.pieceRow][p.pieceColumn], self.board[r][c] = self.board[r][c], self.board[p.pieceRow][p.pieceColumn]
    p.pieceMove(r,c)
    if r == self.rows - 1 or r == 0:
      p.createKing()
      if p.pieceColour == py.Color("white"):
        self.whiteKings = self.whiteKings + 1
      elif p.pieceColour == py.Color("red"):
        self.redKings = self.redKings + 1
  
  def removePiece(self,removePiece):
    '''
    Removes piece and checks if there is no opposing piece
    '''
    for p in removePiece:
      r , c = p
      piece = self.board[r][c]
      self.board[r][c] = "//"
      self.classText.pieceRemoveText(removePiece,piece)
      if piece != "//":
        if piece.pieceColour == py.Color("red"):
          self.redMen = self.redMen - 1
          self.winner()
        else:
          self.whiteMen = self.whiteMen - 1
          self.winner()
    
  
  #==================================================
  # Game Ending Decisions
  #==================================================

  def winner(self):
    reason = "Elimination"
    if self.redMen <= 0:
      winner = "White"
      self.endGameWin(winner,reason)
    if self.whiteMen <= 0:
      winner = "Red"
      self.endGameWin(winner,reason)
  
  def endGameWin(self,colourWinner,reason):
    py.draw.rect(self.window, py.Color("white"),py.Rect(0, 300, 800, 200))
    py.font.init()
    font = py.font.SysFont("arial",15)
    text = font.render(str(colourWinner + " wins!"), True, py.Color("black"))
    position = (0,400)
    self.window.blit(text,position)
    self.classText.gameWin(reason, colourWinner)
    print( colourWinner + " wins! (" + reason + ")")
    self.clickToQuit()

  def jointDraw(self):
    print("")
    print("Joint Draw Decision has been requested")
    print("""
    Red: 
    -> press R key to agree
    -> press X key to disagree
    """)
    stop = 0
    while stop == 0:
      for event in py.event.get():
        if event.type == py.KEYDOWN and event.key == py.K_r:
          stop = stop + 1
          break
        if event.type == py.KEYDOWN and event.key == py.K_x:
          stop = stop + 1
          print("Red has declined the request")
          return None
          break
    stop = 0
    print("""
    White: 
    -> press W key to agree
    -> press X key to disagree
    """)
    while stop == 0:
      for event in py.event.get():
        if event.type == py.KEYDOWN and event.key == py.K_w:
          stop = stop + 1
          break
        if event.type == py.KEYDOWN and event.key == py.K_x:
          stop = stop + 1
          print("White has declined the request")
          return None
          break
    reason = "joint decision"
    self.classText.gameDraw(reason)
    self.clickToQuit()

  
  def resignGame(self,resignColour):
    reason = "Resignation"
    confirm = False
    if resignColour == "red":
      print("""
      Red:
      -> press R key to confirm
      -> press X key to cancel
      """)
      while confirm == False:
        for event in py.event.get():
          if event.type == py.KEYDOWN and event.key == py.K_r:
            confirm = True
            self.endGameWin("White", reason)
            break
          if event.type == py.KEYDOWN and event.key == py.K_x:
            confirm = True
            print("Red has cancelled")
            return None
            break
    if resignColour == "white":
      print("""
      White:
      -> press W key to confirm
      -> press X key to cancel
      """)
      while confirm == False:
        for event in py.event.get():
          if event.type == py.KEYDOWN and event.key == py.K_w:
            confirm = True
            self.endGameWin("Red", reason)
            break
          if event.type == py.KEYDOWN and event.key == py.K_x:
            confirm = True
            print("White has cancelled")
            return None
            break

  def clickToQuit(self):
    stop = 0
    while stop == 0:
      for event in py.event.get():
        if event.type == py.MOUSEBUTTONDOWN and (event.button == self.leftClick or event.button == self.rightClick):
          py.quit()
          stop = stop + 1
  
  
  #==================================================
  # Creating, Getting, Checking Valid Moves
  #==================================================

  def checkForNoValidMoves(self, colour):
    '''
    Checks if there is no valid moves -> No valid moves = the game draws as a stalemate 
    '''
    counter = 0
    for r in range(self.rows):
      for c in range(self.columns):
        piece = self.checkPiece(r,c)
        if piece != "//":
          if piece.pieceColour == colour:
            vmoves = self.createValidMoves(piece)
            if vmoves != {}:
              counter = counter + 1
              reason = "no valid moves."
              break
      if counter != 0 :
        break
    if counter == 0:
      self.classText.gameDraw(reason)
      self.clickToQuit()
  

  def createValidMoves(self,piece):
    '''
    Creates a dictionary for valid moves and creates valid moves
    '''
    vmoves = {}
    vmoves.update(self._getValidMoves(piece, piece.pieceRow, piece.pieceColumn, [], 1))
    vmoves.update(self._getValidMoves(piece, piece.pieceRow, piece.pieceColumn, [], 2))
    return vmoves

  def _getValidMoves(self, piece, row, col, jumpPath, stepSize):
    ''' this method takes in a row and col of where the piece is currently during the jump. It also takes a jumpPath so a king
    does not jump back to where it came from and to prevent jumping over the same piece twice.
    Finally a stepSize is provided: if it's 1 only short jumps are considered, if 2 then jump chains are considered
    '''
    up, down, left, right = [x + y * stepSize for x in [row, col] for y in [-1, +1]]

    moves = {}

    for testColumn in [left, right]:
      for testRow in [up, down]:
        if not self.canMoveTo(piece, row, col, testRow, testColumn, stepSize):
          continue
        
        if stepSize == 1:
          moves[testRow, testColumn] = []
        else:
          middleRow = (testRow + row) // 2
          middleColumn = (testColumn + col) // 2
          if (middleRow, middleColumn) in jumpPath:
              continue
          newJumpPath = jumpPath.copy()
          newJumpPath.append((middleRow, middleColumn))
          moves[(testRow, testColumn)] = newJumpPath
          # recursive call
          moves.update(self._getValidMoves(piece, testRow, testColumn, newJumpPath, stepSize))
    return moves

  def canMoveTo(self, piece, pieceRow, pieceColumn, testRow, testColumn, stepSize) -> bool:
    '''evaluates to True if boundaries are right and if current piece between start/end location is of different color'''
    if not (piece.king or testRow == pieceRow + piece.direction * stepSize):
      # invalid direction
      return False
    if not (0 <= testRow < self.rows and 0 <= testColumn < self.columns):
      # outside of board
      return False
    testLocation = self.checkPiece(testRow, testColumn)
    if testLocation != "//":
      # jump location not empty
      return False
    # all base obstacles have been overcome
    if stepSize == 2:
        middleRow = (pieceRow + testRow) // 2
        middleColumn = (pieceColumn + testColumn) // 2
        middlePiece = self.checkPiece(middleRow, middleColumn)
        if middlePiece == "//" or middlePiece.pieceColour == piece.pieceColour:
            return False
    
    return True

    #==================================================
    # End of Class
    #==================================================





  
class Piece:
  def __init__(self, row, col, colour, window):
    self.window = window
    self.kingMarker = py.transform.scale(py.image.load("images/marker.png"), (60, 56))
    self.width = self.height = 800
    self.rows = self.columns = 8
    self.squareSize = self.height // self.rows
    self.pieceRow = row
    self.pieceColumn = col
    self.pieceColour = colour
    self.king = False
    self.pieceDirection()
    self.x = 0
    self.y = 0
    self.spacing = 12
    self.border = 2
    self.pieceCalculatePosition()



  def pieceMove(self, r,c):
    self.pieceRow = r
    self.pieceColumn = c
    self.pieceCalculatePosition()

  def pieceDirection(self):
    if self.pieceColour == py.Color("red"):
      self.direction = -1
    else:
      self.direction = 1

  def pieceCalculatePosition(self):
    self.x = self.squareSize * self.pieceColumn + self.squareSize // 2
    self.y = self.squareSize * self.pieceRow + self.squareSize // 2

  def createKing(self):
    self.king = True
  
  def checkKing(self):
    if self.king:
      return True
    else:
      return False

  def drawPiece(self):
    radius = self.squareSize // 2 - self.spacing
    black = py.Color("black")
    py.draw.circle(self.window,black,(self.x,self.y), radius + self.border + 2)
    py.draw.circle(self.window,self.pieceColour,(self.x,self.y), radius + self.border)
    py.draw.circle(self.window,self.pieceColour,(self.x,self.y), radius)
    
    if self.king == True:
      self.window.blit(self.kingMarker,(self.x - self.kingMarker.get_width()//2,self.y - self.kingMarker.get_height()//2))

  def __repr__(self):
    return str(self.pieceColour)

class Logic:
  def __init__(self,window):
    self.chosen = None
    self.go = py.Color("red")
    self.vMoves = {}
    self.window = window
    self.classPlayerVsPlayer = PlayerVsPlayer()
    self.width = self.height = 800
    self.rows = self.columns = 8
    self.squareSize = self.height // self.rows
    self.moveCounter = 0
    self.classText = Text()


  def refreshScreen(self):
    self.classPlayerVsPlayer.renderBoard()
    self.drawValidMoves(self.vMoves)
    py.display.update()
  
  def reset(self):
    self.chosen = None
    self.go = py.Color("red")
    self.vMoves = {}
    self.window = window
    self.classPlayerVsPlayer = PlayerVsPlayer()
  
  def choose(self,r,c):
    '''
    Check if a piece has been chosen - then it will create the valid moves
    If piece has been previously chosen and it is a valid move, then the piece will be moved
    '''
    if self.chosen:
      ans = self._move(r,c)
      if not ans:
        self.chosen = None
        self.choose(r,c)
    
    
    piece = self.classPlayerVsPlayer.checkPiece(r,c)
    if piece != "//":
      if piece.pieceColour == self.go:
        self.chosen = piece
        self.vMoves = self.classPlayerVsPlayer.createValidMoves(piece)
        return True
    else:
      self.vMoves = {}
    return False
  
  def _move(self,r,c):
    '''
    Check if the critieria is fulfilled to move a piece
    Changes the turn
    '''
    piece = self.classPlayerVsPlayer.checkPiece(r,c)
    if self.chosen and piece == "//" and (r,c) in self.vMoves:
      self.moveCounter = self.moveCounter + 1
      self.classText.moveCounter(self.moveCounter)
      self.classPlayerVsPlayer.movePiece(self.chosen,r,c)
      removePiece = self.vMoves[(r,c)]
      if removePiece:
        self.classPlayerVsPlayer.removePiece(removePiece)
      self.changeGo()
      self.vMoves = {}
    else:
      return False
    return True
  
  def changeGo(self):
    '''
    Changes the turn and then check if it is a draw
    '''
    self.vMoves = {}
    if self.go == py.Color("red"):
      self.go = py.Color("white")
    else:
      self.go = py.Color("red")
    self.classPlayerVsPlayer.checkForNoValidMoves(self.go)

  def drawValidMoves(self, vmoves):  
    for move in vmoves:
      r, c = move
      py.draw.circle(self.window, py.Color("black"), (c * self.squareSize + self.squareSize//2, r * self.squareSize + self.squareSize // 2), 32)
      py.draw.circle(self.window, py.Color("green"), (c * self.squareSize + self.squareSize//2, r * self.squareSize + self.squareSize // 2), 30)

class Text:
  def __init__(self):
    self.width = 300
    self.height = 300
    self.colour = None
    self.space = str("")

  def pieceMoveText(self,piece, row, column):
    '''
    Prints the move in the text file and console
    '''
    if piece.pieceColour == py.Color("red"):
      self.colour = str("Red")
    elif piece.pieceColour == py.Color("white"):
      self.colour = str("White")
    else:
      self.colour = str("Empty Space")
    text = str(self.colour + " piece at (" + str(piece.pieceColumn + 1) + "," + str(8 - piece.pieceRow) + ") has moved to (" + str(column + 1) + "," + str(8 - row) + ")")
    print(text)
    self.writeTextFile(text)

  def pieceRemoveText(self,removePiece,piece):
    '''
    Prints how the piece was removed in the text file and console
    '''
    if piece.pieceColour == py.Color("red"):
      strRemovePiece = "Red"
    else:
      strRemovePiece = "White"
    text = str(strRemovePiece + " at (" + str(piece.pieceColumn + 1) + "," + str(8 - piece.pieceRow) + ") has been taken")
    print(text)
    self.writeTextFile(text)
  
  def moveCounter(self,counter):
    '''
    Prints how what move number it is
    '''
    text = ("Move " + str(counter) + ":")
    print("")
    print(text)
    self.writeTextFile(self.space)
    self.writeTextFile(text)
  
  def gameDraw(self, reason):
    '''
    Prints that the game is a draw and reason why
    '''
    print("")
    text = str("No one wins! Draw due to " + reason)
    print(text)
    self.writeTextFile(self.space)
    self.writeTextFile(text)
  
  def gameWin(self,reason,colourWinner):
    '''
    Prints that the game is a win and reason why
    '''
    text = str( colourWinner + " wins! (" + reason + ")")
    print(text)
    self.writeTextFile(self.space)
    self.writeTextFile(text)
    
  def createTextFile(self):
    '''
    If there is no "lastgame.text", the file will be created
    If there is a "lastgame.text" file, the file's content will be cleared
    '''
    try:
      textfile = open("lastgame.txt", "x")
    except:
      textfile = open("lastgame.txt","r+")
      textfile.truncate(0)
      textfile.close()
    
  def writeTextFile(self,text):
    textfile = open("lastgame.txt", "a")
    textfile.write(str(text + "\n"))
    textfile.close()


if __name__ == "__main__":
  pmain()

#Hide the space above move one by doing user name vs username