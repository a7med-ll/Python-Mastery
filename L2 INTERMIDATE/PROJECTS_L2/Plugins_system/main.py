import plugins
from register import run_plugin

def main():

    greet_result = run_plugin("greet", "Ahmed")
    multiply_result = run_plugin("multiply",5,5)

    print(greet_result)
    print(multiply_result)

    try:
        result = run_plugin("missing_plugin")

    except KeyError as error:
        print(error)

if __name__ == "__main__":
    main()