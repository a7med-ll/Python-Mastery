from functools import wraps


def lru_cache(max_size=3):

    def decorator(func):
        cache = {}
        usage = []

        @wraps(func)
        def wrapper(*args, **kwargs):

            # create a unique key from arguments
            key = (args, tuple(sorted(kwargs.items())))

            # return cached value if exists
            if key in cache:
                print("Returning from cache")

                # update usage order
                usage.remove(key)
                usage.append(key)

                return cache[key]

            # execute original function
            result = func(*args, **kwargs)

            # store result
            cache[key] = result
            usage.append(key)

            # remove least recently used item
            if len(cache) > max_size:
                old_key = usage.pop(0)
                del cache[old_key]
                print("Removed:", old_key)

            return result

        return wrapper

    return decorator


@lru_cache(max_size=3)
def add(a, b):
    print("Calculating...")
    return a + b


def main():

    print(add(2, 3))  # calculates
    print(add(2, 3))  # cache

    print(add(5, 5))  # calculates
    print(add(10, 10))  # calculates

    print(add(1, 1))  # removes oldest cache

    print(add(2, 3))  # calculates again because it was removed


if __name__ == "__main__":
    main()