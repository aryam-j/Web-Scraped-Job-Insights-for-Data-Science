class Resource:
    def __init__(self, cpu, mem, space):
        self.cpu, self.mem, self.space = cpu, mem, space

    def __lt__(self, other):
        return self.cpu < other.cpu and self.mem < other.mem and self.space < other.space

    def __add__(self, other):
        return Resource(self.cpu + other.cpu,
                        self.mem + other.mem,
                        self.space + other.space)

    def __sub__(self, other):
        return Resource(self.cpu - other.cpu,
                        self.mem - other.mem,
                        self.space - other.space)

class Laptop:
    def __init__(self, resource):
        self.resource = resource
        self.latest_pid = 0
        self.program_requirements = {}

    def run_program(self, resource_requirement):
        if self.resource < resource_requirement:
            return -1
        self.resource -= resource_requirement

        self.latest_pid += 1
        self.program_requirements[self.latest_pid] = resource_requirement
        return self.latest_pid

    def exit_program(self, pid):
        try:
            self.resource += self.program_requirements[pid]
            del self.program_requirements[pid]
            return True
        except KeyError:
            return False


resource = Resource(cpu=20, mem=5000, space=10000)
laptop = Laptop(resource)
pid1 = laptop.run_program()
# pid2 = laptop.run_program(4, 500, 1000)
# pid3 = laptop.run_program(5, 500, 1000)

print(laptop.exit_program(pid1))
print(laptop.exit_program(pid1))
print(laptop.exit_program(pid1))
print(laptop.exit_program(pid1))
print(laptop.exit_program(12))
