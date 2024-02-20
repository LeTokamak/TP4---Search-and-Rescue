from projet_import import Speeder, Climber, Message, robots, run_single_server
import random as rd

taille_case =  1/8
centre_case = (1/8)/2

coordonnees_spawn = [0.5, 0.5]

case_QG = [3, 4]
case_QG_droite = [4, 4]
coordonnees_QG = [case_QG[0]*(taille_case) + centre_case, 
                  case_QG[1]*(taille_case) + centre_case]

liste_etape_climber_gauche = [[3, 7], [0, 7], [0, 0], [3, 0], 
                              [3, 1], [1, 1], [1, 6], [3, 6], 
                              [3, 5], [2, 5], [2, 2], [3, 2], 
                              case_QG
                              ]

liste_etape_climber_droite = [[4, 7], [7, 7], [7, 0], [4, 0],
                              [4, 1], [6, 1], [6, 6], [4, 6], 
                              [4, 5], [5, 5], [5, 2], [4, 2], 
                              case_QG_droite, case_QG
                              ]

team = []  

accusee_reception = "Message bien reçu."                  

class Speeder_chef(Speeder):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.recoit_message = True
        self.envoie_message = False
        
        self.objets_connus = []
        
        self.etape = 0
    
    def envoie_accusee_reception(self, message):
        message = Message(message.sender, self, accusee_reception, "Accusee_reception")
        self.send(message)
    
    def case_actuelle(self):
        return [round((self.x - centre_case)/taille_case), 
                round((self.y - centre_case)/taille_case)]
        
    def analyse_boite_aux_lettres(self):
        msgs = self.receive()
        for m in msgs :
            if isinstance(m.body, list):
                for objet in m.body:
                    if objet not in self.objets_connus:
                        self.objets_connus.append(objet)
            self.envoie_accusee_reception(m)
    
    def step(self):
        # Etape 0 et 1: Le Speeder explore le QG
        if self.etape <= 1:
            for QG in [case_QG, case_QG_droite]:
                coordonnees_QG = [QG[0]*(taille_case) + centre_case, 
                                  QG[1]*(taille_case) + centre_case]
                
                self.goto(*coordonnees_QG)
                
                if [self.x, self.y] == coordonnees_QG:
                    self.etape += 1
        
        # Etape 2 : Le Speeder attent un ordre de mission
        if self.etape == 2:
            pass
        
        
        
        # Etape 3 : Le Speeder recoie une mission
        if self.etape == 3:
            pass
            
            
        print(self.etape)
        print(self.x, self.y)
        print(self.x/taille_case, self.y/taille_case)
        print(self.case_actuelle())
        
        

class Climber_perso(Climber):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        # Variable de communication
        self.recoit_message = False
        self.envoie_message = True
        self.rapport_en_cours = False
        self.accusee_reception_recu = False
        
        # Variable de recherche
        self.etape = 0
        self.recherche_terminee = False
        self.liste_objet_connu = []
        self.trajectoire = []
        self.ancienne_position = []
    
    def deplacement_recherche(self):
        destination_x = self.trajectoire[self.etape][0]*(taille_case) + centre_case
        destination_y = self.trajectoire[self.etape][1]*(taille_case) + centre_case
        
        if   (not self.recherche_terminee) and (self.x != destination_x or self.y != destination_y) :
            self.goto(destination_x, destination_y)
        elif (not self.recherche_terminee) :
            self.etape += 1
            if self.etape == len(self.trajectoire):
                self.etape = -1
                self.recherche_terminee = True

    def detection(self):
        objets_detectes = self.sense()
        for objet in objets_detectes:
            if objet not in self.liste_objet_connu:
                self.liste_objet_connu.append(objet)
                self.ancienne_position = [self.x, self.y]
                self.rapport_en_cours = True
                
    def crie(self):
        for robot in self.model.retrieve_robots():
            if robot.recoit_message and self.liste_objet_connu != []:
                message = Message(robot, self, self.liste_objet_connu, "Information")
                
                self.send(message)
    
    def ecoute_accusee_reception(self):
        for message in self.receive():
            if isinstance(message.sender, Speeder):
                if accusee_reception == message.body :
                    return True
        return False
        
    def step(self):
        if not self.rapport_en_cours:
            self.deplacement_recherche()
        else :
            if not self.accusee_reception_recu :
                self.goto(*coordonnees_QG)
                self.crie()
                self.accusee_reception_recu = self.ecoute_accusee_reception()
            else :
                self.goto(*self.ancienne_position)
                if [self.x, self.y] == self.ancienne_position:
                    self.rapport_en_cours = False
                    self.accusee_reception_recu = False
                    self.ancienne_position = []
                    self.receive() # On vide la liste de message pour ne pas garder d'accusé de réception
        
        self.detection()
        
        
class Climber_gauche(Climber_perso):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = liste_etape_climber_gauche
        

class Climber_droite(Climber_perso):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = liste_etape_climber_droite

team.append(Speeder_chef)
team.append(Climber_gauche)
team.append(Climber_droite)

if __name__ == "__main__":
    run_single_server(team)
