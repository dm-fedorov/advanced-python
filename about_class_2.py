#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/dm-fedorov/advanced-python/blob/master/about_class_2.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open and Execute in Google Colaboratory" target="_blank"></a>

# Свойства класса - способ доступа к переменным класса.

# In[1]:


class Person:
    def __init__(self, name):
        self.name = name


# In[2]:


p = Person("Ivan")


# In[3]:


p.name = "Igor"


# In[4]:


p.name


# In[5]:


class Person:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        print("call get_name()")
        return self._name
    
    def set_name(self, value):
        print("call set_name()")
        self._name = value
    
    # определим св-во класса name (атрибут класса)   
    name = property(fget=get_name, fset=set_name)


# In[6]:


p = Person("Ivan")


# In[7]:


p.__dict__


# In[8]:


p.name # обращаемся к атрибуту класса


# In[9]:


p.name = "Igor"


# In[10]:


p.__dict__


# In[11]:


class Person:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        print("call name()")
        return self._name 
    
    @name.setter
    def name(self, value):
        print("call set_name()")
        self._name = value    


# In[12]:


p = Person("Ivan")


# In[13]:


p.__dict__


# In[14]:


p.name # обращаемся к атрибуту класса


# In[15]:


p.name = "Igor"


# Отделяем внутренний интерфейс класса от внешнего.

# Внутри "геттеров" и "сеттеров" можем сделать валидацию входного значения.

# In[16]:


class Person:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):        
        return self._name 
    
    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self._name = value  
        else:
            raise ValueError("Что же ты делаешь? Это не строка!")


# In[17]:


p = Person("Ivan")


# In[18]:


p.name


# In[19]:


p.name = 5


# Чтобы создать свойство только для чтения надо установить декоратор геттер.

# In[20]:


class Person:
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):        
        return self._name 


# In[21]:


p = Person("Ivan")


# In[22]:


p.name


# In[23]:


p.name = "Olga"


# Вычисляемые свойства:

# In[24]:


class Person:
    def __init__(self, name, surname):
        self._name = name
        self._surname = surname
    
    @property
    def full_name(self):        
        return f'{self._name} {self._surname}'


# In[25]:


p = Person("Ivan", "Ivanov")


# In[26]:


p.full_name


# In[27]:


class Person:
    def __init__(self, name, surname):
        self._name = name
        self._surname = surname
    
    @property
    def name(self):        
        return self._name 
    
    @name.setter
    def name(self, value):
        self._name = value        
    
    @property
    def surname(self):        
        return self._surname 
    
    @surname.setter
    def surname(self, value):
        self._surname = value 
    
    @property
    def full_name(self):        
        return f'{self._name} {self._surname}'


# In[28]:


p = Person("Ivan", "Ivanov")


# In[29]:


p.name = "Pert"


# In[30]:


p.full_name


# Кэширование результата. Вычисляем только при вызове сэттера.

# In[31]:


class Person:
    def __init__(self, name, surname):
        self._name = name
        self._surname = surname
        self._full_name = None 
    
    @property
    def name(self):        
        return self._name 
    
    @name.setter
    def name(self, value):
        self._name = value
        self._full_name = None 
    
    @property
    def surname(self):        
        return self._surname 
    
    @surname.setter
    def surname(self, value):
        self._surname = value
        self._full_name = None 
    
    @property
    def full_name(self):  
        if self._full_name is None:
            self._full_name = f'{self._name} {self._surname}'
        return self._full_name


# In[32]:


p = Person("Ivan", "Ivanov")


# In[33]:


p.__dict__


# In[34]:


p.full_name


# In[35]:


p.__dict__


# In[36]:


p.surname = "Sidoroff"


# In[37]:


p.__dict__


# In[38]:


p.full_name


# In[39]:


p.__dict__


# # Наследование

# In[40]:


class Person:
    age = 0
    def hello(self):
        print("Hello")
        
class Student(Person):
    pass


# In[41]:


s = Student()


# In[42]:


dir(s)


# In[43]:


s.age


# In[44]:


s.hello()


# In[45]:


s.__dict__


# In[46]:


Student.__dict__


# In[47]:


Person.__dict__


# In[48]:


# разрешение пространства имен


# In[49]:


dir(object)


# In[50]:


class IntelCpu:
    cpu_socket = 1151
    name = "Intel"
    
class I7(IntelCpu):
    pass

class I5(IntelCpu):
    pass


# In[51]:


i5 = I5()


# In[52]:


i7 = I7()


# In[53]:


isinstance(i5, IntelCpu) # проверяет цепочку наследования


# In[54]:


type(i5)


# In[55]:


class One:
    pass

class Two(One):
    pass

class Three(Two):
    pass


# In[56]:


issubclass(Three, One) # учитывает непрямое отношение классов


# In[57]:


isinstance(i5, type(i7)) # экземпляр класса i5 не является экз. класса i7


# In[58]:


issubclass(type(i5), type(i7))


# # Перегрузка свойств и методов

# In[59]:


class Person:
    def hello(self):
        print("Hello")
        
class Student(Person):
    def hello(self):
        print("I am student")


# In[60]:


s = Student()


# In[61]:


s.hello()


# In[62]:


Student.__dict__


# In[63]:


# суть полиморфизма


# # Расширение функциональности класса

# In[64]:


class Person:
    def hello(self):
        print("Hello")
        
class Student(Person):
    def goodbye(self):
        print("Goodbye!")


# In[65]:


# Рассмотрим пример разрешения имен:


# In[66]:


class Person:
    def __init__(self, name):
        self.name = name
        
    def hello(self):
        print(f"Hello from {self.name}")
        
class Student(Person):
    pass


# In[67]:


s = Student("Ivan")


# In[68]:


s.hello()


# In[69]:


s.__dict__


# # Множественное наследование

# проблема ромбовидного наследования в [вики](https://ru.wikipedia.org/wiki/%D0%A0%D0%BE%D0%BC%D0%B1%D0%BE%D0%B2%D0%B8%D0%B4%D0%BD%D0%BE%D0%B5_%D0%BD%D0%B0%D1%81%D0%BB%D0%B5%D0%B4%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5)

# In[70]:


class Person:
    def hello(self):
        print("I am Person")
    
class Student(Person):
    def hello(self):
        print("I am Student")
        
class Prof(Person):
    def hello(self):
        print("I am Prof")
        
class Someone(Student, Prof):
    pass


# In[71]:


p = Someone()


# In[72]:


p.hello()


# Работает правило mro (порядок разрешения методов): прав самый левый из родителей.

# In[73]:


class Person:
    def hello(self):
        print("I am Person")
    
class Student(Person):
    def hello(self):
        print("I am Student")
        
class Prof(Person):
    def hello(self):
        print("I am Prof")
        
class Someone(Prof, Student):
    pass


# In[74]:


p = Someone()


# In[75]:


p.hello()


# In[76]:


p.__class__.mro() # в этом методе перечислен порядок, в котором Питон будет искать метод


# # Примеси классов

# в [вики](https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%81%D1%8C_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5))

# In[77]:


class FoodMixin:
    food = None
    
    def get_food(self):
        if self.food is None:
            raise ValueError("Установите еду!")
        print(f"I like {self.food}")

class Person:
    def hello(self):
        print("I am Person")
    
class Student(FoodMixin, Person):
    food = "Pizza"
    
    def hello(self):
        print("I am Student")


# In[78]:


s = Student()


# In[79]:


s.get_food()


# # Полиморфизм

# In[80]:


1 + 1


# In[81]:


"1" + "1" # синтаксический сахар для __add__()


# In[82]:


# Разное поведение в зависимости от типа данных


# In[83]:


class Person:
    age = 1
    def __add__(self, value): # переопределили в классе Person метода из object
        self.age += 1
        return self.age


# In[84]:


p = Person()


# In[85]:


p + 1234


# In[86]:


p + 123443345


# In[87]:


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.area = self.x * self.y
        
    def __add__(self, room_obj):
        if isinstance(room_obj, Room):
            return self.area + room_obj.area
        raise TypeError("Здесь должен быть объект класса Room!")


# In[88]:


r1 = Room(3, 5)


# In[89]:


r2 = Room(4, 7)


# In[90]:


r1.area


# In[91]:


r2.area


# In[92]:


r1 + r2


# In[93]:


class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.area = self.x * self.y
        
    def __add__(self, room_obj):
        if isinstance(room_obj, Room):
            return self.area + room_obj.area
        raise TypeError("Здесь должен быть объект класса Room!")
        
    def __eq__(self, room_obj):
        if isinstance(room_obj, Room):
            return self.area == room_obj.area


# In[94]:


r1 = Room(3, 5)


# In[95]:


r2 = Room(4, 7)


# In[96]:


r1 == r2


# # Равенство объектов

# In[97]:


# про ключи словаря


# In[98]:


import hashlib


# In[99]:


hashlib.md5("ivan".encode("utf8")).hexdigest()


# In[100]:


hashlib.md5("Ivan".encode("utf8")).hexdigest()


# In[101]:


# должны быть hash и eq


# In[102]:


hash("1")


# In[103]:


hash(1)


# In[104]:


class Person:
    def __init__(self, name):
        self._name = name
        
    @property
    def name(self):
        return self._name
    
    def __hash__(self):
        return hash(self._name)
    
    def __eq__(self, person_obj):
        return isinstance(person_obj, Person) and self.name == person_obj.name


# In[105]:


p1 = Person("Ivan")


# In[106]:


p2 = Person("Ivan")


# In[107]:


p1 == p2


# In[108]:


p3 = Person("Olga")


# In[109]:


p1 == p3


# In[110]:


hash(p1)


# In[111]:


hash(p2)


# In[112]:


# можно использовать в качестве ключа словаря


# In[113]:


d = {p1: "Ivanov"}


# In[114]:


d.get(p1)


# # Функция super

# In[115]:


class Person:
    def __init__(self, name):
        self.name = name
        
class Student(Person):
    def __init__(self, surname): # необходимо передать управление в __init__ метод родительского класса
        self.surname = surname


# In[116]:


class Person:
    def __init__(self, name):
        self.name = name
        
class Student(Person):
    def __init__(self, name, surname): 
        super().__init__(name) # делегирование выполнения в родительский класс, обычно первым вызывается
        self.surname = surname


# In[117]:


s = Student("Ivan", "Ivanov")


# In[118]:


s.__dict__


# # Дескрипторы

# Атрибут объекта и сам этот атрибут является объектом определенного класса. Класс с определенными магическими методами, хотя бы одним из \_\_get\_\_ \_\_set\_\_ \_\_delete\_\_

# Дескрипторы - протокол, который стоит за свойствами с декоратором property, статическими методами и методами класса.

# In[119]:


# Много дублирующего кода, если добавим еще одно свойство (одинаковый код):


# In[120]:


class Person:
    def __init__(self, name, surname):
        self._name = name
        self._surname = surname
        self._full_name = None 
    
    @property
    def name(self):        
        return self._name 
    
    @name.setter
    def name(self, value):
        self._name = value
        self._full_name = None 
    
    @property
    def surname(self):        
        return self._surname 
    
    @surname.setter
    def surname(self, value):
        self._surname = value
        self._full_name = None 


# In[121]:


# хорошо бы иметь такой класс:


# In[122]:


class StringD:
    def __init__(self, value=None):
        if value:
            self.set(value)
            
    def set(self, value):
        self._value = value
        
    def get(self):
        return self._value    


# In[123]:


# тогда Person немного сократится:


# In[124]:


class Person:
    def __init__(self, name, surname):
        self.name = StringD(name)
        self.surname = StringD(surname)       


# In[125]:


p = Person("Ivan", "Ivanov")


# In[126]:


p


# In[127]:


p.name


# In[128]:


p.name.get()


# In[129]:


# хочу, чтобы автоматически вызывался метод get,когда я обращаюсь к атрибуту name


# In[130]:


# рассмотрим протокол дескрипторов: non-data - отдают значения (метода get), datа-дескрипторы (умеют сохранять значения)


# In[131]:


from time import time

class Epoch:
    def __get__(self, obj, owner_class):
        return int(time())
    
class MyTime:
    epoch = Epoch()


# In[132]:


m = MyTime()


# In[133]:


m.epoch


# In[134]:


# игральный кубик


# In[135]:


from random import choice

class Dice:
    @property
    def number(self):
        return choice(range(1, 7))


# In[136]:


d = Dice()


# In[137]:


d.number # бросаем кубик


# In[138]:


d.number


# In[139]:


from random import choice
   
class Game:
    @property
    def rock_paper_scissors(self):
        return choice(["Rock", "Paper", "Scissors"])
    
    @property
    def flip(self): # подбрасывание монетки
        return choice(["Heads", "Tails"])
        
    @property
    def dice(self):
        return choice(range(1, 7))          


# In[140]:


d = Game()


# In[141]:


for i in range(3):
    print(d.dice)


# In[142]:


d.flip


# In[143]:


d.rock_paper_scissors


# In[144]:


# код делает одно и тоже, запишем через non-data дескрипторы:


# In[145]:


from random import choice

class Choice:
    def __init__(self, *choice):
        self._choice = choice
    
    def __get__(self, obj, owner):
        return choice(self._choice)
    
class Game:
    dice = Choice(1, 2, 3, 4, 5, 6)
    flip = Choice("Heads", "Tails")
    rock_paper_scissors = Choice("Rock", "Paper", "Scissors")    


# In[146]:


g = Game()


# In[147]:


g.flip


# In[148]:


g.rock_paper_scissors


# In[149]:


from time import time

class Epoch:
    def __get__(self, obj, owner_class):
        print(f"Self: {self}")
        print(f"Obj: {obj}")
        print(f"Owner class: {owner_class}")
        return int(time())
    
class MyTime:
    epoch = Epoch() # дескриптор


# In[150]:


m = MyTime()


# In[151]:


m.epoch


# In[152]:


MyTime.epoch


# In[153]:


# не трогаем объект MyTime


# In[154]:


class Person:
    _name = "Ivan"
    
    @property
    def name(self):
        return self._name


# In[155]:


Person.name # вернул экземпляр класса property


# In[156]:


Person().name # обратился к свойству через экземпляр


# In[157]:


from time import time

class Epoch:
    def __get__(self, instance, owner_class):
        if instance is None:  # был ли передан объект в параметр instance?
            return self        
        return int(time())
    
class MyTime:
    epoch = Epoch() # дескриптор


# In[158]:


# data - дескрипторы


# In[159]:


from time import time

class Epoch:
    def __get__(self, instance, owner_class):
        
        print(f"id of self: {id(self)}") # почему нельзя хранить данные в экз. класса
        
        if instance is None:  # был ли передан объект в параметр instance?
            return self        
        return int(time())
    
    def __set__(self, instance, value): # всегда вызываются из экземпляров
        pass
    
class MyTime:
    epoch = Epoch() # дескриптор


# In[160]:


m1 = MyTime()


# In[161]:


m1.epoch


# In[162]:


m2 = MyTime()


# In[163]:


m2.epoch


# In[164]:


# почему нельзя хранить данные в экз. дескриптора


# In[165]:


class IntDescriptor:
    def __set__(self, instance, value):
        print(f"I got {value}")
        
    def __get__(self, instance, owner):
        if instance is None:
            print("Call from a class")
        print("Call from instance")
       
class Vector:
    x = IntDescriptor()
    y = IntDescriptor()


# In[166]:


v = Vector()


# In[167]:


v.x = 5


# In[168]:


class IntDescriptor:
    def __set__(self, instance, value):
        self._value = value        
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._value
       
class Vector:
    x = IntDescriptor()
    y = IntDescriptor()


# In[169]:


v = Vector()


# In[170]:


v.x = 5


# In[171]:


v2 = Vector()


# In[172]:


v.x


# In[173]:


v2.x = 200


# In[174]:


v.x


# In[175]:


# мы не можем хранить значения в экз. дескрипторов


# In[176]:


class IntDescriptor:    
    def __init__(self):
        self._values = {}
    
    def __set__(self, instance, value):
        self._values[instance] = value
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance)
       
class Vector:
    x = IntDescriptor()
    y = IntDescriptor()


# In[177]:


v1 = Vector()


# In[178]:


v2 = Vector()


# In[179]:


v1.x = 5


# In[180]:


v2.x


# In[181]:


v2.x = 10


# In[182]:


v1.x


# In[183]:


Vector.x._values


# In[ ]:





# In[ ]:





# In[ ]:




