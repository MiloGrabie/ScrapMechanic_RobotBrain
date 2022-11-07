s = "LVIII"

number = 0
i = 0
while i < len(s):
    char = s[i]
    if char == 'I' and i < len(s) and s[i+1] == 'X':
        number += 9
        i += 1
    if char == 'I' and i < len(s) and s[i+1] == 'V':
        number += 4
        i += 1
    elif char == 'V': number += 5
    elif char == 'X': number += 10
    elif char == 'I': number += 1
    elif char == 'I': number += 1
    i += 1

print(number)
