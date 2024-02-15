from projet_import import Rover, Speeder, Balloon, Climber, run_single_server

class Dragster(Speeder):
    def _init_(self, x, y, model, environment):
        super().__init__(self, x, y, model, environment)


if __name__ == "__main__":
    team = ["PLEIN DE ROBOTS"]
    run_single_server(team)
