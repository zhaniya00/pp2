import re
#exercise1
def match_a_zero_or_more_b(s):
    if re.fullmatch(r'ab*', s):
        return True
    return False

#exercise2
def match_a_two_to_three_b(s):
    if re.fullmatch(r'ab{2,3}', s):
        return True
    return False

#exercise3
def find_lowercase_underscore(s):
    return re.findall(r'[a-z]+_[a-z]+', s) 

#exercise4
def find_capital_followed_by_lower(s):
    return re.findall(r'[A-Z][a-z]+', s)

#exercise5
def match_a_anything_b(s):
    if re.fullmatch(r'a.*b', s):
        return True
    return False

#exercise6
def replace_space_comma_dot(s):
    return re.sub(r'[ ,.]', ':', s)

#exercise7
def snake_to_camel(s):
    return re.sub(r'_(\w)', lambda x: x.group(1).upper(), s)

#exercise8
def split_by_uppercase(s):
    return re.split(r'(?=[A-Z])', s)

#exercise9
def insert_space_before_uppercase(s):
    return re.sub(r'([A-Z])', r' \1', s).strip()

#exercise10
def camel_to_snake(s):
    return re.sub(r'([A-Z])', r'_\1', s).lower()