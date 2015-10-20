from math import log10, ceil

numbers = [
'',
'one',
'two',
'three',
'four',
'five',
'six',
'seven',
'eight',
'nine',
'ten',
'eleven',
'twelve',
'thirteen',
'fourteen',
'fifteen',
'sixteen',
'seventeen',
'eighteen',
'nineteen'
]

tenner = [
'',
'ten',
'twenty',
'thirty',
'fourty',
'fifty',
'sixty',
'seventy',
'eighty',
'ninety'
]

powers = [
'',
'thousand',
'million',
'billion'
]

def _hundred_in_english(number, hasAnd=False):
    """Returns a number smaller than 1000 in words.
    If hasAnd is True, the word 'and' is added before the tenner if appropriate
    >>> _hundred_in_english(0)
    ''
    >>> _hundred_in_english(1)
    'one'
    >>> _hundred_in_english(1, True)
    'and one'
    >>> _hundred_in_english(27)
    'twenty seven'
    >>> _hundred_in_english(300)
    'three hundred'
    >>> _hundred_in_english(300, True)
    'three hundred'
    >>> _hundred_in_english(631)
    'six hundred thirty one'
    >>> _hundred_in_english(631, True)
    'six hundred and thirty one'
    >>> _hundred_in_english(601, True)
    'six hundred and one'
    >>> _hundred_in_english(1000)
    Traceback (most recent call last):
    ...
    ValueError: Value must be smaller than 1000
    """
    if number > 999:
        raise ValueError("Value must be smaller than 1000")
    # separate digits
    h = (number//100) % 10
    t = (number//10) % 10
    o = number % 10
    if t == 1:
        # all tenners need to be treated as one number (e.g. not 'ten one' but 'eleven')
        t = 0
        o = number % 100

    word = ''
    if h:
        word += numbers[h] + ' hundred '
    if hasAnd and (t or o):
        word += 'and '
    if t:
        word += tenner[t] + ' '
    if o:
        word += numbers[o]
    return word.strip()

def number_in_english(number):
    """Returns the given number in words
    >>> number_in_english(0)
    'zero'
    >>> number_in_english(5)
    'five'
    >>> number_in_english(11)
    'eleven'
    >>> number_in_english(745)
    'seven hundred and fourty five'
    >>> number_in_english(1380)
    'one thousand three hundred and eighty'
    >>> number_in_english(3204000)
    'three million two hundred four thousand'
    >>> number_in_english(15000)
    'fifteen thousand'
    >>> number_in_english(1005)
    'one thousand and five'
    """
    if not number:
        return 'zero'
    # split number into blocks of 3
    # e.g. 1234567 -> ['567', '234', '1']
    numBlocks = int(ceil((log10(number)+1)/3)) # number of digits / 3
    number_split = [(number//1000**x)%1000 for x in range(numBlocks)]
    # translate each block individual and add the word for the power
    # start with the lowest power
    word = ''
    for n, p in zip(number_split, powers):
        if n:
            # only the tenner block can have an 'and' (e.g. 'one hundred and five' but not 'one million and one thousand')
            word = _hundred_in_english(n, (p == '')) + ' ' + p + ' ' + word
    # remove 'and' that was added but is not precede by a number (e.g. 5 -> 'and five')
    if word.startswith('and'):
        word = word.replace('and', '')
    return word.strip()
