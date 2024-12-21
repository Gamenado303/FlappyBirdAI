import c

class SimpleAI():
    def __init__(self, FLA):
        self.FLA = FLA
        
    def get_next_pipe(self):
        for pipe in self.FLA.pipes:
            if pipe.x + c.NECK_WIDTH > self.FLA.x:
                return pipe
    
    def check_jump(self):
        pipe = self.get_next_pipe()
        if self.FLA.y > pipe.y + c.PIPE_GAP - 2*c.NECK_HEIGHT:
            self.FLA.jump()
