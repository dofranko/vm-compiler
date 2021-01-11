from helping_functions import *


class Expression:

    def __init__(self, variable1, variable2=None):
        self.variable1 = variable1
        self.variable2 = variable2

    def generate_code(self, register):
        pass


class ValueExpression(Expression):

    def generate_code(self, register):
        return load_value_to_register(self.variable1, register)


class AddExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 + self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if self.variable2 == 0:
                return ValueExpression(self.variable1).generate_code(register)
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if self.variable1 == 0:
                return ValueExpression(self.variable2).generate_code(register)
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register)
        code.append("ADD " + register + " " + second_register)
        return code


class SubExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 - self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if self.variable2 == 0:
                return ValueExpression(self.variable1).generate_code(register)
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if self.variable1 == 0:
                return ValueExpression(self.variable2).generate_code(register)
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register)
        code.append("SUB " + register + " " + second_register)
        return code


class MulExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 * self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if self.variable2 == 1:
                return ValueExpression(self.variable1).generate_code(register)
            elif self.variable2 == 0:
                return ["RESET " + register]
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if self.variable1 == 1:
                return ValueExpression(self.variable2).generate_code(register)
            elif self.variable1 == 0:
                return ["RESET " + register]
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register)
        code.append("RESET d")
        # mnożenie
        code.append("JODD c 5")
        code.append("ADD " + register + " " + register)
        code.append("SHR " + second_register)
        code.append("JZERO " + second_register + " 4")
        code.append("JUMP -4")
        code.append("ADD d " + register)
        code.append("JUMP -5")
        code.extend(["RESET " + register, "ADD " + register + " d"])
        return code


class DivExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 // self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if self.variable2 == 0:
                return ["RESET a"]
            if self.variable2 == 1:
                return ValueExpression(self.variable1).generate_code(register)
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if self.variable1 == 0:
                return ["RESET a"]
            
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register)
        code.extend(["RESET d", "RESET e", "RESET f"])
        
        code.append("JZERO c 2") #gdy drugi jest 0
        code.append("JUMP 3")
        code.append("RESET b")
        code.append("JUMP 31") #skok ponad wszystko
        
        ## sprawdzenie czy 1
        code.append("DEC c")
        code.append("JZERO c 29")
        # sprawdzeie czy 2
        code.append("DEC c")
        code.append("JZERO c 4")
        code.append("INC c")
        code.append("INC c")
        code.append("JUMP 3")
        code.append("SHR b")
        code.append("JUMP 22")
        #
        ##
        code.append("INC e") #e=1
        
        code.append("RESET f")
        code.append("ADD f b")
        code.append("SUB f c")
        code.append("JZERO f 4")
        code.append("SHL c")
        code.append("SHL e")
        code.append("JUMP -6")

        code.append("RESET f")
        code.append("ADD f c")
        code.append("SUB f b")
        code.append("JZERO f 2")
        code.append("JUMP 3")
        code.append("SUB b c")
        code.append("ADD d e")
        code.append("SHR c")
        code.append("SHR e")
        code.append("JZERO e 2") #exit
        code.append("JUMP -10")
        
        code.append("RESET b")
        code.append("ADD b d")  
        
        return code


class ModExpression(Expression):

    def generate_code(self, register):
        register = "b"
        second_register = "b" if register != "b" else "c"
        if type(self.variable1) == int and type(self.variable2) == int:
            return load_value_to_register(self.variable1 % self.variable2, register)
        elif isinstance(self.variable1, Variable) and type(self.variable2) == int:
            if self.variable2 == 0 or self.variable2 == 1:
                return ["RESET b"]
        elif type(self.variable1) == int and isinstance(self.variable2, Variable):
            if self.variable1 == 0 or self.variable1 == 1:
                return ["RESET b"]
                
        code = load_two_values_to_registers(self.variable1, self.variable2, register, second_register)
        code.extend(["RESET d", "RESET e", "RESET f"])
        code.append("JZERO c 2") #gdy drugi jest 0
        code.append("JUMP 3")
        code.append("RESET b")
        code.append("JUMP 38") #skok ponad wszystko
        
        ## sprawdzenie czy 1
        code.append("DEC c")
        code.append("JZERO c 2")
        code.append("JUMP 3")
        code.append("RESET b")
        code.append("JUMP 33")
        # sprawdzeie czy 2
        code.append("DEC c")
        code.append("JZERO c 4")
        code.append("INC c")
        code.append("INC c")
        code.append("JUMP 9")
        code.append("JODD b 3") 
        code.append("RESET b") 
        code.append("JUMP 25")
        code.append("RESET b")
        code.append("INC b")
        code.append("JUMP 22") 
        code.append("INC b")
        code.append("JUMP 20")

        code.append("INC e") #e=1
        
        code.append("RESET f")
        code.append("ADD f b")
        code.append("SUB f c")
        code.append("JZERO f 4")
        code.append("SHL c")
        code.append("SHL e")
        code.append("JUMP -6")

        code.append("RESET f")
        code.append("ADD f c")
        code.append("SUB f b")
        code.append("JZERO f 2")
        code.append("JUMP 3")
        code.append("SUB b c")
        code.append("ADD d e")
        code.append("SHR c")
        code.append("SHR e")
        code.append("JZERO e 2") #exit
        code.append("JUMP -10")
        
        return code


