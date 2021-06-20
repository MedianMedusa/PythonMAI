import time
from datetime import datetime
from random import random
from time import sleep


###############
def calc_duration(func):
    def wrapper(*args, **kwargs):
        curr = time.time()
        func()
        print("elapsed time is about {0} seconds".format(time.time() - curr))

    return wrapper


@calc_duration
def long_executing_task():  # func(*args, **kwargs) ==== long_executing_task
    for index in range(3):
        print('Iteration {index}'.format(index=index))
        sleep(random())


#############
def suppress_errors(errors):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors:
                print("Some exceptions raised)) lol")

        return wrapped

    return wrapper


@suppress_errors((
        KeyError,
        ValueError,
))
def potentially_unsafe_func(key: str):
    print(f'Get data by the key {key}')
    data = {'name': 'test', 'age': 30}
    return data[key]


#########
def result_between(value_min, value_max):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            res = func(*args, **kwargs)
            if res < value_min or res > value_max:
                raise ValueError("Ну чёт ниоч.")
            return res

        return wrapped

    return wrapper


def len_more_than(s_len):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            if len(*args) < s_len:
                raise ValueError("Маловато")
            return func(*args, **kwargs)

        return wrapped

    return wrapper


@result_between(0, 10)
def sum_of_values(numbers):
    return sum(numbers)


@len_more_than(10)
def show_message(message: str) -> str:
    return f'Hi, you sent: {message}'


####################
def replace_commas(func):
    def wrapper(*args, **kwargs):
        text = str(*args).replace(',', ' ')
        return func(text)

    return wrapper


def words_title(func):
    def wrapper(*args, **kwargs):
        text = str(*args).split(' ')
        i = 0
        for word in text:
            newWord = word[0].capitalize() + word[1:-1] + word[-1].capitalize()
            text[i] = newWord
            i += 1
        return func(' '.join(text))
    return wrapper


@words_title
@replace_commas
def process_text(text: str) -> str:
    return text.replace(':', ',')


@replace_commas
@words_title
def another_process(text: str) -> str:
    return text.replace(':', ',')



if __name__ == '__main__':
    # long_executing_task()  # print "elapsed time is about <> seconds"
    # print(potentially_unsafe_func('name'))  # everything is ok
    print(potentially_unsafe_func('last_name'))  # error is silented
    # print(sum_of_values((1, 3, 5, 7)))  # ValueError
    # print(show_message('Howdy, howdy my little friend'))  # не ValueError
    # show_message('Howdy')  # ValueError

    print(process_text('the French revolution resulted in 3 concepts: freedom,equality,fraternity'))
    print(another_process('the French revolution resulted in 3 concepts: freedom,equality,fraternity'))
