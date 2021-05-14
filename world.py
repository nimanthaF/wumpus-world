
import random
from random import choice
class World:
    def __init__(self):
        self.world = [[]]
        self.num_rows = 0
        self.num_cols = 0

        self.agent_row = 0
        self.agent_col = 0
        self.cave_entrance_row = 0
        self.cave_entrance_col = 0


    def generate_world(self):


        self.num_rows = 5
        self.num_cols = 5
        self.world = [[[] for i in range(self.num_cols)] for j in range(self.num_rows)]

        self.agent_row = choice([0, 4])
        self.agent_col = choice([4, 0])

        self.world[self.agent_row][self.agent_col].append('A')

        xvalues=[]
        yvalues=[]
            
        def generateNo():
                x=random.randrange(0, 5)
                y=random.randrange(0, 5)
                
                if (x == 0 and y == 0) or (x == 0 and y == 4) or (x == 4 and y == 0) or (x == 4 and y == 4):
                    return generateNo()

                elif (self.agent_col == 0 and self.agent_row == 0):
                    if (x == 0 and y == 1) or (x == 1 and y == 0):  
                       return generateNo()
                    else:
                        value=[x,y]                    
                        return value   
                         
                elif (self.agent_col==4 and self.agent_row==0):
                    if (x==3 and y==0)or(x==4 and y==1):  
                        return generateNo()
                    else:
                         value=[x,y]                    
                         return value    
                elif (self.agent_col==0 and self.agent_row==4):
                    if (x==0 and y==3)or(x==1 and y==4):  
                        return generateNo() 
                    else:
                         value=[x,y]                    
                         return value    
                elif (self.agent_col==4 and self.agent_row==4):
                    if (x==4 and y==3)or(x==3 and y==4):  
                        return generateNo() 
                    else:
                         value=[x,y]                    
                         return value    

                else:
                     value=[x,y]                    
                     return value


        for o in range(7):
                i=1
                while (i==1):

                    value=generateNo()
                    if(o==0):
                        
                        i=0
                            
                    else:
                        for v in range(len(xvalues)):
                            if (value[0]==xvalues[v]and value[1]==yvalues[v]):
                                i=1
                                break
                            else:
                                i=0 

                xvalues.append(value[0])
                yvalues.append(value[1])
                if(o<5):
                  # Generate pits
                 self.world[value[1]][value[0]].append('P')
                elif(o==5):
                    # Generate wumpus
                    self.world[value[1]][value[0]].append('W')
                else:
                    # Generate Gold
                    self.world[value[1]][value[0]].append('G')


        

        self.indicators()
        print("\t\tOriginal Grig\n\n")
        self.printworld()
        print("\n\n")

    def printworld ( self ):
            for r in range (4,-1,-1):
                for c in range (5):
                   self.printTitle ( c, r )
                print("")
                print("")

    def printTitle ( self, j, i ):
        printer = ""
        
        
        if 'A' in self.world[i][j]:printer += "A"
        
        if 'W' in self.world[i][j]:printer += "W"
                    
        if 'P' in self.world[i][j]:printer += "P"
                    
        if 'B' in self.world[i][j]:printer += "B"
                    
        if 'S' in self.world[i][j]:printer += "S"
                    
        if 'G' in self.world[i][j]:printer += "G"
                    
        if printer=="":
             printer += "_"
        
        print(printer.rjust(8), end="")

    def indicators(self):

        for i in range(self.num_rows):
            for j in range(self.num_cols):
                for k in range(len(self.world[i][j])):

                    if self.world[i][j][k] == 'W':

                        try:
                            if i-1 >= 0:
                                if 'S' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('S')
                        except IndexError:
                            pass

                        try:
                            if j+1 < self.num_cols:
                                if 'S' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('S')
                        except IndexError:
                            pass

                        try:
                            if i+1 < self.num_rows:
                                if 'S' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('S')
                        except IndexError:
                            pass

                        try:
                            if j-1 >= 0:
                                if 'S' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('S')
                        except IndexError:
                            pass

                    
                    if self.world[i][j][k] == 'P':

                        try:
                            if i-1 >= 0:
                                if 'B' not in self.world[i-1][j]:
                                    self.world[i-1][j].append('B')
                        except IndexError:
                            pass

                        try:
                            if j+1 < self.num_cols:
                                if 'B' not in self.world[i][j+1]:
                                    self.world[i][j+1].append('B')
                        except IndexError:
                            pass

                        try:
                            if i+1 < self.num_rows:
                                if 'B' not in self.world[i+1][j]:
                                    self.world[i+1][j].append('B')
                        except IndexError:
                            pass

                        try:
                            if j-1 >= 0:
                                if 'B' not in self.world[i][j-1]:
                                    self.world[i][j-1].append('B')
                        except IndexError:
                            pass
