from collections import Counter, defaultdict, OrderedDict

li = [1, 2, 3, 4, 5, 6, 7, 7]

print(Counter("test"))

test = defaultdict(lambda: None, {"a": 1, "b": 2})

print(test["c"])

d = {"v": 1, "z": 2}

d["a"] = 1
d["b"] = 2
d["c"] = 3


d2 = {"v": 1, "z": 2}

d2["b"] = 2
d2["a"] = 1
d2["c"] = 3


# print(d == d2)

from time import time as time2
import pdb
from datetime import time, date

from array import array

# print(time(15, 40, 22))


print(date.today())
pdb.set_trace()

print(time2())

arr = array("i", [1, 2, 3])

print(arr[0])


my_file = open("/home/sergway/AlgoCasts/README.md")
file_content = my_file.read()
index = my_file.seek(0)

print(my_file.read())

my_file.seek(0)

print(my_file.readline())
print(my_file.readline())
my_file.seek(0)

print(my_file.readlines())

my_file.close()


# to avoid closing stuff you can use with


with open("/home/sergway/AlgoCasts/README.md") as file_content:
    print(file_content.readlines())

add pathlib to support linux and win


text = file_content.write("hey its me!")


print(my_file.read())
print(my_file.read())


try:
    with open("./tedst.md", mode="r+") as file_content:
        print(file_content.readlines())
except FileNotFoundError as err:
    print(f"not found, {err}")
    raise err
except IOError as err:
    print(f"IO error, {err}")
    raise err
