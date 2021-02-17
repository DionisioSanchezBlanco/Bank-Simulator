# Luhn algorithm

string = "4000008449433403"
# Drop the last digit
step_1 = string[:len(string) - 1]
print(step_1)
# Multiply odd digits by 2. Take into account the list start with 0, so you will get even indexes
step_2 = [int(num) * 2 if i == 0 or i % 2 == 0 else int(num) for i, num in enumerate(step_1)]
print(step_2)
# Substract 9 to numbers over 9
step_3 = [int(num) - 9 if num > 9 else num for num in step_2]
print(step_3)
# Add all numbers
step_3.append(int(string[len(string) - 1]))
print(step_3)

# Sum the numbers and check the mod
if sum(step_3) % 10 == 0:
    return True
else
    return False