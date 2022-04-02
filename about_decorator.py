#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/dm-fedorov/advanced-python/blob/master/about_decorator.ipynb"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open and Execute in Google Colaboratory" target="_blank"></a>

# Дектораторы обсуждаются в [PEP 318](https://www.python.org/dev/peps/pep-0318/).

# В своей основе декораторы Python позволяют расширять и изменять поведение вызываемых объектов (функций, методов и классов) без необратимой модификации самих вызываемых объектов.
# 
# Любая достаточно универсальная функциональность, которую можно прикрепить к существующему классу или поведению функции, является отличным кандидатом для декорирования. Сюда входят:
# 
# - ведение протокола операций (журналирование);
# - обеспечение контроля за доступом и аутентификацией;
# - функции инструментального оформления и хронометража;
# - ограничение частоты вызова API;
# - кэширование и др.

# Предположим, в вашей программе составления отчетности есть 30 функций с бизнес-логикой. Одним дождливым утром понедельника ваш босс подходит к вашему столу и заявляет: 
# 
# *«Доброго понедельника! Помните ту отчетность по TPS? Мне нужно, чтобы вы в каждый шаг генератора отчетов добавили ведение протокола входных и выходных операций. Компании XYZ это нужно для аудиторских целей. Да, и еще. Я им сказал, что к среде мы сможем все отправить».* 

# Без декораторов следующие три дня вам пришлось бы провести в попытках модифицировать каждую из этих 30 функций, приводя их в полный беспорядок ручными вызовами операции журналирования. 
# 
# Чудесно, не правда ли? 
# 
# А если вы знаете свои декораторы, вы спокойно улыбнетесь своему боссу и скажете: *«Не беспокойся, Джим. Я сделаю это сегодня к 14:00».*

# Декораторы позволяют определять конструктивные блоки многократного использования, которые могут изменять или расширять поведение других функций. И они позволяют это делать без необратимых изменений самой обернутой функции. Поведение функции изменяется, только когда оно декорировано.
# 
# Декоратор — это вызываемый объект, который на входе принимает один вызываемый объект (функцию), а на выходе возвращает другой вызываемый объект (функцию).
# 
# Приведенная ниже функция имеет это свойство и может считаться самым простым декоратором, который вы могли когда-либо написать:

# In[1]:


def null_decorator(func):
    return func


# Как видите, **null_decorator** является вызываемым объектом (это функция). На входе он принимает еще один вызываемый объект и на выходе возвращает тот же самый вызываемый объект без его изменения.

# Давайте его применим, чтобы декорировать (или обернуть) еще одну функцию:

# In[2]:


def greet():
    return 'Привет!'


# In[3]:


greet = null_decorator(greet)


# In[4]:


greet()


# In[5]:


greet


# In[6]:


null_decorator(greet)


# В этом примере я определил функцию **greet** и сразу же ее декорировал, пропустив через функцию **null_decorator**. Понимаю, пока это все выглядит бесполезным. Я ведь о том, что мы намеренно  спроектировали пустой декоратор бесполезным, верно? Но через мгновение этот пример разъяснит, как работает специальный синтаксис Python, предназначенный для декораторов.
# 
# Вместо того чтобы явным образом вызывать **null_decorator** с функцией **greet** и затем по-новому присваивать его переменной, удобнее воспользоваться синтаксисом Python **@** для декорирования функции:

# In[7]:


@null_decorator
def greet():
    return 'Привет!'


# In[8]:


greet()


# Размещение строки **@null_decorator** перед определением функции аналогично тому, что функция сначала определяется и затем уже прогоняется через декоратор. Синтаксис **@** является всего лишь *синтаксическим сахаром (syntactic sugar)* и краткой формой для этого широко применяемого шаблона.
# 
# Обратите внимание: синтаксис **@** декорирует функцию непосредственно во время ее определения. При этом становится трудно получить доступ к недекорированному оригиналу без хрупких хакерских фокусов. По этой причине вы можете решить вручную декорировать некоторые функции для сохранения способности вызвать и недекорированную функцию.

# Рассмотрим еще один пример декоратора:

# In[9]:


def deco(func):
    def inner():
        print('запуск inner()')
    return inner # возвращает внутренний объект-функцию


# In[10]:


@deco # target декорирована deco
def target(): 
    print('запуск target()')    


# In[11]:


target() # при вызове target выполняется inner


# In[12]:


target # target ссылается на inner


# Это всего лишь *синтаксический сахар* для:

# In[13]:


def deco(func):
    def inner():
        print('запуск inner()')
    return inner # возвращает внутренний объект-функцию

def target(): 
    print('запуск target()')   

target = deco(target)
target()


# In[14]:


target


# ## Декораторы могут менять поведение

# Теперь, когда вы чуть ближе познакомились с синтаксисом декораторов, давайте напишем еще один декоратор, который действительно что-то делает и изменяет поведение декорированной функции.
# 
# Вот чуть более сложный декоратор, который преобразовывает результат декорированной функции в буквы верхнего регистра:

# In[15]:


def uppercase(func):
    def wrapper():
        original_result = func()
        modified_result = original_result.upper()
        return modified_result
    return wrapper


# Вместо того чтобы просто возвратить входную функцию, как это делал пустой декоратор, декоратор **uppercase** на лету определяет новую функцию *(замыкание)* и использует ее в качестве обертки входной функции, чтобы изменить ее поведение во время вызова.
# 
# Замыкание **wrapper** имеет доступ к недекорированной входной функции, и оно свободно может выполнить дополнительный программный код до и после ее вызова. (Технически замыканию вообще не нужно вызывать входную функцию.) 
# 
# Заметьте, что вплоть до настоящего момента декорированная функция ни разу не была исполнена. На самом деле, в вызове входной функции на данном этапе нет никакого смысла — потребность в том, чтобы декоратор был в состоянии изменить поведение своей входной функции, возникнет, только когда он наконец будет вызван.

# In[16]:


@uppercase
def greet():
    return 'Привет!' 


# In[17]:


greet()


# В отличие от **null_decorator**, декоратор **uppercase** при декорировании функции возвращает другой объект-функцию:

# In[18]:


uppercase(greet) 


# И как вы видели чуть раньше, ему это нужно, чтобы изменить поведение декорированной функции, когда он в итоге будет вызван. Декоратор **uppercase** сам является функцией. И единственный способ повлиять на «будущее поведение» входной функции, которую он декорирует, состоит в том, чтобы подменить (или обернуть) входную функцию замыканием.
# 
# Вот почему декоратор **uppercase** определяет и возвращает еще одну функцию (замыкание), которая затем может быть вызвана в дальнейшем, выполняет оригинальную входную функцию и модифицирует ее результат.
# 
# Декораторы изменяют поведение вызываемого объекта посредством обертки-замыкания, в результате чего вам не приходится необратимо модифицировать оригинал. Оригинальный вызываемый объект не изменяется необратимо — его поведение меняется, только когда он декорирован.
# 
# Это позволяет прикреплять к существующим функциям и классам конструктивные блоки многократного использования, в частности функционал журналирования и другое инструментальное оформление. Этот факт делает декораторы настолько мощным функциональным средством языка, что они нередко используются в стандартной библиотеке Python и в сторонних пакетах.

# ## Применение многочисленных декораторов к функции

# Возможно, вас не удивит, что к функции можно применять более одного декоратора. В этом случае их эффекты накапливаются, и именно этот факт делает декораторы столь полезными в качестве структурных блоков многократного использования.
# 
# Приведем пример. Представленные ниже два декоратора обертывают выходную строку декорированной функции в HTML-теги. Глядя на то, как теги вложены, вы видите, в каком порядке Python применяет многочисленные декораторы:

# In[19]:


def strong(func):
    def wrapper():
        return '<strong>' + func() + '</strong>'
    return wrapper

def emphasis(func):
    def wrapper():
        return '<em>' + func() + '</em>'
    return wrapper


# Теперь давайте возьмем эти два декоратора и одновременно применим их к нашей функции greet. Для этого вы можете использовать обычный синтаксис **@** и просто «уложить» многочисленные декораторы вертикально поверх одной-единственной функции:

# In[20]:


@strong
@emphasis
def greet():
    return 'Привет!'


# In[21]:


greet()


# Этот результат ясно показывает, в каком порядке декораторы были применены: снизу вверх. Сначала входная функция была обернута декоратором **@emphasis**, и затем результирующая (декорированная) функция снова была обернута декоратором **@strong**.

# Если разложить приведенный выше пример и избавиться от синтаксиса **@**, который применяют декораторы, то цепочка вызовов функций-декораторов выглядит так:     

# In[22]:


decorated_greet = strong(emphasis(greet))


# In[23]:


decorated_greet()


# ## Декорирование функций, принимающих аргументы

# Все примеры пока что декорировали только простую нуль-арную функцию **greet**, которая вообще не принимала никаких аргументов. 
# Вплоть до этого момента декораторам, которые вы здесь видели, не было дела до переадресации аргументов во входную функцию.
# 
# Если применить один из этих декораторов к функции, которая принимает аргументы, то она не заработает правильно. Тогда как декорировать функцию, которая принимает произвольные аргументы?

# ### Вспомним про \*args и \*\*kwargs

# In[24]:


def foo(required, *args, **kwargs):
    print(required)
    if args:
        print(args)
    if kwargs:
        print(kwargs)


# In[25]:


foo(1, 2, 3, 4, key1=5, key2=6)


# Приведенная выше функция требует по крайней мере одного аргумента под названием «required», то есть обязательный, но она также может принимать дополнительные позиционные и именованные аргументы.
# 
# Если мы вызовем функцию с дополнительными аргументами, то **args** соберет дополнительные позиционные аргументы в кортеж, потому что имя параметра имеет префикс \*.
# 
# Аналогичным образом, **kwargs** соберет дополнительные именованные аргументы в словарь, потому что имя параметра имеет префикс \*\*.
# 
# Название параметров **args** и **kwargs** принято по договоренности, как согласованное правило именования. Приведенный выше пример будет работать точно так же, если вы назовете их \*parms и \*\*argv. Фактическим синтаксисом является, соответственно, просто звездочка (\*) или двойная звездочка (\*\*).

# ### Вспомним про распаковку аргументов
# 
# Существует возможность передавать необязательные или именованные параметры из одной функции в другую. Это можно делать при помощи операторов распаковки аргументов \* и \*\* во время вызова функции, в которую вы хотите переадресовать аргументы.

# Это также дает вам возможность модифицировать аргументы перед тем, как вы передадите их дальше. Вот пример:

# In[26]:


def bar(a, b, c, name='Ivan', color='red'):
    print(a, b, c, name, color)


# In[27]:


def foo(x, *args, **kwargs):
    kwargs['name'] = 'Alice'
    new_args = args + (3, )
    bar(x, *new_args, **kwargs)


# In[28]:


foo(1, 2, color='green')


# Вот где на помощь приходят функциональные средства языка Python \*args и \*\*kwargs для работы с неизвестными количествами аргументов. 
# 
# Ниже приведен декоратор **proxy**, в котором задействуется их преимущество:

# In[29]:


def proxy(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


# С этим декоратором происходят две вещи, заслуживающие внимания:
# - В определении замыкания **wrapper** он использует операторы \* и \*\*, чтобы собрать все позиционные и именованные аргументы, и помещает их в переменные (**args** и **kwargs**).
# - Замыкание **wrapper** затем переадресует собранные аргументы в оригинальную входную функцию, используя операторы «распаковки аргументов» \* и \*\*.

# Давайте расширим прием, сформулированный декоратором **proxy**, в более полезный практический пример. 
# Ниже приведен декоратор **trace**, который регистрирует аргументы функции и итоговые результаты, полученные во время исполнения:

# In[30]:


def trace(func):
    def wrapper(*args, **kwargs):
        print(f'ТРАССИРОВКА: вызвана {func.__name__}() с {args}, {kwargs}')
        original_result = func(*args, **kwargs)
        print(f'ТРАССИРОВКА: {func.__name__}() вернула {original_result}')
        return original_result
    return wrapper


# При декорировании функции с использованием декоратора **trace** и последующем ее вызове, будут выведены переданные в декорированную функцию аргументы и возвращаемое ею значение. 
# Этот пример по-прежнему остается несколько «игрушечным» — но в случае крайней необходимости он становится отличным средством отладки:

# In[31]:


@trace 
def say(name, line):
    return f'{name}: {line}'


# In[32]:


say('Джейн', 'Привет, Мир')


# ## Как писать «отлаживаемые» декораторы

# При использовании декоратора вы на самом деле только подменяете одну функцию другой. Оборотной стороной этого процесса является то, что он «скрывает» некоторые метаданные, закрепленные за оригинальной (недекорированной) функцией.

# Например, оригинальное имя функции, ее строка документации *docstring* и список параметров скрыты замыканием-оберткой:

# In[33]:


def greet():
    """Вернуть дружеское приветствие."""
    return 'Привет!'


# In[34]:


decorated_greet = uppercase(greet)


# При попытке получить доступ к каким-либо из этих метаданных функции вместо них вы увидите метаданные замыкания-обертки:

# In[35]:


greet.__name__


# In[36]:


greet.__doc__


# In[37]:


decorated_greet.__name__


# In[38]:


decorated_greet.__doc__


# Это делает отладку и работу с интерпретатором Python неуклюжей и трудоемкой. 
# К счастью, существует быстрое решение этой проблемы: декоратор **functools.wraps**, включенный в стандартную библиотеку Python.
# 
# Декоратор **functools.wraps** можно использовать в своих собственных декораторах для того, чтобы копировать потерянные метаданные из недекорированной функции в замыкание декоратора. Вот пример:

# In[39]:


import functools
def uppercase(func):
    @functools.wraps(func)
    def wrapper():
        return func().upper()
    return wrapper


# Применение декоратора **functools.wraps** к замыканию-обертке, возвращаемому декоратором, переносит в него строку документации и другие метаданные входной функции:

# In[40]:


@uppercase 
def greet():
    """Вернуть дружеское приветствие."""
    return 'Привет!'


# In[41]:


greet.__name__


# In[42]:


greet.__doc__


# В качестве оптимального практического приема я порекомендовал бы использовать декоратор **functools.wraps** во всех декораторах, которые вы пишете сами. Это не займет много времени и уменьшит головную боль вам (и другим) в будущем при отладке.

# ## Измерение времени работы программы

# In[43]:


def benchmark(func):
    import time    
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end-start))
    return wrapper

@benchmark
def fetch_webpage():
    import requests
    webpage = requests.get('https://google.com')

fetch_webpage()


# In[44]:


def benchmark(func):
    import time    
    def wrapper(*args, **kwargs):
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print('[*] Время выполнения: {} секунд.'.format(end-start))
        return return_value
    return wrapper

@benchmark
def fetch_webpage(url):
    import requests
    webpage = requests.get(url)
    return webpage.text[:100]

webpage = fetch_webpage('https://google.com')
print(webpage)


# In[45]:


def benchmark(iters):
    def actual_decorator(func):
        import time        
        def wrapper(*args, **kwargs):
            total = 0
            for i in range(iters):
                start = time.time()
                return_value = func(*args, **kwargs)
                end = time.time()
                total = total + (end-start)
            print('[*] Среднее время выполнения: {} секунд.'.format(total/iters))
            return return_value
        return wrapper
    return actual_decorator


@benchmark(iters=10)
def fetch_webpage(url):
    import requests
    webpage = requests.get(url)
    return webpage.text[:100]

webpage = fetch_webpage('https://google.com')
print(webpage)


# ## Задание 1

# Напишите декоратор **log**
# 
# ```python
# >>> @log
# ... def function(*args):
# ...... return 3 + len(args)
# 
# >>> function(4, 4, 4)
# вы вызвали функцию function(4, 4, 4)
# она вернула значение 6
# 6
# ```

# In[ ]:





# ## Задание 2

# Напишите декоратор **html**, который в результате вызова **function('hi')** записывает в файл с именем "my_file.html" следующий текст:

# 2019/11/27 10:55
# ```html
# <html>
# <strong>'hi'</strong>
# </html>
# ```
# 
# *Подсказка:* время можно взять из time.strftime()
# 
# Пример вызова декоратора:

# ```python
# >>> @html
# ... def function(s='hello'):
# ...... return s
# 
# >>> function('hi')
# ```

# In[ ]:



