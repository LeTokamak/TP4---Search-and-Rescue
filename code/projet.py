from projet_import import Speeder, Climber, Message, robots, run_single_server

taille_case =  1/8
centre_case = (1/8)/2

liste_etape_climber_gauche = [[4, 7], [0, 7], [0, 0], [3, 0], 
                              [3, 1], [1, 1], [1, 6], [4, 6], 
                              [4, 5], [2, 5], [2, 2], [3, 2], 
                              [3, 4]
                              ]

liste_etape_climber_droite = [[4, 7], [7, 7], [7, 0], [3, 0],
                              [3, 1], [6, 1], [6, 6], [4, 6], 
                              [4, 5], [5, 5], [5, 2], [3, 2], 
                              [3, 4]
                              ]

team = []  

accusee_reception = "Message bien reçu."                  

class Speeder_chef(Speeder):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.recoit_message = True
        self.envoie_message = False
        
    def step(self):
        msgs = self.receive()
        for m in msgs :
            print(m)

class Climber_gauche(Climber):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = 0
        self.recherche_terminee = False
        self.liste_objet_connu = []
        self.recoit_message = False
        self.envoie_message = True
    
    def deplacement(self):
        destination_x = liste_etape_climber_gauche[self.etape][0]*(taille_case) + centre_case
        destination_y = liste_etape_climber_gauche[self.etape][1]*(taille_case) + centre_case
        
        if   (not self.recherche_terminee) and (self.x != destination_x or self.y != destination_y) :
            self.goto(destination_x, destination_y)
        elif (not self.recherche_terminee) :
            self.etape += 1
            if self.etape == len(liste_etape_climber_gauche):
                self.etape = -1
                self.recherche_terminee = True

    def crie(self):
        for robot in self.model.retrieve_robots():
            if robot.recoit_message and self.liste_objet_connu != []:
                message = Message(robot, self, self.liste_objet_connu, "Information")
                
                self.send(message)
    
    def ecoute_accusee_reception(self):
        for message in self.receive():
            if message.sender.isinstance(Speeder):
                if accusee_reception == message.content :
                    return True
        return False
        
    def step(self):
        self.deplacement()
        
        objets_detectees = self.sense()
        for objet in objets_detectees:
            if objet not in self.liste_objet_connu:
                print("Nouvel objet détecté : ", objet)
                self.liste_objet_connu.append(objet)
                
        self.crie()
        
        accusee_reception_recu = self.ecoute_accusee_reception()
        
        

class Climber_droite(Climber):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = 0
        self.recherche_terminee = False
        self.liste_objet_connu = []
        self.recoit_message = False
        self.envoie_message = True
        
    def deplacement(self):
        destination_x = liste_etape_climber_droite[self.etape][0]*(taille_case) + centre_case
        destination_y = liste_etape_climber_droite[self.etape][1]*(taille_case) + centre_case
        
        if   (not self.recherche_terminee) and (self.x != destination_x or self.y != destination_y) :
            self.goto(destination_x, destination_y)
        elif (not self.recherche_terminee) :
            self.etape += 1
            if self.etape == len(liste_etape_climber_droite):
                self.etape = -1
                self.recherche_terminee = True
    
    def crie(self):
        for robot in self.model.retrieve_robots():
            if robot.recoit_message and self.liste_objet_connu != []:
                message = Message(robot, self, self.liste_objet_connu, "Information")

                self.send(message)
                    
                    
    def ecoute_accusee_reception(self):
        for message in self.receive():
            if message.sender.isinstance(Speeder):
                if accusee_reception == message.content :
                    return True
        return False
                    
    def step(self):
        self.deplacement()
        
        objets_detectees = self.sense()
        for objet in objets_detectees:
            if objet not in self.liste_objet_connu:
                print("Nouvel objet détecté : ", objet)
                self.liste_objet_connu.append(objet)
                
        self.crie()
        
        accusee_reception_recu = self.ecoute_accusee_reception()

team.append(Speeder_chef)
team.append(Climber_gauche)
team.append(Climber_droite)

if __name__ == "__main__":
    run_single_server(team)
