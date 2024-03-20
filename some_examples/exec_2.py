# import re

# pattern = re.compile(r"([a-zA-Z]).([a])")
# SENTENCE = "search inside of this text please!"


# is_this_present = pattern.search(SENTENCE)

# b = pattern.findall(string=SENTENCE)

# print(b)

# print(is_this_present)

# if is_this_present:
#     print(is_this_present.group())
#     print(is_this_present.span())

import re


email_pattern = re.compile(r"(^[\w_.+-]+@[\w-]+[\w.-]+$)")
password_pattern = re.compile(r"^[\w$%#@]{7,}\d$")

email = email_pattern.search("test@test.com")
password = password_pattern.fullmatch("teaaaaaa42")
print(email)

print(password)

# check for password 8 char long, letter numbers $%#@, and must end with num
