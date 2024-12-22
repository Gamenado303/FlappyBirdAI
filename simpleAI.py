import c

class SimpleAI():
    def __init__(self, FLA, bird):
        self.FLA = FLA
        self.bird = bird
        
    def get_next_pipe(self):
        for pipe in self.FLA.pipes:
            if pipe.x + c.NECK_WIDTH > c.START_X:
                return pipe
    
    def check_jump(self, dt):
        pipe = self.get_next_pipe()
        if self.bird.y > pipe.y + c.PIPE_GAP - 2*c.NECK_HEIGHT:
            self.bird.jump(dt)