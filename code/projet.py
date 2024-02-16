from numpy import cos, pi, sin
from projet_import import Rover, Speeder, Balloon, Climber, run_single_server
import random;

class Rover1(Rover):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.destination = [(random.randint(1,8)/8)-(1/16),(random.randint(1,8)/8)-(1/16)]

    def step(self):
        self.goto(self.destination[0],self.destination[1])
        if self.x == self.destination[0] and self.y == self.destination[1] :
            self.destination = [(random.randint(1,8)/8)-(1/16),(random.randint(1,8)/8)-(1/16)]

class Ballon1(Balloon):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        
        r = 0.2
        theta = 5

        ListTrajectoire =[]
        
        for i in range (0, 360, theta) :

            x = 0.5 + r*cos(i*(2*pi/360))
            y = 0.5 + r*sin(i*(2*pi/360))
         
            A = [x, y]
            print(A)


            ListTrajectoire.append(A)

        print(ListTrajectoire)
        self.trajectoire = ListTrajectoire
        self.step_traj = 0
    
    def step(self):
        self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
        if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
            self.step_traj += 1
            if self.step_traj >= len(self.trajectoire):
                self.step_traj = 0



class Ballon2(Balloon):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        
        r = 0.2
        theta = 5

        ListTrajectoire =[]
        
        for i in range (0, 360, theta) :

            x = 0.5 - r*cos(i*(2*pi/360))
            y = 0.5 - r*sin(i*(2*pi/360))
         
            A = [x, y]
            print(A)


            ListTrajectoire.append(A)

        print(ListTrajectoire)
        self.trajectoire = ListTrajectoire
        self.step_traj = 0
    
    def step(self):
        self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
        if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
            self.step_traj += 1
            if self.step_traj >= len(self.trajectoire):
                self.step_traj = 0

class Climber1(Climber) :
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = [[0.0625,0.0625],[0.0625,1-0.0625],[1-0.0625,1-0.0625],[1-0.0625,0.0625]]
        self.step_traj = 0

    def step(self):
        self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
        if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
            self.step_traj += 1
            if self.step_traj >= len(self.trajectoire):
                self.step_traj = 0
        

if __name__ == "__main__":
    team = [Rover1, Ballon1, Ballon2, Climber1]
    run_single_server(team)
