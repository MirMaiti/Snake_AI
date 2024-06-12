import torch
import random
import numpy as np
from collections import deque
import snake_game_RL_v2 as game
from model import Linear_QNet,QTrainer
from helper import plot

num_rows    = 20
num_columns = 20
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  #randomness
        self.gamma = 0.9    # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)    #popleft if memory full
        self.model = Linear_QNet(11,256,3)
        self.trainer = QTrainer(self.model, lr=LR,gamma=self.gamma)

    def get_state(self,s):
        point_l = (s.head.pos[0] - 1, s.head.pos[1])
        point_r = (s.head.pos[0] + 1, s.head.pos[1])
        point_u = (s.head.pos[0], s.head.pos[1] - 1)
        point_d = (s.head.pos[0], s.head.pos[1] + 1)
        
        dir_l = [s.dirnx,s.dirny] == [-1,0]
        dir_r = [s.dirnx,s.dirny] == [1,0]
        dir_u = [s.dirnx,s.dirny] == [0,-1]
        dir_d = [s.dirnx,s.dirny] == [0,1]

        danger_f,danger_r,danger_l=s.danger()
        state=(danger_f,danger_r,danger_l,
        # Move direction
        dir_l,
        dir_r,
        dir_u,
        dir_d,
        
        # Food location 
        s.snack.pos[0] < s.head.pos[0],  # food left
        s.snack.pos[0] > s.head.pos[0],  # food right
        s.snack.pos[1] < s.head.pos[1],  # food up
        s.snack.pos[1] > s.head.pos[1]  # food down
        )
        
        return np.array(state, dtype=int)

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
        # self.epsilon = max(self.epsilon_min,self.epsilon*self.epsilon_decay)
        self.epsilon = 80-self.n_games
        final_move = [0,0,0]

        # if random.uniform(0,1) < self.epsilon:
        if random.randint(0,200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
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