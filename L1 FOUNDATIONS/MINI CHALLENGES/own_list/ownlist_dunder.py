#----DUNDER METHODS----

#---__init__----
class MyList:
    def __init__(self):
        self.items = []

# Append Method
    def append(self, item):
        self.items.append(item)

# Pop Method
    def pop(self):
        if len(self.items) == 0:
            return None
        else:
            return self.items.pop()

#---__len__---
    def __len__(self):
        return len(self.items)

#---__getitem__---
    def __getitem__(self, index):
        return self.items[index]

#---__iter__---
    def __iter__(self):
        return iter(self.items)

#---output---
ml = MyList()
ml.append(10)
ml.append(20)
ml.append(30)

print(len(ml))
print(ml[0])
print(ml[2])

for value in ml:
    print(value)       # 10, 20, 30 on separate lines

print(ml.pop())
print(len(ml))
