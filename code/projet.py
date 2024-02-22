from projet_import import Rover, Speeder, Balloon, Climber, run_single_server, Message, Person, RescueItem
import random

class Dragster(Speeder):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = "setup"
        self.mailbox = []
        self.person = ""
        self.items = []
        self.items_rescued = 0

    def step(self):
        if self.etape == "setup":
            self.goto(0.51,0.51)
            if self.x == 0.51 and self.y == 0.51 :
                self.etape = "info"
                print("dragster info")
        if self.etape == "info":
            messages = self.receive()
            if len(messages) != 0 :
                for msg in messages :
                    if isinstance(msg.body,Person) :
                        self.person = msg.body
                    if isinstance(msg.body,RescueItem) :
                            if len(self.items) == 0 :
                                self.items.append(msg.body)
                            else :
                                for elt in self.items :    
                                    if msg.body != elt :
                                        self.items.append(msg.body)
            if len(self.items) >= 2 and self.person != "" :
                self.etape = "rescue"
                print("dragster rescue")

        if self.etape == "rescue" :
            if self.taken_item == None and self.x != self.items[self.items_rescued].x and self.y != self.items[self.items_rescued].y :
                self.goto(self.items[self.items_rescued].x,self.items[self.items_rescued].y)
            elif self.taken_item == None and self.x == self.items[self.items_rescued].x and self.y == self.items[self.items_rescued].y :
                self.take(self.items[self.items_rescued])
            elif self.taken_item != None and self.x != self.person.x and self.y != self.person.y :
                self.goto(self.person.x,self.person.y)
            elif self.taken_item != None and self.x == self.person.x and self.y == self.person.y :
                self.drop_item()
                self.items_rescued += 1
                if self.items_rescued > 1 :
                    self.etape = "fin"

        if self.etape == "fin" :
            self.goto(0.5,0.55) 

class Antenne(Balloon):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = [[0.317,0.317],[0.317,1-0.317],[1-0.317,1-0.317],[1-0.317,0.317],[0.317,0.317],[0.5,0.5]]
        self.step_traj = 0
        self.list_obj = []
        self.list_msg = []
    
    def step(self):
        liste = self.sense()
        for elt in liste :
            if elt not in self.list_obj:
                self.list_obj.append(elt)

        if self.step_traj <= 4 :
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
                self.step_traj += 1

        if self.step_traj == 5 :
            list_rob = self.model.retrieve_robots()
            self.goto(0.5,0.5)
            if self.x == 0.5 and self.y == 0.5 :
                for elt in self.list_obj:
                    i=1
                    for robot in list_rob:
                        if isinstance(robot,Dragster):
                            self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                            print(f"msg ballon {i}")
                            i += 1
                self.step_traj += 1

        else :
            for message in self.list_msg :
                self.send(message)
                print("message ballon sent")      


class Drone_reco(Climber) :
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = "reco"
        self.trajectoire = [[0.0750*2,0.0750*2],[0.0625,0.0625],[0.0625,1-0.0625],[0.0750*2,1-0.0750*2],[0.0625,1-0.0625],[1-0.0625,1-0.0625],[1-0.0750*2,1-0.0750*2],[1-0.0625,1-0.0625],[1-0.0625,0.0625],[1-0.0750*2,0.0750*2],[1-0.0625,0.0625],[0.0625,0.0625]]
        self.step_traj = 0
        self.list_msg = []
        self.list_obj = []
        self.nbs_obj = 0

    def step(self):
        
        liste = self.sense()
        for elt in liste :
            if elt not in self.list_obj:
                self.list_obj.append(elt)
        if self.etape == "reco":
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] : 
                self.step_traj += 1
                if self.step_traj > 11 :
                    self.etape = "traj_comm"
        
        elif self.etape == "traj_comm" :
            list_rob = self.model.retrieve_robots()
            self.goto(0.5,0.5)
            if self.x == 0.5 and self.y == 0.5 :
                for elt in self.list_obj:
                    i = 1
                    for robot in list_rob:
                        if isinstance(robot,Dragster):
                            self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                            print(f"msg Climber {i}")
                            i += 1
                self.etape = "comm"

        elif self.etape == "comm" :
            for message in self.list_msg :
                self.send(message)
                print("message climber sent")

class Dragster2(Speeder):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = "setup"
        self.mailbox = []
        self.person = ""
        self.items = []
        self.items_rescued = 0
        self.items_brought = 0

    def step(self):
        liste = self.sense()
        for elt in liste :
            if isinstance(elt,RescueItem) and elt not in self.items:
                self.items.append(elt)
            elif isinstance(elt,Person) :
                self.person = elt

        if self.etape == "setup":
            self.goto(0.51,0.51)
            if self.x == 0.51 and self.y == 0.51 :
                self.etape = "info"

        if self.etape == "info":
            messages = self.receive()
            if len(messages) != 0 :
                for msg in messages :
                    if isinstance(msg.body,Person) :
                        self.person = msg.body
                    if isinstance(msg.body,RescueItem) :
                            if len(self.items) == 0 :
                                self.items.append(msg.body)
                            else :
                                for elt in self.items :    
                                    if msg.body != elt :
                                        self.items.append(msg.body)
            if len(self.items) > self.items_rescued and self.person != "" :
                self.etape = "rescue"
            elif len(self.items) > self.items_brought and self.person == "" :
                self.etape = "bring"

        if self.etape == "rescue" :
            if self.taken_item == None and self.x != self.items[self.items_rescued].x and self.y != self.items[self.items_rescued].y :
                self.goto(self.items[self.items_rescued].x,self.items[self.items_rescued].y)
            elif self.taken_item == None and self.x == self.items[self.items_rescued].x and self.y == self.items[self.items_rescued].y :
                self.take(self.items[self.items_rescued])
            elif self.taken_item != None and self.x != self.person.x and self.y != self.person.y :
                self.goto(self.person.x,self.person.y)
            elif self.taken_item != None and self.x == self.person.x and self.y == self.person.y :
                self.drop_item()
                self.items_rescued += 1
                if len(self.items) == self.items_rescued :
                    self.etape = "setup"

        if self.etape == "bring":
            if self.taken_item == None and self.x != self.items[self.items_brought].x and self.y != self.items[self.items_brought].y :
                self.goto(self.items[self.items_brought].x,self.items[self.items_brought].y)
            elif self.taken_item == None and self.x == self.items[self.items_brought].x and self.y == self.items[self.items_brought].y :
                self.take(self.items[self.items_brought])
            elif self.taken_item != None and self.x != 0.51 and self.y != 0.51 :
                self.goto(0.51,0.51)
            elif self.taken_item != None and self.x == 0.51 and self.y == 0.51 :
                self.drop_item()
                self.items_brought += 1
                if len(self.items) == self.items_brought :
                    self.etape = "info"

        """self.goto(self.destination[0],self.destination[1])
        if self.x == self.destination[0] and self.y == self.destination[1] :
            self.destination = [(random.randint(1,8)/8)-(1/16),(random.randint(1,8)/8)-(1/16)]"""

class Antenne2(Balloon):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = "reco"
        self.trajectoire = [[0.317,0.317],[0.317,0.5],[0.317,1-0.317],[0.5,1-0.317],[1-0.317,1-0.317],[1-0.317,0.5],[1-0.317,0.317],[0.5,0.317],[0.317,0.317],[0.5,0.5]]
        self.step_traj = 0
        self.list_msg = []
        self.list_obj = []
    
    def step(self):
        liste = self.sense()
        for elt in liste :
            if elt not in self.list_obj:
                self.list_obj.append(elt)

        if self.etape == "reco" :
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
                self.step_traj += 1
                if self.step_traj % 2 == 0 :
                    self.etape = "pre_comm"


        if self.etape == "pre_comm" :
            list_rob = self.model.retrieve_robots()
            for elt in self.list_obj:
                i=1
                for robot in list_rob:
                    if isinstance(robot,Dragster2):
                        self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                        print(f"msg ballon {i}")
                        i += 1
            self.etape = "comm"

        if self.etape == "comm" :
            for message in self.list_msg :
                self.send(message)
                print("message ballon sent")
            if self.step_traj < 10:
                self.etape = "reco"

class Drone_reco2(Climber) :
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = "reco"
        self.trajectoire = [[0.0750*2,0.0750*2],[0.0625,0.0625],[0.0625,1-0.0625],[0.0750*2,1-0.0750*2],[0.0625,1-0.0625],[1-0.0625,1-0.0625],[1-0.0750*2,1-0.0750*2],[1-0.0625,1-0.0625],[1-0.0625,0.0625],[1-0.0750*2,0.0750*2],[1-0.0625,0.0625],[0.0625,0.0625]]
        self.step_traj = 0
        self.list_msg = []
        self.list_obj = []
        self.nbs_obj = 0
        self.waiting_time = 0

    def step(self):
        
        liste = self.sense()
        for elt in liste :
            if elt not in self.list_obj:
                self.list_obj.append(elt)
        if self.etape == "reco":
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] : 
                self.step_traj += 1
                if self.step_traj > 11 or len(self.list_obj) != self.nbs_obj :
                    if len(self.list_obj) != self.nbs_obj :
                        self.step_traj -= 1
                    self.nbs_obj = len(self.list_obj)
                    self.etape = "traj_comm"
        
        elif self.etape == "traj_comm" :
            self.goto(0.5,0.5)
            if self.x == 0.5 and self.y == 0.5 :
                list_rob = self.model.retrieve_robots()
                for elt in self.list_obj:
                    i = 1
                    for robot in list_rob:
                        if isinstance(robot,Dragster2):
                            self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                            print(f"msg Climber {i}")
                            i += 1
                self.etape = "comm"

        elif self.etape == "comm" :
            for message in self.list_msg :
                self.send(message)
                print("message climber sent")
            if self.step_traj <= 11 :
                if self.waiting_time < 10 :
                    self.waiting_time +=1
                else :
                    self.waiting_time = 0
                    self.etape = "reco"
        


if __name__ == "__main__":
    team = [Drone_reco2, Antenne2, Dragster2]
    run_single_server(team)
