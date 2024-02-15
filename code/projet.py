from projet_import import Rover, Speeder, Balloon, Climber, run_single_server

class RoverA(Rover):
    def step(self):
        self.goto(0.1, 0.1)

if __name__ == "__main__":
    team = ["PLEIN DE ROBOTS"]
    run_single_server(team)
