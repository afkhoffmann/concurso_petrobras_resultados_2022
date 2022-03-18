import re


x = '1235.5.23.7 123.6.3 123.5.321.5 asd32a asd .s 6a3d. a6'

# find all occurences of numbers dot numbers
# findall returns a list of all matches
y = re.finditer(r'\d{2,3}(\.\d{1,3}){2,3}', x)

# convert y to a list of strings
y = [i.group() for i in y]
print(y)