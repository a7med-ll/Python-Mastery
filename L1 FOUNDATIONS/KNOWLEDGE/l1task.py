# task id: l1-001
   
#---- DATA STRUCTURES ----

   #--List--

l1 = [1,2,3,4,5]

l2 = [

    [1,2,3,4],
    [5,6,7,8],
    [9,10,12,12]
]

   #--Dictionaries--

d1 = {"one":1 ,"two":2, "three":3}

d1 = {

    "one":1,
    "two":2,
    "three":3
}

   #--tuples--

t1 = (1,2,3,4,5)

t2 = (

    (1,2,3,4),
    (5,6,7,8),
    (9,10,11,12)
)

   #--Sets--

s1 = {"Ahmed","Faisal","Lokesh"}

#---- FUNCTIONS ----

def greet():
    return "Hello"

#---- OOP ----

class person:
    def __init__(self,name,lastname):
        self.name = name
        self.lastname = lastname
p1 = ("Ahmed","Lateef")

#---- ERROR HANDLING ----

try:
    print('x')
except:
    print("No Vairable Named X")


#Task id: l1 - 003

#--mutable datatype--
   #--list--

l1 =[1,2,3]
l1.append(4)

#--immutable data types--
   #--tuples--

t1 = (0,1,2,3,4)
t1[0] = 1 # error

#--Refrence--
def list(list1):
    return list1

list2 = ["X"]
list(list2)

#--values--
# a copy of the vairable is passed changes inside the function doesnt affect the orginal
def fun(lst):
    return lst
lst1 = ["x"]
fun(lst1)

#----DEEP COPY----
# a deep copy creates a new compound object and copies it in a recursive manner and any changes made to copied object will not affect the orginal 
import copy
l1 = [[1,2,3],[4,5,6]]
l2 = copy.deepcopy(l1)
l2[0][0] = 99
print("the modifed list is:" ,l2)
print("the orginal list is:" ,l1)

#----SHALLOW COPY----
import copy
l1 = [[1,2,3],[4,5,6]]
l2 = copy.copy(l1)
l2[0][0] = 99
print("the modifed list is:" ,l2)
print("the orginal list is:" ,l1) # orginal list also changes.

#task id: l1-006

#---NAMESPACES(GLOABL , LOCAL VAIRABLES)---
  #--Global--
  # To acess a global vairable inside a function use global vairable_name
score = 10
def show_score():
    print(score)
show_score()

  #--Local--
name = "Ahmed"
def greet():
    message = "Hello"

greet()

#---SCOPES---
#A scope is the region of a program where a name can be accessed.

#task id: l1-007

#---OOP(CLASS)---
class info:
    pass
person1 = info()
person2 = info()

#---__init__(THE CONSTRUCTOR)---
class info:
    def __init__(self,name,lastname,age):
        self.name = name
        self.lastname = lastname
        self.age = age

person1 = info("Ahmed","Lateef",19)

  #---inheritance---
  #super().__init__(...) calls the parent class's __init__, so you don't have to retype self.title = title, etc. It saves duplication and keeps things in sync if the parent changes.
class updated_info(info):
    def __init__(self, name, lastname, age, email):
        super().__init__(name, lastname, age)
        self.email = email

updated_person1 = updated_info("Ahmed","Lateef",19,"ahmedlateef.pro@gmail.com")

#---composition---
# Company HAS a person (info), not IS a person

class Company:
    def __init__(self, company_name, employee):
        self.company_name = company_name
        self.employee = employee   # holds an info object


company1 = Company("firstfintech", person1)

print(company1.company_name)      # firstfintech
print(company1.employee.name)     # Ahmed

#---DUNDER METHODS(double underscope methods)---
class info:
    def __init__(self, name, lastname, age):
        self.name = name
        self.lastname = lastname
        self.age = age

    def __str__(self): #Meant for humans.
        return f"{self.name} {self.lastname}, age {self.age}"
    
    def __repr__(self): #Meant for developers — should ideally let you recreate the object.
        return f"info({self.name!r}, {self.lastname!r}, {self.age})"

    def __eq__(self, other): # checks if they're the same object in memory, not whether their data matches.
        return self.name == other.name and self.lastname == other.lastname
    
    def __len__(self): # returns the length of age
        return self.age


person1 = info("Ahmed", "Lateef", 19)
person2 = info("Ahmed", "Lateef", 25)

#task id: l1-008
#---EXCEPTIONS---

  #--try/except--
try:
    result = 10 / 0 #error codes goes in try block
except ZeroDivisionError:
    print("You can't divide by zero!") #output of error rather than crashing

print("Program keeps running")

  #--ELSE--
try:
    num = int("42")
except ValueError:
    print("Invalid number")
else:
    print("Conversion succeeded:", num)   # only runs if try succeeded

  #--finally--
try:
    num = int("42")
    result = 100 / num
except ValueError:
    print("Invalid number")
except ZeroDivisionError:
    print("Can't divide by zero")
else:
    print("Result:", result)
finally:
    print("Done trying")

#task id: l1-009
#---MODULES--- any .py file is a module---
# math_utils.py
def add(a, b):
    return a + b
                     #-------> if we have this sperate .py file we can use it as a module in a n exsisting file
def subtract(a, b):
    return a - b
# main.py
#import math_utils
                     #-------> EXAMPLE
#print(math_utils.add(2, 3))   # 5

#--- if __name__ == "__main__" ---
def add(a, b):
    return a + b

print("This runs every time the file is loaded")

if __name__ == "__main__":
    print("This only runs when math_utils.py is executed directly")
    print(add(2, 3))

#task id: l1-010
#----FILE I/O, CONTEXT MANAGERS-----

   #---basic file reading with out "WITH"---
f = open("notes.txt" , "r")
lines = f.readlines() #-----> stores each diffrent lines in a list that is named as lines
f.close() #-------> closing required

   #---file reading/writing with "WITH" method---
with open("notes.txt","w") as f:
    f.write("Hello File!")   #--------> no closing the file required because uses dunder method __enter__ and __exit__ in specifc blocks

#----os.path(oldway)----
import os
path = os.path.join("Data","notes.txt") #---> data folder name, notes.txt file name
print(os.path.exists(path)) #---> if the file exsist or no
print(os.path.basename(path)) #---> file name that is notes.txt
print(os.path.dirname(path)) #---> folder name that is Data

#----pathlib(new way treats path as objects)----
from pathlib import path
path = path("Data") / "notes.txt" #---> operator to join folder and file
path.exists() #---> does it exsit ?
path.name #---> path name
path.parent #---> path("data")
path.suffix #---> .txt

#---pathlib can skip open() entirely---

  #---with os.path---
import os
path = os.path.join("data", "notes.txt")
if os.path.exists(path):
    with open(path, "r") as f:
        content = f.read()

  #--WITH PATHLIB--
from pathlib import Path
path = Path("data") / "notes.txt"
if path.exists():
    content = path.read_text()

#task id: l1-012 
#----TYPE HINTS----
def greet(name: str) -> str: #---> name:str name to be taken string value, ->str output should be in strings
    return "Hello" + name

#---COLLECTIONS---
def getnames() -> list[str]:
    return ["Ahmed","Lokesh"]

def get_ages() -> dict[str,int]:  #--> dict key will be string and value will be int
    return {"Ahmed" : 19, "Lokesh" : 21}

#---OPTIONAL this or None---
from typing import Optional
def find_usr(usr_id: int) -> Optional[str]:
    if usr_id == 1:
        return "Ahmed"
    return None

#---UNION---
def get_email(user_id: int) -> Optional[str]:
    users = {1: "ahmed@gmail.com"}
    return users.get(user_id)   # returns None if key doesn't exist

#--list[int]--
def total(numbers: list[int]) -> int:
    return sum(numbers)

total([1, 2, 3])        #--->  matches the hint
total([1, "two", 3])    #--->  breaks the promise (but Python still runs it)
