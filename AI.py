import c
import random

from classes import Bird

class BirdAI():
    def __init__(self, FLA, bird, w1, w2, w3):
        self.FLA = FLA
        self.bird = bird
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3
    
    def get_next_pipe(self):
        for pipe in self.FLA.pipes:
            if pipe.x + c.NECK_WIDTH > c.START_X:
                return pipe
    
    def check_neuron(self, dt):
        pipe = self.get_next_pipe()
        dx = (pipe.x - self.bird.x)/10
        dy1 = (pipe.y - self.bird.y)/10
        dy2 = (pipe.y + c.PIPE_GAP - self.bird.y)/10
        
        if dx*self.w1 + dy1*self.w2 + dy2*self.w3 >= 1.0:
            self.bird.jump(dt)

class GeneticAI():
    def __init__(self, FLA):
        self.FLA = FLA
        self.birdAIs = []
        self.pop_size = 40
        self.w_u = 10
        self.w_l = -10
        self.init_pop()
        
    def return_birds(self):
        birds = []
        for b in self.birdAIs:
            birds.append(b.bird)
        
        return birds
    
    def init_pop(self):
        for _ in range(self.pop_size):
            self.birdAIs.append(BirdAI(self.FLA, Bird(self.FLA.screen), random.uniform(self.w_l,self.w_u), 
                                       random.uniform(self.w_l,self.w_u), random.uniform(self.w_l,self.w_u)))       
    
    def check_generation(self, force=0): 
        if self.all_alive() and not force: return
        
        print("New Generation Made!")
        
        for b in self.birdAIs:
            if b.bird.alive:
                b.bird.alive = 0
                b.bird.score = self.FLA.cur_score
        
        self.birdAIs = self.selection() # contains top half     
        
        if len(self.birdAIs) <= 0:
            self.init_pop()
            return True
           
        self.birdAIs += self.crossover(self.birdAIs)
        
        to_mutate = [random.choice(self.birdAIs) for _ in range(self.pop_size - len(self.birdAIs))]
        self.birdAIs += self.mutate(to_mutate)

        return True
    
    def move_AI(self, dt):
        for b in self.birdAIs:
            b.check_neuron(dt)
        
    
    def all_alive(self):
        for b in self.birdAIs:
            if b.bird.alive:
                return True
        
        return False
        
    def selection(self):
        scores = []
        best = []
        for b in self.birdAIs:
            scores.append((b.bird.score, b))
        
        scores = sorted(scores, key=lambda x: x[0])
        scores = scores[self.pop_size//2:]
        
        best_bird = scores[-1][1]
        print("Best bird:", best_bird.bird.score, "w1:", best_bird.w1, "w2:", best_bird.w2, "w3:", best_bird.w3)

        if best_bird.bird.score <= 0: # too bad
            return []
        
        for s in scores:
            best.append(BirdAI(self.FLA, Bird(self.FLA.screen), s[1].w1, s[1].w2, s[1].w3))
        
        return best

    def crossover(self, best):
        children = []
        n = len(best)
        for i in range(n//2):
            w1 = (best[i].w1 + best[n-i-1].w1) / 2
            w2 = (best[i].w2 + best[n-i-1].w2) / 2
            w3 = (best[i].w3 + best[n-i-1].w3) / 2
            children.append(BirdAI(self.FLA, Bird(self.FLA.screen), w1, w2, w3))
        
        return children
    
    def mutate(self, to_mutate):
        children = []
        for i in to_mutate:
            w1 = i.w1 + random.uniform(-1, 1)
            w2 = i.w2 + random.uniform(-1, 1)
            w3 = i.w3 + random.uniform(-1, 1)
            children.append(BirdAI(self.FLA, Bird(self.FLA.screen), w1, w2, w3))
        
        return children
        