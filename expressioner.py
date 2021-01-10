from helping_functions import *


class Expression:

    def __init__(self, variable1, variable2=None):
        self.variable1 = variable1
        self.variable2 = variable2

    def generate_code(self, register):
        pass


class ValueExpression(Expression):

    def generate_code(self, register):
        if type(self.variable1) == int:
            return load_value_to_register(self.variable1, register)

        elif isinstance(self.variable1, Variable):
            code = load_variable_to_register(self.variable1, register)
            code.append("LOAD " + register + " " + register)
            return code


class AddExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 + self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                if self.variable2 == 0:
                    return ValueExpression(self.variable1).generate_code(register)
                else:
                    code = load_variable_to_register(self.variable1, register)
                    code.extend(load_value_to_register(
                        self.variable2, second_register))
                    code.append("ADD " + register + " " + second_register)
                    return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                if self.variable1 == 0:
                    return ValueExpression(self.variable2).generate_code(register)
                else:
                    code = load_variable_to_register(self.variable2, register)
                    code.extend(load_value_to_register(
                        self.variable1, second_register))
                    code.append("ADD " + register + " " + second_register)
                    return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("ADD " + register + " " + second_register)
                return code


class SubExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 - self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                if self.variable2 == 0:
                    return ValueExpression(self.variable1).generate_code(register)
                else:
                    code = load_variable_to_register(self.variable1, register)
                    code.extend(load_value_to_register(
                        self.variable2, second_register))
                    code.append("SUB " + register + " " + second_register)
                    return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                if self.variable1 == 0:
                    return ValueExpression(self.variable2).generate_code(register)
                else:
                    code = load_variable_to_register(self.variable2, register)
                    code.extend(load_value_to_register(
                        self.variable1, second_register))
                    code.append("SUB " + register + " " + second_register)
                    return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("SUB " + register + " " + second_register)
                return code


class MulExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 * self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                if self.variable2 == 0:
                    return ValueExpression(self.variable1).generate_code(register)
                else:
                    code = load_variable_to_register(self.variable1, register)
                    code.extend(load_value_to_register(
                        self.variable2, second_register))
                    code.append("RESET a")
                    code.append("JZERO c 4")
                    code.append("ADD a b")
                    code.append("DEC c")
                    code.append("JUMP -3")
                    return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                if self.variable1 == 0:
                    return ValueExpression(self.variable2).generate_code(register)
                else:
                    code = load_variable_to_register(self.variable2, register)
                    code.extend(load_value_to_register(
                        self.variable1, second_register))
                    code.append("RESET a")
                    code.append("JZERO c 4")
                    code.append("ADD a b")
                    code.append("DEC c")
                    code.append("JUMP -3")
                    return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("RESET a")
                code.append("JZERO c 4")
                code.append("ADD a b")
                code.append("DEC c")
                code.append("JUMP -3")
                return code


class DivExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 // self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                if self.variable2 == 0:
                    return ["RESET a"]
                else:
                    code = load_variable_to_register(self.variable1, register)
                    code.extend(load_value_to_register(
                        self.variable2, second_register))
                    code.append("RESET a")
                    code.append("JZERO b 9")
                    code.append("RESET d")
                    code.append("ADD d b ")
                    code.append("INC d")
                    code.append("SUB d c")
                    code.append("JZERO d 4")
                    code.append("INC a")
                    code.append("SUB b c")
                    code.append("JUMP -8")
                    return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                if self.variable1 == 0:
                    return ["RESET a"]
                else:
                    code = load_variable_to_register(self.variable2, register)
                    code.extend(load_value_to_register(
                        self.variable1, second_register))
                    code.append("RESET a")
                    code.append("JZERO b 9")
                    code.append("RESET d")
                    code.append("ADD d b ")
                    code.append("INC d")
                    code.append("SUB d c")
                    code.append("JZERO d 4")
                    code.append("INC a")
                    code.append("SUB b c")
                    code.append("JUMP -8")
                    return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("RESET a")
                code.append("JZERO b 9")
                code.append("RESET d")
                code.append("ADD d b ")
                code.append("INC d")
                code.append("SUB d c")
                code.append("JZERO d 4")
                code.append("INC a")
                code.append("SUB b c")
                code.append("JUMP -8")
                return code


class ModExpression(Expression):

    def generate_code(self, register):
        register = "a"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 % self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if type(self.variable1) == Variable:
                if self.variable2 == 0:
                    return ["RESET a"]
                else:
                    code = load_variable_to_register(self.variable1, register)
                    code.extend(load_value_to_register(
                        self.variable2, second_register))
                    code.append("JZERO b ile")
                    code.append("RESET c")
                    code.append("ADD c a ")
                    code.append("INC c")
                    code.append("SUB c b")
                    code.append("JZERO d 4")
                    code.append("SUB a b")
                    code.append("JUMP -6")
                    code.append("RESET a")
                    return code
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if type(self.variable2) == Variable:
                if self.variable1 == 0:
                    return ["RESET a"]
                else:
                    code = load_variable_to_register(self.variable2, register)
                    code.extend(load_value_to_register(
                        self.variable1, second_register))
                    code.append("JZERO b ile")
                    code.append("RESET c")
                    code.append("ADD c a ")
                    code.append("INC c")
                    code.append("SUB c b")
                    code.append("JZERO d 4")
                    code.append("SUB a b")
                    code.append("JUMP -6")
                    code.append("RESET a")
                    return code
        elif isinstance(self.variable1, Variable) and isinstance(self.variable2, Variable):
            if type(self.variable1) == Variable and type(self.variable2) == Variable:
                code = load_variable_to_register(self.variable1, register)
                code.extend(load_variable_to_register(
                    self.variable2, second_register))
                code.append("JZERO b ile")
                code.append("RESET c")
                code.append("ADD c a ")
                code.append("INC c")
                code.append("SUB c b")
                code.append("JZERO d 4")
                code.append("SUB a b")
                code.append("JUMP -6")
                code.append("RESET a")
                return code
