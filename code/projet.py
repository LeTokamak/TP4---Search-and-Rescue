from projet_import import Rover, Speeder, Balloon, Climber, run_single_server, Message
import random

class Dragster(Speeder):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.destination = [(random.randint(1,8)/8)-(1/16),(random.randint(1,8)/8)-(1/16)]

    def step(self):
        self.goto(self.destination[0],self.destination[1])
        if self.x == self.destination[0] and self.y == self.destination[1] :
            self.destination = [(random.randint(1,8)/8)-(1/16),(random.randint(1,8)/8)-(1/16)]

class Antenne(Balloon):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = [[0.310,0.310],[0.310,1-0.310],[1-0.310,1-0.310],[1-0.310,0.310],[0.310,0.310],[0.5,0.5]]
        self.step_traj = 0
    
    def step(self):
        if self.step_traj <= 5 :
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
                self.step_traj += 1
        
class Drone_reco(Climber) :
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = [[0.0700*2,0.0700*2],[0.0625,0.0625],[0.0625,1-0.0625],[0.0700*2,1-0.0700*2],[0.0625,1-0.0625],[1-0.0625,1-0.0625],[1-0.0700*2,1-0.0700*2],[1-0.0625,1-0.0625],[1-0.0625,0.0625],[1-0.0700*2,0.0700*2],[1-0.0625,0.0625],[0.0625,0.0625]]
        self.step_traj = 0
        self.list_obj = []
        self.list_msg = []


    def step(self):
        liste = self.sense()
        for elt in liste :
            if elt not in self.list_obj:
                self.list_obj.append(elt)

        if self.step_traj <= 11:
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
                self.step_traj += 1
        
        elif self.step_traj == 12 :
            self.goto(0.5,0.5)
            if self.x == 0.5 and self.y == 0.5 :
                '''for elt in self.list_obj:
                    self.list_msg.append(Message("Speeder","Climber",elt,"informer","position item"))'''
                self.step_traj += 1

        '''else :
            for message in self.list_msg :
                self.send(message)'''
        


if __name__ == "__main__":
    team = [Drone_reco, Antenne, Dragster]
    run_single_server(team)
