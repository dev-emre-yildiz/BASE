from cgitb import text
from turtle import position

#CONSTANTS
DIGITS = '0123456789'


#ERRORS
class Error:
    def __init__ (self, error_name, details):
        self.error_name = error_name
        self.details = details
    def as_string(self):
        result= f'{self.error_name}: {self.details}'
        return result

class IllegalCharError(Error):
    def __init__ (self, details):
        super().__init__('Illegal Character', details)

#TOKENS
TOKEN_INT     = "TOKEN_INT"
TOKEN_FLOAT   = "TOKEN_FLOAT"
TOKEN_PLUS    = "PLUS"
TOKEN_MINUS   = "MINUS"
TOKEN_MUL     = "MUL"
TOKEN_DIV     = "DIV"
TOKEN_LPAREN  = "LPAREN"
TOKEN_RPAREN  = "RPAREN"
class Token:
    def __init__ (self, type, value):
        self.type = type
        self.value= value
    
    def __repr__ (self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'


class Lexer:
    def __init__ (self,text):
        self.text = text
        self.pos= -1      //position
        self.current_char= None
        self.get_next()

    def get_next(self):
        self.pos+=1
        self.current_char= self.text[pos] if self.pos < len (self.text) else None

    def get_tokens(self):
        tokens= []
        while self.current_char != None:
            if self.current_char in ' \t' :
                self.get_next()
            elif self.current_char in DIGITS:
                tokens.append(self.convert_number())
            elif self.current_char == '+':
                tokens.append(Token(TOKEN_PLUS))
                self.get_next()
            elif self.current_char == '-':
                tokens.append(Token(TOKEN_MINUS))
                self.get_next()
            elif self.current_char == '*':
                tokens.append(Token(TOKEN_MUL))
                self.get_next()
            elif self.current_char == '/':
                tokens.append(Token(TOKEN_DIV))
                self.get_next()
            elif self.current_char == '(':
                tokens.append(Token(TOKEN_LPAREN))
                self.get_next()
            elif self.current_char == ')':
                tokens.append(Token(TOKEN_RPAREN))
                self.get_next()
            else:
                char = self.current_char
                self.get_next()
                return [] , IllegalCharError("'" + char + "'")

        return tokens , None      
        

    def convert_number(self):
        num_str= ''
        dot_count=0

        while self.current_char != None and self.current_char in DIGITS + '.' :
            if self.current_char== '.':
                if dot_count ==1 :
                    break
                dot_count +=1
                num_str += '.'
        
        if dot_count==0:
            return Token(TOKEN_INT , int (num_str))
        
        else:
            return Token(TOKEN_FLOAT , float(num_str))

