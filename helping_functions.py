from variables import *
import commander


def load_value_to_register(value, register, do_variablearray_memory = False, second_register="c", do_iterator_memory = False):
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
        code = load_value_to_register(iterator.memory_location, register)
        if not do_iterator_memory:
            code.append("LOAD " + register + " " + register)
        return code
    elif type(value) == VariableOfArray:
        code = load_value_to_register(value.array.memory_location, register)
        code.extend(load_value_to_register(value.index, second_register))
        code.append("ADD " + register + " " + second_register)
        code.extend(load_value_to_register(value.array.start, second_register))
        code.append("SUB " + register + " " + second_register)
        if not do_variablearray_memory:
            code.append("LOAD " + register + " " + register)
        return code
        


def load_variable_to_register(variable, register):
    return load_value_to_register(variable, register)

def load_two_values_to_registers(value1, value2, register1="b", register2="c", register3="d"):
    code = load_value_to_register(value1, register1, second_register=register2)
    code.extend(load_value_to_register(value2, register2, second_register=register3))
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
                code.append("SHL " + register)
    return code
