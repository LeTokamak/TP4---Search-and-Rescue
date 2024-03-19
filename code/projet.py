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
            if self.x != 0.51 and self.y != 0.51 :
                self.goto(0.51,0.51)

        messages = self.receive()
        if len(messages) != 0 :
            for msg in messages :
                if isinstance(msg.body,Person) :
                    self.person = msg.body
                if isinstance(msg.body,RescueItem) :
                    if msg.body not in self.items :
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
                if len(self.items) >= self.items_rescued :
                    self.etape = "setup"
                    if len(self.items)>1:
                        if self.items_rescued == 1 and (self.items[self.items_rescued].x == self.person.x and self.items[self.items_rescued].y == self.person.y) :
                            self.items_rescued = 0

        if self.etape == "bring":
            if self.taken_item == None and self.x != self.items[self.items_brought].x and self.y != self.items[self.items_brought].y :
                self.goto(self.items[self.items_brought].x,self.items[self.items_brought].y)
            elif self.taken_item == None and self.x == self.items[self.items_brought].x and self.y == self.items[self.items_brought].y :
                self.take(self.items[self.items_brought])
            elif self.taken_item != None and self.x != 0.51 and self.y != 0.51 :
                self.goto(0.51,0.51+0.03*self.items_brought)
            elif self.taken_item != None and self.x == 0.51 and self.y == 0.51 :
                self.drop_item()
                self.items_brought += 1
                if len(self.items) == self.items_brought :
                    self.etape = "setup"

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

        messages = self.receive()
        if len(messages) != 0 :
            for msg in messages :
                if msg.body not in self.list_obj :
                    self.list_obj.append(msg.body)

        if self.etape == "reco" :
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
                self.step_traj += 1
                if self.step_traj % 2 == 0 :
                    self.etape = "comm"


        if self.etape == "comm" :
            list_rob = self.model.retrieve_robots()
            for elt in self.list_obj:
                for robot in list_rob:
                    if isinstance(robot,Dragster2):
                        self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                    if isinstance(robot,Drone_reco2):
                        self.list_msg.append(Message(robot,self,elt,"informer","position item"))
            if self.step_traj < 10:
                self.etape = "reco"

        if self.list_msg != [] :
            for message in self.list_msg :
                self.send(message)

class Drone_reco2(Climber) :
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = "reco"
        self.trajectoire = [[0.0625,0.5],[0.0625,1-0.0625],[0.0750*2,1-0.0750*2],[0.0625,1-0.0625],[0.5,1-0.0625],[1-0.0625,1-0.0625],[1-0.0750*2,1-0.0750*2],[1-0.0625,1-0.0625],[1-0.0625,0.5],[1-0.0625,0.0625],[1-0.0750*2,0.0750*2],[1-0.0625,0.0625],[0.5,0.0625],[0.0625,0.0625],[0.0750*2,0.0750*2],[0.0625,0.0625],[0.0625,0.5]]
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

        messages = self.receive()
        if len(messages) != 0 :
            for msg in messages :
                if msg.body not in self.list_obj :
                    self.list_obj.append(msg.body)
        
        if self.etape == "reco":
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] : 
                self.step_traj += 1
                if self.step_traj > 16 or (len(self.list_obj) != self.nbs_obj and (self.step_traj-1) % 4 == 0) :
                    if len(self.list_obj) != self.nbs_obj :
                        self.step_traj -= 1
                    self.nbs_obj = len(self.list_obj)
                    self.etape = "comm"
        
        elif self.etape == "comm" :
            self.goto(0.5,0.5)
            if self.x == 0.5 and self.y == 0.5 :
                list_rob = self.model.retrieve_robots()
                for elt in self.list_obj:
                    for robot in list_rob:
                        if isinstance(robot,Dragster2):
                            self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                        if isinstance(robot,Antenne2):
                            self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                if self.step_traj < 16:
                    self.etape = "reco"

        if self.list_msg != [] :
            for message in self.list_msg :
                self.send(message)

class Dragster3(Speeder):
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
            if self.x != 0.51 and self.y != 0.51 :
                self.goto(0.51,0.51)

        messages = self.receive()
        if len(messages) != 0 :
            for msg in messages :
                if isinstance(msg.body,Person) :
                    self.person = msg.body
                if isinstance(msg.body,RescueItem) :
                    if msg.body not in self.items :
                        self.items.append(msg.body)
                if isinstance(msg.sender,Climber) :
                    list_rob = self.model.retrieve_robots()
                    for robot in list_rob:
                        if isinstance(robot,Climber):
                            self.send(Message(robot,self,"Merci pour l'information","confirmer","reception position item"))
                
                    
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
                if len(self.items) >= self.items_rescued :
                    self.etape = "setup"
                    if len(self.items)>1:
                        if self.items_rescued == 1 and (self.items[self.items_rescued].x == self.person.x and self.items[self.items_rescued].y == self.person.y) :
                            self.items_rescued = 0

        if self.etape == "bring":
            if self.taken_item == None and self.x != self.items[self.items_brought].x and self.y != self.items[self.items_brought].y :
                self.goto(self.items[self.items_brought].x,self.items[self.items_brought].y)
            elif self.taken_item == None and self.x == self.items[self.items_brought].x and self.y == self.items[self.items_brought].y :
                self.take(self.items[self.items_brought])
            elif self.taken_item != None and self.x != 0.51 and self.y != 0.51 :
                self.goto(0.51+0.01*self.items_brought,0.51)
            elif self.taken_item != None and self.x == 0.51 and self.y == 0.51 :
                self.drop_item()
                self.items_brought += 1
                if len(self.items) == self.items_brought :
                    self.etape = "setup"

        """self.goto(self.destination[0],self.destination[1])
        if self.x == self.destination[0] and self.y == self.destination[1] :
            self.destination = [(random.randint(1,8)/8)-(1/16),(random.randint(1,8)/8)-(1/16)]"""

class Antenne3(Balloon):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = "reco"
        self.trajectoire = [[0.5,0.317],[0.317,0.317],[0.317,0.5],[0.317,1-0.317],[0.5,1-0.317],[1-0.317,1-0.317],[1-0.317,0.5],[1-0.317,0.317],[0.5,0.317],[0.5,0.5]]
        self.step_traj = 0
        self.list_msg = []
        self.list_obj = []
    
    def step(self):
        liste = self.sense()
        for elt in liste :
            if elt not in self.list_obj:
                self.list_obj.append(elt)

        messages = self.receive()
        if len(messages) != 0 :
            for msg in messages :
                if msg.body not in self.list_obj :
                    self.list_obj.append(msg.body)

        if self.etape == "reco" :
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] :
                self.step_traj += 1
            self.etape = "comm"


        if self.etape == "comm" :
            self.list_msg = []
            list_rob = self.model.retrieve_robots()
            for elt in self.list_obj:
                for robot in list_rob:
                    if isinstance(robot,Dragster3):
                        self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                    if isinstance(robot,Drone_reco3):
                        self.list_msg.append(Message(robot,self,elt,"informer","position item"))
            if self.step_traj < 10:
                self.etape = "reco"

        if self.list_msg != [] :
            for message in self.list_msg :
                self.send(message)
            

class Drone_reco3(Climber) :
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = "reco"
        self.trajectoire = [[0.0625,0.5],[0.0625,1-0.09*2],[0.0750*2,1-0.0750*2],[0.0625,1-0.0625],[1-0.09*2,1-0.0625],[1-0.0750*2,1-0.0750*2],[1-0.0625,1-0.0625],[1-0.0625,0.5],[1-0.0625,0.09*2],[1-0.0750*2,0.0750*2],[1-0.0625,0.0625],[0.09*2,0.0625],[0.0750*2,0.0750*2],[0.0625,0.0625],[0.0625,0.5]]
        self.step_traj = 0
        self.list_msg = []
        self.list_obj = []
        self.nbs_obj = 0
        self.msg_recu = False

    def step(self):
        
        liste = self.sense()
        for elt in liste :
            if elt not in self.list_obj:
                self.list_obj.append(elt)

        messages = self.receive()
        if len(messages) != 0 :
            for msg in messages :
                if msg.body not in self.list_obj and msg.performative == "informer" :
                    self.list_obj.append(msg.body)
                    self.nbs_obj += 1
                if msg.performative == "confirmer" :
                    self.msg_recu = True
        
        if len(self.list_obj) == 3 :
            self.step_traj = 16
            self.etape = "comm"
        
        if self.etape == "reco":
            self.goto(self.trajectoire[self.step_traj][0],self.trajectoire[self.step_traj][1])
            if self.x == self.trajectoire[self.step_traj][0] and self.y == self.trajectoire[self.step_traj][1] : 
                self.step_traj += 1
                if self.step_traj > 14 or (len(self.list_obj) != self.nbs_obj and (self.step_traj == 8)) :
                    self.nbs_obj = len(self.list_obj)
                    self.etape = "comm"
        
        elif self.etape == "comm" :
            self.goto(0.5,0.5)
            self.list_msg = []
            list_rob = self.model.retrieve_robots()
            for elt in self.list_obj:
                for robot in list_rob:
                    if isinstance(robot,Dragster3):
                        self.list_msg.append(Message(robot,self,elt,"informer","position item"))
                    if isinstance(robot,Antenne3):
                        self.list_msg.append(Message(robot,self,elt,"informer","position item"))
            if self.step_traj < 14 and self.msg_recu == True:
                self.nbs_obj = len(self.list_obj)
                self.step_traj -= 1
                self.etape = "reco"

        if self.list_msg != [] :
            for message in self.list_msg :
                self.send(message)
        


if __name__ == "__main__":
    team = [Antenne3,Dragster3,Drone_reco3]
    run_single_server(team)
