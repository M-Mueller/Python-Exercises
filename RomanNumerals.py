
literals = {1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL', 50: 'L', 90: 'XC', 100: 'C', 500: 'D', 900: 'CM', 1000: 'M'}
literalsInv = dict([(v,k) for k,v in literals.items()])

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

def roman_to_arabic(roman):
    """Converts a roman number into an arabic number.
    >>> roman_to_arabic('I')
    1
    >>> roman_to_arabic('IV')
    4
    >>> roman_to_arabic('V')
    5
    >>> roman_to_arabic('DXV')
    515
    >>> roman_to_arabic('DCCLXXXIX')
    789
    >>> roman_to_arabic('MDCCCLXXXVIII')
    1888
    >>> roman_to_arabic('MCMLXXXIV')
    1984
    >>> roman_to_arabic('MCMXCIX')
    1999
    >>> roman_to_arabic('MMI')
    2001
    >>> roman_to_arabic('MMVI')
    2006
    """
    if len(roman) == 0:
        return 0
    if len(roman) == 1:
        return literalsInv[roman]
    else:
        a,b = roman[:2]
        if a+b in literalsInv:
            return literalsInv[a+b] + roman_to_arabic(roman[2:])
        else:
            return literalsInv[a] + roman_to_arabic(roman[1:])
