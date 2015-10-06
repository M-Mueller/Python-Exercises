numbers = '''
 _     _  _     _  _  _  _  _
| |  | _| _||_||_ |_   ||_||_|
|_|  ||_  _|  | _||_|  ||_| _|
'''

class Converter:
    def __init__(self):
        digits = self.splitDigits(numbers)
        self.digitLineDicts = [{} for i in range(3)]
        self.digitIdDict = {}
        digitIndices = [0]*3
        for d in digits:
            for (lineIdx, line) in enumerate(d.split('\n')):
                lDict = self.digitLineDicts[lineIdx]
                if not line in lDict:
                    lDict[line] = digitIndices[lineIdx]
                    digitIndices[lineIdx] += 1
        for i,d in enumerate(digits):
            self.digitIdDict[self.generateID(d)] = i

    def generateID(self, digit):
        id = 0
        for (lineIdx, line) in enumerate(digit.split('\n')):
            id *= 10
            id += self.digitLineDicts[lineIdx][line]
        return id

    def convertDigit(self, digit):
        return self.digitIdDict[self.generateID(digit)]

    def splitDigits(self, code):
        lines = [l for l in code.split('\n') if l]
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

    def convert(self, digits):
        for d in self.splitDigits(digits):
            yield self.convertDigit(d)

c = Converter()
print(list(c.convert(numbers)))
