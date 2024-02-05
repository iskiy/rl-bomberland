import torch
import math 

from components.types import Observation
from components.utils.observation import (
    get_nearest_active_bomb, 
    get_nearest_obstacle,
    dangerous_bomb_count,
    dangerous_bomb_distances,
    get_nearest_blast,
    get_nearest_blast_powerup,
    get_nearest_freeze_powerup,
    get_nearest_obstacle_count,
    get_nearest_1_barier_count,
    get_unit_activated_bombs, 
    get_count_wooden_obstacle_in_blast_diameter,
    get_count_ore_obstacle_in_blast_diameter,
    get_count_metal_obstacle_in_blast_diameter
)
from components.utils.metrics import manhattan_distance


def find_my_units_alive(observation: Observation, current_agent_id: str) -> int:
    alive = 0
    for unit_props in observation['unit_state'].values():
        if unit_props['agent_id'] == current_agent_id:
            if unit_props['hp'] != 0:
                alive += 1
    return alive


def find_enemy_units_alive(observation: Observation, current_agent_id: str) -> int:
    alive = 0
    for unit_props in observation['unit_state'].values():
        if unit_props['agent_id'] != current_agent_id:
            if unit_props['hp'] != 0:
                alive += 1
    return alive


def find_my_units_hps(observation: Observation, current_agent_id: str) -> int:
    hps = 0
    for unit_props in observation['unit_state'].values():
        if unit_props['agent_id'] == current_agent_id:
            hps += unit_props['hp']
    return hps


def find_enemy_units_hps(observation: Observation, current_agent_id: str) -> int:
    hps = 0
    for unit_props in observation['unit_state'].values():
        if unit_props['agent_id'] != current_agent_id:
            hps += unit_props['hp']
    return hps


def find_current_tick(observation: Observation) -> int:
    tick = observation['tick']
    return tick

def unit_within_reach_of_a_bomb(observation: Observation, current_unit_id: str):
    unit = observation['unit_state'][current_unit_id]
    unit_coords = unit['coordinates']
    nearest_bomb = get_nearest_active_bomb(observation, current_unit_id)
    if nearest_bomb is None:
        return False
    nearest_bomb_coords = [nearest_bomb['x'], nearest_bomb['y']]
    within_reach_of_a_bomb = manhattan_distance(unit_coords, nearest_bomb_coords) <= int(nearest_bomb['blast_diameter'])/2.
    return within_reach_of_a_bomb
    

def unit_within_reach_of_a_bomb_count(observation: Observation, current_unit_id: str) -> int:
    return dangerous_bomb_count(observation, current_unit_id)

def unit_within_reach_of_a_bomb_distances(observation: Observation, current_unit_id: str) -> int:
    return dangerous_bomb_distances(observation, current_unit_id)

def unit_within_safe_cell_nearby_bomb(observation: Observation, current_unit_id: str):
    unit = observation['unit_state'][current_unit_id]
    unit_coords = unit['coordinates']
    nearest_bomb = get_nearest_active_bomb(observation, current_unit_id)
    if nearest_bomb is None:
        return False
    nearest_bomb_coords = [nearest_bomb['x'], nearest_bomb['y']]
    within_safe_cell_nearby_bomb = manhattan_distance(unit_coords, nearest_bomb_coords) > int(nearest_bomb['blast_diameter'])/2.
    return within_safe_cell_nearby_bomb
    
def unit_within_safe_cell_nearby_bombs(observation: Observation, current_unit_id: str):
    return dangerous_bomb_count(observation, current_unit_id) == 0

"""
Bomb definition: {'created': 74, 'x': 11, 'y': 10, 'type': 'b', 'unit_id': 'd', 'agent_id': 'b', 'expires': 104, 'hp': 1, 'blast_diameter': 3}
"""
def unit_activated_bomb_near_an_obstacle(observation: Observation, current_unit_id: str):
    unit_activated_bombs = get_unit_activated_bombs(observation, current_unit_id)
    if not len(unit_activated_bombs):
        return False
    for unit_bomb in unit_activated_bombs:
        unit_bomb_coords = [unit_bomb['x'], unit_bomb['y']]
        nearest_obstacle = get_nearest_obstacle(observation, unit_bomb_coords)
        if nearest_obstacle is None:
            continue
        nearest_obstacle_coords = [nearest_obstacle['x'], nearest_obstacle['y']]
        if manhattan_distance(unit_bomb_coords, nearest_obstacle_coords) <= int(unit_bomb['blast_diameter'])/2.:
            return True
    return False
    
def unit_activated_bomb_near_a_wooden_obstacle_count(observation: Observation, current_unit_id: str)->int:
    unit_activated_bombs = get_unit_activated_bombs(observation, current_unit_id)
    if not len(unit_activated_bombs):
        return 0
    all_count = 0
    for unit_bomb in unit_activated_bombs:
        unit_bomb_coords = [unit_bomb['x'], unit_bomb['y']]
        wooden_obstacle_count = get_count_wooden_obstacle_in_blast_diameter(observation, unit_bomb_coords, int(unit_bomb['blast_diameter'])/2.)
        all_count += wooden_obstacle_count
    return all_count

def unit_activated_bomb_near_an_ore_obstacle_count(observation: Observation, current_unit_id: str)->int:
    unit_activated_bombs = get_unit_activated_bombs(observation, current_unit_id)
    if not len(unit_activated_bombs):
        return 0
    all_count = 0
    for unit_bomb in unit_activated_bombs:
        unit_bomb_coords = [unit_bomb['x'], unit_bomb['y']]
        ore_obstacle_count = get_count_ore_obstacle_in_blast_diameter(observation, unit_bomb_coords, int(unit_bomb['blast_diameter'])/2.)
        all_count += ore_obstacle_count
    return all_count
    
def unit_activated_bomb_near_a_metal_obstacle_count(observation: Observation, current_unit_id: str)->int:
    unit_activated_bombs = get_unit_activated_bombs(observation, current_unit_id)
    if not len(unit_activated_bombs):
        return 0
    all_count = 0
    for unit_bomb in unit_activated_bombs:
        unit_bomb_coords = [unit_bomb['x'], unit_bomb['y']]
        metal_obstacle_count = get_count_metal_obstacle_in_blast_diameter(observation, unit_bomb_coords, int(unit_bomb['blast_diameter'])/2.)
        all_count += metal_obstacle_count
    return all_count

def unit_activated_bomb_near_an_enemy_count(observation: Observation, current_unit_id: str, current_agent_id: str)->int:
    unit_activated_bombs = get_unit_activated_bombs(observation, current_unit_id)
    if not len(unit_activated_bombs):
        return 0
    count = 0
    for unit_bomb in unit_activated_bombs:
        unit_bomb_coords = [unit_bomb['x'], unit_bomb['y']]
        for unit_props in observation['unit_state'].values():
            if unit_props['agent_id'] != current_agent_id:
                enemy_coords = unit_props['coordinates']
                if manhattan_distance(unit_bomb_coords, enemy_coords) <= int(unit_bomb['blast_diameter'])/2.:
                    count += 1
    return count
    
    
def unit_activated_bomb_near_a_teammate_count(observation: Observation, current_unit_id: str, current_agent_id: str)->int:
    unit_activated_bombs = get_unit_activated_bombs(observation, current_unit_id)
    if not len(unit_activated_bombs):
        return 0
    count = 0
    for unit_bomb in unit_activated_bombs:
        unit_bomb_coords = [unit_bomb['x'], unit_bomb['y']]
        for unit_props in observation['unit_state'].values():
            if unit_props['agent_id'] == current_agent_id:
                enemy_coords = unit_props['coordinates']
                if manhattan_distance(unit_bomb_coords, enemy_coords) <= int(unit_bomb['blast_diameter'])/2.:
                    count += 1
    return count
    
def near_blast_powerup(observation: Observation, current_unit_id: str)->int:
    unit = observation['unit_state'][current_unit_id]
    unit_coords = unit['coordinates']
    nearest_blast_powerup = get_nearest_blast_powerup(observation, unit_coords)
    if nearest_blast_powerup is None:
        return +math.inf
    nearest_blast_powerup_coords = [nearest_blast_powerup['x'], nearest_blast_powerup['y']]
    return manhattan_distance(nearest_blast_powerup_coords, unit_coords)
    

def near_freeze_powerup(observation: Observation, current_unit_id: str)->int:
    unit = observation['unit_state'][current_unit_id]
    unit_coords = unit['coordinates']
    nearest_freeze_powerup = get_nearest_freeze_powerup(observation, unit_coords)
    if nearest_freeze_powerup is None:
        return +math.inf
    nearest_freeze_powerup_coords = [nearest_freeze_powerup['x'], nearest_freeze_powerup['y']]
    return manhattan_distance(nearest_freeze_powerup_coords, unit_coords)
    

def unit_is_in_deadend(observation: Observation, current_unit_id: str):
    unit = observation['unit_state'][current_unit_id]
    unit_coords = unit['coordinates']
    obstacle_count, obstacles = get_nearest_obstacle_count(observation, unit_coords)
    barier_count, bariers = get_nearest_1_barier_count(observation, unit_coords)
    if (obstacle_count + barier_count < 2):
        return False
    
    bomb_count = dangerous_bomb_count(observation, current_unit_id)
    if ((unit_coords[0] <= 0 and (unit_coords[1] <= 0 or unit_coords[1] >= 15)) or (unit_coords[0] >= 15 and (unit_coords[1] <= 0 or unit_coords[1] >= 15))):
        if (bomb_count != 0 and obstacle_count + barier_count > 1):
            return True
        
    if (unit_coords[0] <= 0 or unit_coords[1] <= 0 or unit_coords[0] >= 15 or unit_coords[1] >= 15):
        if (bomb_count != 0 and obstacle_count + barier_count > 2):
            return True
            
    if (bomb_count != 0 and obstacle_count + barier_count > 3):
        return True
    return False
    
    
def unit_near_blast_distance(observation: Observation, current_unit_id: str) -> int:
    unit = observation['unit_state'][current_unit_id]
    unit_coords = unit['coordinates']
    nearest_blast = get_nearest_blast(observation, unit_coords)
    if nearest_blast is None:
        return +math.inf
    nearest_blast_coords = [nearest_blast['x'], nearest_blast['y']]
    return manhattan_distance(unit_coords, nearest_blast_coords)


"""
Reward function definition:
1. +0.5: when dealing 1 hp for 1 enemy
2. +1: when killing opponent
3. +1: when killing all 3 opponents
4. -0.25: when losing 1 hp for 1 teammate
5. -0.5: when losing teammate
6. -1: when losing all 3 teammates
7. -0.01: the longer game the bigger punishment is
8. -0.000666: the unit is in a cell within reach of a bomb
9. +0.002: the unit is in a safe cell when there is an active bomb nearby 
10. +0.1: the unit activated bomb near an obstacle
"""
def calculate_reward(prev_observation: Observation, next_observation: Observation, current_agent_id: str, current_unit_id: str):
    reward = 0        

    # 1. +0.5: when dealing 1 hp for 1 enemy

    prev_enemy_units_hps = find_enemy_units_hps(prev_observation, current_agent_id)
    next_enemy_units_hps = find_enemy_units_hps(next_observation, current_agent_id)
    
    enemy_units_hps_diff = prev_enemy_units_hps - next_enemy_units_hps
    if enemy_units_hps_diff > 0:
        reward += (enemy_units_hps_diff * 0.5)

    # 2. +1: when killing opponent

    prev_enemy_units_alive = find_enemy_units_alive(prev_observation, current_agent_id)
    next_enemy_units_alive = find_enemy_units_alive(next_observation, current_agent_id)

    if prev_enemy_units_alive > next_enemy_units_alive:
        reward += 1 * (prev_enemy_units_alive - next_enemy_units_alive)

    # 3. +1: when killing all 3 opponents

    if next_enemy_units_alive == 0:
        reward += 1

    # 4. -0.25: when losing 1 hp for 1 teammate

    prev_my_units_hps = find_my_units_hps(prev_observation, current_agent_id)
    next_my_units_hps = find_my_units_hps(next_observation, current_agent_id)

    my_units_hps_diff = prev_my_units_hps - next_my_units_hps
    if my_units_hps_diff > 0:
        reward += (my_units_hps_diff * -0.25)

    # 5. -0.5: when losing teammate

    prev_my_units_alive = find_my_units_alive(prev_observation, current_agent_id)
    next_my_units_alive = find_my_units_alive(next_observation, current_agent_id)

    if next_my_units_alive < prev_my_units_alive:
        reward += (-0.7) * (prev_my_units_alive - next_my_units_alive)

    # 6. -1: when losing all 3 teammates

    if next_my_units_alive == 0:
        reward += (-1)

    # 7. -0.01: the longer game the bigger punishment is

    reward += (-0.01) #0,5

    # 8. -0.000666: the agent is in a cell within reach of a bomb

    #prev_within_reach_of_a_bomb = unit_within_reach_of_a_bomb(prev_observation, current_unit_id)
    #next_within_reach_of_a_bomb = unit_within_reach_of_a_bomb(next_observation, current_unit_id)

    #if not prev_within_reach_of_a_bomb and next_within_reach_of_a_bomb:
    #    reward += (-0.0666)
    #if prev_within_reach_of_a_bomb and next_within_reach_of_a_bomb:
    #    reward += (-0.1666)
    
    #prev_within_reach_of_a_bomb_count = unit_within_reach_of_a_bomb_count(prev_observation, current_unit_id)
    #next_within_reach_of_a_bomb_count = unit_within_reach_of_a_bomb_count(next_observation, current_unit_id)
    
    #if (prev_within_reach_of_a_bomb_count < next_within_reach_of_a_bomb_count):
    #    reward += -0.00666 * (next_within_reach_of_a_bomb_count - prev_within_reach_of_a_bomb_count)
    #elif (prev_within_reach_of_a_bomb_count == next_within_reach_of_a_bomb_count and next_within_reach_of_a_bomb_count != 0):
    #    reward += -0.007
    #if (prev_within_reach_of_a_bomb_count > next_within_reach_of_a_bomb_count):
    #    reward += 0.006 * (prev_within_reach_of_a_bomb_count - next_within_reach_of_a_bomb_count)
    
    prev_my_units_deadend = unit_is_in_deadend(prev_observation, current_unit_id) #??????
    next_my_units_deadend = unit_is_in_deadend(next_observation, current_unit_id)    
    if not prev_my_units_deadend and next_my_units_deadend:
        reward += (-0.05)
        
    elif prev_my_units_deadend and next_my_units_deadend:
        reward += (-0.06)
        
    prev_within_reach_of_a_bomb_distances = unit_within_reach_of_a_bomb_distances(prev_observation, current_unit_id)
    next_within_reach_of_a_bomb_distances = unit_within_reach_of_a_bomb_distances(next_observation, current_unit_id)
    
    prev_distance_penalty = 0
    for distance in prev_within_reach_of_a_bomb_distances:
        prev_distance_penalty += 1.0/(distance + 1)
    #prev_distance/=len(prev_within_reach_of_a_bomb_distances) + 1

    next_distance_penalty = 0
    for distance in next_within_reach_of_a_bomb_distances:
        next_distance_penalty += 1.0/(distance + 1)
    #next_distance/=len(next_within_reach_of_a_bomb_distances) + 1     
    
    if (prev_distance_penalty < next_distance_penalty):
        reward += -0.4 * (next_distance_penalty - prev_distance_penalty)
    elif (prev_distance_penalty == next_distance_penalty and next_distance_penalty!=0):
        reward += -0.4 * next_distance_penalty
    else:
        reward += 0.02

    # 9. +0.002: the agent is in a safe cell when there is an active bomb nearby

    # prev_within_safe_cell_nearby_bomb = unit_within_safe_cell_nearby_bombs(prev_observation, current_unit_id)
    # next_within_safe_cell_nearby_bomb = unit_within_safe_cell_nearby_bombs(next_observation, current_unit_id)

    # if not prev_within_safe_cell_nearby_bomb and next_within_safe_cell_nearby_bomb:
    #    reward += 0.02
        
    # 10. +0.1: the unit activated bomb near an obstacle

    prev_unit_activated_bomb_near_an_wooden_obstacle_count = unit_activated_bomb_near_a_wooden_obstacle_count(prev_observation, current_unit_id)
    next_unit_activated_bomb_near_an_wooden_obstacle_count = unit_activated_bomb_near_a_wooden_obstacle_count(next_observation, current_unit_id)
    
    if prev_unit_activated_bomb_near_an_wooden_obstacle_count < next_unit_activated_bomb_near_an_wooden_obstacle_count:
        reward += 0.05 * (next_unit_activated_bomb_near_an_wooden_obstacle_count - prev_unit_activated_bomb_near_an_wooden_obstacle_count)
        
    prev_unit_activated_bomb_near_an_ore_obstacle_count = unit_activated_bomb_near_an_ore_obstacle_count(prev_observation, current_unit_id)
    next_unit_activated_bomb_near_an_ore_obstacle_count = unit_activated_bomb_near_an_ore_obstacle_count(next_observation, current_unit_id)
    
    if prev_unit_activated_bomb_near_an_ore_obstacle_count < next_unit_activated_bomb_near_an_ore_obstacle_count:
        reward += 0.03 * (next_unit_activated_bomb_near_an_ore_obstacle_count - prev_unit_activated_bomb_near_an_ore_obstacle_count)
        
    # prev_unit_activated_bomb_near_a_metal_obstacle_count = unit_activated_bomb_near_a_metal_obstacle_count(prev_observation, current_unit_id)
    # next_unit_activated_bomb_near_a_metal_obstacle_count = unit_activated_bomb_near_a_metal_obstacle_count(next_observation, current_unit_id)
    
    # if prev_unit_activated_bomb_near_a_metal_obstacle_count < next_unit_activated_bomb_near_a_metal_obstacle_count:
    #    reward += 0.0000001 * (next_unit_activated_bomb_near_a_metal_obstacle_count - prev_unit_activated_bomb_near_a_metal_obstacle_count)
        
        
    # 11. +0.1: the unit activated bomb near an enemy

    prev_unit_activated_bomb_near_an_enemy_count = unit_activated_bomb_near_an_enemy_count(prev_observation, current_unit_id, current_agent_id)
    next_unit_activated_bomb_near_an_enemy_count = unit_activated_bomb_near_an_enemy_count(next_observation, current_unit_id, current_agent_id)
    
    if prev_unit_activated_bomb_near_an_enemy_count < next_unit_activated_bomb_near_an_enemy_count:
        reward += 0.09 * (next_unit_activated_bomb_near_an_enemy_count - prev_unit_activated_bomb_near_an_enemy_count) #0.3
    elif prev_unit_activated_bomb_near_an_enemy_count == next_unit_activated_bomb_near_an_enemy_count and next_unit_activated_bomb_near_an_enemy_count != 0:
        reward += 0.03 * (next_unit_activated_bomb_near_an_enemy_count)
        
    # 12. +0.1: the unit activated bomb near an teammate

    prev_unit_activated_bomb_near_a_teammate_count = unit_activated_bomb_near_a_teammate_count(prev_observation, current_unit_id, current_agent_id)
    next_unit_activated_bomb_near_a_teammate_count = unit_activated_bomb_near_a_teammate_count(next_observation, current_unit_id, current_agent_id)
    
    if prev_unit_activated_bomb_near_a_teammate_count < next_unit_activated_bomb_near_a_teammate_count and next_unit_activated_bomb_near_a_teammate_count != 0:
        reward -= 0.07 * (next_unit_activated_bomb_near_a_teammate_count - prev_unit_activated_bomb_near_a_teammate_count - 1)
    elif prev_unit_activated_bomb_near_a_teammate_count == next_unit_activated_bomb_near_a_teammate_count and next_unit_activated_bomb_near_an_enemy_count != 0:
        reward -= 0.02 * (prev_unit_activated_bomb_near_a_teammate_count - 1)
    
        
    # 14. +0.1: unit in blast
    
    prev_unit_near_blast_distance = unit_near_blast_distance(prev_observation, current_unit_id)
    next_unit_near_blast_distance = unit_near_blast_distance(next_observation, current_unit_id)
        
    if prev_unit_near_blast_distance > next_unit_near_blast_distance and next_unit_near_blast_distance == 0:
       reward += (-0.09)
    
    elif prev_unit_near_blast_distance == next_unit_near_blast_distance and next_unit_near_blast_distance == 0:
        reward += (-0.1)
        
    # 15. +0.1: unit in blastpowerup
    
    prev_near_blast_powerup = near_blast_powerup(prev_observation, current_unit_id)
    next_near_blast_powerup = near_blast_powerup(next_observation, current_unit_id)

    #if prev_near_blast_powerup > next_near_blast_powerup and next_near_blast_powerup != 0:
    #    reward += 0.01 / next_near_blast_powerup
        
    if prev_near_blast_powerup > next_near_blast_powerup and next_near_blast_powerup == 0:
        reward += (0.03)
        
    # 16. +0.1: unit in freezepowerup
    
    prev_near_freeze_powerup = near_freeze_powerup(prev_observation, current_unit_id)
    next_near_freeze_powerup = near_freeze_powerup(next_observation, current_unit_id)

    #if prev_near_freeze_powerup > next_near_freeze_powerup and next_near_freeze_powerup != 0:
    #    reward += (0.01) / next_near_freeze_powerup
        
    if prev_near_freeze_powerup > next_near_freeze_powerup and next_near_freeze_powerup == 0:
        reward += (0.03)
    
    print(reward)

    return torch.tensor(reward, dtype=torch.float32).reshape(1)
