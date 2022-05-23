#!/usr/bin/env python
import sys

fileName = "input.txt"
with open(sys.argv[1], 'r') as my_file:
    inputContent = my_file.read()
fileIndex = 0
EOF = "EOF"
INVALID = "INVALID"
tokens = []
lexemes = []
tokens_lines = []
lexemes_lines = []

# Character classes
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# Token codes
INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
IF_TOKEN = 41
THEN_TOKEN = 42
FLOAT_TOKEN = 46
COMMA = 48
SEMI_COLON = 49
GOTO_TOKEN = 50
EQUALS_TO = 51
GREATER = 52
LESS = 53


lexeme = ""
lexLen = 0


def lookupSymbol(character):
    if (character == "("):
        nextToken = LEFT_PAREN
    elif (character == ")"):
        nextToken = RIGHT_PAREN
    elif (character == ">"):
        nextToken = GREATER
    elif (character == "<"):
        nextToken = LESS
    elif (character == "-"):
        nextToken = SUB_OP
    elif (character == "*"):
        nextToken = MULT_OP
    elif (character == "/"):
        nextToken = DIV_OP
    elif (character == ","):
        nextToken = COMMA
    elif (character == ";"):
        nextToken = SEMI_COLON
    else:
        nextToken = INVALID

    return nextToken


def getChar():
    global inputContent
    global fileIndex
    if (fileIndex < len(inputContent)):
        nextChar = inputContent[fileIndex]
        fileIndex += 1
        return nextChar
    else:
        return EOF


def getNonBlank():
    char = getChar()
    while (char.isspace()):
        char = getChar()
    return char


def getCharClass(char):
    if char.isalpha():
        charClass = LETTER
    elif char.isdigit():
        charClass = DIGIT
    else:
        charClass = UNKNOWN
    return charClass


def lex(char):
    lexeme = ""
    charClass = getCharClass(char)
    global fileIndex

    if (charClass == LETTER):
        lexeme += char
        nextChar = getChar()
        while(nextChar != EOF and nextChar != " " and (getCharClass(nextChar) == LETTER or getCharClass(nextChar) == DIGIT)):
            lexeme += nextChar
            nextChar = getChar()

        # Check for keywords
        if (lexeme == "IF"):
            nextToken = IF_TOKEN
        if (lexeme == "THEN"):
            nextToken = THEN_TOKEN
        if (lexeme == "SET"):
            nextToken = ASSIGN_OP
        elif (lexeme == "integer"):
            nextToken = INT_LIT
        elif (lexeme == "float"):
            nextToken = FLOAT_TOKEN
        elif (lexeme == "GOTO"):
            nextToken = GOTO_TOKEN
        elif (lexeme == "ADD"):
            nextToken = ADD_OP
        elif (lexeme == "SUB"):
            nextToken = SUB_OP
        elif (lexeme == "MULT"):
            nextToken = MULT_OP
        elif (lexeme == "DIV"):
            nextToken = DIV_OP
        elif (lexeme == "EQ"):
            nextToken = EQUALS_TO
        else:
            nextToken = IDENT

        if nextChar != " " and nextChar != EOF:
            fileIndex -= 1

    elif (charClass == DIGIT):
        lexeme += char
        nextChar = getChar()
        while((nextChar != EOF) and (nextChar != " ") and (getCharClass(nextChar) == DIGIT)):
            lexeme += nextChar
            nextChar = getChar()
        nextToken = INT_LIT
        if nextChar != " " and nextChar != EOF:
            fileIndex -= 1

    elif (charClass == UNKNOWN):
        token = lookupSymbol(char)
        lexeme += char
        nextToken = token

    tokens.append(nextToken)
    lexemes.append(lexeme)
    return nextToken


def match_set_code(program, i):
    match program[i]:
        case ((20, _), (25, _), (11, x), (48, _), (10, y), (26, _)):
            globals()[x] = int(y)
            print(globals()[x])


def match_int_code(program, i):
    match program[i]:
        case ((10, _), (11, x)):
            globals()[x] = 0
        case ((10, _), (11, x), (48, _), (10, y)):
            globals()[x] = int(y)

        case ((10, _), (25, _), (11, x), (48, _), (10, y), (26, _)):
            globals()[x] = int(y)


def match_add_code(program, i):
    match program[i]:
        case ((21, _), (25, _), (11, x), (48, _), (11, y), (26, _)):
            globals()[x] = globals()[x] + globals()[y]


def match_operator(program, i):
    match program[i][0][0]:
        case 10:
            match_int_code(program, i)
        case 20:
            match_set_code(program, i)
        case 21:
            match_add_code(program, i)
        case ('DIV', x, y):
            return int(x) / int(y)
        case _:
            raise TypeError("not a operator we support")

#   for line in lines:
#     line = re.split(', | ', lines[count])
#     count += 1
#     print(match_operator(line))


def merge(list1, list2):

    merged_list = tuple(zip(list1, list2))
    return merged_list


def first_list_partition(list, x):
    return list[:list.index(x)]


def second_list_partition(list, x):
    return list[list.index(x)+1:]


def getLines_addAnother(list, x, list_to_add):
    if(x not in list):
        return

    list_to_add.append(first_list_partition(list, x))
    getLines_addAnother(second_list_partition(list, x), x, list_to_add)


def merge_lists_toTuple(list1, list2):
    merged_list = []
    for i in range(len(list1)):
        merged_list.append(merge(list1[i], list2[i]))
    return merged_list


def main():
    nextChar = getNonBlank()
    if (nextChar == EOF):
        print("File is empty")
        return

    while nextChar != EOF:
        nextToken = lex(nextChar)
        if (nextToken == INVALID):
            break
        nextChar = getNonBlank()

    print(lexemes)
    print(tokens)

    print(len(lexemes))
    print(len(tokens))
    # print(merge(tokens, lexemes))
    print(merge(tokens, lexemes))
    getLines_addAnother(lexemes, ';', lexemes_lines)
    print(lexemes_lines)

    getLines_addAnother(tokens, SEMI_COLON, tokens_lines)
    print(tokens_lines)
    program = merge_lists_toTuple(tokens_lines, lexemes_lines)
    print(program)
    print(program[0][0][0])
    print(program[0][1][0])
    match_operator(program, 0)
    match_operator(program, 1)
    match_operator(program, 2)
    match_operator(program, 3)
    match_operator(program, 4)
    print(apple)
    print(banana)
    print(carrot)


main()
