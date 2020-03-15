from ast import *
def parseField(cur_token, tokens):
    '''parseField possible:
    1. "field[*|?],','"
    2. "field[*|?],')'"
    '''
    f = Field(cur_token)
    next_token = next(tokens)
    if next_token is None:
        return f, None
    if next_token in ["*", "?"]:
        f.option = next_token
        next_token = next(tokens)
        if next_token is None:
            return f, None
    if next_token == ")":
        return f, ")"
    elif next_token != ",":
        f.id = next_token
        return f, next(tokens)
    else:
        return f, ","


def parseFields(cur_token, tokens):
    if cur_token != "(":
        raise Exception("parseFields not start with '('")
    next_token = next(tokens)
    fields = []
    while next_token != ")":
        if next_token is None:
            return Fields(fields), None
        field, next_token = parseField(next_token, tokens)
        fields.append(field)
        if next_token != "," and next_token != ")":
            raise Exception("field without ', | )', cur field is " + field + " next token is ", next_token)
        if next_token == ",":
            next_token = next(tokens)
            if next_token == ")":
                raise Exception("field with ',)'")
            if next_token is None:
                return Fields(fields), next_token

    return Fields(fields), next(tokens)

def parseCon(cur_token, tokens):
    con = Constructor(cur_token)
    if not cur_token[0].isupper():
        raise Exception("ConId[0] must upper.")
    next_token = next(tokens)
    if next_token is None:
        return con, next_token
    if next_token == "(":
        fields, next_token = parseFields(next_token, tokens)
        con.fields = fields
        return con, next_token
    return con, next_token
    ##if next_token != "(":
    ##    raise Exception("'(' is needed to constuct a ConId")


def parseSum(cur_token, tokens):
    cs = []
    c, next_token = parseCon(cur_token, tokens)
    cs.append(c)
    if next_token is None:
        return Sum(cs), next_token
    while next_token == "|":
        next_token = next(tokens)
        if next_token is None:
            return Sum(cs), next_token
        c, next_token = parseCon(next_token, tokens)
        cs.append(c)
        if next_token is None:
            return Sum(cs), next_token

    ## print("Sum next_token is", next_token)
    return Sum(cs), next_token


def parseProduct(cur_token, tokens):
    fields, next_token = parseFields(cur_token, tokens)
    return Product(fields), next_token
    

def parseType(cur_token, tokens):
    if cur_token is None:
        return None, None
    if cur_token == "(":
        sum_product, next_token = parseProduct(cur_token, tokens)
    else:
        sum_product, next_token = parseSum(cur_token, tokens)

    if next_token == "attributes":
        cur_token = next(tokens)
        if cur_token is None:
            return Type(sum_product), cur_token
        fields, next_token = parseFields(cur_token, tokens)
        return Type(sum_product, fields), next_token

    return Type(sum_product), next_token


def parseDfn(cur_token, tokens):
    typeId = cur_token
    next_token = next(tokens)
    if next_token != "=":
        raise Exception("definitions need '=', but get", next_token, "cur_token is", cur_token)
    
    cur_token = next(tokens)
    type, next_token = parseType(cur_token, tokens)
    return Definition(typeId, type), next_token
    ##return typeId+"="+",".join(type), next_token


def parseDfns(cur_token, tokens):
    if cur_token is None:
        return None, None
    dfn, next_token = parseDfn(cur_token, tokens)
    dfns = [dfn]
    while next_token != None and next_token != "}":
        dfn, next_token = parseDfn(next_token, tokens)
        dfns.append(dfn)

    return dfns, next_token

def parseModule(cur_token, tokens):
    if cur_token != "module":
        raise Exception("should be start with 'module' keyword")
    cur_token = next(tokens)
    if cur_token is None:
        return None, None
    moduleName = cur_token
    cur_token = next(tokens)
    if cur_token != "{":
        raise Exception("'{' should after with 'module'")
    cur_token = next(tokens)
    if cur_token is None:
        return None, None
    dfns, next_token = parseDfns(cur_token, tokens)
    if next_token != "}":
        raise Exception("'}' is needed at the end of the module's definition")
    next_token = next(tokens)
    return Module(moduleName, dfns), next_token
    ##return "module:" + moduleName + "{" + ",".join(dfns) + "}", next_token
