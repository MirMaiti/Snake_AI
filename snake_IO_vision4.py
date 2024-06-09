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

def ok(x,y):
    return (0<=x<num_rows and 0<=y<num_columns)

class Cube(object):

    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.rows = num_rows
        self.w = 500
        self.pos = start
        self.dirnx = dirnx
        self.dirny = dirny
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
        self.alive = True
        self.body = []
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        self.color = color
        self.head = Cube(pos, self.dirnx, self.dirny)
        self.body.append(self.head)



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

        def getDirAction(self, output):
            action = [0, 0]
            max_output = max(output)
            dir_map = {
                (1, 0): [[0, -1], [0, 1]],   # Moving right: Left -> Up, Right -> Down
                (-1, 0): [[0, 1], [0, -1]],  # Moving left: Left -> Down, Right -> Up
                (0, -1): [[-1, 0], [1, 0]],  # Moving up: Left -> Left, Right -> Right
                (0, 1): [[1, 0], [-1, 0]]    # Moving down: Left -> Right, Right -> Left
            }

            if max_output == output[0]:  # LEFT
                action = dir_map[(self.dirnx, self.dirny)][0]
                print("Left")
            elif max_output == output[1]:  # RIGHT
                action = dir_map[(self.dirnx, self.dirny)][1]
                print("Right")
            elif max_output == output[2]:  # FORWARD
                action = [self.dirnx, self.dirny]

            return action
        
        self.turns[self.head.pos[:]] = getDirAction(self,output)

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
            # self.alive = False
            return True  # Collision with wall

        # Check self-collision
        for x in range(len(self.body)):
            if self.body[x].pos in list(map(lambda z: z.pos, self.body[x+1:])):
                # self.alive = False
                return True  # Self-collision

        return False  # No collision   

    def reset(self, pos):
        self.dirnx = 0
        self.dirny = 1
        self.head = Cube(pos, self.dirnx, self.dirny)
        self.body = []
        self.body.append(self.head)
        self.turns = {}



    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        #print(f"addcube {id(self)}")
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

    def distWall(self):
            global num_rows
            head_x, head_y = self.head.pos
            wallDist = [num_rows, num_rows, num_rows]

            if self.dirnx == 1:
                wallDist[0] = num_rows - head_x
                wallDist[1] = head_y
                wallDist[2] = num_rows - head_y

            elif self.dirnx == -1:
                wallDist[0] = head_x
                wallDist[1] = num_rows - head_y
                wallDist[2] = head_y

            elif self.dirny == 1:
                wallDist[0] = num_rows - head_y
                wallDist[1] = head_x
                wallDist[2] = num_rows - head_x

            elif self.dirny == -1:
                wallDist[0] = head_y
                wallDist[1] = num_rows - head_x
                wallDist[2] = head_x

            return wallDist
    
    def vision(self, snack):
        global num_rows
        defaultDist = num_rows / 2
        dist = [defaultDist, defaultDist, defaultDist]
        dirSnack = [0, 0, 0]

        head_x, head_y = self.body[0].pos
        snack_x, snack_y = snack.pos

        for body in self.body[1:]:
            body_x, body_y = body.pos

            if self.dirnx == 1:  # Right
                if head_y == body_y:
                    if head_x < body_x < head_x + defaultDist:
                        dist[0] = min(dist[0], body_x - head_x)
                if head_x == body_x:
                    if head_y > body_y:
                        dist[1] = min(dist[1], head_y - body_y)
                    elif head_y < body_y:
                        dist[2] = min(dist[2], body_y - head_y)

            elif self.dirnx == -1:  # Left
                if head_y == body_y:
                    if head_x > body_x > head_x - defaultDist:
                        dist[0] = min(dist[0], head_x - body_x)
                if head_x == body_x:
                    if head_y < body_y:
                        dist[1] = min(dist[1], body_y - head_y)
                    elif head_y > body_y:
                        dist[2] = min(dist[2], head_y - body_y)

            elif self.dirny == 1:  # Down
                if head_x == body_x:
                    if head_y < body_y < head_y + defaultDist:
                        dist[0] = min(dist[0], body_y - head_y)
                if head_y == body_y:
                    if head_x < body_x:
                        dist[1] = min(dist[1], body_x - head_x)
                    elif head_x > body_x:
                        dist[2] = min(dist[2], head_x - body_x)

            elif self.dirny == -1:  # Up
                if head_x == body_x:
                    if head_y > body_y > head_y - defaultDist:
                        dist[0] = min(dist[0], head_y - body_y)
                if head_y == body_y:
                    if head_x > body_x:
                        dist[1] = min(dist[1], head_x - body_x)
                    elif head_x < body_x:
                        dist[2] = min(dist[2], body_x - head_x)

        wallDist = self.distWall()
        dist = [min(dist[i], wallDist[i]) for i in range(3)]

        if self.dirnx == 1:
            if head_x < snack_x:
                dirSnack[0] = 1
            elif head_x > snack_x:
                dirSnack[random.choice([1, 2])] = 1
            if head_y > snack_y:
                dirSnack[1] = 1
            if head_y < snack_y:
                dirSnack[2] = 1

        elif self.dirnx == -1:
            if head_x > snack_x:
                dirSnack[0] = 1
            elif head_x < snack_x:
                dirSnack[random.choice([1, 2])] = 1
            if head_y < snack_y:
                dirSnack[1] = 1
            if head_y > snack_y:
                dirSnack[2] = 1

        elif self.dirny == 1:
            if head_y < snack_y:
                dirSnack[0] = 1
            elif head_y > snack_y:
                dirSnack[random.choice([1, 2])] = 1
            if head_x < snack_x:
                dirSnack[1] = 1
            if head_x > snack_x:
                dirSnack[2] = 1

        elif self.dirny == -1:
            if head_y > snack_y:
                dirSnack[0] = 1
            elif head_y < snack_y:
                dirSnack[random.choice([1, 2])] = 1
            if head_x > snack_x:
                dirSnack[1] = 1
            if head_x < snack_x:
                dirSnack[2] = 1
        print(f"vision: {dirSnack+dist}   head:{self.body[0].pos}")
        return dirSnack + dist



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
        x = random.randrange(0, rows)
        y = random.randrange(0, rows)
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

def num_snakesAlive(snakes):
    count = 0
    for snake in snakes:
        if snake.alive == True:
            count+=1
    return count

def main_loop(genomes, config):
    # global width, rows, s, snack
    width = 500
    rows = num_rows
    nets = []
    ge_list = []
    snakes = []
    foods = []
    scores = []
    frames = []

    for genome_id,genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        snakes.append(Snake((255,0,0), (10,10)))
        foods.append(Cube(randomSnack(rows,snakes[-1]))) 
        scores.append(genome.fitness)
        ge_list.append(genome)
        frames.append(0)

        #print(f"going to while {len(snakes)}")
        while num_snakesAlive(snakes)>0 :
            #print(f"in while {len(snakes)}")
            for index,snake in enumerate(snakes):
                if snake.alive == True:
                    out_put = nets[index].activate(snake.vision(foods[index]))
                    print(f"Output : {out_put}")
                    snake.move(out_put)

                    if snake.body[0].pos == foods[index].pos:
                        print("YUM")
                        frames[index] = 0
                        ge_list[index].fitness += 1
                        snake.addCube()
                        foods[index] = Cube(randomSnack(rows, snake), color=(0,255,0))
                        scores[index] = ge_list[index].fitness

                    frames[index] +=1 

                    if snake.check_collision() or frames[index]>=100:
                        #print(f"{index} is DEAD length:{len(snake.body)}, collide?{snake.check_collision()}   frame?{frames[index]}")
                        ge_list[index].fitness -= 2
                        snake.alive = False
                        # snakes.pop(index)
                        # foods.pop(index)
                        # nets.pop(index)
                        # scores.pop(index)
                        # ge_list.pop(index)
                        # frames.pop(index)
                        # snakes.remove(snake)
                        # break
                    
                    


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
    winner = p.run(main_loop,100)

    #Show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config_feedforward.txt")
    run(config_path)