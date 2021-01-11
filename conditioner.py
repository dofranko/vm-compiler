from variables import *
from helping_functions import *


class Condition:

    def __init__(self, variable1, variable2):
        self.variable1 = variable1
        self.variable2 = variable2
        self.jump_length = 0
        self.is_condition_static = False

    def generate_code(self, jump_length, register1="a", register2="b"):
        pass

    def get_jump_length(self, code: list):
        toret = self.jump_length if self.jump_length >= 0 else self.jump_length - \
            len(code)
        return str(toret)


class LessCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 < self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register, "c")
        code.append("SUB " + second_register + " " + register)
        code.append("JZERO " + second_register +
                    " " + self.get_jump_length(code)) #when false, jump to else/end
        return code


class GreaterCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 > self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register, "c")
        code.append("SUB " + register + " " + second_register)
        code.append("JZERO " + register + " " +
                    self.get_jump_length(code)) #when false, jump to else/end
        return code


class LessEqualsCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 <= self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register, "c")
        code.append("INC " + second_register)
        code.append("SUB " + second_register + " " + register)
        code.append("JZERO " + second_register +
                    " " + self.get_jump_length(code))
        return code


class GreaterEqualsCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 >= self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register, "c")
        code.append("INC " + register)
        code.append("SUB " + register + " " + second_register)
        code.append("JZERO " + register + " " +
                    self.get_jump_length(code))
        return code


class EqualsCondition(Condition):

    def get_jump_length_first(self, code1: list, code2: list):
        if self.jump_length > 0:
            return str(self.jump_length + len(code2))
        elif self.jump_length < 0:
            return str(self.jump_length - len(code1))

    def get_jump_length_second(self, code1: list, code2: list):
        if self.jump_length > 0:
            return str(self.jump_length)
        elif self.jump_length < 0:
            return str(self.jump_length - len(code1) - len(code2) + 1) # +1 gdyż nie liczymy instr JUMP do len()

    def generate_code(self, jump_length, register="a", second_register="b", third_register="c"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 == self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]

        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register, "c")
        code.append("RESET c")
        code.append("ADD c a")  # a<-first, b<-second, c<-first
        code.append("SUB a b")
        code.append("JZERO a 2")
        # tutaj jeszcze jest dodawane
        code2 = ["SUB b c", "JZERO b 2", "JUMP "]
        code.append("JUMP " + self.get_jump_length_first(code, code2))
        code2[-1] += self.get_jump_length_second(code, code2) # add jump length
        code.extend(code2)
        return code


class NotEqualsCondition(Condition):

    def get_jump_length_first(self, code1: list, code2: list):
        if self.jump_length > 0:
            return str(len(code2) + 1)
        elif self.jump_length < 0:
            return str(self.jump_length - len(code1))

    def get_jump_length_second(self, code1: list, code2: list):
        if self.jump_length > 0:
            return str(self.jump_length)
        elif self.jump_length < 0:
            return str(self.jump_length - len(code1) - len(code2) + 1)

    def generate_code(self, jump_length, register="a", second_register="b", third_register="c"):
        self.jump_length = jump_length
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 != self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + self.get_jump_length([])]
        
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register, "c")
        code.append("RESET c")
        code.append("ADD c a")  # a<-first, b<-second, c<-first
        code.append("SUB a b")
        code.append("JZERO a 2")
        # tutaj jeszcze jest dodawane
        code2 = ["SUB b c", "JZERO b "]
        code.append("JUMP " + self.get_jump_length_first(code, code2))
        code2[-1] += self.get_jump_length_second(code, code2)
        code.extend(code2)
        return code
