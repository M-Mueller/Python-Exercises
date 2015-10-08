import functools

def splitDigits(code):
    lines = [l for l in code.split('\n')]
    # assure that all lines have the same amount of characters
    numChars = max([len(l) for l in lines])
    def adjustLine(l):
        return l + ' ' * max(numChars-len(l), 0);
    lines = [adjustLine(l) for l in lines]
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
__digitMap = dict([(d,str(i)) for i,d in enumerate(splitDigits(__numbers))])
def convertDigit(digit):
    return __digitMap[digit]

def convertDigits(digits):
    for d in splitDigits(digits):
        yield convertDigit(d)

def test(input, expected):
    actual = ''.join(convertDigits(input))
    if (actual != expected):
        print(input)
    print("{0} ({1})".format(actual, expected))

# for k,v in __digitMap.items():
#     print(k)
#     print(v)

with open('BankOCR_Test.txt', 'r') as f:
    codes = [c for c in f.read().split(';\n') if c]
    for code in codes:
        lines = code.split('\n')
        test('\n'.join(lines[0:3]), lines[3])
