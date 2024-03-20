
# # # dictionary = {
# # #   123: [1,2,3],
# # #   True: 'test',
# # #   'test': 'test',
# # #   'age': 54
# # # }

# # # print(dictionary.get('age', 55))
# # # # print(dictionary.get('age'))

# # # # usr2 = dict(name='test')

# # # # print(usr2)

# # # # keys check
# # # print(True in dictionary.keys()) 
# # # print('age' in dictionary) 
# # # # values check
# # # print('test' in dictionary.values()) 
# # # # tuples
# # # print(dictionary.items())

# # # dictionary2 = dictionary.copy()

# # # dictionary.clear()

# # # print(dictionary)


# # # dictionary2.pop(123) # remove key

# # # dictionary2['testtttttt'] = 'test'
# # # dictionary2.popitem() # removed last inserted key
# # # dictionary.update({'age': 55})
# # # print(dictionary2)

# # some_tuple = (1,2,3,4,5, 2)
# # # # print(list(some_tuple))
# # # print(some_tuple[1:2])
# # # # print(dictionary)

# # # firstNum, secondNum, *rest = some_tuple

# # # print(firstNum)
# # # print(secondNum)
# # # print(rest)

# # print(some_tuple.count(2))
# # print(some_tuple.index(2))

# is_old = False
# is_licensed = False

# if is_old and is_licensed:
#     print('happen')
# elif is_licensed:
#     print('test')
# else:
#     print('not happens')

# can_message = "message allowed" if is_licensed else "not allowed"
# print(can_message)

is_magician = True
is_expert = False

if is_magician and is_expert:
  print("you are a master magician")
elif is_magician:
    print("at least you're getting there")
else:
   print("You need magic powers")
