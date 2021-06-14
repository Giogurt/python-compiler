class Parser:
    def __init__(self, ids, nums, tokens):
        self.ids = ids
        self.nums = nums
        self.tokens = tokens
        self.current_token = tokens[0]
        self.token_value = ""
        self.token_pos = 0
        self.call_flag = False
        self.res_list = ["err", "else", "if", "int", "return",
                         "void", "while", "input", "output"]
        self.del_list = [
            "+", "-", "*", "/", "<", "<=", ">", ">=", "==", "!=", "=", ";", ",", "(", ")", "[", "]", "{", "}"
        ]
        self.tokens.append(["del", "$"])

    def get_current_token(self):
        return self.token_value

    def error(self, err_msg="SYNTAX ERROR"):
        print(err_msg)
        print("Error in the following token sequence" + self.get_token_value(self.tokens[self.token_pos-1]) + " -> " + self.token_value)
        exit()

    def get_token_value(self, token):
        value = ""
        if (token[0] == "res"):
            value = self.res_list[token[1]]
        elif (token[0] == "del"):
            if(token[1] == "$"):
                value = "$"
            else:
                value = self.del_list[token[1]]
        elif (token[0] == "id"):
            value = self.ids[token[1]]
        elif (token[0] == "num"):
            value = self.nums[token[1]]
        else:
            print("UNRECOGNIZED TOKEN TYPE")
            exit()
        return value

    def match(self, terminal):
        if (self.token_value == terminal):
            self.token_pos += 1
            self.current_token = self.tokens[self.token_pos]
            self.token_value = self.get_token_value(self.current_token)
        else:
            self.error("THE CURRENT TOKEN WAS NOT EXPECTED")

    def match_id(self):
        if (self.current_token[0] == "id"):
            self.token_pos += 1
            self.current_token = self.tokens[self.token_pos]
            self.token_value = self.get_token_value(self.current_token)
        else:
            self.error("THE CURRENT TOKEN WAS NOT EXPECTED")
    def match_num(self):
        if (self.current_token[0] == "num"):
            self.token_pos += 1
            self.current_token = self.tokens[self.token_pos]
            self.token_value = self.get_token_value(self.current_token)
        else:
            self.error("THE CURRENT TOKEN WAS NOT EXPECTED")

    def check_id(self):
        if (self.current_token[0] == "id"):
            return True
        else:
            return False

    def check_num(self):
        if (self.current_token[0] == "num"):
            return True
        else:
            return False
            
    def declaration_list(self):
        self.token_value = self.get_token_value(self.current_token)
        self.declaration()
        self.declaration_list_prime()

    def declaration_list_prime(self):
        if (self.token_value == "int" or self.token_value == "void"):
            self.declaration()
            self.declaration_list_prime()
        elif(self.token_value == "$"):
            return
        else:
            self.error("THE DECLARATIONS WERE NOT CORRECTLY WRITTEN")

    def declaration(self):
        if (self.token_value == "int"):
            self.var_declaration()
        elif (self.token_value == "void"):
            self.fun_declaration()
        else:
            self.error("THE DECLARATION WERE NOT CORRECTLY WRITTEN")
    
    def var_declaration(self):
        self.match("int")
        self.match_id()
        if (self.token_value == "("):
            self.fun_declaration()
            return
        self.var_declaration_prime()
    
    def var_declaration_prime(self):
        if (self.token_value == ";"):
            self.match(";")
        elif (self.token_value == "["):
            self.match("[")
            self.match_num()
            self.match("]")
            self.match(";")
        else:
            self.error("VARIABLE DECLARATION HAS AN INCORRECT FORMAT")
    
    def fun_declaration(self):
        if (self.token_value == "("):
            self.match("(")
            self.params()
            self.match(")")
            self.compound_stmt()
        elif (self.token_value == "void"):
            self.match("void")
            self.match_id()
            self.match("(")
            self.params()
            self.match(")")
            self.compound_stmt()
        else:
            self.error("FUNCTION DECLARATION HAS AN INCORRECT FORMAT")
    
    def params(self):
        if (self.token_value == "int"):
            self.param_list()
        elif (self.token_value == "void"):
            self.match("void")
        else:
            self.error("UNRECOGNIZED PARAMETERS")
    
    def param_list(self):
        self.param()
        self.param_list_prime()

    def param_list_prime(self):
        if (self.token_value == ","):
            self.match(",")
            self.param()
            self.param_list_prime()
        elif (self.token_value == ")"):
            return
        else:
            self.error("ONE OR MORE PARAMS HAVE AN INCORRECT FORMAT")

    def param(self):
        self.match("int")
        self.match_id()
        self.param_prime()

    def param_prime(self):
        if (self.token_value == "["):
            self.match("[")
            self.match("]")
        elif (self.token_value == "," or self.token_value == ")"):
            return
        else:
            self.error("THE PARAMETER HAS AN INCORRECT FORMAT")
    
    def compound_stmt(self):
        self.match("{")
        self.local_declarations()
        self.statement_list()
        self.match("}")
    
    def local_declarations(self):
        if (self.token_value == "int"):
            self.var_declaration()
            self.local_declarations()
        elif (self.check_id() or self.token_value == "{" or self.token_value == "if" or self.token_value == "while"
             or self.token_value == "return" or self.token_value == "input" or self.token_value == "output" ):
            return
        else:
            self.error("LOCAL DECLARATION HAS AN INCORRECT FORMAT")

    def statement_list(self):
        self.statement()
        self.statement_list_prime()
    
    def statement_list_prime(self):
        if (self.check_id() or self.token_value == "{" or self.token_value == "if" or self.token_value == "while"
             or self.token_value == "return" or self.token_value == "input" or self.token_value == "output" ):
            self.statement()
            self.statement_list_prime()
        elif (self.token_value == "}"):
            return
        else:
            self.error("A STATEMENT HAS AN INCORRECT FORMAT")
    
    def statement(self):
        if (self.check_id()):
            self.var()
            if(self.call_flag == False):
                self.match("=")
                self.expression()
            else:
                self.call_flag = False
            self.match(";")
        elif (self.token_value == "{"):
            self.compound_stmt()
        elif (self.token_value == "if"):
            self.match("if")
            self.match("(")
            self.expression()
            self.match(")")
            self.statement()
            self.selection_stmt_else()
        elif (self.token_value == "while"):
            self.match("while")
            self.match("(")
            self.expression()
            self.match(")")
            self.statement()
        elif (self.token_value == "return"):
            self.match("return")
            self.return_stmt_prime()
        elif(self.token_value == "input"):
            self.match("input")
            self.var()
            self.match(";")
        elif(self.token_value == "output"):
            self.match("output")
            self.output_stmt_prime()
        else:
            self.error("STATEMENT HAS AN INCORRECT FORMAT")
    
    def selection_stmt_else(self):
        if(self.token_value == "else"):
            self.match("else")
            self.statement()
        elif (self.check_id() or self.token_value == "{" or self.token_value == "if" or self.token_value == "while"
            or self.token_value == "return" or self.token_value == "input" or self.token_value == "output"
            or self.token_value == "}" or self.token_value == "else" ):
            return
        else:
            self.error("THE IF SELECTION HAS AN INCORRECT FORMAT")
    
    def return_stmt_prime(self):
        if self.token_value == ";":
            self.match(";")
        elif (self.token_value == "(" or self.check_id() or self.check_num()):
            self.expression()
            self.match(";")
        else:
            self.error("THE RETURN METHOD HAS AN INCORRECT FORMAT")
    
    def output_stmt_prime(self):
        if self.check_id():
            self.var()
            self.match(";")
        elif (self.token_value == "(" or self.check_id() or self.check_num()):
            self.expression()
            self.match(";")
        else:
            self.error("THE OUTPUT METHOD HAS AN INCORRECT FORMAT")
    
    def var(self):
        self.match_id()
        if(self.token_value == "("):
            #call
            self.call_flag = True
            self.match("(")
            self.args()
            self.match(")")
            return
        self.var_prime()

    def var_prime(self):
        if(self.token_value == "["):
            self.match("[")
            self.arithmetic_expression()
            self.match("]")
        elif(self.token_value == "*" or self.token_value == "/" or self.token_value == "+"
            or self.token_value == "-" or self.token_value == "<=" or self.token_value == "<"
            or self.token_value == ">" or self.token_value == ">=" or self.token_value == "=="
            or self.token_value == "!=" or self.token_value == ";" or self.token_value == ")"
            or self.token_value == "," or self.token_value == "="  or self.token_value == "]"):
            return
        else:
            self.error("VARIABLE HAS AN INCORRECT FORMAT")
    
    def expression(self):
        self.arithmetic_expression()
        self.expression_prime()
    
    def expression_prime(self):
        if(self.token_value == "<=" or self.token_value == "<"
            or self.token_value == ">" or self.token_value == ">=" or self.token_value == "=="
            or self.token_value == "!="):
            self.relop()
            self.arithmetic_expression()
        elif(self.token_value == ";" or self.token_value == ")"):
            return
        else:
            self.error("EXPRESSION HAS AN INCORRECT FORMAT")
    
    def relop(self):
        if(self.token_value == "<="):
            self.match("<=")
        elif(self.token_value == "<"):
            self.match("<")
        elif(self.token_value == ">"):
            self.match(">")
        elif(self.token_value == ">="):
            self.match(">=")
        elif(self.token_value == "=="):
            self.match("==")
        elif(self.token_value == "!="):
            self.match("!=")
        else:
            self.error("COMPARATOR OPERATOR EXPECTED")
    
    def arithmetic_expression(self):
        self.term()
        self.arithmetic_expression_prime()

    def arithmetic_expression_prime(self):
        if(self.token_value == "+" or self.token_value == "-"):
            self.addop()
            self.term()
            self.arithmetic_expression_prime()
        elif(self.token_value == "<=" or self.token_value == "<"
            or self.token_value == ">" or self.token_value == ">=" or self.token_value == "=="
            or self.token_value == "!=" or self.token_value == ";" or self.token_value == ")"
            or self.token_value == ","  or self.token_value == "]"):
            return
        else:
            self.error("ARITHMETIC OR LOGIC EXPRESSION HAS AN INCORRECT FORMAT")
        
    def addop(self):
        if(self.token_value == "+"):
            self.match("+")
        elif(self.token_value == "-"):
            self.match("-")
        else:
            self.error("PLUS OR MINUS OPERATOR EXPECTED")
    
    def term(self):
        self.factor()
        self.term_prime()
    
    def term_prime(self):
        if(self.token_value == "*" or self.token_value == "/"):
            self.mulop()
            self.factor()
            self.term_prime()
        elif(self.token_value == "+"
            or self.token_value == "-" or self.token_value == "<=" or self.token_value == "<"
            or self.token_value == ">" or self.token_value == ">=" or self.token_value == "=="
            or self.token_value == "!=" or self.token_value == ";" or self.token_value == ")"
            or self.token_value == ","  or self.token_value == "]"):
            return
        else:
            self.error("TERM HAS AN INCORRECT FORMAT")
    
    def mulop(self):
        if(self.token_value == "*"):
            self.match("*")
        elif(self.token_value == "/"):
            self.match("/")
        else:
            self.error("MULTIPLICATION OR DIVISION OPERATOR EXPECTED")
    
    def factor(self):
        if(self.token_value == "("):
            self.match("(")
            self.arithmetic_expression()
            self.match(")")
        elif(self.check_id()):
            self.var()
        elif(self.check_num()):
            self.match_num()
        else:
            self.error("FACTOR HAS AN INCORRECT FORMAT")

    def args(self):
        if(self.token_value == "(" or self.check_id() or self.check_num()):
            self.args_list()
        elif(self.token_value == ")"):
            return
        else:
            self.error("ARGUMENTS HAVE AN INCORRECT FORMAT")

    def args_list(self):
        self.arithmetic_expression()
        self.args_list_prime()

    def args_list_prime(self):
        if(self.token_value == ","):
            self.match(",")
            self.arithmetic_expression()
            self.args_list_prime()
        elif(self.token_value == ")"):
            return
        else:
            self.error("COMA IS EXPECTED BETWEEN ARGUMENTS")         







    

