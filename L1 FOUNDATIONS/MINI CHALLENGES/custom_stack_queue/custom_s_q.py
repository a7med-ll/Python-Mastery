class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.isEmpty():
            return None
        else:
            return self.items.pop()

    def peek(self):
        if self.isEmpty():
            return None
        else:
            return self.items[-1]

    def isEmpty(self):
        return len(self.items) == 0

s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(s.pop())    # 3
print(s.peek())   # 2
print(s.pop())    # 2
print(s.isEmpty()) # False, one item left

s.pop()
print(s.pop())    # should print None

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.isEmpty():
            return None
        else:
            return self.items.pop(0)

    def isEmpty(self):
        return len(self.items) == 0

q = Queue()
q.enqueue("Ahmed")
q.enqueue("Sara")
q.enqueue("Lokesh")

print(q.dequeue())   # "Ahmed"
print(q.dequeue())   # "Sara"
print(q.dequeue())   # "Lokesh"
print(q.isEmpty())    # True
print(q.dequeue())    # None, no crash