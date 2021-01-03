from variables import *
from commander import *


class Condition:

    def __init__(self, variable1, variable2):
        self.variable1 = variable1
        self.variable2 = variable2
        self.jump_length = 0
        self.is_condition_static = False

    def generate_code(self, jump_length, register1="a", register2="b"):
        pass


class LessCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b"):
        jump_length = jump_length if jump_length >= 0 else jump_length - \
            len(code)
        jump_length = str(jump_length)
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 < self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + jump_length]
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_value_to_register(
                    self.variable2, second_register))
                code.append("SUB " + second_register + " " + register)
                code.append("JZERO " + second_register + " " + jump_length)
                return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable2, register)
                code.extend(load_value_to_register(
                    self.variable1, second_register))
                code.append("SUB " + second_register + " " + register)
                code.append("JZERO " + second_register + " " + jump_length)
                return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("SUB " + second_register + " " + register)
                code.append("JZERO " + second_register + " " + jump_length)
                return code


class GreaterCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b"):
        jump_length = jump_length if jump_length >= 0 else jump_length - \
            len(code)
        jump_length = str(jump_length)
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 > self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + jump_length]
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_value_to_register(
                    self.variable2, second_register))
                code.append("SUB " + register + " " + second_register)
                code.append("JZERO " + register + " " + jump_length)
                return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable2, register)
                code.extend(load_value_to_register(
                    self.variable1, second_register))
                code.append("SUB " + register + " " + second_register)
                code.append("JZERO " + register + " " + jump_length)
                return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("SUB " + register + " " + second_register)
                code.append("JZERO " + register + " " + jump_length)
                return code


class LessEqualsCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b"):
        jump_length = jump_length if jump_length >= 0 else jump_length - \
            len(code)
        jump_length = str(jump_length)
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 <= self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + jump_length]
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_value_to_register(
                    self.variable2, second_register))
                code.append("INC " + second_register)
                code.append("SUB " + second_register + " " + register)
                code.append("JZERO " + second_register + " " + jump_length)
                return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable2, register)
                code.extend(load_value_to_register(
                    self.variable1, second_register))
                code.append("INC " + second_register)
                code.append("SUB " + second_register + " " + register)
                jump_length = jump_length if jump_length >= 0 else jump_length - \
                    len(code)
                code.append("JZERO " + second_register + " " + jump_length)
                return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("INC " + second_register)
                code.append("SUB " + second_register + " " + register)
                jump_length = jump_length if jump_length >= 0 else jump_length - \
                    len(code)
                code.append("JZERO " + second_register + " " + jump_length)
                return code


class GreaterEqualsCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b"):
        jump_length = jump_length if jump_length >= 0 else jump_length - \
            len(code)
        jump_length = str(jump_length)
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 >= self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + jump_length]
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_value_to_register(
                    self.variable2, second_register))
                code.append("INC " + register)
                code.append("SUB " + register + " " + second_register)
                code.append("JZERO " + register + " " + jump_length)
                return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable2, register)
                code.extend(load_value_to_register(
                    self.variable1, second_register))
                code.append("INC " + register)
                code.append("SUB " + register + " " + second_register)
                code.append("JZERO " + register + " " + jump_length)
                return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("INC " + register)
                code.append("SUB " + register + " " + second_register)
                code.append("JZERO " + register + " " + jump_length)
                return code


class EqualsCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b", third_register="c"):
        jump_length = jump_length if jump_length >= 0 else jump_length - \
            len(code)
        jump_length = str(jump_length)
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 == self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + jump_length]
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_value_to_register(
                    self.variable2, second_register))
                code.append("RESET c")
                code.append("ADD c a")  # a<-first, b<-second, c<-first
                code.append("SUB a b")
                code.append("JZERO a 2")
                # tutaj jeszcze jest dodawane
                code2 = ["SUB b c", "JZERO b 2", "JUMP " + jump_length]
                code.append("JUMP " + str(int(jump_length) + len(code2)))
                code.extend(code2)
                return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable2, register)
                code.extend(load_value_to_register(
                    self.variable1, second_register))
                code.append("RESET c")
                code.append("ADD c a")  # a<-first, b<-second, c<-first
                code.append("SUB a b")
                code.append("JZERO a 2")
                # tutaj jeszcze jest dodawane
                code2 = ["SUB b c", "JZERO b 2", "JUMP " + jump_length]
                code.append("JUMP " + str(int(jump_length) + len(code2)))
                code.extend(code2)
                return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("RESET c")
                code.append("ADD c a")  # a<-first, b<-second, c<-first
                code.append("SUB a b")
                code.append("JZERO a 2")
                # tutaj jeszcze jest dodawane
                code2 = ["SUB b c", "JZERO b 2", "JUMP " + jump_length]
                code.append("JUMP " + str(int(jump_length) + len(code2)))
                code.extend(code2)
                return code


class NotEqualsCondition(Condition):

    def generate_code(self, jump_length, register="a", second_register="b", third_register="c"):
        jump_length = jump_length if jump_length >= 0 else jump_length - \
            len(code)
        jump_length = str(jump_length)
        if type(self.variable1) == int and type(self.variable2) == int:
            self.is_condition_static = True
            if self.variable1 != self.variable2:  # when always true
                return []
            else:  # always false
                return ["JUMP " + jump_length]
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_value_to_register(
                    self.variable2, second_register))
                code.append("RESET c")
                code.append("ADD c a")  # a<-first, b<-second, c<-first
                code.append("SUB a b")
                code.append("JZERO a 2")
                # tutaj jeszcze jest dodawane
                code2 = ["SUB b c", "JZERO b " + jump_length]
                code.append("JUMP " + str(int(jump_length) + len(code2)))
                code.extend(code2)
                return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable2, register)
                code.extend(load_value_to_register(
                    self.variable1, second_register))
                code.append("RESET c")
                code.append("ADD c a")  # a<-first, b<-second, c<-first
                code.append("SUB a b")
                code.append("JZERO a 2")
                # tutaj jeszcze jest dodawane
                code2 = ["SUB b c", "JZERO b " + jump_length]
                code.append("JUMP " + str(int(jump_length) + len(code2)))
                code.extend(code2)
                return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("RESET c")
                code.append("ADD c a")  # a<-first, b<-second, c<-first
                code.append("SUB a b")
                code.append("JZERO a 2")
                # tutaj jeszcze jest dodawane
                code2 = ["SUB b c", "JZERO b " + jump_length]
                code.append("JUMP " + str(int(jump_length) + len(code2)))
                code.extend(code2)
                return code
