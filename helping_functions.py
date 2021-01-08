from variables import *


def load_value_to_register(value: int, register):
    code = []
    code.append("RESET " + register)
    code.extend(generate_number(value, register))
    return code


def load_variable_to_register(variable, register):
    if type(variable) == Variable:
        code = load_value_to_register(variable.memory_location, register)
        code.append("LOAD " + register + " " + register)
        return code


def generate_number(value: int, register):
    if value <= 0:
        return []
    elif value == 1:
        return ["INC " + register]
    else:
        code = []
        value_in_binary = str(bin(value)[2:])
        for i in range(len(value_in_binary)):
            if value_in_binary[i] == "1":
                code.append("INC " + register)
            if i < len(value_in_binary) - 1:
                code.append("ADD " + register + " " + register)
    return code
