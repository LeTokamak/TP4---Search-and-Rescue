from projet_import import Rover, Speeder, Balloon, Climber, run_single_server
import random;

class Dragster(Speeder):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.destination = [random.randint(0,100)/100,random.randint(0,100)/100]

    def step(self):
        self.goto(self.destination[0],self.destination[1])
        if self.x == self.destination[0] and self.y == self.destination[1] :
            self.destination = [random.randint(0,100)/100,random.randint(0,100)/100]

class Antenne(Balloon):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = [[0.325,0.325],[0.325,1-0.325],[1-0.325,1-0.325],[1-0.325,0.325]]
        self.step_traj = 0
    
    def step(self):
        self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
        if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
            self.step_traj += 1
            if self.step_traj > 3:
                self.step_traj = 0

class Drone_reco(Climber) :
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = [[0.0625,0.0625],[0.0625,1-0.0625],[1-0.0625,1-0.0625],[1-0.0625,0.0625]]
        self.step_traj = 0

    def step(self):
        self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
        if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
            self.step_traj += 1
            if self.step_traj > 3:
                self.step_traj = 0
        

if __name__ == "__main__":
    team = [Dragster, Antenne, Drone_reco]
    run_single_server(team)
