#-------------------------------------------L2(PYTHON-INTERMEDIATE)-------------------------------------------

#-------------------------------------------task id:l2-002-------------------------------------------
   #-----ITERATORS-----
class MyNumbers:

    def __iter__(self):
        self.a= 2
        return self  # Returning self means the object hands back itself as the thing to iterate over.

    def __next__(self):
        if self.a>10:
            raise StopIteration
        else:
            x = self.a
            self.a += 2
            return x

my_numbers = MyNumbers()
myiter = iter(my_numbers)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))

   #-----YIELD-----
def my_numbers():
    a = 2
    while a <= 10:
        yield a
        a += 2

   #-----YIELD(FROM)----
def small_numbers():
    yield 1
    yield 2
    yield 3

def big_numbers():
    yield from small_numbers()
    yield 4
    yield 5

for num in big_numbers():
    print(num)

#-------------------------------------------task id:l2-003-------------------------------------------
   #-----DECORATOR-----
def my_decorator(func):
    def wrapper():
        print("2 multiples are: ")
        func()
        print("Do You Want to see 3 multiples?")
    return wrapper

class TwoMultiples:
    def __iter__(self):
        self.a = 2
        return self

    def __next__(self):
        if self.a>10:
            raise StopIteration
        else:
            x = self.a
            self.a += 2
            return x

@my_decorator  # @ as shorthand for exactly show_multiples = my_decorator(show_multiples)
def show_multiples():
    for num in  TwoMultiples():
        print(num)
show_multiples()

   #-----handling functions that take arguments-----
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("2 multiples are: ")
        result = func(*args, **kwargs)
        print("Do You Want to see 3 multiples?")
        return result
    return wrapper

class TwooMultiples:
    def __init__(self, limit=10):
        self.limit = limit

    def __iter__(self):
        self.a = 2
        return self

    def __next__(self):
        if self.a > self.limit:
            raise StopIteration
        else:
            x = self.a
            self.a += 2
            return x

@my_decorator
def show_multiples(limit=10):
    for num in TwooMultiples(limit=limit):
        print(num)

show_multiples(limit=6)

#-------------------------------------------task id:l2-004-------------------------------------------
   #-----contextlib.contextmanager(example-1)-----
class MyContextManager:
    def __enter__(self):
        print("Entering context manager")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting context manager")
        return False # False means don't suppress the exception

with MyContextManager() as cm:
    print("Inside the with block")

   #-----contextlib.contextmanager(example-2)-----
class Announcer:
    def __enter__(self):
        print("Starting")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Finishing")

with Announcer():
    print("Doing something in the middle")

   #-----writing __enter__/__exit__ by hand-----
from contextlib import contextmanager

@contextmanager
def Announcer():
    print("Starting")
    yield
    print("Finishing")

with Announcer():
    print("Doing something in the middle")

#-------------------------------------------task id:l2-005-------------------------------------------
   #-----ADVANCED TYPING(TypedDict)-----
from typing import TypedDict
class Movie(TypedDict):
    title: str
    year: int
    rating: float

def print_movie(movie: Movie) -> None:
    print(f"{movie['title']} by {movie['year']} rating: {movie['rating']}")

m: Movie = {"title" : "Inception", "year" : 1999, "rating" : 8.5}
print_movie(m)


class Student(TypedDict):
    name: str
    age: int
    gpa: float

def print_student(student: Student) -> None:
    print(f"my name is {student['name']} my age is {student['age']} my gpa is {student['gpa']}")

s: Student = {"name" : "Ahmed", "age" : 19, "gpa" : 3.5}
print_student(s)

  #-----ADVANCED TYPING(Protocol)-----
from typing import Protocol
class Speaker(Protocol):
    def speak(self) -> str: ...

class Person:
    def speak(self) -> str:
        return "Hello!"

class Robot:
    def speak(self) -> str:
        return "beep boop"

def make_speak(speaker: Speaker) -> None:
    print(speaker.speak())

make_speak(Person())
make_speak(Robot())

  #-----ADVANCED TYPING(Generics -> TypeVar())-----
from typing import TypeVar
T = TypeVar("T")

def last_item(item: list[T]) -> T:
    return item[-1]

def get_second(items: list[T]) -> T:
    return items[1]

print(last_item([10, 20, 30, 40]))
print(last_item(["apple", "banana", "orange"]))
print(get_second([5, 10, 15]))
print(get_second(["A", "B", "C"]))

  #-----ADVANCED TYPING(@overload)-----
from typing import overload

@overload
def convert_value(value: int) -> str: ...

@overload
def convert_value(value: str) -> int: ...

def convert_value(value):
    if isinstance(value, int):
        return str(value)
    else:
        return int(value)

a = convert_value(100)
b = convert_value("123")

print(a)
print(type(a))

print(b)
print(type(b))

  #-----ADVANCED TYPING(mypy/pyright)-----
#pip install mypy         #---->This scans your file and reports type mismatches
#mypy your_file.py        #---->This scans your file and reports type mismatches

#-------------------------------------------task id:l2-006-------------------------------------------
   #-----PLAIN CLASSES (what we know alr)-----
class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"Person(name={self.name}, age={self.age})"

    def __eq__(self, other):
        return self.name == other.name and self.age == other.age

person1 = Person("Ahmed", 19)
print(person1)

   #-----dataclass(auto-generates the boilerplate)-----
from dataclasses import dataclass

@dataclass #@dataclass does for you automatically: generates __init__, __repr__, and __eq__ based on the type-annotated fields
class Person:
    name: str
    age: int

person1 = Person("Ahmed", 19)
print(person1)  #Person(name = 'Ahmed', age = 19)
person2 = Person("Lokesh", 20)
print(person2)

@dataclass
class Contact:
    name: str
    age: int
    email: str

contact1 = Contact("Ahmed", 19, "ahmedlateef.pro@gmail.com")
print(contact1)

  #-----Pydantic(Validate Data Models)-----
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    pages: int


#b1 = Book(title="Dune", author="Frank Herbert", pages=412)
#print(b1)

#b2 = Book(title="Dune", author="Frank Herbert", pages="four hundred")  ----> ERROR values doesnt match

#-------------------------------------------task id:l2-007-------------------------------------------
   #-----FUNCTIONAL PATTERNS(map())-----

   #---w/o map() func---
numbers = [1,2,3,4]
squared = [x ** 2 for x in numbers]
print(squared)

   #---with map() func---
temp_c = [0,20,37,100]
fah = list(map(lambda x: x * 9/5 + 32, temp_c)) # --> lambda denoted as square using map lazy iterator already implemented and list function to see the output
print(fah)

   #-----FUNCTIONAL PATTERNS(filter())-----
animals = ["cat", "elephant", "dog", "giraffe"]
new_animals = list(filter(lambda x: len(x) > 4, animals)) # --> keep only items matching a condition
print(new_animals)

   #-----ITERTOOLS-----
import itertools

# count() - infinite counter (be careful, needs a break/limit)
counter = itertools.count(start=1, step=2)
print(next(counter))  # 1
print(next(counter))  # 3
print(next(counter))  # 5

# chain() - combine multiple iterables into one
combined = list(itertools.chain([1, 2], [3, 4], [5]))
print(combined)   # [1, 2, 3, 4, 5]

# combinations() - all possible groupings of a given size
combos = list(itertools.combinations([1, 2, 3], 2))
print(combos)   # [(1, 2), (1, 3), (2, 3)]

   #-----functools.lru_cache-----
from functools import lru_cache
import time

@lru_cache(maxsize=4)

def slow_cube(n):
    print("Calculating...")
    time.sleep(2)
    return n**3

print(slow_cube(3))
print(slow_cube(3))
print(slow_cube(5))
print(slow_cube(5))

   #-----functools.partial-----
from functools import partial

def multiply(a, b):
    return a * b

double = partial(multiply, 2)
triple = partial(multiply, 3)

print(double(5))
print(double(10))

print(triple(5))
print(triple(10))

#-------------------------------------------task id:l2-008------------------------------------------
   #-----Exception hierarchies-----
class BankError(Exception): # --> parent of all your custom errors.
    pass

class AccountError(BankError):
    pass

class InsufficientFundsError(AccountError):
    pass

class SecurityError(BankError):
    pass

class WrongPinError(SecurityError):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError("Not enough funds")
    else:
        return balance - amount

def login(pin):
    if pin == "1234":
        return "Login Successful"
    else:
        raise WrongPinError("Incorrect PIN")

try:
    withdraw(100,200)
except InsufficientFundsError as e:
    print(e)

try:
    login("9999")
except SecurityError as e:
    print(e)

   #-----Retries — automatically trying again after a failure-----
import time
def download_file(attempt_number):
    if attempt_number < 4:
        raise ConnectionError("Download Failed")
    else:
        return "Download Successful"

def download_with_retry(max_attempts = 5, delay = 1):

    for attempt in range(1, max_attempts + 1):

        try:
            result = download_file(attempt)
            print(f"Successful download of {attempt} attempts")
            return result
        except ConnectionError as e:
            print(f"Attempt {attempt} failed: Download failed")
            if attempt == max_attempts:
                raise
            time.sleep(delay)

download_with_retry()

   #-----Graceful degradation-----
def get_weather(city):
    try:
        return fetch_weather_api(city)
    except ConnectionError:
        print("Using cached weather data")
        return {
    "temperature": "Unknown",
    "condition": "Not available"
}

def fetch_weather_api(city):
    if city == "Dubai":
        return {
    "temperature": 35,
    "condition": "Sunny"
}
    else:
         raise ConnectionError("Weather service unavailable")

print(get_weather("Dubai"))
print(get_weather("London"))

#-------------------------------------------task id:l2-009------------------------------------------
  #-----LOGGING MODULE-----
import logging
logging.basicConfig(level=logging.DEBUG)  # --> level=logging.INFO, only INFO, WARNING, EROOR and CRITICAL would show

logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")

#-----LOGGER-----
logging.basicConfig(level=logging.DEBUG, force = True)
logger = logging.getLogger(__name__)

logger.debug("No Bugs As Of Now To Debug")

#-----FORMATTERS controlling what each log line looks like-----

logging.basicConfig(                                                 # -->  %(asctime)s — timestamp
    level=logging.DEBUG,                                             # -->  %(name)s — the logger's name (from __name__)
    force = True,                                                    # -->  %(levelname)s — DEBUG/INFO/WARNING/etc.
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"    # -->  %(message)s — your actual message text
)

logger = logging.getLogger(__name__)
logger.info("Server started")

#-----HANDLERS(A handler decides where a log message goes — console, a file, or both at once.)-----
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# handler 1: print to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO,)

# handler 2: write to a file
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug("This only goes to the file, not the console")
logger.info("This goes to both the file AND the console")

#-------------------------------------------task id:l2-010------------------------------------------
  #-----Fixtures-----            --> to visually view the test run this command in terminal pytest TASKS/L2\ INTERMIDATE/KNOWLEDGE_L2/knowledge_l2.py
import pytest

@pytest.fixture
def sample_product():
    return {
    "id": 101,
    "name": "Laptop",
    "price": 3500,
    "in_stock": True
}

def test_product_in_stock(sample_product):
    assert sample_product["in_stock"] == True

def test_product_name(sample_product):
    assert sample_product["name"] == "Laptop"

def test_product_price(sample_product):
    assert sample_product["price"] == 3500

   #-----MOCKING(faking outside world)-----
from unittest.mock import patch

def payment_api(amount):
    raise ConnectionError("Payment server down")

def make_payment(amount):
    result = payment_api(amount)
    return result["status"]

@patch("knowledge_l2.payment_api")
def test_make_payment(mock_payment):

    mock_payment.return_value = {
    "status": "success",
    "transaction_id": "TX123"
}
    result = make_payment(100)
    assert result == "success"
    mock_payment.assert_called_once_with(100)

#-----PARAMETERIZED TESTS-----
import pytest

def multiply(a,b):
    return a*b

@pytest.mark.parametrize("a,b,expected", [

    (2,3,6),
    (5,0,0),
    (-2,4,-8),
    (-3,-3,9),
    (10,10,100)
])

def test_multiply(a,b,expected):
    assert multiply(a,b) == expected

#-----TEST COVERAGE (how much of your code is tested)-----
def withdraw(balance, amount):

    if amount > balance:
        raise ValueError("Not enough funds")
    else:
        return balance - amount

import pytest

def test_withdraw_1():  # --> test 1 a successful withdrawal
    assert withdraw(1000,250) == 750

def test_withdraw_2():  # --> test 2 unsuccessful withdrawal
    with pytest.raises(ValueError):
        withdraw(100,200)

#-------------------------------------------task id:l2-011------------------------------------------
# ---> this task is in packaging folder.

#-------------------------------------------task id:l2-012------------------------------------------

  #-----singleton(design pattern)-----
class Singleton:
    _instance = None   # --> _instance the object is initially assigned as none

    def __new__(cls, *args, **kwargs):  # --> checking the object conditions

        if cls._instance is None:
            cls._instance = super().__new__(cls)  # --> if none create a object and super it to __new__

        return cls._instance

class Logger(Singleton):

    def __init__(self):

        if not hasattr(self, "initialized"):  # --> __init__ gaurd gaurentees that the object is only created once

            self.logs = []
            self.initialized = True

    def add_log(self, message):
        self.logs.append(message)

logger1 = Logger()  # --> object 1
logger2 = Logger()  # --> object 1 both are the same objects
logger1.add_log("Program Started")
logger1.add_log("User Logged In")

print(logger2.logs)
print(logger1 is logger2)

   #-----FACTORY-----
from abc import ABC, abstractmethod   # --> Abstract Base Class

class Animal(ABC):
    @abstractmethod    # --> the base class is Animal
    def speak(self) -> str:
        pass

class Dog(Animal):   # --> object 1
    def speak(self) -> str:
        return "Woof!"

class Cat(Animal):   # --> object 2
    def speak(self) -> str:
        return "Meow!"

def animal_factory(animal_type) -> Animal:  # --> checking object conditions to return speak
    animal_type = animal_type.lower()
    if animal_type == "dog":
        return Dog()

    elif animal_type == "cat":
        return Cat()

    raise ValueError("Unknown animal type")   # --> if animal_type doesnt match raise valueerror

animal1 = animal_factory("dog")
animal2 = animal_factory("cat")

print(animal1.speak())
print(animal2.speak())

#-----STRATEGY-----
class PaymentStrategy(ABC):
    @abstractmethod
    def pay (self, amount: float) -> float:
        pass

class CreditCardPayment(PaymentStrategy):

    def pay (self, amount: float) -> str:
        return f"Paid {amount} using credit card"  # --> behaviour 1

class PayPalPayment(PaymentStrategy):
    def pay (self, amount: float) -> str:
        return f"Paid {amount} using PayPal"       # --> behaviour 2

class Checkout:
    def __init__(self, amount: float, payment: PaymentStrategy):
        self.amount = amount
        self.payment = payment

    def complete_payment(self):
        return self.payment.pay(self.amount)  # --> chooses what behaviour to use

checkout1 = Checkout(100, CreditCardPayment())
checkout2 = Checkout(250, PayPalPayment())

print(checkout1.complete_payment())
print(checkout2.complete_payment())

#-----OBSERVER-----
class NewsChannel:         # --> Subject class

    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish_news(self, news):

        print(f"Breaking News: {news}")

        for subscriber in self.subscribers:
            subscriber.update(news)

class MobileSubscriber:   # --> Observer 1 class

    def update(self, news):
        print(f"[MOBILE] Received: {news}")

class EmailSubscriber:   # --> Observer 2 class
    def update(self, news):
        print(f"[EMAIL] Received: {news}")

class SMSSubscriber:    # --> Observer 3 class
    def update(self, news):
        print(f"[SMS] Received: {news}")

channel = NewsChannel()

channel.subscribe(MobileSubscriber())
channel.subscribe(EmailSubscriber())
channel.subscribe(SMSSubscriber())

channel.publish_news("Someone Died")

#-----BUILDER-----
class Computer:

    def __init__(self):
        self.cpu = None
        self.ram = None
        self.storage = None
        self.gpu = None

    def __repr__(self):
        return f"Computer: cpu = {self.cpu}, ram = {self.ram}, storage = {self.storage}, gpu = {self.gpu}"

class ComputerBuilder:

    def __init__(self):
        self.computer = Computer()

    def set_cpu(self, cpu):
        self.computer.cpu = cpu
        return self

    def set_ram(self, ram):
        self.computer.ram = ram
        return self

    def set_storage(self, storage):
        self.computer.storage = storage
        return self

    def set_gpu(self, gpu):
        self.computer.gpu = gpu
        return self

    def build(self) -> Computer:

        if self.computer.cpu is None:
            raise ValueError("CPU is required")

        if self.computer.ram is None:
            raise ValueError("RAM is required")

        return self.computer

computer = (
    ComputerBuilder()
    .set_cpu("Intel i7")
    .set_ram("16GB")
    .set_storage("1TB SSD")
    .set_gpu("RTX 4060")
    .build()
)
print(computer)