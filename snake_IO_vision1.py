#Snake Tutorial Python
import math
import random
import neat.statistics
import pygame
import tkinter as tk
from tkinter import messagebox
import os
import neat

num_rows    = 20
num_columns = 20
class Cube(object):
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
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self,output):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()

        #     keys = pygame.key.get_pressed()

            #for key in keys:
            # if keys[pygame.K_LEFT]:
            #     self.dirnx = -1
            #     self.dirny = 0
            #     self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            # elif keys[pygame.K_RIGHT]:
            #     self.dirnx = 1
            #     self.dirny = 0
            #     self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            # elif keys[pygame.K_UP]:
            #     self.dirnx = 0
            #     self.dirny = -1
            #     self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            # elif keys[pygame.K_DOWN]:
            #     self.dirnx = 0
            #     self.dirny = 1
            #     self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        if max(output) == output[0]: #LEFT
            if self.dirnx == 1:
                self.dirnx = 0
                self.dirny = -1
            elif self.dirnx == -1:
                self.dirnx = 0
                self.dirny = 1
            elif self.dirny == -1:
                self.dirnx = -1
                self.dirny = 0
            elif self.dirny == 1:
                self.dirnx = 1
                self.dirny = 0


        elif max(output) == output[1]: #RIGHT
            if self.dirnx == 1:
                self.dirnx = 0
                self.dirny = 1
            elif self.dirnx == -1:
                self.dirnx = 0
                self.dirny = -1
            elif self.dirny == -1:
                self.dirnx = 1
                self.dirny = 0
            elif self.dirny == 1:
                self.dirnx = -1
                self.dirny = 0

        elif max(output)==output[2]:    #FORWARD
            pass
        
        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        # elif max(output)==output[3]:
        #     self.dirnx = 0
        #     self.dirny = 1
        #     self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                #if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                #elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                #elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                #elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                #else: c.move(c.dirnx,c.dirny)
                c.move(c.dirnx,c.dirny)
    
    def check_collision(self):
        head_pos = self.body[0].pos
        #print(str(head_pos[0]),",", str(head_pos[1]),"\n")
        # Check collision with walls
        if head_pos[0] < 0 or head_pos[0] >= num_rows or head_pos[1] < 0 or head_pos[1] >= num_columns:
            return True  # Collision with wall

        # Check self-collision
        for x in range(len(self.body)):
            if self.body[x].pos in list(map(lambda z: z.pos, self.body[x+1:])):
                return True  # Self-collision

        return False  # No collision   

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

    def vision(self,fruit):
        output = []
        if (self.dirnx,self.dirny) == (0,1):
            #Distance to the food
            output.append((self.body[0]).pos[0] - fruit.pos[0] -1)  #Right
            if fruit.pos[0] <= ((self.body[0]).pos[0] - 1) and fruit.pos[1] >= ((self.body[0].pos[1])+1):
                output.append(
                    distance((self.body[0]).pos[0]-1,fruit.pos[0],(self.body[0].pos[1])+1,fruit.pos[1])
                )  #Forward Right
        else:
            output.append(-distance((self.body[0]).pos[0]-1,fruit.pos[0],(self.body[0].pos[1])+1,fruit.pos[1]))   #Forward Right
        output.append(fruit.pos[1]-(self.body[0]).pos[1]-1)  #Forward

        if fruit.pos[0] >= (self.body[0].pos[0] + 1) and fruit.pos[1] >= (self.body[0].pos[1] + 1):
                output.append(
                    distance(self.body[0].pos[0] + 1, fruit.pos[0], self.body[0].pos[1] + 1,
                             fruit.pos[0]))  # ForwardLeft
        else:
                output.append(
                    - distance(self.body[0].pos[0] + 1, fruit.pos[0], self.body[0].pos[1] + 1,
                               fruit.pos[0]))  # ForwardLeft
        output.append(fruit.pos[0] - self.body[0].pos[0] - 1)  # Left

        #Distance to nearest obstacle
        # 1(Right)
        d = 1000
        x = self.body[0].pos[0]
        y = self.body[0].pos[1]
        run = True
        while ok(x,y) and run:
            for i in range(0,len(self.body)):
                if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                    d = self.body[0].pos[0] - x - 1
                    run = False
                    break
            x-=1
        output.append(min(d,self.body[0].pos[0]))

        # 8(ForwardRight)
        d = 1000
        x = self.body[0].pos[0]-1
        y=self.body[0].pos[1]+1
        run = True
        while ok(x,y) and run:
            for i in range(0,len(self.body)):
                if x ==self.body[i].pos[0] and y==self.body[i].pos[1]:
                    d = distance(self.body[0].pos[0],x,self.body[0].pos[1],y)
                    run = False
                    break
            y+=1
            x-=1
        output.append(min(d,(distance(self.body[0].pos[0],0,self.body[0].pos[1],num_columns))))

        # 7(Forward)
        d = 1000
        x = self.body[0].pos[0]
        y=self.body[0].pos[1]+1
        run = True
        while ok(x,y) and run:
            for i in range(0,len(self.body)):
                if x ==self.body[i].pos[0] and y==self.body[i].pos[1]:
                    d = y - self.body[0].pos[1] - 1
                    run = False
                    break
            y+=1
        output.append(min(d,(num_columns - self.body[0].pos[1] - 1)))

        #(Forward Left)
        d = 1000
        x = self.body[0].pos[0]+1
        y=self.body[0].pos[1]+1
        run = True
        while ok(x,y) and run:
            for i in range(0,len(self.body)):
                if x ==self.body[i].pos[0] and y==self.body[i].pos[1]:
                    d = distance(self.body[0].pos[0],x,self.body[0].pos[1],y)
                    run = False
                    break
            x+=1
            y+=1
        output.append(min(d,(distance(self.body[0].pos[0],num_rows,self.body[0].pos[1],num_rows))))

        # (Left)
        d = 1000
        x = self.body[0].pos[0]+1
        y=self.body[0].pos[1]
        run = True
        while ok(x,y) and run:
            for i in range(0,len(self.body)):
                if x ==self.body[i].pos[0] and y==self.body[i].pos[1]:
                    d = x - (self.body[0].pos[0] +1 )
                    run = False
                    break
            x+=1
        output.append(min((num_rows - self.body[0].pos[0] -1),d))


        
        if (self.dirnx,self.dirny) == (-1,0):
            # Distance to the food
            output.append(self.body[0].pos[1] - fruit.pos[1] - 1)  # Right
            if fruit.pos[0] <= (self.body[0].pos[0] - 1) and fruit.pos[1] <= (self.body[0].pos[1] - 1):
                output.append(
                    distance(self.body[0].pos[0] - 1, fruit.pos[0], self.body[0].pos[1] - 1,
                             fruit.pos[1]))  # Forward Right
            else:
                output.append(
                    - distance(self.body[0].pos[0] - 1, fruit.pos[0], self.body[0].pos[1] - 1,
                               fruit.pos[1]))  # Forward Right
            output.append(self.body[0].pos[0] - fruit.pos[0] - 1)  # Forward
            if fruit.pos[0] <= (self.body[0].pos[0] - 1) and fruit.pos[1] >= (self.body[0].pos[1] + 1):
                output.append(
                    distance(self.body[0].pos[0] - 1, fruit.pos[0], self.body[0].pos[1] + 1,
                             fruit.pos[1]))  # Forward Left
            else:
                output.append(
                    - distance(self.body[0].pos[0] - 1, fruit.pos[0], self.body[0].pos[1] + 1,
                               fruit.pos[1]))  # Forward Left
            output.append(fruit.pos[1] - self.body[0].pos[1] - 1)  # Left

            # Distance to the nearest obstacle
            # (Right)
            d = 100
            x = self.body[0].pos[0]
            y = self.body[0].pos[1] - 1
            run = True

            while ok(x, y) and run:
                for i in range(0, len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = self.body[0].pos[1] - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.body[0].pos[1]))

            # (Forward Right)
            d = 100
            x = self.body[0].pos[0] - 1
            y = self.body[0].pos[1] - 1
            run = True

            while ok(x, y) and run:
                for i in range(0, len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = distance(self.body[0].pos[0], x, self.body[0].pos[1], y)
                        run = False
                        break
                x -= 1
                y -= 1
            output.append(min(d, (distance(self.body[0].pos[0], 0, self.body[0].pos[1], 0))))

            # (Forward)
            d = 100
            x = self.body[0].pos[0] - 1
            y = self.body[0].pos[1]
            run = True

            while ok(x, y) and run:
                for i in range(0, len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = self.body[0].pos[0] - x - 1
                        run = False
                        break
                x -= 1
            output.append(min(d, self.body[0].pos[0]))

            # (Forward Left)
            d = 100
            x = self.body[0].pos[0] - 1
            y = self.body[0].pos[1] + 1
            run = True

            while ok(x, y) and run:
                for i in range(0, len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = distance(self.body[0].pos[0], x, self.body[0].pos[1], y)
                        run = False
                        break
                y += 1
                x -= 1
            output.append(min(d, (distance(self.body[0].pos[0], 0, self.body[0].pos[1], num_rows))))

            # (Left)
            d = 100
            x = self.body[0].pos[0]
            y = self.body[0].pos[1] + 1
            run = True

            while ok(x, y) and run:
                for i in range(0, len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = y - self.body[0].pos[1] - 1
                        run = False
                        break
                y += 1
            output.append(min(d, (num_rows - self.body[0].pos[1] - 1)))

        if (self.dirnx,self.dirny) == (1,0):
            # Distance to the food
            output.append(fruit.pos[1] - self.body[0].pos[1] - 1)  # Right
            if fruit.pos[0] >= (self.body[0].pos[0] + 1) and fruit.pos[1] >= (self.body[0].pos[1] + 1):
                output.append(
                    distance(self.body[0].pos[0] + 1, fruit.pos[0], self.body[0].pos[1] + 1,
                             fruit.pos[1]))  # Forward Right
            else:
                output.append(
                    - distance(self.body[0].pos[0] + 1, fruit.pos[0], self.body[0].pos[1] + 1,
                               fruit.pos[1]))  # Forward Right
            output.append(fruit.pos[0] - self.body[0].pos[0] - 1)  # Forward
            if fruit.pos[0] >= (self.body[0].pos[0] + 1) and fruit.pos[1] <= (self.body[0].pos[1] - 1):
                output.append(
                    distance(self.body[0].pos[0] + 1, fruit.pos[0], self.body[0].pos[1] - 1,
                             fruit.pos[1]))  # Forward left
            else:
                output.append(
                    - distance(self.body[0].pos[0] + 1, fruit.pos[0], self.body[0].pos[1] - 1,
                               fruit.pos[1]))  # Forward left
            output.append(self.body[0].pos[1] - fruit.pos[1] - 1)  # Left

            # Distance to the nearest object
            # 7(Right)
            d = 100
            x = self.body[0].pos[0]
            y = self.body[0].pos[1] + 1
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = y - self.body[0].pos[1] - 1
                        run = False
                        break
                y += 1
            output.append(min(d, (num_rows - self.body[0].pos[1] - 1)))

            # 8(Forward Right)
            d = 100
            x = self.body[0].pos[0] + 1
            y = self.body[0].pos[1] + 1
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = distance(self.body[0].pos[0], x, self.body[0].pos[1], y)
                        run = False
                        break
                y += 1
                x += 1
            output.append(min(d, (distance(self.body[0].pos[0], 0, self.body[0].pos[1], num_rows))))

            # 5(Forward)
            d = 100
            x = self.body[0].pos[0] + 1
            y = self.body[0].pos[1]
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = x - self.body[0].pos[0] - 1
                        run = False
                        break
                x += 1
            output.append(min(d, (num_rows - self.body[0].pos[0] - 1)))

            # 4(Forward Left)
            d = 100
            x = self.body[0].pos[0] + 1
            y = self.body[0].pos[1] - 1
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = distance(self.body[0].pos[0], x, self.body[0].pos[1], y)
                        run = False
                        break
                y -= 1
                x += 1
            output.append(min(d, (distance(self.body[0].pos[0], num_rows, self.body[0].pos[1], 0))))

            # 3(Left)
            d = 100
            x = self.body[0].pos[0]
            y = self.body[0].pos[1] - 1
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = self.body[0].pos[1] - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.body[0].pos[1]))

        if (self.dirnx,self.dirny) == (0,-1):
            # Distance to the food
            output.append(fruit.pos[0] - self.body[0].pos[0] - 1)  # Right
            if fruit.pos[0] >= (self.body[0].pos[0] + 1) and fruit.pos[1] <= (self.body[0].pos[1] - 1):
                output.append(
                    distance(self.body[0].pos[0] + 1, fruit.pos[0], self.body[0].pos[1] - 1,
                             fruit.pos[1]))  # Forward Right
            else:
                output.append(
                    - distance(self.body[0].pos[0] + 1, fruit.pos[0], self.body[0].pos[1] - 1,
                               fruit.pos[1]))  # Forward Right
            output.append(self.body[0].pos[1] - fruit.pos[1] - 1)  # Forward
            if fruit.pos[0] <= (self.body[0].pos[0] - 1) and fruit.pos[1] <= (self.body[0].pos[1] - 1):
                output.append(
                    distance(self.body[0].pos[0] - 1, fruit.pos[0], self.body[0].pos[1] - 1,
                             fruit.pos[1]))  # Forward Left
            else:
                output.append(
                    - distance(self.body[0].pos[0] - 1, fruit.pos[0], self.body[0].pos[1] - 1,
                               fruit.pos[1]))  # Forward Left
            output.append(self.body[0].pos[0] - fruit.pos[0] - 1)  # Left

            # Distance to the nearest object
            # 5(Right)
            d = 100
            x = self.body[0].pos[0] + 1
            y = self.body[0].pos[1]
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = x - self.body[0].pos[0] - 1
                        run = False
                        break
                x += 1
            output.append(min(d, (num_rows - self.body[0].pos[0] - 1)))

            # (Forward Right)
            d = 100
            x = self.body[0].pos[0] + 1
            y = self.body[0].pos[1] - 1
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = distance(self.body[0].pos[0], x, self.body[0].pos[1], y)
                        run = False
                        break
                y -= 1
                x += 1
            output.append(min(d, (distance(self.body[0].pos[0], num_rows, self.body[0].pos[1], 0))))

            # (Forward)
            d = 100
            x = self.body[0].pos[0]
            y = self.body[0].pos[1] - 1
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = self.body[0].pos[1] - y - 1
                        run = False
                        break
                y -= 1
            output.append(min(d, self.body[0].pos[1]))

            # (Forward Left)
            d = 100
            x = self.body[0].pos[0] - 1
            y = self.body[0].pos[1] - 1
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = distance(self.body[0].pos[0], x, self.body[0].pos[1], y)
                        run = False
                        break
                x -= 1
                y -= 1
            output.append(min(d, (distance(self.body[0].pos[0], 0, self.body[0].pos[1], 0))))

            # (Left)
            d = 100
            x = self.body[0].pos[0] - 1
            y = self.body[0].pos[1]
            run = True

            while ok(x, y) and run:
                for i in range(0,len(self.body)):
                    if x == self.body[i].pos[0] and y == self.body[i].pos[1]:
                        d = self.body[0].pos[0] - x - 1
                        run = False
                        break
                x -= 1
            output.append(min(d, self.body[0].pos[0]))

        return output        


def ok(x,y):
    if 0<=x<=num_rows and 0<=y<=num_columns:
        return True
    return False

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
        

def redrawWindow(surface):
    pass
    # global rows, width, snakes, snack
    # surface.fill((0,0,0))
    # for s in snakes:
    #     s.draw(surface)
    #     snack.draw(surface)
    # drawGrid(width,rows, surface)
    # pygame.display.update()


def randomSnack(rows, item):

    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
        
    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def distance(x1,x2,y1,y2):
    return int(((x1-x2)**2+(y1-y2)**2)**(0.5))-1
# def get_inputs(snake, food):
#     return [(snake.body[0]).pos[0],(snake.body[0]).pos[1],food.pos[0],food.pos[1]]

def main_loop(genomes, config):
    # global width, rows, s, snack
    width = 500
    rows = num_rows
    nets = []
    ge_list = []
    snakes = []
    foods = []
    scores = []

    for genome_id,genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        snakes.append(Snake((255,0,0), (10,10)))
        foods.append(Cube(randomSnack(rows,snakes[-1]))) 
        scores.append(genome.fitness)
        ge_list.append(genome)
        
        while len(snakes)>0 :
            for index,snake in enumerate(snakes):
                out_put = nets[index].activate(snake.vision(foods[index]))
                # print(f"\nInput : {snake.vision(foods[index])},Output : {out_put}\n")
                snake.move(out_put)
                if snake.body[0].pos == foods[index].pos:
                    ge_list[index].fitness += 10
                    snake.addCube()
                    foods[index] = Cube(randomSnack(rows, snake), color=(0,255,0))
                    scores[index] = ge_list[index].fitness
                if snake.check_collision():
                    ge_list[index].fitness -= 2
                    snakes.pop(index)
                    foods.pop(index)
                    nets.pop(index)
                    scores.pop(index)
                    ge_list.pop(index)
                    
                    


    # global width, rows, s, snack
    # width = 500
    # rows = num_rows
    # win = pygame.display.set_mode((width, width))
    # s = Snake((255,0,0), (10,10))
    # snack = Cube(randomSnack(rows, s), color=(0,255,0))
    # flag = True

    # clock = pygame.time.Clock()
    
    # while flag:
    #     pygame.time.delay(50)
    #     clock.tick(10)

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             break
        
        # for x,s in enumerate(snakes):
        #     ge_list[x].fitness += 0.1
        #     output = nets[x].activate(get_inputs(s,snack))
        #     s.move(output)    
        #     # print(output)
            # if s.body[0].pos == snack.pos:
            #     genome.fitness += 10
            #     s.addCube()
            #     snack = Cube(randomSnack(rows, s), color=(0,255,0))

        
        # for s in snakes:
        #     if s.check_collision():
        #         ge_list[snakes.index(s)].fitness -= 2
        #         nets.pop(snakes.index(s))
        #         ge_list.pop(snakes.index(s))
        #         snakes.pop(snakes.index(s))
            # print('Score: ', len(s.body))
            # message_box('You Lost!', 'Play again...')
            # s.reset((10,10))
            # break
            
        # redrawWindow(win)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)   

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    #Run for 50 generations
    winner = p.run(main_loop,50)

    #Show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config_feedforward.txt")
    run(config_path)