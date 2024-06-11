import torch
import random
import numpy as np
from collections import deque
import snake_game_RL as game
from model import Linear_QNet,QTrainer
from helper import plot

num_rows    = 20
num_columns = 20
MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.01

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 1  #randomness
        self.gamma = 0.9    # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)    #popleft if memory full
        self.model = Linear_QNet(6,256,3)
        self.trainer = QTrainer(self.model, lr=LR,gamma=self.gamma)


    def get_state(self, s):
        food = s.snack
        def vision(s, snack):
            global num_rows
            dist = [-1,-1,-1] #AHEAD,LEFT,RIGHT
            distBody = [-1,-1,-1] #If body if 1 away AHEAD, LEFT, RIGHT
            defaultDist = num_rows/2

            head_x, head_y = s.head.pos
            for i, body in enumerate(s.body[1:]):
        
                #GOING RIGHT
                if s.dirnx == 1:
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
                elif s.dirnx == -1:
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
                elif s.dirny == -1:
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
                elif s.dirny == 1:
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
            wallDist = distWall(s)
            for i, wall in enumerate(wallDist):
                if wall != -1 and dist[i] == -1:
                    dist[i] = wall


            #Getting for the direction of the snack
            dirSnack = [-1,-1,-1] #AHEAD, LEFT, RIGHT
            xDist = abs(head_x - snack.pos[0])
            yDist = abs(head_y - snack.pos[1])
            block = [-1,-1,-1] #BLOCKED BY BODY AHEAD, LEFT, RIGHT

            if s.dirnx == 1:
                if head_x < snack.pos[0]:
                    if dist[0] < xDist and dist[0] != -1:
                        block[0] = 1
                    else:
                        dirSnack[0] = 1#abs(s.head.pos[0]-snack.pos[0])
                elif head_x > snack.pos[0] and head_y == snack.pos[1]:
                    if(random.randint(0,1)):
                        dirSnack[1] = 1
                    else:
                        dirSnack[2] = 1
                if head_y > snack.pos[1]:
                    if dist[1] < yDist and dist[1] != -1:
                        block[1] = 1
                    else:
                        dirSnack[1] = 1#abs(s.head.pos[1]-snack.pos[1])
                if head_y < snack.pos[1]:
                    if dist[2] < yDist and dist[2] != -1:
                        block[2] = 1
                    else:
                        dirSnack[2] = 1#abs(s.head.pos[1]-snack.pos[1])

                
            elif s.dirnx == -1:
                if head_x > snack.pos[0]:
                    if dist[0] < xDist and dist[0] != -1:
                        block[0] = 1
                    else:
                        dirSnack[0] = 1#abs(s.head.pos[0]-snack.pos[0])
                elif head_x < snack.pos[0] and head_y == snack.pos[1]:
                    if(random.randint(0,1)):
                        dirSnack[1] = 1
                    else:
                        dirSnack[2] = 1
                if head_y < snack.pos[1]:
                    if dist[1] < yDist and dist[1] != -1:
                        block[1] = 1
                    else:
                        dirSnack[1] = 1#abs(s.head.pos[1]-snack.pos[1])
                if head_y > snack.pos[1]:
                    if dist[2] < yDist and dist[2] != -1:
                        block[2] = 1
                    else:
                        dirSnack[2] = 1#abs(s.head.pos[1]-snack.pos[1])

            
            elif s.dirny == -1: 
                if head_y > snack.pos[1]:
                    if dist[0] < yDist and dist[0] != -1:
                        block[0] = 1
                    else:
                        dirSnack[0] = 1#abs(s.head.pos[1]-snack.pos[1])
                elif head_y < snack.pos[1] and head_x == snack.pos[0]:
                    if(random.randint(0,1)):
                        dirSnack[1] = 1
                    else:
                        dirSnack[2] = 1
                if head_x > snack.pos[0]:
                    if dist[1] < xDist and dist[1] != -1:
                        block[1] = 1
                    else:
                        dirSnack[1] = 1#abs(s.head.pos[0]-snack.pos[0])
                if head_x < snack.pos[0]:
                    if dist[2] < xDist and dist[2] != -1:
                        block[2] = 1
                    else:
                        dirSnack[2] = 1#abs(s.head.pos[0]-snack.pos[0])


            elif s.dirny == 1: 
                if head_y < snack.pos[1]:
                    if dist[0] < yDist and dist[0] != -1:
                        block[0] = 1
                    else:
                        dirSnack[0] = 1#abs(s.head.pos[1]-snack.pos[1])
                elif head_y > snack.pos[1] and head_x == snack.pos[0]:
                    if(random.randint(0,1)):
                        dirSnack[1] = 1
                    else:
                        dirSnack[2] = 1
                if head_x < snack.pos[0]:
                    if dist[1] < xDist and dist[1] != -1:
                        block[1] = 1
                    else:
                        dirSnack[1] = 1#abs(s.head.pos[0]-snack.pos[0])
                if head_x > snack.pos[0]:
                    if dist[2] < xDist and dist[2] != -1:
                        block[2] = 1
                    else:
                        dirSnack[2] = 1#abs(s.head.pos[0]-snack.pos[0])
            
            if -1 not in dist:
                dirSnack = [-1,-1,-1]
                for i in range(len(dist)): 
                    dirSnack[dist.index(max(dist))] = 1

            elif sum(block) > -2 or (1 in block and 1 in wallDist):
                dirSnack = [-1,-1,-1]
                dirSnack[dist.index(-1)] = 1             

            #print("V:"+str(dirSnack+dist))
            return dirSnack+dist

        def distWall(s):
            global num_rows
            defaultDist = 5
            dist = [-1,-1,-1] #AHEAD, LEFT, RIGHT
            
            head_x, head_y = s.head.pos
            if s.dirnx == 1:
                if (head_x + defaultDist) >= (num_rows-1):
                    dist[0] = abs(head_x - (num_rows-1))
                if (head_y - defaultDist) <= 0:
                    dist[1] = abs(s.head.pos[1] - 0)
                if (head_y+defaultDist) >= (num_rows-1):
                    dist[2] = abs(head_y - (num_rows-1))
            elif s.dirnx == -1:  
                if (head_x - defaultDist) <= 0:
                    dist[0] = abs(head_x)
                if (head_y - defaultDist) <= 0:
                    dist[2] = abs(s.head.pos[1] - 0)
                if (head_y + defaultDist) >= (num_rows-1):
                    dist[1] = abs(head_y - (num_rows-1))
            elif s.dirny == -1: 
                if (head_y - defaultDist) <= 0:
                    dist[0] = abs(head_y - 0)
                if  (head_x + defaultDist) >= (num_rows - 1):
                    dist[2] = abs(head_x - (num_rows - 1))
                if (head_x - defaultDist) <= 0:
                    dist[1] = abs(head_x)
            elif s.dirny == 1: 
                if (head_y + defaultDist) >= (num_rows - 1):
                    dist[0] = abs(head_y - (num_rows-1))
                if (head_x + defaultDist) >= (num_rows-1):
                    dist[1] = abs(head_x - (num_rows-1))
                if  (head_x - defaultDist) <= 0:
                    dist[2] = abs(head_x)

            return dist
        
        return np.array(vision(s,food),dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))    #pops left if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory,BATCH_SIZE)    #returns random batch_size no of tuples
        else:
            mini_sample = self.memory

        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        #Random Move, Exploration vs Exploitation
        # self.epsilon = 800 - self.n_games
        # self.epsilon = 1
        epsilon_decay = 0.005
        if self.epsilon > 0.105:
            self.epsilon -= epsilon_decay
        final_move = [0,0,0]

        if random.randint(0,200) < self.epsilon:
            final_move[random.randint(0,2)] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move_index_max = torch.argmax(prediction).item()
            final_move[move_index_max] = 1

        return final_move


def train():
    scores = []
    mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    s = game.Snake((255,0,0), (10,10))

    while True:
        #Get old state  
        state_old = agent.get_state(s)

        # Get move
        final_move = agent.get_action(state_old)

        #Get new state
        reward, done, score = s.move(final_move)
        state_new = agent.get_state(s)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        #remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #Train the long memory and plot the result
            s.reset((10,10))
            agent.n_games +=1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
                print('Game: ',agent.n_games,', Score: ',score,'Record: ',record)

            scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            mean_scores.append(mean_score)
            
            plot(scores,mean_scores)


if __name__ == '__main__':
    train()