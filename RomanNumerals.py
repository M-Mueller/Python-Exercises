
literals = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC', 100: 'C', 500: 'D', 900: 'CM', 1000: 'M'}

def arabic_to_roman(arabic):
    """Converts an arabic number into a roman number.
    >>> arabic_to_roman(1)
    'I'
    >>> arabic_to_roman(4)
    'IV'
    >>> arabic_to_roman(5)
    'V'
    >>> arabic_to_roman(515)
    'DXV'
    >>> arabic_to_roman(789)
    'DCCLXXXIX'
    >>> arabic_to_roman(1888)
    'MDCCCLXXXVIII'
    >>> arabic_to_roman(1984)
    'MCMLXXXIV'
    >>> arabic_to_roman(1999)
    'MCMXCIX'
    >>> arabic_to_roman(2001)
    'MMI'
    >>> arabic_to_roman(2006)
    'MMVI'
    """
    roman = ''
    for l in sorted(literals.keys(), reverse=True):
        roman += (arabic//l) * literals[l]
        arabic %= l
    return roman
