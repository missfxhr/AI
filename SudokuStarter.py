#!/usr/bin/env python
import struct, string, math, heapq

class SudokuBoard:
    """This will be the sudoku board game object your player will manipulate."""

    def __init__(self, size, board):
        """the constructor for the SudokuBoard"""
        subsize = int(math.sqrt(size))
        self.BoardSize = size #the size of the board
        self.CurrentGameBoard= board #the current state of the game board
        self.BoardSubSize = subsize
        self.fullSet = set()
        self.rowSet = {i:set()for i in range(size)}
        self.colSet = {i:set() for i in range(size)}
        self.gridSet = {(i,j):set() for i in range(subsize) for j in range(subsize)}
        self.cellList = {(i,j):set() for i in range(size) for j in range(size)}
        #forward table initialization
        self.forwardTable = {(i,j):list() for i in range(size) for j in range(size)}
        for row in range(size):
            for col in range(size): 
                self.forwardTable[(row,col)] = (-1,-1)

        for x in range(1,size+1):
            self.fullSet.add(x)
        for row in range(size):
            for col in range(size):
                if self.CurrentGameBoard[row][col] != 0:
                    self.rowSet[row].add(self.CurrentGameBoard[row][col])
                    self.colSet[col].add(self.CurrentGameBoard[row][col])
                    self.gridSet[(row//subsize,col//subsize)].add(self.CurrentGameBoard[row][col])
        
        for row in range(size):
            for col in range(size):
                if self.CurrentGameBoard[row][col] == 0:
                    for x in range(1,size+1):
                        if not (x in self.rowSet[row] or x in self.colSet[col] or x in self.gridSet[(row//subsize,col//subsize)]): 
                            self.cellList[(row,col)].add(x)
                else:
                    for x in range(0,size+1):
                        self.cellList[(row,col)].add(x)

    def generateLegalNumbers(self,row,col):
        subsize = self.BoardSubSize
        result = self.fullSet - (self.rowSet[row] | self.colSet[col] | self.gridSet[(row//subsize,col//subsize)])
        return result

    def generatePairedLegalNumbers(self,row,col,forward_checking):
        size = self.BoardSize
        subsize = self.BoardSubSize
        moveList = []
        if not forward_checking:
            for x in range(1,size+1):
                if not (x in self.rowSet[row] or x in self.colSet[col] or x in self.gridSet[(row//subsize,col//subsize)]):
                    self.setCell(x,row,col,True)
                    result = 0
                    for colNum in range(size):
                        if self.CurrentGameBoard[row][colNum] == 0:
                            result = result + len(self.generateLegalNumbers(row,colNum))
                    for rowNum in range(size):
                        if self.CurrentGameBoard[rowNum][col] == 0:
                            result = result + len(self.generateLegalNumbers(rowNum,col))
                    for gridNum in range(size):
                        gridRowNum = (row//subsize)*subsize+gridNum//subsize
                        gridColNum = (col//subsize)*subsize+gridNum%subsize
                        if self.CurrentGameBoard[gridRowNum][gridColNum] == 0 and gridRowNum != row and gridColNum != col:
                            result = result + len(self.generateLegalNumbers(gridRowNum,gridColNum))
                    heapq.heappush(moveList,(-result,x))
                    self.setCell(x,row,col,False)
        else:
            for x in self.cellList[(row,col)]:
                self.setCell(x,row,col,True)
                self.updateCellList(row,col)
                result = 0
                for colNum in range(size):
                    if self.CurrentGameBoard[row][colNum] == 0:
                        result = result + len(self.cellList[(row,colNum)])
                for rowNum in range(size):
                    if self.CurrentGameBoard[rowNum][col] == 0:
                        result = result + len(self.cellList[(rowNum,col)])
                for gridNum in range(size):
                    gridRowNum = (row//subsize)*subsize+gridNum//subsize
                    gridColNum = (col//subsize)*subsize+gridNum%subsize
                    if self.CurrentGameBoard[gridRowNum][gridColNum] == 0 and gridRowNum != row and gridColNum != col:
                        result = result + len(self.cellList[(gridRowNum,gridColNum)])
                heapq.heappush(moveList,(-result,x))
                self.setCell(x,row,col,False)
                self.updateCellList(row,col)
        return moveList



    def setCell(self,x,row,col,isAdd):
        subsize = self.BoardSubSize
        if isAdd:
            self.CurrentGameBoard[row][col] = x
            self.rowSet[row].add(x)
            self.colSet[col].add(x)
            self.gridSet[(row//subsize,col//subsize)].add(x)
        else:
            self.CurrentGameBoard[row][col] = 0
            self.rowSet[row].remove(x)
            self.colSet[col].remove(x)
            self.gridSet[(row//subsize,col//subsize)].remove(x)

    def updateCellList(self,row,col):
        size = self.BoardSize
        subsize = self.BoardSubSize
        result = True
        # for this row
        for colNum in range(size):
            if self.CurrentGameBoard[row][colNum] == 0:
                self.cellList[(row,colNum)] = self.fullSet - (self.rowSet[row] | self.colSet[colNum] | self.gridSet[(row//subsize,colNum//subsize)])
                result = result and (len(self.cellList[(row,colNum)]) != 0)

        for rowNum in range(size):
            if self.CurrentGameBoard[rowNum][col] == 0:
                self.cellList[(rowNum,col)] = self.fullSet - (self.rowSet[rowNum] | self.colSet[col] | self.gridSet[(rowNum//subsize,col//subsize)])
                result = result and (len(self.cellList[(rowNum,col)]) != 0)

        for gridNum in range(size):
            gridRowNum = (row//subsize)*subsize+gridNum//subsize
            gridColNum = (col//subsize)*subsize+gridNum%subsize
            if self.CurrentGameBoard[gridRowNum][gridColNum] == 0 and gridRowNum != row and gridColNum != col:
                self.cellList[(gridRowNum, gridColNum)] = self.fullSet - (self.rowSet[gridRowNum] | self.colSet[gridColNum] | self.gridSet[(row//subsize,col//subsize)])
                result = result and (len(self.cellList[(gridRowNum,gridColNum)]) != 0)      
        return result

    ''' 
    def cellListUpdateNum(self):
        size = self.BoardSize
        subsize = self.BoardSubSize
        result = 0
        for colNum in range(size):
            if self.CurrentGameBoard[row][colNum] == 0:
                temp = len(self.cellList([(row,colNum)]))
                self.cellList[(row,colNum)] = self.fullSet - (self.rowSet[row] | self.colSet[colNum] | self.gridSet[(row//subsize,colNum//subsize)])
                result += (temp - len(self.cellList([(row,colNum)]))) 

        for rowNum in range(size):
            if self.CurrentGameBoard[rowNum][col] == 0:
                temp = len(self.cellList([(rowNum,col)]))
                self.cellList[(rowNum,col)] = self.fullSet - (self.rowSet[rowNum] | self.colSet[col] | self.gridSet[(rowNum//subsize,col//subsize)])
                result += (temp - len(self.cellList([(rowNum,col)]))) 

        for gridNum in range(size):
            gridRowNum = (row//subsize)*subsize+gridNum//subsize
            gridColNum = (col//subsize)*subsize+gridNum%subsize
            if self.CurrentGameBoard[gridRowNum][gridColNum] == 0:
                temp = len(self.cellList([(gridRowNum,gridColNum)]))
                self.cellList[(gridRowNum, gridColNum)] = self.fullSet - (self.rowSet[gridRowNum] | self.colSet[gridColNum] | self.gridSet[(row//subsize,col//subsize)])
                result += (temp - len(self.cellList([(gridRowNum,gridColNum)]))) 
        return result
    '''
    
    def allLegalNumbers(self):
        size = self.BoardSize
        subsize = self.BoardSubSize
        result = 0
        for row in range(size):
            for col in range(size):
                if self.CurrentGameBoard[row][col] == 0:
                    result += self.cellList[(row,col)]
        return result


    def set_value(self, row, col, value):
        """This function will create a new sudoku board object with the input
        value placed on the GameBoard row and col are both zero-indexed"""

        #add the value to the appropriate position on the board
        self.CurrentGameBoard[row][col]=value
        #return a new board of the same size with the value added
        return SudokuBoard(self.BoardSize, self.CurrentGameBoard)


    def print_board(self):
        """Prints the current game board. Leaves unassigned spots blank."""
        div = int(math.sqrt(self.BoardSize))
        dash = ""
        space = ""
        line = "+"
        sep = "|"
        for i in range(div):
            dash += "----"
            space += "    "
        for i in range(div):
            line += dash + "+"
            sep += space + "|"
        for i in range(-1, self.BoardSize):
            if i != -1:
                print "|",
                for j in range(self.BoardSize):
                    if self.CurrentGameBoard[i][j] > 9:
                        print self.CurrentGameBoard[i][j],
                    elif self.CurrentGameBoard[i][j] > 0:
                        print "", self.CurrentGameBoard[i][j],
                    else:
                        print "  ",
                    if (j+1 != self.BoardSize):
                        if ((j+1)//div != j/div):
                            print "|",
                        else:
                            print "",
                    else:
                        print "|"
            if ((i+1)//div != i/div):
                print line
            else:
                print sep

def parse_file(filename):
    """Parses a sudoku text file into a BoardSize, and a 2d array which holds
    the value of each cell. Array elements holding a 0 are considered to be
    empty."""

    f = open(filename, 'r')
    BoardSize = int( f.readline())
    NumVals = int(f.readline())

    #initialize a blank board
    board= [ [ 0 for i in range(BoardSize) ] for j in range(BoardSize) ]

    #populate the board with initial values
    for i in range(NumVals):
        line = f.readline()
        chars = line.split()
        row = int(chars[0])
        col = int(chars[1])
        val = int(chars[2])
        board[row-1][col-1]=val

    return board
    
def is_complete(sudoku_board):
    """Takes in a sudoku board and tests to see if it has been filled in
    correctly."""
    BoardArray = sudoku_board.CurrentGameBoard
    size = len(BoardArray)
    subsquare = int(math.sqrt(size))

    #check each cell on the board for a 0, or if the value of the cell
    #is present elsewhere within the same row, column, or square
    for row in range(size):
        for col in range(size):
            if BoardArray[row][col]==0:
                return False
            for i in range(size):
                if ((BoardArray[row][i] == BoardArray[row][col]) and i != col):
                    return False
                if ((BoardArray[i][col] == BoardArray[row][col]) and i != row):
                    return False
            #determine which square the cell is in
            SquareRow = row // subsquare
            SquareCol = col // subsquare
            for i in range(subsquare):
                for j in range(subsquare):
                    if((BoardArray[SquareRow*subsquare+i][SquareCol*subsquare+j] == BoardArray[row][col]) and (SquareRow*subsquare + i != row) and (SquareCol*subsquare + j != col)):
                        return False
    return True

def init_board(file_name):
    """Creates a SudokuBoard object initialized with values from a text file"""
    board = parse_file(file_name)
    return SudokuBoard(len(board), board)

def solve(initial_board, forward_checking = False, MRV = False, MCV = False, LCV = False):
    """Takes an initial SudokuBoard and solves it using back tracking, and zero
    or more of the heuristics and constraint propagation methods (determined by
    arguments). Returns the resulting board solution. """
    
    '''
    initializing hashset for starting board
    '''

    size = initial_board.BoardSize
    subsize = int(math.sqrt(size))
    count = [0]
    
    #if not forward_checking: 
        #solveBackTracking(initial_board,0,0,rowSet,colSet,gridSet)
    #else:  
    if MRV == False and MCV == False:
        solveSimple(initial_board,0,0,forward_checking,LCV,count)
        print count[0]
    elif MRV == True and MCV == False:
        solveMRV(initial_board,forward_checking,LCV,count)
        print count[0]
    elif MRV == False and MCV == True:
        solveMCV(initial_board,0,0,forward_checking,LCV,count)
        print count[0]
    else:
        print "MRV and MCV cannot be True at the same time!"

    #print "Your code will solve the initial_board here!"
    #print "Remember to return the final board (the SudokuBoard object)."
    #print "I'm simply returning initial_board for demonstration purposes."
    return initial_board


def solveSimple(board,row,col,forward_checking,LCV, count):
    #count[0] += 1
    print str(count) + "\r",
    size = board.BoardSize
    subsize = board.BoardSubSize
    if row==size:
        #board.print_board()
        return True
    if not forward_checking:
        if board.CurrentGameBoard[row][col] == 0: 
            if not LCV:
                for x in range(1,size+1):
                    count[0] += 1
                    if not (x in board.rowSet[row] or x in board.colSet[col] or x in board.gridSet[(row//subsize,col//subsize)]):
                        board.setCell(x,row,col,True)
                        if solveSimple(board,row+(col+1)//size,(col+1)%size,forward_checking,LCV,count):
                            return True
                        else:
                            board.setCell(x,row,col,False)
                return False
            else:
                pairedNumbers = board.generatePairedLegalNumbers(row,col,forward_checking)
                while(pairedNumbers):
                    count[0] += 1
                    x = (heapq.heappop(pairedNumbers))[1]
                    board.setCell(x,row,col,True)
                    if solveSimple(board,row+(col+1)//size,(col+1)%size,forward_checking,LCV,count):
                        return True
                    else:
                        board.setCell(x,row,col,False)
                return False
        else:
            return solveSimple(board,row+(col+1)//size,(col+1)%size,forward_checking,LCV,count) 
    else:
        if board.CurrentGameBoard[row][col] == 0:
            if not LCV:
                legalNumbers = set(board.cellList[(row,col)])
                for x in legalNumbers:
                    count[0] += 1
                    board.setCell(x,row,col,True)
                    if board.updateCellList(row,col) and solveSimple(board,row+(col+1)//size,(col+1)%size,forward_checking,LCV,count):
                            return True
                    else:
                        board.setCell(x,row,col,False)
                        board.updateCellList(row,col)
                return False
            else:
                pairedNumbers = board.generatePairedLegalNumbers(row,col,forward_checking)
                while(pairedNumbers):
                    count[0] += 1
                    x = (heapq.heappop(pairedNumbers))[1]
                    board.setCell(x,row,col,True)
                    if board.updateCellList(row,col) and solveSimple(board,row+(col+1)//size,(col+1)%size,forward_checking,LCV,count):
                            return True
                    else:
                        board.setCell(x,row,col,False)
                        board.updateCellList(row,col)
                return False
        else:
            return solveSimple(board,row+(col+1)//size,(col+1)%size,forward_checking,LCV,count)


def solveMRV(board, forward_checking,LCV,count):
    print str(count) + "\r",
    size = board.BoardSize
    minLen = size
    subsize = board.BoardSubSize
    # no forward checking method:
    if forward_checking != True:
        for row in range(0, size): 
            for col in range(0, size):
                if board.CurrentGameBoard[row][col] == 0 and len(board.generateLegalNumbers(row, col)) < minLen:
                    minLen = len(board.generateLegalNumbers(row, col))
                    minRow = row
                    minCol = col
        if minLen == size:
            #board.print_board()
            return True
        if not LCV:
            for x in range(1,size+1):
                count[0] += 1
                if not (x in board.rowSet[minRow] or x in board.colSet[minCol] or x in board.gridSet[(minRow//subsize,minCol//subsize)]): 
                    board.setCell(x,minRow,minCol,True)
                    if solveMRV(board, forward_checking,LCV,count):
                        return True
                    else:
                        board.setCell(x,minRow,minCol,False)
            return False
        else:
            pairedNumbers = board.generatePairedLegalNumbers(minRow,minCol,forward_checking)
            while(pairedNumbers):
                count[0] += 1
                x = (heapq.heappop(pairedNumbers))[1]
                board.setCell(x,minRow,minCol,True)
                if solveMRV(board,forward_checking,LCV,count):
                    return True
                else:
                    board.setCell(x,minRow,minCol,False)
            return False
    else:
        for row in range(0, size): 
            for col in range(0, size):
                if board.CurrentGameBoard[row][col] == 0 and len(board.cellList[(row,col)]) < minLen:
                    minLen = len(board.cellList[(row,col)])
                    minRow = row
                    minCol = col
        if minLen == size:
            #board.print_board()
            return True
        if not LCV:
            legalNumbers = set(board.cellList[(minRow,minCol)])
            for x in legalNumbers:
                count[0] += 1
                board.setCell(x,minRow,minCol,True)
                if board.updateCellList(minRow,minCol) and solveMRV(board, forward_checking,LCV,count):
                    return True
                else:
                    board.setCell(x,minRow,minCol,False)
                    board.updateCellList(minRow,minCol)
            return False
        else:
            pairedNumbers = board.generatePairedLegalNumbers(minRow,minCol,forward_checking)
            while(pairedNumbers):
                count[0] += 1
                x = (heapq.heappop(pairedNumbers))[1]
                board.setCell(x,minRow,minCol,True)
                if board.updateCellList(minRow,minCol) and solveMRV(board,forward_checking,LCV,count):
                    return True
                else:
                    board.setCell(x,minRow,minCol,False)
                    board.updateCellList(minRow,minCol)
            return False            


def solveMCV(board, p_row, p_col,forward_checking,LCV,count):
    print str(count) + "\r",
    size = board.BoardSize
    maxCon = 0
    maxRow = -1
    maxCol = -1
    subsize = int(math.sqrt(size))
    if board.forwardTable[(p_row,p_col)] == (-1,-1):
        for row in range(0, size): 
            for col in range(0, size):
                if board.CurrentGameBoard[row][col] == 0:
                    tempCon = 3 * size - len(board.rowSet[row]) - len(board.colSet[col]) - len(board.gridSet[(row//subsize,col//subsize)])
                    gridRowNum = (row//subsize)*subsize
                    gridColNum = (col//subsize)*subsize
                    for gridR in range(subsize):
                        if board.CurrentGameBoard[gridR+gridRowNum][col] == 0:
                            tempCon -= 1
                    for gridC in range(subsize):
                        if board.CurrentGameBoard[row][gridC+gridColNum] == 0:
                            tempCon -= 1
                    if tempCon > maxCon:
                        maxCon = tempCon
                        maxRow = row
                        maxCol = col
        board.forwardTable[(p_row,p_col)] = (maxRow,maxCol)
    else:
        maxRow = board.forwardTable[(p_row,p_col)][0]
        maxCol = board.forwardTable[(p_row,p_col)][1]
        maxCon = 1

    if maxCon == 0:
        #board.print_board()
        return True

    if forward_checking != True:
        if not LCV:
            for x in range(1,size+1):
                count[0] += 1
                if not (x in board.rowSet[maxRow] or x in board.colSet[maxCol] or x in board.gridSet[(maxRow//subsize,maxCol//subsize)]): 
                    board.setCell(x,maxRow,maxCol,True)

                    if solveMCV(board,maxRow,maxCol, forward_checking, LCV,count):

                        return True
                    else:
                        board.setCell(x,maxRow,maxCol,False)
            return False
        else:
            pairedNumbers = board.generatePairedLegalNumbers(maxRow,maxCol,forward_checking)
            while(pairedNumbers):
                count[0] += 1
                x = (heapq.heappop(pairedNumbers))[1]           
                board.setCell(x,maxRow,maxCol,True)

                if solveMCV(board,maxRow,maxCol, forward_checking, LCV,count):

                    return True
                else:
                    board.setCell(x,maxRow,maxCol,False)
            return False
    else:
        if not LCV:
            legalNumbers = set(board.cellList[(maxRow,maxCol)])
            for x in legalNumbers:
                count[0] += 1
                board.setCell(x,maxRow,maxCol,True)

                if board.updateCellList(maxRow,maxCol) and solveMCV(board, maxRow,maxCol,forward_checking, LCV,count):

                    return True
                else:
                    board.setCell(x,maxRow,maxCol,False)
                    board.updateCellList(maxRow,maxCol)
            return False
        else:
            pairedNumbers = board.generatePairedLegalNumbers(maxRow,maxCol,forward_checking)
            while(pairedNumbers):
                count[0] += 1
                x = (heapq.heappop(pairedNumbers))[1]           
                board.setCell(x,maxRow,maxCol,True)

                if board.updateCellList(maxRow,maxCol) and solveMCV(board,maxRow,maxCol, forward_checking, LCV,count):

                    return True
                else:
                    board.setCell(x,maxRow,maxCol,False)
                    board.updateCellList(maxRow,maxCol)
            return False


