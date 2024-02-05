import math 
import typing as t

from components.types import Coordinate, Observation
from components.utils.metrics import manhattan_distance


"""
Bomb definition: 
    {'created': 74, 'x': 11, 'y': 10, 'type': 'b', 'unit_id': 'd', 'agent_id': 'b', 'expires': 104, 'hp': 1, 'blast_diameter': 3}
"""
def get_bomb_to_detonate(observation: Observation, unit_id: str) -> Coordinate or None:
    entities = observation["entities"]
    bombs = list(filter(lambda entity: entity.get("unit_id") == unit_id and entity.get("type") == "b", entities))
    bomb = next(iter(bombs or []), None)
    if bomb != None:
        return [bomb.get("x"), bomb.get("y")]
    else:
        return None


"""
Bomb definition: 
    {'created': 74, 'x': 11, 'y': 10, 'type': 'b', 'unit_id': 'd', 'agent_id': 'b', 'expires': 104, 'hp': 1, 'blast_diameter': 3}
"""
def get_nearest_active_bomb(observation: Observation, unit_id: str):
    unit = observation["unit_state"][unit_id]
    unit_coords = unit['coordinates']

    entities = observation["entities"]
    bombs = list(filter(lambda entity: entity.get("type") == "b", entities))

    min_distance, nearest_bomb = +math.inf, None
    for bomb in bombs:
        bomb_coords = [bomb['x'], bomb['y']]
        bomb_distance = manhattan_distance(unit_coords, bomb_coords)
        if bomb_distance < min_distance:
            min_distance = bomb_distance
            nearest_bomb = bomb

    return nearest_bomb


"""
Bomb definition: 
    {'created': 74, 'x': 11, 'y': 10, 'type': 'b', 'unit_id': 'd', 'agent_id': 'b', 'expires': 104, 'hp': 1, 'blast_diameter': 3}
"""
def get_unit_activated_bombs(observation: Observation, unit_id: str):
    entities = observation["entities"]
    unit_bombs = list(filter(lambda entity: entity["type"] == "b" and entity["unit_id"] == unit_id, entities))
    return unit_bombs
    

"""
Obstacle definitions: 
    a. Wooden Block: {"created":0, "x":10, "y":1, "type":"w", "hp":1}
    b. Ore Block: {"created":0, "x":0, "y":13, "type":"o", "hp":3}
    c. Metal Block: {"created":0, "x":3, "y":7, "type":"m"}
"""
def get_obtacles(observation: t.Dict):
    entities = observation["entities"]
    obstacles = list(filter(lambda entity: entity.get("type") in ["w", "o", "m"], entities))
    return obstacles


def get_nearest_obstacle(observation: Observation, coords: Coordinate):
    entities = observation["entities"]
    obstacles = list(filter(lambda entity: entity.get("type") in ["w", "o", "m"], entities))

    min_distance, nearest_obstacle = +math.inf, None
    for obstacle in obstacles:
        obstacle_coords = [obstacle['x'], obstacle['y']]
        obstacle_distance = manhattan_distance(coords, obstacle_coords)
        if obstacle_distance < min_distance:
            min_distance = obstacle_distance
            nearest_obstacle = obstacle

    return nearest_obstacle
    
    
def get_nearest_obstacle_count(observation: Observation, coords: Coordinate):
    entities = observation["entities"]
    obstacles = list(filter(lambda entity: entity.get("type") in ["w", "o", "m"], entities))

    min_distance, nearest_obstacle = +math.inf, None
    nearest_obstacles = []
    if obstacles:
        count = 1
    for obstacle in obstacles:
        obstacle_coords = [obstacle['x'], obstacle['y']]
        obstacle_distance = manhattan_distance(coords, obstacle_coords)
        if obstacle_distance < min_distance:
            min_distance = obstacle_distance
            nearest_obstacle = obstacle
            count = 1
            nearest_obstacles = [nearest_obstacle]
        elif obstacle_distance == min_distance:
            count += 1
            nearest_obstacles.append(obstacle)
            
    if (min_distance > 1):
        return 0, []
    return (count, nearest_obstacles)
    
def get_nearest_1_barier_count(observation: Observation, coords: Coordinate):
    entities = observation["entities"]
    obstacles = list(filter(lambda entity: entity.get("type") in ["b", "x"], entities))

    min_distance, nearest_obstacle = +math.inf, None
    nearest_obstacles = []
    if obstacles:
        count = 1
    for obstacle in obstacles:
        obstacle_coords = [obstacle['x'], obstacle['y']]
        obstacle_distance = manhattan_distance(coords, obstacle_coords)
        if obstacle_distance < min_distance:
            min_distance = obstacle_distance
            nearest_obstacle = obstacle
            count = 1
            nearest_obstacles = [nearest_obstacle]
        elif obstacle_distance == min_distance:
            count += 1
            nearest_obstacles.append(obstacle)
            
    if (min_distance > 1):
        return 0, []
    return (count, nearest_obstacles)

def get_bomb(observation: Observation):
    entities = observation["entities"]
    bomb = list(filter(lambda entity: entity.get("type") in ["b"], entities))
    return bomb
    
def dangerous_bomb_count(observation: Observation, unit_id: str)->int:
    unit = observation["unit_state"][unit_id]
    unit_coords = unit['coordinates']

    entities = observation["entities"]
    bombs = list(filter(lambda entity: entity.get("type") == "b", entities))

    count = 0
    for bomb in bombs:
        bomb_coords = [bomb['x'], bomb['y']]
        bomb_distance = manhattan_distance(unit_coords, bomb_coords)
        if (bomb_distance <= int(bomb['blast_diameter']))/2.:
            count += 1

    return count

def dangerous_bomb_distances(observation: Observation, unit_id: str)->int:
    unit = observation["unit_state"][unit_id]
    unit_coords = unit['coordinates']

    entities = observation["entities"]
    bombs = list(filter(lambda entity: entity.get("type") == "b", entities))

    distances = []
    for bomb in bombs:
        bomb_coords = [bomb['x'], bomb['y']]
        bomb_distance = manhattan_distance(unit_coords, bomb_coords)
        if (bomb_distance <= int(bomb['blast_diameter']))/2.: #??????????? obstacle
            distances.append(bomb_distance)

    return distances

def get_blast(observation: Observation):
    entities = observation["entities"]
    blast = list(filter(lambda entity: entity.get("type") in ["x"], entities))
    return blast
    
def get_nearest_blast(observation: Observation, coords: Coordinate):
    blasts = get_blast(observation)
    min_distance, nearest_blast = +math.inf, None
    for blast in blasts:
        blast_coords = [blast['x'], blast['y']]
        blast_distance = manhattan_distance(coords, blast_coords)
        if blast_distance < min_distance:
            min_distance = blast_distance
            nearest_blast = blast

    return nearest_blast
    
def get_wooden_obstacle(observation: Observation):
    entities = observation["entities"]
    wooden = list(filter(lambda entity: entity.get("type") in ["w"], entities))
    return wooden
    
def get_nearest_wooden_obstacle(observation: Observation, coords: Coordinate):
    wooden_obstacles = get_wooden_obstacle(observation)
    min_distance, nearest_wooden_obstacle = +math.inf, None
    for wooden_obstacle in wooden_obstacles:
        wooden_obstacle_coords = [wooden_obstacle['x'], wooden_obstacle['y']]
        wooden_obstacle_distance = manhattan_distance(coords, wooden_obstacle_coords)
        if wooden_obstacle_distance < min_distance:
            min_distance = wooden_obstacle_distance
            nearest_wooden_obstacle = wooden_obstacle

    return nearest_wooden_obstacle
    
def get_count_wooden_obstacle_in_blast_diameter(observation: Observation, coords: Coordinate, blast_diameter)->int:
    wooden_obstacles = get_wooden_obstacle(observation)
    count = 0
    for wooden_obstacle in wooden_obstacles:
        wooden_obstacle_coords = [wooden_obstacle['x'], wooden_obstacle['y']]
        wooden_obstacle_distance = manhattan_distance(coords, wooden_obstacle_coords)
        if wooden_obstacle_distance < blast_diameter:
            count += 1

    return count
    
def get_ore_obstacle(observation: Observation):
    entities = observation["entities"]
    ore = list(filter(lambda entity: entity.get("type") in ["o"], entities))
    return ore
    
def get_nearest_ore_obstacle(observation: Observation, coords: Coordinate):
    ore_obstacles = get_ore_obstacle(observation)
    min_distance, nearest_ore_obstacle = +math.inf, None
    for ore_obstacle in ore_obstacles:
        ore_obstacle_coords = [ore_obstacle['x'], ore_obstacle['y']]
        ore_obstacle_distance = manhattan_distance(coords, ore_obstacle_coords)
        if ore_obstacle_distance < min_distance:
            min_distance = ore_obstacle_distance
            nearest_ore_obstacle = ore_obstacle

    return nearest_ore_obstacle
    
def get_count_ore_obstacle_in_blast_diameter(observation: Observation, coords: Coordinate, blast_diameter)->int:
    ore_obstacles = get_ore_obstacle(observation)
    count = 0
    for ore_obstacle in ore_obstacles:
        ore_obstacle_coords = [ore_obstacle['x'], ore_obstacle['y']]
        ore_obstacle_distance = manhattan_distance(coords, ore_obstacle_coords)
        if ore_obstacle_distance < blast_diameter:
            count += 1

    return count
    
def get_nearest_blast(observation: Observation, coords: Coordinate):
    blasts = get_blast(observation)
    min_distance, nearest_blast = +math.inf, None
    for blast in blasts:
        blast_coords = [blast['x'], blast['y']]
        blast_distance = manhattan_distance(coords, blast_coords)
        if blast_distance < min_distance:
            min_distance = blast_distance
            nearest_blast = blast

    return nearest_blast
    
def get_metal_obstacle(observation: Observation):
    entities = observation["entities"]
    metal = list(filter(lambda entity: entity.get("type") in ["m"], entities))
    return metal
    
def get_nearest_metal_obstacle(observation: Observation, coords: Coordinate):
    metal_obstacles = get_metal_obstacle(observation)
    min_distance, nearest_metal_obstacle = +math.inf, None
    for metal_obstacle in metal_obstacles:
        metal_obstacle_coords = [metal_obstacle['x'], metal_obstacle['y']]
        metal_obstacle_distance = manhattan_distance(coords, metal_obstacle_coords)
        if metal_obstacle_distance < min_distance:
            min_distance = metal_obstacle_distance
            nearest_metal_obstacle = metal_obstacle

    return nearest_metal_obstacle
    
def get_count_metal_obstacle_in_blast_diameter(observation: Observation, coords: Coordinate, blast_diameter)->int:
    metal_obstacles = get_metal_obstacle(observation)
    count = 0
    for metal_obstacle in metal_obstacles:
        metal_obstacle_coords = [metal_obstacle['x'], metal_obstacle['y']]
        metal_obstacle_distance = manhattan_distance(coords, metal_obstacle_coords)
        if metal_obstacle_distance < blast_diameter:
            count += 1

    return count
    
def get_freeze_powerup(observation: Observation):
    entities = observation["entities"]
    freeze_powerup = list(filter(lambda entity: entity.get("type") in ["fp"], entities))
    return freeze_powerup
    
def get_nearest_freeze_powerup(observation: Observation, coords: Coordinate):
    freeze_powerups = get_freeze_powerup(observation)
    min_distance, nearest_freeze_powerup = +math.inf, None
    for freeze_powerup in freeze_powerups:
        freeze_powerup_coords = [freeze_powerup['x'], freeze_powerup['y']]
        freeze_powerup_distance = manhattan_distance(coords, freeze_powerup_coords)
        if freeze_powerup_distance < min_distance:
            min_distance = freeze_powerup_distance
            nearest_freeze_powerup = freeze_powerup

    return nearest_freeze_powerup
    
def get_blast_powerup(observation: Observation):
    entities = observation["entities"]
    blast_powerup = list(filter(lambda entity: entity.get("type") in ["bp"], entities))
    return blast_powerup
    
def get_nearest_blast_powerup(observation: Observation, coords: Coordinate):
    blast_powerups = get_blast_powerup(observation)
    min_distance, nearest_blast_powerup = +math.inf, None
    for blast_powerup in blast_powerups:
        blast_powerup_coords = [blast_powerup['x'], blast_powerup['y']]
        blast_powerup_distance = manhattan_distance(coords, blast_powerup_coords)
        if blast_powerup_distance < min_distance:
            min_distance = blast_powerup_distance
            nearest_blast_powerup = blast_powerup

    return nearest_blast_powerup
    
def get_ammunition(observation: Observation):
    entities = observation["entities"]
    blast_powerup = list(filter(lambda entity: entity.get("type") in ["a"], entities))
    return blast_powerup