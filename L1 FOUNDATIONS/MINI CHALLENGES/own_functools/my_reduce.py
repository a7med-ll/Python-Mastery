#----FUNCTOOLS(REDUCE)----

def my_reduce(func,items):
    result = items[0]

    for item in items[1:]:
        result = func(result,item)
    return result
