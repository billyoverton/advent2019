import util
class SantaInteropt(object):

    STATE_HALTED = 0
    STATE_WAITING_FOR_INPUT = 1
    STATE_READY = 2
    STATE_RUNNING = 3
    STATE_OUT_OF_MEMORY = 4

    def __init__(self, memory=None, input_buffer=None):
        if memory is None:
            self.memory = [99]
        else:
            self.memory = memory

        self.instruction_pointer = 0

        if input_buffer is None:
            self.input_buffer = []
        else:
            self.input_buffer = input_buffer

        self.output_buffer = []

        self.state = self.STATE_READY

    @property
    def memory(self):
        return self._memory

    @memory.setter
    def memory(self, memory):
        self._memory = memory
        self._original_memory = [x for x in memory]
        self.reset()

    def reset(self):
        self._memory = [x for x in self._original_memory]
        self.instruction_pointer = 0
        self.input_buffer = []
        self.output_buffer = []
        self.state = self.STATE_READY

    def input(self, value):
        self.input_buffer.append(value)

    def _get_input(self):
        if len(self.input_buffer) > 0:
            val = self.input_buffer.pop(0)
            return val
        else:
            self.state = self.STATE_WAITING_FOR_INPUT
            return None

    def _execute_opt(self, opt_code):

        digits = [ util.get_digit(opt_code, x) for x in range(5)]
        opt_code = digits[0] + 10*digits[1]

        param_modes = digits[2:]

        if opt_code == 1:
            self._opt_1(param_modes)
        elif opt_code == 2:
            self._opt_2(param_modes)
        elif opt_code == 3:
            self._opt_3(param_modes)
        elif opt_code == 4:
            self._opt_4(param_modes)
        elif opt_code == 5:
            self._opt_5(param_modes)
        elif opt_code == 6:
            self._opt_6(param_modes)
        elif opt_code == 7:
            self._opt_7(param_modes)
        elif opt_code == 8:
            self._opt_8(param_modes)
        elif opt_code == 99:
            self.state = self.STATE_HALTED

    def _get_value(self, input, opt_mode):
        if opt_mode == 0:
            return self.memory[input]
        if opt_mode == 1:
            return input

    # Add operator
    def _opt_1(self, param_modes):

        param1 = self._get_value(self.memory[self.instruction_pointer], param_modes[0])
        param2 = self._get_value(self.memory[self.instruction_pointer+1], param_modes[1])
        dest = self.memory[self.instruction_pointer+2]
        self.instruction_pointer += 3

        self.memory[dest] = param1 + param2

    # Multiply operator
    def _opt_2(self, param_modes):
        param1 = self._get_value(self.memory[self.instruction_pointer], param_modes[0])
        param2 = self._get_value(self.memory[self.instruction_pointer+1], param_modes[1])
        dest = self.memory[self.instruction_pointer+2]
        self.instruction_pointer += 3

        self.memory[dest] = param1 * param2

    # Input operator
    def _opt_3(self, param_modes):
        dest = self.memory[self.instruction_pointer]
        self.instruction_pointer += 1
        val = self._get_input()

        if val is None:
            # We are waiting for input so reset us back
            self.instruction_pointer += -1
        else:
            self.memory[dest] = val

    # Output operator
    def _opt_4(self, param_modes):
        param1 = self._get_value(self.memory[self.instruction_pointer], param_modes[0])
        self.instruction_pointer += 1

        self.output_buffer.append(param1)

    # Jump-if-true operator
    def _opt_5(self, param_modes):
        param1 = self._get_value(self.memory[self.instruction_pointer], param_modes[0])
        param2 = self._get_value(self.memory[self.instruction_pointer+1], param_modes[1])
        self.instruction_pointer += 2

        if param1 != 0:
            self.instruction_pointer = param2

    # Jump-if-false operator
    def _opt_6(self, param_modes):
        param1 = self._get_value(self.memory[self.instruction_pointer], param_modes[0])
        param2 = self._get_value(self.memory[self.instruction_pointer+1], param_modes[1])
        self.instruction_pointer += 2

        if param1 == 0:
            self.instruction_pointer = param2

    # less than operator
    def _opt_7(self, param_modes):
        param1 = self._get_value(self.memory[self.instruction_pointer], param_modes[0])
        param2 = self._get_value(self.memory[self.instruction_pointer+1], param_modes[1])
        param3 = self.memory[self.instruction_pointer+2]
        self.instruction_pointer += 3

        if param1 < param2:
            self.memory[param3] = 1
        else:
            self.memory[param3] = 0

    # equals operator
    def _opt_8(self, param_modes):
        param1 = self._get_value(self.memory[self.instruction_pointer], param_modes[0])
        param2 = self._get_value(self.memory[self.instruction_pointer+1], param_modes[1])
        param3 = self.memory[self.instruction_pointer+2]
        self.instruction_pointer += 3

        if param1 == param2:
            self.memory[param3] = 1
        else:
            self.memory[param3] = 0

    def execute(self):
        self.state = self.STATE_RUNNING

        while self.state == self.STATE_RUNNING:
            opt_code = self.memory[self.instruction_pointer]
            self.instruction_pointer += 1
            self._execute_opt(opt_code)
            if self.state in [self.STATE_WAITING_FOR_INPUT]:
                self.instruction_pointer += -1
