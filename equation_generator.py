#!/usr/bin/python

import sys
import random
import argparse
import inspect

# Defines operators that can be used in the equation
# operators = {
#         "addition" : 1,
#         "multiplication" : 2,
#         "division" : 3
#         }

class OperatorSymbols:
    ADDITION = "addition"
    MULTIPLICATION = "multiplication"
    DIVISION = "division"

class RenderSymbols:
    PARENTHESIS = "parenthesis"
    
operators = [obj for name, obj in inspect.getmembers(OperatorSymbols) if not name.startswith("__") and not inspect.isroutine(obj)]

# Extract command line arguments
arg_parser = argparse.ArgumentParser(description="Generate a hand-solvable equation that solves to the given value")
arg_parser.add_argument("eq_value", type=int, help="value the equation will solve to")
arg_parser.add_argument("--min-complexity", type=int, help="minimum number of operators to use (must be > 0)", default=1)
arg_parser.add_argument("--max-complexity", type=int, help="maximum number of operators to use (must be <= " + str(len(operators)), default=len(operators))
arg_parser.add_argument("--max-log-base", type=int, help="maximum base to use for the log operator")
command_args = arg_parser.parse_args()

# Validate input args
if command_args.min_complexity < 1:
    print("Minimum complexity must be > 0!")
    sys.exit()
if command_args.max_complexity > len(operators):
    print("Maximum complexity must be <= " + len(operators))

# Grabs a sample of the defined operators of size [min_complexity, max_complexity]
num_ops = random.randint(command_args.min_complexity, command_args.max_complexity)
operators_list = random.sample(operators, num_ops)

def factors(n):
    """Finds the positive and negative factors of the given number"""
    n = abs(n)
    factors = set()
    for i in range(1, int(n**0.5) + 1): 
        if n % i == 0:
            factors.update({i, -i, n/i, -n/i})
    factors = list(factors)
    return factors

def apply_operators(operators_list, expression, value):
    """Recursive function that verbally applies the operator to the expression and numerically applies it to the constant
    
    Keyword Args:
    operators_list -- list of operators to apply in order
    expression -- string expression to verbally modify with operators
    value -- value to numerically modify with operators

    Return: (expression, value)
    expression -- the verbal expression with all operators applied
    value -- the value with all operators applied
    """

    # Base case
    if len(operators_list) == 0:
        return expression, value

    # Recursive case
    operator = operators_list[0]

    # Addition operator
    if operator == OperatorSymbols.ADDITION:
        # TODO Change scale on random constant generated
        # Don't use zero as an addition operator
        constant = random.randint(-50, 50)
        while constant == 0:
            constant = random.randint(-50, 50)

        if (constant > 0):
            new_expression = expression + " + " + str(constant)
        else:
            new_expression = expression + " - " + str(abs(constant))
        new_value = value + constant
        return apply_operators(operators_list[1:], new_expression, new_value)

    # Multiplication operator
    elif operator == OperatorSymbols.MULTIPLICATION:
        # TODO Change scale on random constant generated
        constant = random.randint(-50, 50)

        new_expression = str(constant) + " * (" + expression + ")"
        new_value = value * constant
        return apply_operators(operators_list[1:], new_expression, new_value)

    # Division operator
    elif operator == OperatorSymbols.DIVISION:
        # TODO Change scale on random constant generated
        constant = random.choice(factors(value))

        new_expression = "(" + expression + ") / " + str(constant)
        new_value = value / constant
        return apply_operators(operators_list[1:], new_expression, new_value)

    # Parenthesis renderer


expression, value = apply_operators(operators_list, "x", command_args.eq_value)
print(expression + " = " + str(value))







