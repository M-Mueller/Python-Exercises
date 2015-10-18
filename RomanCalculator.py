numbers = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
substracted = [('IV', 'IIII'), ('IX', 'VIIII'), ('XL', 'XXXX'), ('XC', 'LXXXX'), ('CD', 'CCCC'), ('CM', 'DCCCC') ]
carry_numbers = ['IIIII', 'VV', 'XXXXX', 'LL', 'CCCCC', 'DD']

def _remove_substraction(r):
    """Replaces substracted numbers such as IV by their non-substracted number, e.g. IIII
    >>> _remove_substraction('')
    ''
    >>> _remove_substraction('III')
    'III'
    >>> _remove_substraction('IV')
    'IIII'
    >>> _remove_substraction('IX')
    'VIIII'
    """
    for a, b in substracted:
        r = r.replace(a, b)
    return r

def _add_substraction(r):
    """Replaces numbers appearing 4 times with their substracted equivalent (e.g. IIII to IV)
    >>> _add_substraction('')
    ''
    >>> _add_substraction('III')
    'III'
    >>> _add_substraction('IIII')
    'IV'
    >>> _add_substraction('VIIII')
    'IX'
    """
    for a, b in reversed(substracted):
        r = r.replace(b, a)
    return r

def _split_numbers(r):
    """Splits a roman number into blocks of same numbers
    >>> _split_numbers('')
    ['', '', '', '', '', '', '']
    >>> _split_numbers('XXIII')
    ['', '', '', '', 'XX', '', 'III']
    >>> _split_numbers('MDCLXVI')
    ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    """
    s = ['' for n in numbers]
    for n in r:
        s[numbers.index(n)] += n
    return list(reversed(s))

def add(a, b):
    """Adds to roman numbers only using string based operations
    >>> add('', '')
    ''
    >>> add('I', 'I')
    'II'
    >>> add('II', 'II')
    'IV'
    >>> add('IV', 'IV')
    'VIII'
    >>> add('DCCCXC', 'XX')
    'CMX'
    """
    al = _split_numbers(_remove_substraction(a));
    bl = _split_numbers(_remove_substraction(b));
    # reverse so that lowest values are first
    al.reverse();
    bl.reverse();
    cl = ['' for n in numbers]
    assert len(al) == len(bl) == len(cl) == len(numbers)
    for i in range(len(numbers)):
        # add all numbers starting with the lowest
        cl[i] += al[i] + bl[i]
        # check if the sum carries over to the higher value
        if i<len(carry_numbers) and carry_numbers[i] in cl[i]:
            # remove the value and add it to the higher value, keep the rest
            cl[i] = cl[i].replace(carry_numbers[i], '', 1)
            al[i+1] += numbers[i+1]
    return _add_substraction(''.join(reversed(cl)))
