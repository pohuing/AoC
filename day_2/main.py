class Intmachine():
    def __init__(self, path, a=12, b=2):
        self.memory = [99]
        self.clock = 0
        self.finished = False
        self.load_file(path)
        self.memory[1] = a
        self.memory[2] = b

    def load_file(self, path):
        with open(path, "r") as f:
            self.memory = [int(raw) for raw in f.readline().split(",")]

    def tick(self):
        (code, location_1, location_2, target_location) = self.memory[self.clock:self.clock+4]
        if code == 1:
            self.memory[target_location] = self.memory[location_1] + self.memory[location_2]
        elif code == 2:
            self.memory[target_location] = self.memory[location_1] * self.memory[location_2]
        elif code == 99:
            print("Execution finished")
            print(f"Position 0: {self.memory[0]}")
            print(f"Clock: {self.clock}")
            self.finished = True
        else:
            print("Something went wrong")
            breakpoint()
        self.clock += 4
    
    def mainloop(self):
        while not self.finished:
            self.tick()
        return self.memory[0]


if __name__ == "__main__":
    part_1 = Intmachine("C:/Users/patri/Desktop/AoC/day_2/input.txt").mainloop()
    result = 0
    results = []
    found = False
    # Bruteforcing part two
    for a in range(0,1000):
        for b in range(0,100):
            intmachine = Intmachine("C:/Users/patri/Desktop/AoC/day_2/input.txt",a=a,b=b)
            result = intmachine.mainloop()
            results.append((a,b,result))
            if result >= 19690720:
                print(f"found combination: {a} {b}")
                found = True
                break
        if found:
            break
