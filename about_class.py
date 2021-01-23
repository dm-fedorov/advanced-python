#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/dm-fedorov/advanced-python/blob/master/about_class.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open and Execute in Google Colaboratory" target="_blank"></a>

# In[1]:


class Person:
    name = "Ivan"  


# In[2]:


print(dir(Person))


# In[3]:


Person.__dict__


# In[4]:


# что это?
from types import MappingProxyType # c Python 3.3
# https://docs.python.org/3/library/types.html#types.MappingProxyType


# In[5]:


d = {"key": "value"}


# In[6]:


m = MappingProxyType(d)


# In[7]:


print(m)


# In[8]:


type(m)


# In[9]:


m["key"] = "new"


# In[10]:


d["1"] = "2"


# In[11]:


print(m)


# In[12]:


print(dir(m))


# In[13]:


m.get('1')


# In[14]:


Person.__dict__


# In[15]:


getattr(Person, "name")


# In[16]:


setattr(Person, "age", "4")


# In[17]:


Person.__dict__


# In[18]:


class Person:
    name = "Ivan"
    
    def hello(self):
        print("Hello")


# In[19]:


Person.__dict__


# In[20]:


# про объекты
p1 = Person() # вызываемый объект


# In[21]:


p2 = Person()


# In[22]:


p1.name


# In[23]:


id(p1.name), id(Person.name), id(p2.name)


# In[24]:


p1.__dict__


# In[25]:


p1.age = 13


# In[26]:


p1.__dict__


# In[27]:


Person.__dict__


# In[28]:


# про функции
Person.hello


# In[29]:


type(Person.hello)


# In[30]:


p1.hello


# In[31]:


hex(id(p1))


# In[32]:


type(p1.hello)


# In[33]:


# что произошло???


# In[34]:


print(dir(Person.hello))


# In[35]:


print(dir(p1.hello))


# In[36]:


# __self__


# In[37]:


p1.hello.__self__ # хранит адрес экземляра класса


# In[38]:


p1.hello.__func__


# In[39]:


p1.hello()


# In[40]:


Person.hello(p1) # класс обращается к пространству имен экземпляра класса


# Методы позволяют вызвать функцию класса и передать туда содержимое пространства имен экземплара класса

# In[41]:


p1.hello.__func__(p1.hello.__self__)


# Функция становится методом в экземпляре класса.

# In[42]:


class Person:
    def create(self):
        self.name = "Ivan"
        
    def display(self):
        print(self.name)


# In[43]:


p = Person()


# In[44]:


p.display()


# In[45]:


p.__dict__


# In[46]:


# инициализация


# In[47]:


class Person:
    def __init__(self, name): # есть конструктор __new__, поэтому иницализатор
        self.name = "Ivan"
        
    def display(self):
        print(self.name)


# In[48]:


p = Person("Ivan")


# In[49]:


p.__dict__


# In[50]:


# static


# In[51]:


class Person:
    def hello(self):
        print("Hello")
        
    def goodbye():
        print("Goodbye")


# In[52]:


p = Person()
p.goodbye()


# Что делать, если методу не нужно получать доступ к экземплярам класса?

# In[53]:


class Person:
    def hello(self):
        print("Hello")
    
    @staticmethod
    def goodbye(): # теперь это один объект на все экземпляры класса
        print("Goodbye")


# In[54]:


p = Person()
p.goodbye()


# In[55]:


a = Person()
b = Person()


# In[56]:


a.hello()


# In[57]:


a.goodbye()


# In[58]:


id(a.hello), id(b.hello), id(Person.hello)


# In[59]:


id(a.goodbye), id(b.goodbye), id(Person.goodbye)


# In[60]:


type(a.goodbye)


# In[61]:


Person.goodbye()


# Статические методы не связываются ни с экземпляром класса, ни с самим классом.

# In[62]:


class Person:
    def __init__(self, name): # есть конструктор __new__, поэтому иницализатор
        self._name = name # приватные атрибуты
        self.name = f'Mr. {self._name}' # публичное


# In[63]:


p = Person("Ivan")


# In[64]:


p.name


# Name mangling 

# In[65]:


class Person:
    __name = "Ivan"    


# In[66]:


p = Person()


# In[67]:


p.__name


# In[68]:


p.__name = "Oleg"


# In[69]:


p.__dict__


# In[70]:


print(dir(p))


# In[71]:


p._Person__name


# * Local
# * Enclosed
# * Global
# * Builtins

# In[72]:


class Person:
    name_1 = "Egor" # область видимости класса
    
    def print_name(self): 
        print(name_1)

p = Person()
p.print_name() # область видимости экземпляра класса


# Resolution - разрешение имен.
# 
# Несвязанные локальные переменные (unbound local variables) ищутся в глобальном пространстве имен:

# In[73]:


x = 1

def a():
    print(x)
        
a()


# In[74]:


x = 1

def a():
    x = x + 1  # несвязанная со значением
    print(x)
        
a()


# In[75]:


def a():
    k = 1
    
def b():
    print(x) # не видим из этого пространства имен
    
b()


# In[76]:


class Person:
    name_1 = "Egor" # область видимости класса
    
    def print_name(self): 
        print(self.name_1) # найдет в классе

p = Person()
p.print_name() 
print("Экземпляр: ", p.__dict__)
p.name_1 = "asdlasdl;sd" # создает в экземпляре 
print("Экземпляр: ", p.__dict__)
print("Person: ", Person.name_1)


# In[77]:


class Person:
    name_1 = "Egor" # область видимости класса
    
    @classmethod
    def change_name(cls, name): # метод класса, принимает класс 
        cls.name_1 = name

p = Person()
print("Person: ", Person.name_1)
print("Экземпляр: ", p.__dict__)
p.change_name("12345") 
print("Экземпляр: ", p.__dict__)
print("Person: ", Person.name_1)


# Методы класса не имеют доступа к экземплярм, но имеют доступ к свойствам самого класса.

# In[78]:


#Person.change_name("678")


# In[79]:


#print("Person: ", Person.name_1)


# In[80]:


class Person:
    def __init__(self, name):
        self.name = name
    
    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            name = f.read().strip()
        return cls(name=name)
    
    @classmethod
    def from_obj(cls, obj):
        if hasattr(obj, "name"):
            name = getattr(obj, "name")
            return cls(name=name)
        return cls


# In[81]:


get_ipython().run_cell_magic('writefile', 'text_file.txt', 'sdfs')


# In[82]:


p = Person("Olga")


# In[83]:


p.__dict__


# In[84]:


p.name


# In[85]:


p = Person.from_file("text_file.txt")


# In[86]:


p.__dict__


# In[87]:


class Config:
    name = "Igor"   


# In[88]:


p = Person.from_obj(Config)


# In[89]:


p.__dict__


# In[ ]:




