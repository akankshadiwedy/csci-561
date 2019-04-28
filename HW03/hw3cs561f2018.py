import numpy as np
import math
import time

class Car:
    def set_startlocation(self, position):
        self.startLocation = position

    def set_endlocation(self, position):
        self.endLocation = position

def value_iteration(size,car,epsilon,obstacles):
    utility = [[-1.0] * size for i in range(size)]
    for xy in obstacles:
        utility[xy[0]][xy[1]] = -101.0
    utility[car.endLocation[0]][car.endLocation[1]] = 99.0
    iterations_count = 0
    while True:
        iterations_count += 1
        t =[[0.0] * size for i in range(size)]
        delta = 0.0
        for i in range(size):
            for j in range(size):
                if (i,j) == car.endLocation:
                    t[i][j] = 99.0
                    continue
                if (i,j) in obstacles:
                    reward = -101.0
                else:
                    reward = -1.0
                if checkValidity(i, j + 1, size):
                    E = utility[i][j + 1]
                else:
                    E = utility[i][j]
                if checkValidity(i, j - 1, size):
                    W = utility[i][j - 1]
                else:
                    W = utility[i][j]
                if checkValidity(i + 1, j, size):
                    S = utility[i + 1][j]
                else:
                    S = utility[i][j]
                if checkValidity(i - 1, j, size):
                    N = utility[i - 1][j]
                else:
                    N = utility[i][j]
                t[i][j] = reward + (0.9 * max(np.float64(0.7 * W + 0.1 * S + 0.1 * E + 0.1 * N), np.float64(0.7 * N + 0.1 * S + 0.1 * E + 0.1 * W), np.float64(0.7 * E + 0.1 * S + 0.1 * N + 0.1 * W), np.float64(0.7 * S + 0.1 * N + 0.1 * E + 0.1 * W)))
                delta = max(delta,abs(t[i][j] - utility[i][j]))
                utility[i][j] = t[i][j]
        utility = t
        if delta < 0.1*((1.0-0.9)/0.9):
            break
    #print iterations_count
    return utility


def set_policy(utility,size):
    pie = [[None]*size for i in range(size)]
    for i in range(size):
        for j in range(size):
            if checkValidity(i - 1, j,size):
                N = utility[i - 1][j]
            else:
                N = utility[i][j]

            if checkValidity(i, j + 1,size):
                E = utility[i][j + 1]
            else:
                E = utility[i][j]

            if checkValidity(i, j - 1,size):
                W = utility[i][j - 1]
            else:
                W = utility[i][j]

            if checkValidity(i + 1, j,size):
                S = utility[i + 1][j]
            else:
                S = utility[i][j]

            North = np.float64(0.7 * N + 0.1 * S + 0.1 * E + 0.1 * W)
            East = np.float64(0.1 * N + 0.1 * S + 0.1 * W + 0.7 * E)
            West = np.float64(0.1 * N + 0.1 * S + 0.7 * W + 0.1 * E)
            South = np.float64(0.1 * N + 0.7 * S + 0.1 * W + 0.1 * E)
            if East >= West:
                pie[i][j] = "E"
            else:
                pie[i][j] = "W"
            if South >= East and South >= West:
                pie[i][j] = "S"
            if North >= South and North >= East and North >= West:
                pie[i][j] = "N"
    #print pie
    return pie

def checkValidity(x,y,size):
    if x < 0 or x >= size or y < 0 or y >= size:
        return False
    return True

def get_money_earned(car, grid_size, obstacles, policy_grid, seed):
    current_location = car.startLocation
    money = 0.0
    np.random.seed(seed)
    swerve = np.random.random_sample(1000000)
    k = 0
    while current_location != car.endLocation:
        desired_move = policy_grid[current_location[0]][current_location[1]]
        actual_move = desired_move
        if swerve[k] > 0.7:
            if swerve[k] > 0.8:
                if swerve[k] > 0.9:
                    actual_move = turn_left(turn_left(desired_move))
                else:
                    actual_move = turn_right(desired_move)
            else:
                actual_move = turn_left(desired_move)
        #print "swerve:",str(swerve[k]),"desired move :",desired_move,"actual : ",actual_move
        if actual_move == "N":
            increment = (-1, 0)
        elif actual_move == "S":
            increment = (1, 0)
        elif actual_move == "E":
            increment = (0, 1)
        else:
            increment = (0, -1)
        next_location = (current_location[0] + increment[0], current_location[1] + increment[1])
        if checkValidity(next_location[0], next_location[1], grid_size):
            current_location = next_location

        money -= 1.0
        if current_location in obstacles:
            money -= 100.0
        k += 1
    money += 100.0
    #print money
    return money


def turn_left(move):
    if move == "N":
        return "W"
    elif move == "S":
        return "E"
    elif move == "E":
        return "N"
    elif move == "W":
        return "S"


def turn_right(move):
    if move == "N":
        return "E"
    elif move == "S":
        return "W"
    elif move == "E":
        return "S"
    elif move == "W":
        return "N"


lines = [line.rstrip() for line in open("input.txt")]
size = int(lines[0])
cars_count = int(lines[1])
obstacles_count = int(lines[2])
carsInfo = {}
obstacles = []

for i in range(0, obstacles_count):
    obstacle_loc = lines[3 + i]
    obstacle_xy = obstacle_loc.split(",")
    obstacles.append((int(obstacle_xy[1]),int(obstacle_xy[0])))
#print obstacles
line_index = 3 + obstacles_count
for i in range(0, cars_count):
    car = Car()
    carsInfo[i] = car
    start_loc = lines[line_index + i]
    start_xy = start_loc.split(",")
    car.set_startlocation((int(start_xy[1]), int(start_xy[0])))
line_index += cars_count
for i in range(0, cars_count):
    car = carsInfo[i]
    end_loc = lines[line_index + i]
    end_xy = end_loc.split(",")
    car.set_endlocation((int(end_xy[1]), int(end_xy[0])))

for i in range(0,cars_count):
    car = carsInfo[i]
    #print car.startLocation,car.endLocation

start = time.time()

for i in range(0, cars_count):
    car = carsInfo[i]
    money = 0.0
    EU = value_iteration(size,car,0.1,obstacles)
    #print EU
    policy = set_policy(EU, size)
    for random_seeds in range(0, 10):
        #print random_seeds
        money += get_money_earned(car, size, obstacles, policy, random_seeds)
    answer = math.floor(money / 10.0)
    #print int(answer)
    output_file = open("output.txt", "a")
    output_file.write(str(int(answer)))
    if(i != cars_count-1):
        output_file.write(("\n"))
output_file.close()
#print time.time()-start
