"""
Solves equations of the form:
`a ? b ? c ? ... = d`
where a, b, c, d ... are given natural numbers
and `?` are operators +, -, * or / that should
be determined.
"""
import itertools


def solve(numbers, result):
    """Places the operators +-*/ between the numbers and returns all equations
    that evaluate to the result.
    >>> list(solve([1, 2], 3))
    ['1+2=3']
    >>> list(solve([2, 3, 2], 8))
    ['2+3*2=8', '2*3+2=8']
    """
    numbers = [str(n) for n in numbers]
    operators = '+-/*'
    # get all combinations of operators between numbers
    # e.g. [('+', '+'), ('+', '-'), ...]
    combis = itertools.product(*itertools.repeat(operators, len(numbers) - 1))
    for combi in combis:
        # put the operators between the numbers
        # e.g. [('1', '+'), ('2', '*'), ('3', '')]
        formula = itertools.zip_longest(numbers, combi, fillvalue='')
        # combine to string e.g. '1+2*3'
        formula = ''.join([''.join(f) for f in formula])
        try:
            if eval(formula) == result:
                yield '{}={}'.format(formula, result)
        except ZeroDivisionError:
            pass


def solve_no_itertools(numbers, result):
    """Alternative implementation of solve without itertools."""
    combis = combinations('+-/*', len(numbers)-1)
    for combi in combis:
        formula = []
        for n, op in zip(numbers, combi):
            formula.append(n)
            formula.append(op)
        formula.append(numbers[-1])
        try:
            if evaluate(formula) == result:
                yield '{}={}'.format(formula, result)
        except ZeroDivisionError:
            pass


def combinations(iterables, length):
    """Returns all combinations of input with the given length.
    >>> list(combinations('+-', 2))
    [('+', '+'), ('+', '-'), ('-', '+'), ('-', '-')]
    """
    for item in iterables:
        if length == 1:
            yield (item,)
        else:
            for p in combinations(iterables, length-1):
                yield (item,) + p


def evaluate(formula):
    """Evaluates a formula containing the operator +, -, * and /.
    Does not support brackets.
    >>> evaluate([1, '+', 1])
    2
    >>> evaluate([2, '+', 3, '*', 4])
    14
    """
    def calc(formula, i):
        """Calculates the value of the formula around the operator at
        index i."""
        a = formula[i-1]
        op = formula[i]
        b = formula[i+1]
        if op == '+':
            result = a+b
        elif op == '-':
            result = a-b
        elif op == '*':
            result = a*b
        elif op == '/':
            result = a/b
        # build the remaining list with the new result
        return formula[:max(0, i-1)] + [result] + formula[i+2:]

    while len(formula) > 1:
        for i in range(1, len(formula), 2):
            # evaluate all */ first
            op = formula[i]
            if op in '*/':
                formula = calc(formula, i)
                break
        else:
            # evaluate the remaining +-
            for i in range(1, len(formula), 2):
                op = formula[i]
                if op in '+-':
                    formula = calc(formula, i)
                    break
    return formula[0]


if __name__ == '__main__':
    print(list(solve([1, 2], 3)))
    print(list(solve([1, 2, 0], 3)))
    print(list(solve([3, 4, 2], 6)))
    print(list(solve([3, 4, 2], 13)))
    print(list(solve([2, 3, 2], 8)))

    print(list(solve_no_itertools([1, 2], 3)))
    print(list(solve_no_itertools([1, 2, 0], 3)))
    print(list(solve_no_itertools([3, 4, 2], 6)))
    print(list(solve_no_itertools([3, 4, 2], 13)))
    print(list(solve_no_itertools([2, 3, 2], 8)))
