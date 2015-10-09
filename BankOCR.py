import functools

def normalizeCode(code):
    lines = [l for l in code.split('\n')]
    if len(lines) < 3:
        raise ValueError("Invalid number of lines ({0})".format(len(lines)))
    numChars = max([len(l) for l in lines])
    # assure that all lines have the same amount of characters
    def adjustLine(l):
        return l + ' ' * max(numChars-len(l), 0);
    lines = [adjustLine(l) for l in lines]
    return '\n'.join(lines)

def splitDigits(code):
    lines = [l for l in code.split('\n')]
    numChars = max([len(l) for l in lines])
    numDigits = numChars//3
    digits = ['']*numDigits
    for i in range(numDigits):
        digits[i] += lines[0][i*3:i*3+3] + '\n'
        digits[i] += lines[1][i*3:i*3+3] + '\n'
        digits[i] += lines[2][i*3:i*3+3]
    return digits

__numbers = '''
 _     _  _     _  _  _  _  _
| |  | _| _||_||_ |_   ||_||_|
|_|  ||_  _|  | _||_|  ||_| _|
'''[1:]#remove first newline
#create a dict that maps each digit in string representation to its number (also str to keep leading 0)
__digitMap = dict([(d,str(i)) for i,d in enumerate(splitDigits(normalizeCode(__numbers)))])
def convertDigit(digit):
    try:
        return __digitMap[digit]
    except KeyError:
        return '?'

def convertDigits(digits):
    for d in splitDigits(digits):
        yield convertDigit(d)

def checksum(number):
    if len(number) == 9:
        sum = 0
        for i, n in enumerate(number):
            try:
                sum += int(n) * (9-i)
            except ValueError:
                return False;
        return sum % 11 == 0
    return False;

def recover(code):
    recovered = []
    def replace(code, i, c):
        #print(code[:i] + c + code[i+1:])
        number = ''.join(convertDigits(code[:i] + c + code[i+1:]))
        if checksum(number):
            recovered.append(number)
    for i,c in enumerate(code):
        if c == '_' or c == '|':
            replace(code, i, ' ')
        elif c == ' ':
            replace(code, i, '_')
            replace(code, i, '|')

    return recovered


def test(code, expected):
    code = normalizeCode(code)
    digits = splitDigits(code)
    number = ''.join([convertDigit(d) for d in digits])
    actual = number
    if '?' in actual or not checksum(actual):
        recovered = recover(code)
        if not recovered:
            actual += ' ILL'
        elif len(recovered) == 1:
            actual = recovered[0]
        else:
            actual = number + ' AMB ' + str(recovered)

    if (actual != expected):
        print(code)
        print("Got: {0}\n Expected: {1}) ".format(actual, expected))
    else:
        print(actual)

# for k,v in __digitMap.items():
#     print(k)
#     print(v)

with open('BankOCR_Test.txt', 'r') as f:
    codes = [c for c in f.read().split(';\n') if c]
    for code in codes:
        lines = code.split('\n')
        test('\n'.join(lines[0:3]), lines[3])
