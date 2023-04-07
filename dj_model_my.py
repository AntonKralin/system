from datetime import datetime

class Field:
    def __init__(self, default = None, blank = False) -> None:
        self.default = default
        self.blank = blank

    def __str__(self):
        return str(self.default)
    
    def __eq__(self, other):
        if self.default == other:
            return True
        return False
    
    def validate(self, value):
        pass


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message


class CharField(Field):
    def __init__(self, min_length=0, max_length=None, default=None, blank=False):
        super().__init__(default, blank)
        self.min_length = min_length
        self.max_length = max_length
        
    def validate(self, value):
        if value == None:
            return
        if not isinstance(value, str):
            raise ValidationError('wrong type')
        if self.min_length:
            if len(value) < self.min_length:
                raise ValidationError('min_length is out of range')
        if self.max_length:
            if len(value) > self.max_length or self.max_length < 0:
                raise ValidationError('max_length is out of range')
        if self.min_length < 0:
            raise ValidationError("length can be < 0")


class IntegerField(Field):
    def __init__(self, min_value=None, max_value=None, default=None, blank=False):
        super().__init__(default, blank)
        self.min_value = min_value
        self.max_value = max_value
        
    def validate(self, value):
        if value == None:
            return
        if type(value) != int:
            raise ValidationError('wrong type')
        if self.min_value:
            if value < self.min_value:
                raise ValidationError('min_value is out of range')
        if self.max_value:
            if value > self.max_value:
                raise ValidationError('max_value is out of range')


class BooleanField(Field):
    def __init__(self, default=None, blank=False):
        super().__init__(default, blank)
        
    def validate(self, value):
        if value == None:
            return
        if type(value) != bool:
            raise ValidationError('wrong type')


class DateTimeField(Field):
    def __init__(self, auto_now=False, default=None, blank=False):
        #super().__init__(default, blank)
        self.blank = blank
        self.__default = default       
        self.auto_now = auto_now
        
    @property
    def default(self):
        if self.auto_now and self.__default == None:
            default = datetime.now()
        else:
            default = self.__default
        return default
    
    @default.setter
    def default(self, default):
        self.__default = default
        
    def validate(self, value):
        if value == None:
            return
        if not isinstance(value, datetime):
            raise ValidationError('wrong type')
    

class EmailField(Field):
    def __init__(self, min_length=0, max_length=None, default=None, blank=False):
        super().__init__(default, blank)
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value):
        if value == None:
            return
        if not isinstance(value, str):
            raise ValidationError('wrong type')
        if self.min_length:
            if len(value) < self.min_length:
                raise ValidationError('min_length is out of range')
        if self.max_length:
            if len(value) > self.max_length or self.max_length < 0:
                raise ValidationError('max_length is out of range') 
        if value.find("@") == -1:
            raise ValidationError('@ not contain') 
        arr = value.split("@")
        if arr[1].find(".") == -1:
            raise ValidationError('not find domain') 
        if self.min_length < 0:
            raise ValidationError("length can be < 0")

class MetaModel(type):
    
    def __init__(self, *args, **kwargs):
        arr = dir(self)
        for i_atr in arr:
            if i_atr.startswith("_"):
                continue
            val = getattr(self, i_atr)
            if hasattr(val, 'validate'):                  
                    setattr(self, i_atr.upper(), val)
                    delattr(self, i_atr)
    
           

class Model(metaclass=MetaModel):
    
    def __init__(self, *args, **kwargs) -> None:
        arr = dir(self)
        for i_atr in arr:
            val = self.__getattribute__(i_atr)
            
            if hasattr(val, 'validate'):
                if i_atr.lower() in kwargs:
                    self.__setattr__(i_atr.lower(), kwargs.get(i_atr.lower()))
                else:
                    if not i_atr.startswith("__clas"):
                        self.__setattr__(i_atr.lower(), val.default)
    

                    
    
    def validate(self):
        arr = dir(self)
        for i_atr in arr:
            if i_atr.startswith("__"):
                continue
            val = self.__getattribute__(i_atr)
            if hasattr(val, 'validate') and hasattr(self, i_atr.lower()):
                value = self.__getattribute__(i_atr.lower())
                if val.blank == False and value == None:
                    raise ValidationError("value can't be None")
                val.validate(value)
                
                
class User(Model):
        first_name = CharField(max_length=30, default='Adam')
        last_name = CharField(max_length=50, blank=True)
        email = EmailField(max_length=50, blank=False)
        is_verified = BooleanField(default=False)
        date_joined = DateTimeField(auto_now=True)
        age = IntegerField(min_value=5, max_value=120, blank=True)        
        
if __name__ == '__main__':
    #print(dir(User))
    #print(not hasattr(User, 'first_name'))
    #print(not hasattr(User(), 'first_name'))
    user = User(first_name='Liam', email='liam@example.com')
    #user.age = 25
    #print(user.is_verified)
    #if isinstance(user.is_verified, bool):
    #    print('the same')
    #if user.is_verified == False:
    #    print(user.first_name)   
    #print(dir(user))
    #print(user.first_name)
    #print(user.is_verified)
    #user3 = User(first_name='Liam', email='liam@example.com')
    #print(user3.date_joined)
    #print(datetime(2000, 1, 1, 0, 0))
    #user.validate()
    #print(not hasattr(User, 'first_name'))
    #user.age = 999
    print(isinstance(True, int))
    print(type(True), type(bool))
    user.is_verified=True
    user.validate()