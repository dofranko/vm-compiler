from variables import *
from expressioner import *
from conditioner import *
from helping_functions import *


class Program:

    variables = {}
    iterators_stack = []
    next_free_memory_location = -1

    def __init__(self):
        self.commands = []

    def __init__(self, commands: list, variables_dict: dict, next_free_memory_location: int, output_file_name: str):
        self.commands = commands
        self.output_file_name = output_file_name
        Program.variables = variables_dict
        Program.next_free_memory_location = next_free_memory_location

    def add_command(self, command):
        self.commands.append(command)

    def execute_commands(self):
        self.commands.append(HaltCommand())
        try:
            code = ""
            for i in self.commands:
                if isinstance(i, Command):
                    i.generate_code()
                    code += "\n".join(i.code) + "\n"
                    print("\n".join(i.code))
            with open(self.output_file_name, "w") as file:
                file.write(code)
        except Exception as e:
            print(e)


class Command:

    def __init__(self):
        pass

    def generate_code(self):
        pass


class HaltCommand(Command):

    def __init__(self):
        self.code = []

    def generate_code(self):
        self.code = ["HALT"]


class WriteCommand(Command):

    def __init__(self, variable):
        self.variable = variable
        self.code = []

    def generate_code(self):
        if type(self.variable) == int:
            pass
        elif isinstance(self.variable, Variable):
            self.code = load_value_to_register(
                self.variable, "a")
            self.code.append("PUT " + "a")


class ReadCommand(Command):

    def __init__(self, variable):
        self.variable = variable
        self.code = []

    def generate_code(self):
        self.code = load_value_to_register(
            self.variable.memory_location, "a")
        self.code.append("GET " + "a")


class AssignCommand(Command):

    def __init__(self, variable, expression: Expression):
        self.variable = variable
        self.expression = expression
        self.code = []

    def generate_code(self, register="b"):
        self.code = self.expression.generate_code("b")
        self.code.extend(load_value_to_register(
            self.variable, "a"))
        self.code.append("STORE " + register + " a")


class IfCommand(Command):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)
        code = self.condition.generate_code(len(commands_code)+1)
        code.extend(commands_code)


class IfElseCommand(Command):

    def __init__(self, condition: Condition, commands_if: list, commands_else: list):
        self.condition = condition
        self.commands_if = commands_if
        self.commands_else = commands_else
        self.code = []

    def generate_code(self, register="a"):
        commands_if_code = []
        commands_else_code = []
        for command in self.commands_if:
            command.generate_code()
            commands_if_code.extend(command.code)

        for command in self.commands_else:
            command.generate_code()
            commands_else_code.extend(command.code)

        self.code = self.condition.generate_code(len(commands_if_code)+1)
        self.code.extend(commands_if_code)
        self.code.extend(commands_else_code)


class WhileCommand(Command):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)

        self.code = self.condition.generate_code(len(commands_code)+2)
        self.code.extend(commands_code)
        self.code.append("JUMP " + str(-len(self.code)))


class RepeatCommand(Command):

    def __init__(self, condition: Condition, commands: list):
        self.condition = condition
        self.commands = commands
        self.code = []

    def generate_code(self, register="a"):
        commands_code = []
        for command in self.commands:
            command.generate_code()
            commands_code.extend(command.code)

        self.code = commands_code
        self.code.extend(self.condition.generate_code(-len(self.code)))


class ForCommand(Command):

    def __init__(self, pid: str,  from_value: int, to_value: int, commands: list):
        self.pid = pid
        self.commands = commands
        self.from_value = from_value
        self.to_value = to_value
        self.code = []

    def contains_another_for(self):
        return True

    def generate_code(self, register="a"):
        # optymalizacje: gdy jeden for; przeskoczenie pierwszego wczytania
        self.code = load_value_to_register(self.from_value, "e")
        self.code.extend(load_value_to_register(self.to_value, "f"))
        self.code.append("INC f")

        my_iterator = add_iterator(self.pid, self.from_value, self.to_value)

        self.code.extend(load_value_to_register(
            my_iterator.memory_location, "d"))
        # e-poczatek iteratora, f-koniec iteratora +1, (+1 dla warunku czy wiekszy)
        # d-memory iteratora, d+1 -> memory konca iteratora
        self.code.extend(["STORE e d", "INC d", "STORE f d", "DEC d"])
        # --- kod sprawdzenia warunku
        condition_code = ["SUB f e"]
        # --- kody podkomend + store iteratora
        sub_commands_code = ["STORE e d"]
        for command in self.commands:
            command.generate_code()
            sub_commands_code.extend(command.code)
        # --- kod inkrementacji iteratora
        incrementation_code = load_value_to_register(
            my_iterator.memory_location, "d")
        incrementation_code.extend(
            ["LOAD e d", "INC d", "LOAD f d", "DEC d", "INC e"])
        # --- przeskok z warunku poza for'a
        # +1 żeby poza kod, +1 żeby ponad jumpa
        condition_code.append("JZERO f " + str(len(sub_commands_code)+2))
        # --- przeskok do sprawdzania warunku
        jump_code = "JUMP " + \
            str(-(len(sub_commands_code) +
                  len(condition_code) + len(incrementation_code)))

        self.code.extend(condition_code)
        self.code.extend(sub_commands_code)
        self.code.extend(incrementation_code)
        self.code.append(jump_code)
        remove_iterator(my_iterator)


class ForDownCommand(Command):
    def __init__(self, pid: str,  from_value: int, to_value: int, commands: list):
        self.pid = pid
        self.commands = commands
        self.from_value = from_value
        self.to_value = to_value
        self.code = []

    def contains_another_for(self):
        return True

    def generate_code(self, register="a"):
        # Różnica z ForNormal: zawsze jest INC iteratora przy sprawdzaniu, zamiast dodac go na początku
        # optymalizacje: gdy jeden for; przeskoczenie pierwszego wczytania
        self.code = load_value_to_register(self.from_value, "e")
        self.code.extend(load_value_to_register(self.to_value, "f"))

        my_iterator = add_iterator(self.pid, self.from_value, self.to_value)

        self.code.extend(load_value_to_register(
            my_iterator.memory_location, "d"))
        # e-poczatek iteratora, f-koniec iteratora +1, (+1 dla warunku czy wiekszy)
        # d-memory iteratora, d+1 -> memory konca iteratora
        self.code.extend(["STORE e d", "INC d", "STORE f d", "DEC d"])
        # --- kod sprawdzenia warunku
        condition_code = ["INC e", "SUB e f"]
        # --- kody podkomend + store iteratora z przywróceniem
        sub_commands_code = ["ADD e f", "DEC e", "DEC e", "STORE e d"]
        for command in self.commands:
            command.generate_code()
            sub_commands_code.extend(command.code)
        # --- kod inkrementacji iteratora
        incrementation_code = load_value_to_register(
            my_iterator.memory_location, "d")
        incrementation_code.extend(
            ["LOAD e d", "JZERO e " + str(1+len(jump_code)), "INC d", "LOAD f d", "DEC d"])  # +1 poza kod, +1 poza jump_code
        # --- przeskok z warunku poza for'a
        # +1 żeby poza kod, +1 żeby ponad jumpa
        condition_code.append(
            "JZERO e " + str(len(sub_commands_code) + 2))
        # --- przeskok do sprawdzania warunku
        jump_code = "JUMP " + \
            str(-(len(sub_commands_code) +
                  len(condition_code) +
                  len(incrementation_code)))

        self.code.extend(condition_code)
        self.code.extend(sub_commands_code)
        self.code.extend(incrementation_code)
        self.code.append(jump_code)
        remove_iterator(my_iterator)

# TODO nie wiem co


def add_iterator(pid, start, end):
    iterator = VariableIterator(
        pid, Program.next_free_memory_location, start, end)
    Program.next_free_memory_location += 2
    if [el for el in commander.Program.iterators_stack if el.pid == value][0]:
        Program.iterators_stack.append(iterator)
    if pid in Program.variables:
        Program.variables[pid].is_shadowed = True
        Program.variables[pid].reference_to_iterator = iterator
    return iterator


def remove_iterator(iterator: VariableIterator):
    Program.iterators_stack.remove(iterator)
    if iterator.pid in Program.variables:
        Program.variables[iterator.pid].is_shadowed = False
        Program.variables[iterator.pid].reference_to_iterator = None
