class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'point({self.x}, {self.y})'


p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(5, 5)

# __eq__ test
print(p1 == p2)  # True - same x, y
print(p1 == p3)  # False - different x, y

# __hash__ test
print(hash(p1) == hash(p2))  # True - equal objects must have equal hashes

# Using them in a set (this is what breaks WITHOUT __hash__)
points = {p1, p2, p3}
print(len(points))  # 2, not 3 - p1 and p2 are treated as the same item

for point in points:
    print(point)
