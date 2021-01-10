from variables import *
import commander


def load_value_to_register(value, register):
    if type(value) == Variable:
        if not value.is_shadowed:
            code = []
            code.append("RESET " + register)
            code.extend(generate_number(value.memory_location, register))
            code.append("LOAD " + register + " " + register)
            return code
        else:
            return load_value_to_register(value.reference_to_iterator.memory_location, register)
    elif type(value) == int:
        code = []
        code.append("RESET " + register)
        code.extend(generate_number(value, register))
        return code
    elif type(value) == str:
        iterator = [
            el for el in commander.Program.iterators_stack if el.pid == value][0]
        if not iterator:
            raise NotImplementedError  # TODO
        return load_value_to_register(iterator.memory_location, register)


def load_variable_to_register(variable, register):
    return load_value_to_register(variable, register)


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
