from projet_import import Speeder, Climber, Message, Person, robots, run_single_server
import random as rd

taille_case =  1/8
centre_case = (1/8)/2

coordonnees_spawn = [3.5*(taille_case) + centre_case, 4*(taille_case) + centre_case]

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

OBJET_TO_QG = "Amener un objet au QG"
OBJET_TO_PERSONNE = "Amener un objet à une personne"

class Speeder_chef(Speeder):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.recoit_message = True
        self.envoie_message = False
        
        self.objets_connus = []
        self.objet_objectif = None
        
        self.personne = None
        self.objets_au_QG = []
        self.objets_sur_personne = []
        
        self.mission = None
        
        self.etape_mission = 0
        self.etape = 0
    
    def envoie_accusee_reception(self, message):
        message = Message(message.sender, self, accusee_reception, "Accusee_reception")
        self.send(message)
    
    def case_actuelle(self):
        return [round((self.x - centre_case)/taille_case), 
                round((self.y - centre_case)/taille_case)]
        
    def analyse_boite_aux_lettres(self):
        liste_nouveaux_objets = []
        msgs = self.receive()
        for m in msgs :
            if isinstance(m.body, list):
                for objet in m.body:
                    if isinstance(objet, Person) :
                        self.personne = objet
                        
                    elif objet not in self.objets_connus:
                        self.objets_connus.append(objet)
                        liste_nouveaux_objets.append(objet)
                        
            self.envoie_accusee_reception(m)
        return liste_nouveaux_objets
    
    def mission_OBJET_TO_QG(self):
        # 1 - Récupération de l'objet
        if self.etape_mission == 0:
            self.goto(self.objet_objectif.x, self.objet_objectif.y)
            
            if [self.x, self.y] == [self.objet_objectif.x, self.objet_objectif.y]:
                self.etape_mission += 1
                self.take(self.objet_objectif)
    
    def mission_OBJET_TO_PERSONNE(self):
        # 1 - Récupération de l'objet
        if self.etape_mission == 0:
            self.goto(self.objet_objectif.x, self.objet_objectif.y)
            
            if [self.x, self.y] == [self.objet_objectif.x, self.objet_objectif.y]:
                self.etape_mission += 1
                self.take(self.objet_objectif)
         
        # 2 - Livraison de l'objet à la personne
        if self.etape_mission == 1:
            self.goto(self.personne.x, self.personne.y)
            
            if [self.x, self.y] == [self.personne.x, self.personne.y]:
                self.etape_mission = 0
                self.drop_item()
                self.objets_sur_personne.append(self.objet_objectif)
                self.objet_objectif = None
                self.mission = None
    
    def detection(self):
        objets_detectes = self.sense()
        for objet in objets_detectes:
            if objet not in self.objets_connus:
                if isinstance(objet, Person) :
                    self.personne = objet
                else :
                    self.objets_connus.append(objet)
        
    def step(self):
        
        # Etape 0 et 1: Le Speeder explore le QG
        if self.etape == 0 :
            destination = case_QG
        elif self.etape == 1 :
            destination = case_QG_droite
        
        if self.etape <= 1:
            coordonnees_QG = [destination[0]*(taille_case) + centre_case, 
                              destination[1]*(taille_case) + centre_case]
                
            self.goto(*coordonnees_QG)
                
            if [self.x, self.y] == coordonnees_QG:
                self.etape += 1
        
        # Etape 2 : Le Speeder attend un ordre de mission
        if self.etape == 2:
            self.goto(*coordonnees_spawn)
            
            
            
            # Si le Speeder sait où est la personne et qu'il a un objet au QG
            if self.personne != None:
                if len(self.objets_connus) != len(self.objets_au_QG) + len(self.objets_sur_personne):
                    objets_non_recuperes = [objet 
                                            for objet in self.objets_connus 
                                            if (objet not in self.objets_au_QG and objet not in self.objets_sur_personne)]
                    
                    self.mission = OBJET_TO_PERSONNE
                    self.objet_objectif = objets_non_recuperes[0]
                    self.mission = 3
                    self.etape_mission = 0
                    
                    self.mission_OBJET_TO_PERSONNE()
                    
                elif len(self.objets_au_QG) != 0:
                    self.mission = OBJET_TO_PERSONNE
                    self.objet_objectif = self.objets_au_QG[0]
                    self.etape = 3
                    self.etape_mission = 0
                    
                    self.objets_au_QG.remove(self.objet_objectif)
                    
                    self.mission_OBJET_TO_PERSONNE()
                    
            # Si le Speeder ne sais pas où est la personne
            else :
                if len(self.objets_connus) != len(self.objets_au_QG) + len(self.objets_sur_personne):
                    objets_non_recuperes = [objet 
                                            for objet in self.objets_connus 
                                            if (objet not in self.objets_au_QG and objet not in self.objets_sur_personne)]
                    
                    self.mission = OBJET_TO_QG
                    self.objet_objectif = objets_non_recuperes[0]
                    self.etape = 3
                    self.etape_mission = 0
                    
                    self.mission_OBJET_TO_QG()

        
        # Etape 3 : Le Speeder reçois une mission
        if self.etape == 3:
            if self.mission == OBJET_TO_QG:
                self.mission_OBJET_TO_QG()
                
            elif self.mission == OBJET_TO_PERSONNE:
                self.mission_OBJET_TO_PERSONNE()
        
        self.detection()
        self.analyse_boite_aux_lettres()
        
            
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
                self.goto(*self.coordonnees_position_rapport)
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
        self.coordonnees_position_rapport = [3.25*(taille_case)+centre_case, 
                                             4*(taille_case)+centre_case]
        

class Climber_droite(Climber_perso):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.trajectoire = liste_etape_climber_droite
        self.coordonnees_position_rapport = [3.75*(taille_case)+centre_case, 
                                             4*(taille_case)+centre_case]

team.append(Speeder_chef)
team.append(Climber_gauche)
team.append(Climber_droite)

if __name__ == "__main__":
    run_single_server(team)
