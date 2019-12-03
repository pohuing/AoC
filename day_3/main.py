import matplotlib.pyplot as plt 
from matplotlib.path import Path
import matplotlib.patches as patches


class Wire():
    def __init__(self, movements):
        self.points={(0,0):0}
        self.trace_movements(movements)

    def trace_movements(self, movements):
        x,y = (0,0)
        distance_walked = 0
        for movement in movements:
            direction = movement[0]
            distance = int(movement[1:])
            if direction == "U":
                while distance > 0:
                    distance -= 1
                    y += 1
                    distance_walked +=1
                    # Pathetic attempt at minimizing loops, but as it turns out
                    # we're not supposed to do that anyways
                    # if (x,y) in self.points:
                    #     distance_walked = self.points[(x,y)]
                    # else:
                    #     self.points[(x,y)] = distance_walked
                    self.points[(x,y)] = distance_walked
            elif direction == "R":
                while distance > 0:
                    distance -= 1
                    x += 1
                    distance_walked +=1
                    # if (x,y) in self.points:
                    #     distance_walked = self.points[(x,y)]
                    # else:
                    #     self.points[(x,y)] = distance_walked
                    self.points[(x,y)] = distance_walked
            elif direction == "D":
                while distance > 0:
                    distance -= 1
                    y -= 1
                    distance_walked +=1
                    # if (x,y) in self.points:
                    #     distance_walked = self.points[(x,y)]
                    # else:
                    #     self.points[(x,y)] = distance_walked
                    self.points[(x,y)] = distance_walked
            elif direction == "L":
                while distance > 0:
                    distance -= 1
                    x -= 1
                    distance_walked +=1
                    # if (x,y) in self.points:
                    #     distance_walked = self.points[(x,y)]
                    # else:
                    #     self.points[(x,y)] = distance_walked
                    self.points[(x,y)] = distance_walked
            else:
                print("didn't recognize movement: ", movement)
                breakpoint()


class Point():
    def __init__(self, x, y, distance_walked):
        self.x = x
        self.y = y
        self.distance_walked = distance_walked

    def get_points(self):
        return (self.x, self.y)

    def __lt__(self, other):
        return abs(self.x) + abs(self.y) < abs(other.x) + abs(other.y)

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __str__(self):
        return f"{self.x} {self.y}"

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.distance_walked})"

def find_intersections(a:Wire,b:Wire):
    intersections = []
    for key in a.points:
        if key in b.points:
            intersections.append(Point(*key, a.points[key] + b.points[key]))
    return intersections



def test_distance_intersections():
    a = Wire("U7,R6,D4,L4".split(","))
    b = Wire("R8,U5,L5,D3".split(","))
    intersections = find_intersections(a,b)
    closest = sorted(intersections)
    least_distance = sorted(intersections, key=lambda x: x.distance_walked)
    for i,intersection in enumerate(closest):
        assert intersection.get_points() == [(0,0), (3,3), (6,5)][i]
    for i,intersection in enumerate(least_distance):
        assert intersection.distance_walked == [0,30,40][i]

    a = Wire("R75,D30,R83,U83,L12,D49,R71,U7,L72".split(","))
    b = Wire("U62,R66,U55,R34,D71,R55,D58,R83".split(","))
    intersections = find_intersections(a,b)
    least_distance = sorted(intersections, key=lambda x: x.distance_walked)[1]
    assert least_distance.distance_walked == 610

    a = Wire("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(","))
    b = Wire("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(","))
    intersections = find_intersections(a,b)
    least_distance = sorted(intersections, key=lambda x: x.distance_walked)[1]
    assert least_distance.distance_walked == 410


def visualize():
    line_a = []
    with open("./day_3/input.txt", "r") as f:
        for movement in f.readline().split(","):
            line_a.append(movement)
            
    positions = [(0,0)]
    movement_types = [Path.MOVETO]
    
    (x,y) = (0,0)
    for movement in line_a:
        direction = movement[0]
        distance = int(movement[1:])
        if direction == "U":
            y += distance
        elif direction == "R":
            x += distance
        elif direction == "D":
            y -= distance
        elif direction == "L":
            x -= distance
        else:
            print("didn't recognize movement: ", movement)
            breakpoint()
        positions.append((x,y))
        movement_types.append(Path.LINETO)
    
    path = Path(positions, movement_types)
    fix,ax = plt.subplots()
    patch = patches.PathPatch(path, lw=1, facecolor="none")
    ax.add_patch(patch)


    line_a = []
    with open("./day_3/input.txt", "r") as f:
        f.readline()
        for movement in f.readline().split(","):
            line_a.append(movement)
            
    positions = [(0,0)]
    movement_types = [Path.MOVETO]
    
    (x,y) = (0,0)
    for movement in line_a:
        direction = movement[0]
        distance = int(movement[1:])
        if direction == "U":
            y += distance
        elif direction == "R":
            x += distance
        elif direction == "D":
            y -= distance
        elif direction == "L":
            x -= distance
        else:
            print("didn't recognize movement: ", movement)
            breakpoint()
        positions.append((x,y))
        movement_types.append(Path.LINETO)
    
    path = Path(positions, movement_types)
    patch = patches.PathPatch(path, lw=1, facecolor="none", edgecolor="red")
    ax.add_patch(patch)


    ax.set_xlim(-10000, 10000)
    ax.set_ylim(-10000, 10000)
    plt.show()



if __name__ == "__main__":
    test_distance_intersections()

    wires = []
    with open("./day_3/input.txt", "r") as f:
        for line in f:
            wires.append(Wire(line.split(",")))

    visualize()

    intersections = find_intersections(*wires)
    least_distance = sorted(intersections, key=lambda x: x.distance_walked)
    print(f"\"shortest\" way to an intersection is {least_distance[1].distance_walked}")