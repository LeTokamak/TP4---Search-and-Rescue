import json  # Pour la sérialisation/désérialisation des objects
import math
import random
import string
from collections import defaultdict
from typing import List, Dict

import mesa
import mesa.space
import numpy as np
# import spade  # Framework multi-agents de messages
import networkx as nx  # Pour le parcours du réseau de planètes
from matplotlib import pyplot as plt
from mesa import Agent, Model
from threading import Lock  # Pour le mutual exclusion

from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from mesa.visualization import ModularVisualization
from mesa.visualization.ModularVisualization import VisualizationElement, ModularServer
from mesa.visualization.modules import ChartModule
from mesa_viz_tornado.UserParam import UserParam, Slider
import uuid  # Génération de Unique ID
import pyvisgraph as vg
from shapely import Polygon, unary_union, Point

NEW_ITEM_PROBA = 0.05
PROBA_ISSUE_ROAD = 0.05
ROAD_BRANCHING_FACTOR = 0.5
WAITING_TIME = 3
EPSILON = 1e-6
#random.seed(0)
mailing_boxes = {}


# vérifie l'intersection entre le segment[p1, p2] et [q1, q2]
def intersect(p1, p2, q1, q2) -> bool:
    x_p1, y_p1 = p1
    x_p2, y_p2 = p2
    x_q1, y_q1 = q1
    x_q2, y_q2 = q2
    denom = (y_q2 - y_q1) * (x_p2 - x_p1) - (x_q2 - x_q1) * (y_p2 - y_p1)
    if denom == 0:  # parallèle
        return False
    ua = ((x_q2 - x_q1) * (y_p1 - y_q1) - (y_q2 - y_q1) * (x_p1 - x_q1)) / denom
    if ua < 0 or ua > 1:  # hors segment
        return False
    ub = ((x_p2 - x_p1) * (y_p1 - y_q1) - (y_p2 - y_p1) * (x_p1 - x_q1)) / denom
    if ub < 0 or ub > 1:  # hors segment
        return False
    return True


class Maze(Agent):
    def __init__(self, planets: List, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        walls_file = open("./code/resources/walls.json", "r")
        self.walls = json.load(walls_file)
        walls_file.close()
        x_min = min([w["x1"] for w in self.walls] + [w["x2"] for w in self.walls])
        x_max = max([w["x1"] for w in self.walls] + [w["x2"] for w in self.walls])
        y_min = min([w["y1"] for w in self.walls] + [w["y2"] for w in self.walls])
        y_max = max([w["y1"] for w in self.walls] + [w["y2"] for w in self.walls])
        for w in self.walls:
            w['x1'] = (w["x1"] - x_min) / (x_max-x_min)
            w['x2'] = (w["x2"] - x_min) / (x_max-x_min)
            w['y1'] = (w["y1"] - y_min) / (y_max-y_min)
            w['y2'] = (w["y2"] - y_min) / (y_max-y_min)
        polys = [Polygon([(w["x1"], w["y1"]),
                          (w["x1"] + 0.001, w["y1"] + 0.001),
                          (w["x2"] + 0.001, w["y2"] + 0.001),
                          (w["x2"], w["y2"])])
                 for w in self.walls]
        multipoly = unary_union(polys)
        polys=[]
        self.shapely_polys = list(multipoly.geoms)

        for polygon in list(multipoly.geoms):
            polys.append(shapely_to_vizgraph(polygon))
        self.viz_graph = vg.VisGraph()
        self.viz_graph.build(polys)

    def step(self):
        pass

    def portrayal_method(self):
        portrayals = []
        for w in self.walls:
                portrayal = {"Shape": "line",
                             "width": 2,
                             "Layer": 1,
                             "Color": "white",
                             "from_x": w["x1"],
                             "from_y": w["y1"],
                             "to_x": w["x2"],
                             "to_y": w["y2"]
                             }
                portrayals.append(portrayal)
        return portrayals


def in_wall(x1, y1, x2, y2, px, py) -> bool:
    """
    check if (px, py) is on the segment [(x1, y1), (x2, y2)]
    """
    if px > max(x1, x2) or px < min(x1, x2) or py > max(y1, y2) or py < min(y1, y2):
        return False
    if x1 == x2:
        return min(y1, y2) <= py <= max (y1, y2)
    percent = (px - min(x1, x2))/(max(x1, x2) - min(x1, x2))
    return min(y1, y2) + percent * (max(y1, y2) - min(y1, y2)) == py


class Item:
    def __init__(self, environment: Maze, x=None, y=None):
        self.uid = uuid.uuid1()
        if not x:
            x = random.random()
        if not y:
            y = random.random()
        recompute = any([in_wall(w["x1"],w["y1"],w["x2"], w["y2"], x, y) for w in environment.walls])
        while recompute:
            x = random.random()
            y = random.random()
            recompute = any([in_wall(w["x1"],w["y1"],w["x2"], w["y2"], x, y) for w in environment.walls])
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Item) and self.uid == other.uid

    def __hash__(self):
        return int(self.uid)


class Person(Item):
    @staticmethod
    def portrayal_method():
        color = "yellow"
        r = 5
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": color,
                     "r": r}
        return portrayal


class RescueItem(Item):
    @staticmethod
    def portrayal_method():
        color = "blue"
        r = 2
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 2,
                     "Color": color,
                     "r": r}
        return portrayal


class Message:
    def __init__(self, to, sender, body, performative, thread=None):
        self.to = to
        self.sender = sender
        self.body = body
        self.performative = performative
        self.thread = thread

    def __str__(self):
        return (f"Message from {self.sender} to {self.to}; performative: {self.performative}; " +
                (f"thread: {self.thread}; " if self.thread != None else "") + "body:\n" + self.body)


class CommunicatingAgent(Agent):
    def __init__(self, unique_id: int, model: Model):
        super().__init__(unique_id, model)
        mailing_boxes[self] = []

    def send(self, msg) -> None:
        if isinstance(msg.to, CommunicatingAgent):  # Cas: 1 seul agent
            mailing_boxes[msg.to].append(msg)
        else:  # Cas: liste d'agents
            for agent in msg.to:
                mailing_boxes[agent].append(msg)

    def receive(self) -> List[Message]:
        messages = mailing_boxes[self].copy()
        mailing_boxes[self] = []
        return messages

    def __str__(self):
        return str(self.__class__.__name__) + str(self.unique_id)


def shapely_to_vizgraph(polygon: Polygon):
    xx, yy = polygon.exterior.coords.xy
    xx, yy = list(xx), list(yy)
    result = []
    for i in range(len(xx)):
        result.append(vg.Point(xx[i], yy[i]))
    return result


class Robot(CommunicatingAgent):
    def __init__(self, communication_range: float, moving_range:float, vision_range: float, price:int,
                 x: float, y: float, unique_id: int, model: Model, environment: Maze, terrestrial=False):
        super().__init__(unique_id, model)
        self.communication_range = communication_range
        self.moving_range = moving_range
        self.vision_range = vision_range
        self.x = x
        self.y = y
        self.environment = environment
        self.waypoint = None
        while any([polygon.contains(Point(self.x, self.y)) for polygon in self.environment.shapely_polys]):
            self.x = random.random()
            self.y = random.random()
        self.taken_item = None

    def goto(self, destination_x, destination_y):
        if (self.x, self.y) == (destination_x, destination_y):
            return
        success = False
        to_add = [(0, 0), (0, EPSILON), (0, -EPSILON), (EPSILON, 0), (-EPSILON, 0)]
        index = 0
        while not success and index < 5:
            if not any([polygon.intersects(Point(self.x + to_add[index][0], self.y + to_add[index][1]))
                        for polygon in self.environment.shapely_polys]):
                try:
                    shortest = self.environment.viz_graph.shortest_path(vg.Point(self.x + to_add[index][0], self.y + to_add[index][1]),
                                               vg.Point(destination_x, destination_y))
                    success = True
                except (KeyError, UnboundLocalError):
                    index = index + 1
                    success = False
            else:
                index = index + 1
                success = False
        if not success:
            print("Erreur! pas de chemin trouvé")
            print(f'position: {self.x}, {self.y}')
            return
        distance_covered = 0
        start = (self.x, self.y)
        next_point_index = 0
        while distance_covered < self.moving_range and next_point_index < len(shortest):
            next_point = (shortest[next_point_index].x, shortest[next_point_index].y)
            if distance(start, next_point) + distance_covered >= self.moving_range:
                percent = (self.moving_range - distance_covered) / distance(start, next_point)
                start = (start[0] + percent * (next_point[0]-start[0]), start[1] + percent * (next_point[1]-start[1]))
                distance_covered = self.moving_range
                self.waypoint = next_point
            else:
                distance_covered = distance_covered + distance(start, next_point)
                start = next_point
            next_point_index += 1
        self.x, self.y = start[0], start[1]
        if self.taken_item is not None:
            self.taken_item.x, self.taken_item.y = (self.x, self.y)

    def step(self) -> None:
        pass

    def sense(self) -> List[Item]:
        sensed = []
        for item in [i for i in self.model.items if distance((i.x, i.y), (self.x, self.y)) < self.vision_range]:
            if not any([intersect((item.x, item.y), (self.x, self.y), (w["x1"],w["y1"]),(w["x2"],w["y2"]))
                        for w in self.environment.walls]):
                sensed.append(item)
        return sensed

    def send(self, msg) -> None:
        if isinstance(msg.to, Robot) and distance((msg.to.x, msg.to.y), (self.x, self.y)) < self.communication_range:
            super().send(msg)
        else:
            msg.to = [agent for agent in msg.to if distance((agent.x, agent.y), (self.x, self.y)) < self.communication_range]
            if len(msg.to) > 0:
                super().send(msg)

    def portrayal_method(self):
        portrayal = {"Shape": "arrowHead", "s": 1, "Filled": "true", "Color": "Red", "Layer": 2, 'x': self.x,
                     'y': self.y}
        if self.waypoint and not (self.waypoint[0] == self.x and self.waypoint[1] == self.y):
            if self.waypoint[1] - self.y > 0:
                portrayal['angle'] = math.acos((self.waypoint[0] - self.x) /
                                               np.linalg.norm((self.waypoint[0] - self.x, self.waypoint[1] - self.y)))
            else:
                portrayal['angle'] = 2 * math.pi - math.acos((self.waypoint[0] - self.x) /
                                                             np.linalg.norm(
                                                                 (self.waypoint[0] - self.x,
                                                                  self.waypoint[1] - self.y)))
        else:
            portrayal['angle'] = 0
        return portrayal


class Speeder(Robot):
    def __init__(self, x, y, model, environment):
        
        super().__init__(0.05, 0.15, 0.1, 8, x, y, int(uuid.uuid1()), model, environment, terrestrial=True)

    def take(self, item: RescueItem):
        if item.x == self.x and self.y == item.y:
            self.taken_item = item

    def drop_item(self):
        if self.taken_item is not None:
            self.taken_item = None


class Balloon(Robot):
    def __init__(self, x, y, model, environment):
        super().__init__(0.2, 0.05, 0.2, 3, x, y, int(uuid.uuid1()), model, environment)

    def sense(self) -> List[Item]:
        return [i for i in self.model.items if distance((i.x, i.y), (self.x, self.y)) < self.vision_range]

    def goto(self, destination_x, destination_y):
        if distance((self.x, self.y), (destination_x, destination_y)) >= self.moving_range:
            percent = self.moving_range / distance((self.x, self.y), (destination_x, destination_y))
            self.x, self.y = self.x + percent * (destination_x - self.x), self.y + percent * (destination_y - self.y)
        else:
            self.x, self.y = destination_x, destination_y

    def portrayal_method(self):
        portrayal = {"Shape": "circle", "r": 0.2, "Filled": "true", "Color": "Teal", "Layer": 2, 'x': self.x,
                     'y': self.y}
        return portrayal


class Rover(Robot):
    def __init__(self, x, y, model, environment):
        super().__init__(0.1, 0.1, 0.15, 5, x, y, int(uuid.uuid1()), model, environment, terrestrial=True)

    def take(self, item: RescueItem):
        if item.x == self.x and self.y == item.y:
            self.taken_item = item

    def drop_item(self):
        if self.taken_item is not None:
            self.taken_item = None

    def portrayal_method(self):
        portrayal = {"Shape": "rectangle", "aspect": 0.75, "size":6, "Filled": "true", "Color": "Brown", "Layer": 2, 'x': self.x,
                     'y': self.y}
        if self.waypoint and not (self.waypoint[0] == self.x and self.waypoint[1] == self.y):
            if self.waypoint[1] - self.y > 0:
                portrayal['angle'] = math.acos((self.waypoint[0] - self.x) /
                                               np.linalg.norm((self.waypoint[0] - self.x, self.waypoint[1] - self.y)))
            else:
                portrayal['angle'] = 2 * math.pi - math.acos((self.waypoint[0] - self.x) /
                                                             np.linalg.norm(
                                                                 (self.waypoint[0] - self.x,
                                                                  self.waypoint[1] - self.y)))
        else:
            portrayal['angle'] = 0
        return portrayal


class Climber(Robot):
    def __init__(self, x, y, model, environment):
        super().__init__(0.05, 0.15, 0.1, 3, x, y, int(uuid.uuid1()), model, environment)

    def goto(self, destination_x, destination_y):
        if distance((self.x, self.y), (destination_x, destination_y)) >= self.moving_range:
            percent = self.moving_range / distance((self.x, self.y), (destination_x, destination_y))
            self.x, self.y = self.x + percent * (destination_x - self.x), self.y + percent * (destination_y - self.y)
        else:
            self.x, self.y = destination_x, destination_y
        self.waypoint = (destination_x, destination_y)

    def portrayal_method(self):
        portrayal = {"Shape": "rectangle", "aspect": 0.5, "size":4, "Filled": "true", "Color": "Green", "Layer": 2, 'x': self.x,
                     'y': self.y}
        if self.waypoint and not (self.waypoint[0] == self.x and self.waypoint[1] == self.y):
            if self.waypoint[1] - self.y > 0:
                portrayal['angle'] = math.acos((self.waypoint[0] - self.x) /
                                               np.linalg.norm((self.waypoint[0] - self.x, self.waypoint[1] - self.y)))
            else:
                portrayal['angle'] = 2 * math.pi - math.acos((self.waypoint[0] - self.x) /
                                                             np.linalg.norm(
                                                                 (self.waypoint[0] - self.x,
                                                                  self.waypoint[1] - self.y)))
        else:
            portrayal['angle'] = 0
        return portrayal



def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class SpeederChef(Speeder):
    def step(self):
        self.goto(0.1, 0.1)
    

team = [SpeederChef]

class SearchAndRescue(mesa.Model):

    def __init__(self):
        mesa.Model.__init__(self)
        self.space = mesa.space.ContinuousSpace(600, 600, False)
        self.schedule = RandomActivation(self)
        environment = Maze([], int(uuid.uuid1()), self)
        robots = [r(0.5, 0.55, self, environment) for r in team]
        self.schedule.add(environment)
        for robot in robots:
            self.schedule.add(robot)
        self.items = [Person(environment)] + [RescueItem(environment) for _ in range(2)]
        self.computed_items_nb = 0
        self.datacollector = DataCollector(
            model_reporters={"items": lambda model: len(model.items),
                             "Delivered": lambda model: model.computed_items_nb
                             },
            agent_reporters={})

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        x, y = self.items[0].x, self.items[0].y
        if all([i.x == x and i.y == y for i in self.items]):
            self.running = False


class ContinuousCanvas(VisualizationElement):
    local_includes = [
        "./code/js/simple_continuous_canvas.js",
        "./code/js/jquery.min.js",
    ]

    def __init__(self, canvas_height=500,
                 canvas_width=500, instantiate=True):
        VisualizationElement.__init__(self)
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.identifier = "space-canvas"
        if instantiate:
            new_element = ("new Simple_Continuous_Module({}, {},'{}')".
                           format(self.canvas_width, self.canvas_height, self.identifier))
            self.js_code = "elements.push(" + new_element + ");"

    @staticmethod
    def portrayal_method(obj):
        return obj.portrayal_method()

    def render(self, model):
        representation = defaultdict(list)
        for obj in model.schedule.agents:
            portrayal = self.portrayal_method(obj)
            if portrayal:
                if isinstance(obj, Maze):
                    for p in portrayal:
                        representation[p["Layer"]].append(p)
                else:
                    portrayal["x"] = obj.x
                    portrayal["y"] = obj.y
                    representation[portrayal["Layer"]].append(portrayal)
        for obj in model.items:
            portrayal = self.portrayal_method(obj)
            portrayal["x"] = obj.x
            portrayal["y"] = obj.y
            representation[portrayal["Layer"]].append(portrayal)
        return representation


def run_single_server():
    server = ModularServer(SearchAndRescue,
                           [ContinuousCanvas()],
                           "Search and rescue",
                           {})
                           # {"n_planets": Slider("Number of planets", 10, 3, 20, 1),
                           #  "n_ships": Slider("Number of spaceships", 15, 3, 30, 1)})

    server.port = 8521
    server.launch()