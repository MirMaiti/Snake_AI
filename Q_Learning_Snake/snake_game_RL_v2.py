#Snake Tutorial Python
import numpy as np
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

num_rows    = 20
num_columns = 20
vec = pygame.math.Vector2

class cube(object):
    rows = num_rows
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

class Snake(object):
    
    def __init__(self, color, pos):
        self.reward = 0
        self.win = pygame.display.set_mode((500, 500))
        self.body = []
        self.turns = {}
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.frame = 0
        self.snack = cube(self.randomSnack(num_rows, self))
        self.clock = pygame.time.Clock()


    def move(self,action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        if action == [1, 0, 0]:  # Move forward
            action[0] = self.dirnx
            action[1] = self.dirny
        elif action == [0, 1, 0]:  # Turn right
            if self.dirnx == 0:
                self.dirnx = self.dirny
                self.dirny = 0
            else:
                self.dirny = -self.dirnx
                self.dirnx = 0
            action[0] = self.dirnx
            action[1] = self.dirny
        elif action == [0, 0, 1]:  # Turn left
            if self.dirnx == 0:
                self.dirnx = -self.dirny
                self.dirny = 0
            else:
                self.dirny = self.dirnx
                self.dirnx = 0
            action[0] = self.dirnx
            action[1] = self.dirny
        else:
            raise ValueError("Invalid action provided")


        self.turns[self.head.pos[:]] = [self.dirnx,self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx,c.dirny)
        
        self.reward =0* -(abs(self.head.pos[0]-self.snack.pos[0])+abs(self.head.pos[1]-self.snack.pos[1]))
        
        self.frame+=1
        # self.reward -= 0.05
        #Display the game:
        
        self.redrawWindow(self.win)

        #Adjusting Reward
        if self.body[0].pos == self.snack.pos:
            self.reward = 10
            self.frame = 0
            self.addCube()
            self.snack = cube(self.randomSnack(num_rows, self), color=(0,255,0))

        if self.check_collision() or (self.frame>100*len(self.body)):
            self.reward = -10
            return (self.reward,True,len(self.body))
        

        return (self.reward,self.check_collision(),len(self.body))
    
    def danger(self):
        point_l = (self.head.pos[0] - 1, self.head.pos[1])
        point_r = (self.head.pos[0] + 1, self.head.pos[1])
        point_u = (self.head.pos[0], self.head.pos[1] - 1)
        point_d = (self.head.pos[0], self.head.pos[1] + 1)

        danger_forward,danger_left,danger_right=False,False,False

        if [self.dirnx,self.dirny] == [1,0]:
            if (point_r in self.body) or (point_r[0] < 0 or point_r[0] >= num_rows or point_r[1] < 0 or point_r[1] >= num_columns):
                danger_forward = True
            if (point_u in self.body) or (point_u[0] < 0 or point_u[0] >= num_rows or point_u[1] < 0 or point_u[1] >= num_columns):
                danger_left = True
            if (point_d in self.body) or (point_d[0] < 0 or point_d[0] >= num_rows or point_d[1] < 0 or point_d[1] >= num_columns):
                danger_right = True
        
        if [self.dirnx,self.dirny] == [-1,0]:
            if (point_l in self.body) or (point_l[0] < 0 or point_l[0] >= num_rows or point_l[1] < 0 or point_l[1] >= num_columns):
                danger_forward = True
            if (point_d in self.body) or (point_d[0] < 0 or point_d[0] >= num_rows or point_d[1] < 0 or point_d[1] >= num_columns):
                danger_left = True
            if (point_u in self.body) or (point_u[0] < 0 or point_u[0] >= num_rows or point_u[1] < 0 or point_u[1] >= num_columns):
                danger_right = True

        if [self.dirnx,self.dirny] == [0,1]:
            if (point_d in self.body) or (point_d[0] < 0 or point_d[0] >= num_rows or point_d[1] < 0 or point_d[1] >= num_columns):
                danger_forward = True
            if (point_r in self.body) or (point_r[0] < 0 or point_r[0] >= num_rows or point_r[1] < 0 or point_r[1] >= num_columns):
                danger_left = True
            if (point_l in self.body) or (point_l[0] < 0 or point_l[0] >= num_rows or point_l[1] < 0 or point_l[1] >= num_columns):
                danger_right = True

        if [self.dirnx,self.dirny] == [0,-1]:
            if (point_u in self.body) or (point_u[0] < 0 or point_u[0] >= num_rows or point_u[1] < 0 or point_u[1] >= num_columns):
                danger_forward = True
            if (point_l in self.body) or (point_l[0] < 0 or point_l[0] >= num_rows or point_l[1] < 0 or point_l[1] >= num_columns):
                danger_left = True
            if (point_r in self.body) or (point_r[0] < 0 or point_r[0] >= num_rows or point_r[1] < 0 or point_r[1] >= num_columns):
                danger_right = True       
        
        return (danger_forward,danger_right,danger_left)


    def check_collision(self):
        self.frame = 0
        head_pos = self.body[0].pos
        print(str(head_pos[0]),",", str(head_pos[1]),"\n")
        # Check collision with walls
        if head_pos[0] < 0 or head_pos[0] >= num_rows or head_pos[1] < 0 or head_pos[1] >= num_columns:
            return True  # Collision with wall

        # Check self-collision
        for x in range(len(self.body)):
            if self.body[x].pos in list(map(lambda z: z.pos, self.body[x+1:])):
                return True  # Self-collision

        return False  # No collision   

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)


    def getDirAction(self, output):
        action = vec(0,0)
        #Calculating which direction is which depending on the current state
        if output[0] == 1: #LEFT
            if self.dirnx == 1:
                action.x = 0
                action.y = -1
            elif self.dirnx == -1:
                action.x = 0
                action.y = 1
            elif self.dirny == -1:
                action.x = -1
                action.y = 0
            elif self.dirny == 1:
                action.x = 1
                action.y = 0
        elif output[1] == 1: #RIGHT
            if self.dirnx == 1:
                action.x = 0
                action.y = 1
            elif self.dirnx == -1:
                action.x = 0
                action.y = -1
            elif self.dirny == -1:
                action.x = 1
                action.y = 0
            elif self.dirny == 1:
                action.x = -1
                action.y = 0
        elif output[2] == 1: #FORWARD:
            action.x = self.dirnx
            action.y = self.dirny

        return action

    def vision(self, snack):
        global num_rows
        dist = [-1,-1,-1] #AHEAD,LEFT,RIGHT
        distBody = [-1,-1,-1] #If body if 1 away AHEAD, LEFT, RIGHT
        defaultDist = num_rows/2

        head_x, head_y = self.head.pos
        for i, body in enumerate(self.body[1:]):
    
            #GOING RIGHT
            if self.dirnx == 1:
                if (head_x + defaultDist) >= body.pos[0] and head_y == body.pos[1] and head_x < body.pos[0]: #BODY FORWARD
                    if dist[0] == -1 or dist[0] > abs(head_x - body.pos[0]):
                        dist[0] = abs(head_x - body.pos[0])
                        if dist[0] == 1:
                            distBody[0] = 1
                if head_x == body.pos[0] and (head_y - defaultDist) <= body.pos[1] and head_y > body.pos[1]: #LEFT
                    if dist[1] == -1 or dist[1] > abs(head_y - body.pos[1]):
                        dist[1] = abs(head_y - body.pos[1])
                        if dist[1] == 1:
                            distBody[1] = 1
                if head_x == body.pos[0] and (head_y + defaultDist) >= body.pos[1] and head_y < body.pos[1]: #RIGHT
                    if dist[2] == -1 or dist[2] > abs(head_y - body.pos[1]):
                        dist[2] = abs(head_y - body.pos[1])
                        if dist[2] == 1:
                            distBody[2] = 1
            #GOING LEFT
            elif self.dirnx == -1:
                if (head_x - defaultDist) <= body.pos[0] and head_y == body.pos[1] and head_x > body.pos[0]: #BODY FORWARD
                    if dist[0] == -1 or dist[0] > abs(head_x - body.pos[0]):
                        dist[0] = abs(head_x - body.pos[0])
                        if dist[0] == 1:
                            distBody[0] = 1
                if head_x == body.pos[0] and (head_y + defaultDist) >= body.pos[1] and head_y < body.pos[1]: #LEFT
                    if dist[1] == -1 or dist[1] > abs(head_y - body.pos[1]):
                        dist[1] = abs(head_y - body.pos[1])
                        if dist[1] == 1:
                            distBody[1] = 1
                if head_x == body.pos[0] and (head_y - defaultDist) <= body.pos[1] and head_y > body.pos[1]: #RIGHT
                    if dist[2] == -1 or dist[2] > abs(head_y - body.pos[1]):
                        dist[2] = abs(head_y - body.pos[1])
                        if dist[2] == 1:
                            distBody[2] = 1
            #GOING UP
            elif self.dirny == -1:
                if (head_y - defaultDist) <= body.pos[1] and head_x == body.pos[0] and head_y > body.pos[1]: #BODY FORWARD
                    if dist[0] == -1 or dist[0] > abs(head_y - body.pos[1]):
                        dist[0] = abs(head_y - body.pos[1])
                        if dist[0] == 1:
                            distBody[0] = 1
                if head_y == body.pos[1] and (head_y - defaultDist) <= body.pos[0] and head_x > body.pos[0]: #LEFT
                    if dist[1] == -1 or dist[1] > abs(head_x - body.pos[0]):
                        dist[1] = abs(head_x - body.pos[0])
                        if dist[1] == 1:
                            distBody[1] = 1
                if head_y == body.pos[1] and (head_x + defaultDist) >= body.pos[0] and head_x < body.pos[0]: #RIGHT
                    if dist[2] == -1 or dist[2] > abs(head_x-body.pos[0]):
                        dist[2] = abs(head_x - body.pos[0])
                        if dist[2] == 1:
                            distBody[2] = 1                    

            #GOING DOWN 
            elif self.dirny == 1:
                if (head_y + defaultDist) >= body.pos[1] and head_x == body.pos[0] and head_y < body.pos[1]: #BODY FORWARD
                    if dist[0] == -1 or dist[0] > abs(head_y - body.pos[1]):    
                        dist[0] = abs(head_y - body.pos[1])
                        if dist[0] == 1:
                            distBody[0] = 1
                if head_y == body.pos[1] and (head_x + defaultDist) >= body.pos[0] and head_x < body.pos[0]: #LEFT
                    if dist[1] == -1 or dist[1] > abs(head_x - body.pos[0]):
                        dist[1] = abs(head_x - body.pos[0])
                        if dist[1] == 1:
                            distBody[1] = 1
                if head_y == body.pos[1] and (head_x - defaultDist) <= body.pos[0] and head_x > body.pos[0]: #RIGHT
                    if dist[2] == -1 or dist[2] > abs(head_x - body.pos[0]):
                        dist[2] = abs(head_x - body.pos[0])
                        if dist[2] == 1:
                            distBody[2] = 1

        #Adds vision of walls
        wallDist = self.distWall(self)
        for i, wall in enumerate(wallDist):
            if wall != -1 and dist[i] == -1:
                dist[i] = wall


        #Getting for the direction of the snack
        dirSnack = [-1,-1,-1] #AHEAD, LEFT, RIGHT
        xDist = abs(head_x - snack.pos[0])
        yDist = abs(head_y - snack.pos[1])
        block = [-1,-1,-1] #BLOCKED BY BODY AHEAD, LEFT, RIGHT

        if self.dirnx == 1:
            if head_x < snack.pos[0]:
                if dist[0] < xDist and dist[0] != -1:
                    block[0] = 1
                else:
                    dirSnack[0] = 1#abs(self.head.pos[0]-snack.pos[0])
            elif head_x > snack.pos[0] and head_y == snack.pos[1]:
                if(random.randint(0,1)):
                    dirSnack[1] = 1
                else:
                    dirSnack[2] = 1
            if head_y > snack.pos[1]:
                if dist[1] < yDist and dist[1] != -1:
                    block[1] = 1
                else:
                    dirSnack[1] = 1#abs(self.head.pos[1]-snack.pos[1])
            if head_y < snack.pos[1]:
                if dist[2] < yDist and dist[2] != -1:
                    block[2] = 1
                else:
                    dirSnack[2] = 1#abs(self.head.pos[1]-snack.pos[1])

            
        elif self.dirnx == -1:
            if head_x > snack.pos[0]:
                if dist[0] < xDist and dist[0] != -1:
                    block[0] = 1
                else:
                    dirSnack[0] = 1#abs(self.head.pos[0]-snack.pos[0])
            elif head_x < snack.pos[0] and head_y == snack.pos[1]:
                if(random.randint(0,1)):
                    dirSnack[1] = 1
                else:
                    dirSnack[2] = 1
            if head_y < snack.pos[1]:
                if dist[1] < yDist and dist[1] != -1:
                    block[1] = 1
                else:
                    dirSnack[1] = 1#abs(self.head.pos[1]-snack.pos[1])
            if head_y > snack.pos[1]:
                if dist[2] < yDist and dist[2] != -1:
                    block[2] = 1
                else:
                    dirSnack[2] = 1#abs(self.head.pos[1]-snack.pos[1])

        
        elif self.dirny == -1: 
            if head_y > snack.pos[1]:
                if dist[0] < yDist and dist[0] != -1:
                    block[0] = 1
                else:
                    dirSnack[0] = 1#abs(self.head.pos[1]-snack.pos[1])
            elif head_y < snack.pos[1] and head_x == snack.pos[0]:
                if(random.randint(0,1)):
                    dirSnack[1] = 1
                else:
                    dirSnack[2] = 1
            if head_x > snack.pos[0]:
                if dist[1] < xDist and dist[1] != -1:
                    block[1] = 1
                else:
                    dirSnack[1] = 1#abs(self.head.pos[0]-snack.pos[0])
            if head_x < snack.pos[0]:
                if dist[2] < xDist and dist[2] != -1:
                    block[2] = 1
                else:
                    dirSnack[2] = 1#abs(self.head.pos[0]-snack.pos[0])


        elif self.dirny == 1: 
            if head_y < snack.pos[1]:
                if dist[0] < yDist and dist[0] != -1:
                    block[0] = 1
                else:
                    dirSnack[0] = 1#abs(self.head.pos[1]-snack.pos[1])
            elif head_y > snack.pos[1] and head_x == snack.pos[0]:
                if(random.randint(0,1)):
                    dirSnack[1] = 1
                else:
                    dirSnack[2] = 1
            if head_x < snack.pos[0]:
                if dist[1] < xDist and dist[1] != -1:
                    block[1] = 1
                else:
                    dirSnack[1] = 1#abs(self.head.pos[0]-snack.pos[0])
            if head_x > snack.pos[0]:
                if dist[2] < xDist and dist[2] != -1:
                    block[2] = 1
                else:
                    dirSnack[2] = 1#abs(self.head.pos[0]-snack.pos[0])
        
        if -1 not in dist:
            dirSnack = [-1,-1,-1]
            for i in range(len(dist)): 
                dirSnack[dist.index(max(dist))] = 1

        elif sum(block) > -2 or (1 in block and 1 in wallDist):
            dirSnack = [-1,-1,-1]
            dirSnack[dist.index(-1)] = 1             

        #print("V:"+str(dirSnack+dist))
        return dirSnack+dist

    def distWall(self):
        global num_rows
        defaultDist = 5
        dist = [-1,-1,-1] #AHEAD, LEFT, RIGHT
        
        head_x, head_y = self.head.pos
        if self.dirnx == 1:
            if (head_x + defaultDist) >= (num_rows-1):
                dist[0] = abs(head_x - (num_rows-1))
            if (head_y - defaultDist) <= 0:
                dist[1] = abs(self.head.pos[1] - 0)
            if (head_y+defaultDist) >= (num_rows-1):
                dist[2] = abs(head_y - (num_rows-1))
        elif self.dirnx == -1:  
            if (head_x - defaultDist) <= 0:
                dist[0] = abs(head_x)
            if (head_y - defaultDist) <= 0:
                dist[2] = abs(self.head.pos[1] - 0)
            if (head_y + defaultDist) >= (num_rows-1):
                dist[1] = abs(head_y - (num_rows-1))
        elif self.dirny == -1: 
            if (head_y - defaultDist) <= 0:
                dist[0] = abs(head_y - 0)
            if  (head_x + defaultDist) >= (num_rows - 1):
                dist[2] = abs(head_x - (num_rows - 1))
            if (head_x - defaultDist) <= 0:
                dist[1] = abs(head_x)
        elif self.dirny == 1: 
            if (head_y + defaultDist) >= (num_rows - 1):
                dist[0] = abs(head_y - (num_rows-1))
            if (head_x + defaultDist) >= (num_rows-1):
                dist[1] = abs(head_x - (num_rows-1))
            if  (head_x - defaultDist) <= 0:
                dist[2] = abs(head_x)

        return dist


    def drawGrid(self,w, rows, surface):
        sizeBtwn = w // rows

        x = 0
        y = 0
        for l in range(rows):
            x = x + sizeBtwn
            y = y + sizeBtwn

            pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
            pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
            

    def redrawWindow(self,surface):
        # global rows, width, s, snack
        surface.fill((0,0,0))
        self.draw(surface)
        self.snack.draw(surface)
        self.drawGrid(500,20, surface)
        pygame.display.update()


    def randomSnack(self,rows, item):

        positions = item.body

        while True:
            x = random.randrange(rows)
            y = random.randrange(rows)
            if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
                continue
            else:
                break
            
        return (x,y)


    def message_box(self,subject, content):
        root = tk.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        messagebox.showinfo(subject, content)
        try:
            root.destroy()
        except:
            pass



# def main_loop():
#     global width, rows, s, snack
#     width = 500
#     rows = num_rows
#     win = pygame.display.set_mode((width, width))
#     s = Snake((255,0,0), (10,10))
#     snack = cube(randomSnack(rows, s), color=(0,255,0))
#     flag = True

#     clock = pygame.time.Clock()
    
#     while flag:
#         pygame.time.delay(50)
#         clock.tick(10)
#         s.move()
#         # if s.body[0].pos == snack.pos:
#         #     s.addCube()
#         #     snack = cube(randomSnack(rows, s), color=(0,255,0))

#         # if s.check_collision():
#         #     print('Score: ', len(s.body))
#         #     message_box('You Lost!', 'Play again...')
#         #     s.reset((10,10))
#         #     break
            
#         redrawWindow(win)


# if __name__ == '__main__':
#     main_loop()