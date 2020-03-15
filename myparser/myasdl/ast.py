class Field:
    def __init__(self, field, option=None, id=None):
        self.field = field
        self.option = option
        self.id = id

    def __repr__(self):
        return f'''<Field {self.field} {self.option if self.option is not None else ""} {"" if self.id is None else self.id}>'''

class Fields:
    def __init__(self, fields):
        self.fields = fields

    def __repr__(self):
        return f'''<Fields: {",".join(repr(f) for f in self.fields)}>'''


class Constructor:
    def __init__(self, conid, fields=None):
        self.conid = conid
        self.fields = fields
    def __repr__(self):
        return f'''<Constructor {self.conid} {self.fields}>'''


class Product:
    def __init__(self, fields):
        self.fields = fields

    def __repr__(self):
        return f'''<Product fields:{repr(self.fields)}>'''


class Sum:
    def __init__(self, cons):
        self.cons = cons
    def __repr__(self):
        return f'''<Sum {"|".join(repr(c) for c in self.cons)}>'''

class Type:
    def __init__(self, type, attributes=None):
        self.type = type
        self.attributes = attributes
    def __repr__(self):
        return f'''<type:{self.type}
        attr:{self.attributes}
        >'''

class Definition:
    def __init__(self, typ_id, type):
        self.typ_id = typ_id
        self.type = type
    
    def __repr__(self):
        return f'''<dfn:{self.typ_id}
    type:{self.type}
  >'''

class Module:
    def __init__(self, modulename, dfns):
        self.modulename = modulename
        self.dfns = dfns

    def __repr__(self):
        return f'''<Module:{self.modulename}
  {(chr(10)+"  ").join(repr(d) for d in self.dfns)}
>
        '''
