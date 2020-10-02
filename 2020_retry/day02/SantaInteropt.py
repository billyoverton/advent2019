import util

class SantaInteropt(object):

    def __init__(self, memory=None):

        # Init the memory
        if memory is None:
            self.memory = [99] # Init memory to a halt only program
        else:
            self.memory = memory.copy()
            self._original_memory = memory.copy()

        # Start the instruction pointer at 0
        self.ip = 0
        self.is_halted = False

    def _execute_opt(self, code):
        if code == 1:
            self._opt_1()
        elif code == 2:
            self._opt_2()
        elif code == 99:
            self.is_halted = True
        else:
            sys.exit(f'Invalid instruction {code} encountered')

    def _opt_1(self):
        value1_loc = self.memory[self.ip + 1]
        value2_loc = self.memory[self.ip + 2]
        result_loc = self.memory[self.ip + 3]
        self.memory[result_loc] = self.memory[value1_loc] + self.memory[value2_loc]
        self.ip += 4

    def _opt_2(self):
        value1_loc = self.memory[self.ip + 1]
        value2_loc = self.memory[self.ip + 2]
        result_loc = self.memory[self.ip + 3]
        self.memory[result_loc] = self.memory[value1_loc] * self.memory[value2_loc]
        self.ip += 4

    def step(self):
        opt_code = self.memory[self.ip]
        self._execute_opt(opt_code)

    def execute(self):
        while not self.is_halted:
            self.step()

    def reset(self):
        self.memory = self._original_memory.copy()
        self.ip = 0
        self.is_halted = False
