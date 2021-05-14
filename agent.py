
import time
from os import system
from time import sleep
import copy
class Agent:
    def __init__(self, world):
        self.world = world
        self.knowledge = [[[] for i in range(self.world.num_cols)] for j in range(self.world.num_rows)]
        self.knowledge[self.world.agent_row][self.world.agent_col].append('A')
        self.stinks = 0
        self.poc = [[self.world.agent_row, self.world.agent_col]]
        self.visitcells()
        self.world.cave_entrance_row = self.world.agent_row
        self.world.cave_entrance_col = self.world.agent_col
        self.found_gold = False 
        self.exited = False
        ch='u'
        if self.world.agent_row==0:
            ch='d'

        print("\t\tOriginal Grid\n")
        self.world.printworld()
        print("\n\n\t\tAgent Map")
        self.printworld(ch)
        



    def printworld(self,dir):
        for i in range(self.world.num_rows-1,-1,-1):
            for j in range(self.world.num_cols):
                self.printTile ( i, j ,dir)
            print("\n")
             
 

    def printTile ( self, i, j ,dir):
        printer = ""
        
        
        if 'A' in self.knowledge[i][j]:
            
            if dir == "r":
                printer += ">"
            
            elif dir == "d":
                printer += "^"
            
            elif dir == "l":
                printer += "<"
            
            elif dir == "u":
                printer += "v"
        
        if 'W' in self.knowledge[i][j]:printer += "W"
                    
        if 'P' in self.knowledge[i][j]:printer += "P"
                    
        if 'B' in self.knowledge[i][j]:printer += "B"
                    
        if 'S' in self.knowledge[i][j]:printer += "S"
                    
        if 'G' in self.knowledge[i][j]:printer += "G"
        if '.' in self.knowledge[i][j]:printer +="."
                    


            
        if printer=="":
             printer += "_"
        
        print(printer.rjust(8), end="")

    def printagain(self,lm):
                  time.sleep(0.5)
                  system('cls') 
                  print("\t\tOriginal Grid\n")
                  self.world.printworld()
                  print("\n\n\t\tAgent Map") 
                  self.printworld(lm)

    def goback(self,lm):
        
        
        if len(self.poc)==0:
            print("Agent can't find the path to gold")
            exit()
      
        else:
           if self.world.agent_row-1 == self.poc[-1][0]:
              if lm=='d':
                  self.printagain('r')
                  self.printagain('u')
              elif lm=='r' or lm=='l':
                  self.printagain('u')



                    
              self.move('u')
           if self.world.agent_row+1 == self.poc[-1][0]:
              if lm=='u':
                  self.printagain('r')
                  self.printagain('d')
              elif lm=='r' or lm=='l':
                      self.printagain('d')   
              self.move('d')
           if self.world.agent_col+1 ==  self.poc[-1][1]:
              if lm=='l':
                   self.printagain('u')
                   self.printagain('r')
              elif lm=='d' or lm=='u':
                      self.printagain('r')
              self.move('r')
           if self.world.agent_col-1 ==  self.poc[-1][1]:
              if lm=='r':
                   self.printagain('d')
                   self.printagain('l')
              elif lm=='u' or lm=='d':
                      self.printagain('l')
              self.move('l')
        
           del self.poc[-1]


    def start(self):
        last_move = ''
        already_moved = False
        while self.found_gold == False:

            if self.found_gold == True:
                break

            try:
                if  '.' not in self.knowledge[self.world.agent_row-1][self.world.agent_col] and self.checkmove(self.world.agent_row-1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('u'):
                            already_moved = True
                            last_move='u'

                   
            except IndexError:
                pass

            try:
                if '.' not in self.knowledge[self.world.agent_row][self.world.agent_col+1] and self.checkmove(self.world.agent_row, self.world.agent_col+1):
                    if already_moved == False:
                        if self.move('r'):
                            already_moved = True
                            last_move='r'
                    
            except IndexError:
                pass

            try:
                if '.' not in self.knowledge[self.world.agent_row+1][self.world.agent_col] and self.checkmove(self.world.agent_row+1, self.world.agent_col):
                    if already_moved == False:
                        if self.move('d'):
                            already_moved = True
                            last_move='d'
                    
            except IndexError:
                pass

            try:
                if '.' not in self.knowledge[self.world.agent_row][self.world.agent_col-1] and self.checkmove(self.world.agent_row, self.world.agent_col-1):
                    if already_moved == False:
                        if self.move('l'):
                            already_moved = True
                            last_move='l'
                    
            except IndexError:
                pass

            

            if already_moved == False:
                self.goback(last_move)


            already_moved = False




    def move(self, direction):
        
        
        successful_move = False
        if direction == 'u':
            if self.checkmove(self.world.agent_row-1, self.world.agent_col):
                successful_move = self.move_up()
        if direction == 'r':
            if self.checkmove(self.world.agent_row, self.world.agent_col+1):
                successful_move = self.move_right()
        if direction == 'd':
            if self.checkmove(self.world.agent_row+1, self.world.agent_col):
                successful_move = self.move_down()
        if direction == 'l':
            if self.checkmove(self.world.agent_row, self.world.agent_col-1):
                successful_move = self.move_left()

        if successful_move:
            self.add_indicators_to_KB()
            self.visitcells()
            self.predict_wumpus()
            self.predict_pits()
            self.clean_predictions()
            self.confirm_wumpus_knowledge()


            if 'G' in self.knowledge[self.world.agent_row][self.world.agent_col]:
                
                self.found_gold = True

            if self.found_gold == False:
                self.poc.append([self.world.agent_row, self.world.agent_col])


        
            time.sleep(1)
        
        system('cls') 
        print("\t\tOriginal Grid\n")
        self.world.printworld()
        print("\n\n\t\tAgent Map")    
        self.printworld(direction)    

        return successful_move


    def add_indicators_to_KB(self):
        if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'B' not in self.knowledge[self.world.agent_row][self.world.agent_col]:
                self.knowledge[self.world.agent_row][self.world.agent_col].append('B')
        if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'S' not in self.knowledge[self.world.agent_row][self.world.agent_col]:
                self.knowledge[self.world.agent_row][self.world.agent_col].append('S')
        if 'G' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'G' not in self.knowledge[self.world.agent_row][self.world.agent_col]:
                self.knowledge[self.world.agent_row][self.world.agent_col].append('G')
        if 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'P' not in self.knowledge[self.world.agent_row][self.world.agent_col]:
                self.knowledge[self.world.agent_row][self.world.agent_col].append('P')
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            if 'W' not in self.knowledge[self.world.agent_row][self.world.agent_col]:
                self.knowledge[self.world.agent_row][self.world.agent_col].append('W')


    def predict_pits(self):
        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'P' not in self.knowledge[self.world.agent_row-1][self.world.agent_col]:
                            self.knowledge[self.world.agent_row-1][self.world.agent_col].append('P')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.num_cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'P' not in self.knowledge[self.world.agent_row][self.world.agent_col+1]:
                            self.knowledge[self.world.agent_row][self.world.agent_col+1].append('P')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.num_rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'P' not in self.knowledge[self.world.agent_row+1][self.world.agent_col]:
                            self.knowledge[self.world.agent_row+1][self.world.agent_col].append('P')
        except IndexError:
            pass

        try:
            if 'B' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'P' not in self.knowledge[self.world.agent_row][self.world.agent_col-1]:
                            self.knowledge[self.world.agent_row][self.world.agent_col-1].append('P')
        except IndexError:
            pass


    def predict_wumpus(self):
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row-1][self.world.agent_col]:
                        if 'W' not in self.knowledge[self.world.agent_row-1][self.world.agent_col]:
                            self.knowledge[self.world.agent_row-1][self.world.agent_col].append('W')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col+1 < self.world.num_cols:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col+1]:
                        if 'W' not in self.knowledge[self.world.agent_row][self.world.agent_col+1]:
                            self.knowledge[self.world.agent_row][self.world.agent_col+1].append('W')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_row+1 < self.world.num_rows:
                    if '.' not in self.world.world[self.world.agent_row+1][self.world.agent_col]:
                        if 'W' not in self.knowledge[self.world.agent_row+1][self.world.agent_col]:
                            self.knowledge[self.world.agent_row+1][self.world.agent_col].append('W')
        except IndexError:
            pass
        try:
            if 'S' in self.world.world[self.world.agent_row][self.world.agent_col]:
                if self.world.agent_col-1 >= 0:
                    if '.' not in self.world.world[self.world.agent_row][self.world.agent_col-1]:
                        if 'W' not in self.knowledge[self.world.agent_row][self.world.agent_col-1]:
                            self.knowledge[self.world.agent_row][self.world.agent_col-1].append('W')
        except IndexError:
            pass


    def clean_predictions(self):
        self.stinks = 0
        self.newlist = copy.copy(self.knowledge)
        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):

                if 'S' in self.knowledge[i][j]:
                    self.stinks += 1
                if 'W' in self.knowledge[i][j]:
                    try:
                        if i-1 >= 0:
                            if '.' in self.knowledge[i-1][j]:
                                if 'S' not in self.knowledge[i-1][j]:
                                    self.newlist[i][j].remove('W')
                                    self.newlist[i][j].append(' ')
                                    self.knowledge=copy.copy(self.newlist)
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.num_cols:
                            if '.' in self.knowledge[i][j+1]:
                                if 'S' not in self.knowledge[i][j+1]:
                                    self.newlist[i][j].remove('W')
                                    self.newlist[i][j].append(' ')
                                    self.knowledge=copy.copy(self.newlist)

                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.num_rows:
                            if '.' in self.knowledge[i+1][j]:
                                if 'S' not in self.knowledge[i+1][j]:
                                    self.newlist[i][j].remove('W')
                                    self.newlist[i][j].append(' ')
                                    self.knowledge=copy.copy(self.newlist)

                                    
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if '.' in self.knowledge[i][j-1]:
                                if 'S' not in self.knowledge[i][j-1]:
                                    self.newlist[i][j].remove('W')
                                    self.newlist[i][j].append(' ')                                   
                                    self.knowledge=copy.copy(self.newlist)

                    except IndexError:
                        pass

                if 'P' in self.knowledge[i][j]:
                    try:
                        if i-1 >= 0:
                            if '.' in self.knowledge[i-1][j]:
                                if 'B' not in self.knowledge[i-1][j]:
                                    self.newlist[i][j].remove('P')
                                    self.newlist[i][j].append(' ')
                                    self.knowledge=copy.copy(self.newlist)

                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.num_cols:
                            if '.' in self.knowledge[i][j+1]:
                                if 'B' not in self.knowledge[i][j+1]:
                                    self.newlist[i][j].remove('P')
                                    self.newlist[i][j].append(' ')
                                    self.knowledge=copy.copy(self.newlist)
                                    
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.num_rows:
                            if '.' in self.knowledge[i+1][j]:
                                if 'B' not in self.knowledge[i+1][j]:
                                    self.newlist[i][j].remove('P')
                                    self.newlist[i][j].append(' ')
                                    self.knowledge=copy.copy(self.newlist)
                                    
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if '.' in self.knowledge[i][j-1]:
                                if 'B' not in self.knowledge[i][j-1]:
                                    self.newlist[i][j].remove('P')
                                    self.newlist[i][j].append(' ')
                                    self.knowledge=copy.copy(self.newlist)
                                    
                    except IndexError:
                        pass


    def confirm_wumpus_knowledge(self):
        self.newlis = copy.copy(self.knowledge)
        for i in range(self.world.num_rows):
            for j in range(self.world.num_cols):
                if 'W' in self.knowledge[i][j]:
                    stinks_around = 0
                    try:
                        if i-1 >= 0:
                            if 'S' in self.knowledge[i-1][j]:
                                stinks_around += 1
                    except IndexError:
                        pass
                    try:
                        if j+1 < self.world.num_cols:
                            if 'S' in self.knowledge[i][j+1]:
                                stinks_around += 1
                    except IndexError:
                        pass
                    try:
                        if i+1 < self.world.num_rows:
                            if 'S' in self.knowledge[i+1][j]:
                                stinks_around += 1
                    except IndexError:
                        pass
                    try:
                        if j-1 >= 0:
                            if 'S' in self.knowledge[i][j-1]:
                                stinks_around += 1
                    except IndexError:
                        pass

                    if stinks_around < self.stinks:
                        self.newlis[i][j].remove('W')
                        self.newlis[i][j].append(' ')
                        self.knowledge=copy.copy(self.newlis)


    def checkmove(self, row, col):
        
        try:
            if 'W' in self.knowledge[row][col]:
                
                return False
        except IndexError:
            pass
        try:
            if 'P' in self.knowledge[row][col]:
                
                return False
        except IndexError:
            pass

        return True



    def move_up(self):
        try:
            if self.world.agent_row-1 >= 0:
                self.remove_agent()
                self.world.agent_row -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_right(self):
        try:
            if self.world.agent_col+1 < self.world.num_cols:
                self.remove_agent()
                self.world.agent_col += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_down(self):
        try:
            if self.world.agent_row+1 < self.world.num_rows:
                self.remove_agent()
                self.world.agent_row += 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def move_left(self):
        try:
            if self.world.agent_col-1 >= 0:
                self.remove_agent()
                self.world.agent_col -= 1
                self.add_agent()
                return True
            else:
                return False
        except IndexError:
            return False


    def remove_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].remove('A')
        self.knowledge[self.world.agent_row][self.world.agent_col].remove('A')


    def add_agent(self):
        self.world.world[self.world.agent_row][self.world.agent_col].append('A')
        self.knowledge[self.world.agent_row][self.world.agent_col].append('A')


    def visitcells(self):
        if '.' not in self.knowledge[self.world.agent_row][self.world.agent_col]:
            self.world.world[self.world.agent_row][self.world.agent_col].append('.')
            self.knowledge[self.world.agent_row][self.world.agent_col].append('.')


    def is_dead(self):
        if 'W' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have been killed by the Wumpus!")
            return True
        elif 'P' in self.world.world[self.world.agent_row][self.world.agent_col]:
            print("You have fallen in a pit!")
            return True
        else:
            return False


