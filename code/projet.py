from projet_import import Rover, Speeder, Balloon, Climber, run_single_server

class Dragster(Speeder):
    def _init_(self, x, y, model, environment):
        super().__init__(self, x, y, model, environment)

    def step(self):
        self.goto(0.1,0.1)

class drone_reco(Balloon):
    def _init_(self, x, y, model, environment):
        super().__init__(self, x, y, model, environment)
    
    def step(self):
        self.goto(0.1,0.1)


if __name__ == "__main__":
    team = [drone_reco, Dragster]
    run_single_server(team)
