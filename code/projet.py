from projet_import import Speeder, Climber, run_single_server

taille_case =  1/8
centre_case = (1/8)/2

liste_etape_climber_gauche = [[4, 7], [0, 7], [0, 0], [3, 0], 
                              [3, 1], [1, 1], [1, 6], [4, 6], 
                              [4, 5], [2, 5], [2, 2], [3, 2], 
                              [3, 4]]

liste_etape_climber_droite = [[4, 7], [7, 7], [7, 0], [3, 0],
                              [3, 1], [6, 1], [6, 6], [4, 6], 
                              [4, 5], [5, 5], [5, 2], [3, 2], 
                              [3, 4]]
                            

class Speeder_chef(Speeder):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        
    def step(self):
        self.goto(0, 0)

class Climber_gauche(Climber):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = 0
        self.recherche_terminee = False
        
    def step(self):
        destination_x = liste_etape_climber_gauche[self.etape][0]*(taille_case) + centre_case
        destination_y = liste_etape_climber_gauche[self.etape][1]*(taille_case) + centre_case
        
        if   (not self.recherche_terminee) and (self.x != destination_x or self.y != destination_y) :
            self.goto(destination_x, destination_y)
        elif (not self.recherche_terminee) :
            self.etape += 1
            if self.etape == len(liste_etape_climber_gauche):
                self.etape = -1
                self.recherche_terminee = True

class Climber_droite(Climber):
    def __init__(self, x, y, model, environment):
        super().__init__(x, y, model, environment)
        self.etape = 0
        self.recherche_terminee = False
        
    def step(self):
        destination_x = liste_etape_climber_droite[self.etape][0]*(taille_case) + centre_case
        destination_y = liste_etape_climber_droite[self.etape][1]*(taille_case) + centre_case
        
        if   (not self.recherche_terminee) and (self.x != destination_x or self.y != destination_y) :
            self.goto(destination_x, destination_y)
        elif (not self.recherche_terminee) :
            self.etape += 1
            if self.etape == len(liste_etape_climber_droite):
                self.etape = -1
                self.recherche_terminee = True

if __name__ == "__main__":
    team = [Speeder_chef, Climber_gauche, Climber_droite]
    run_single_server(team)
