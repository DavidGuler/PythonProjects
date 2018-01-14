"""
Name: print_pascal.py
Author: David Guler
Purpose: Print the Pascal Triangle with only one line of code.

Activity Log:
    #1 - 09/04/2017, Created
    #2 - 16/04/2017, 
        #1.1 - Created the function "create pascal_line"
        #1.2 - Finished
"""

def create_pascal_line(pre_line):
    """
    """

    pre_line = [0] + pre_line + [0]
    zipped_line = list(zip(pre_line[:-1], pre_line[1:]))
    line = list(map(lambda t: t[0] + t[1], zipped_line))
    return list(line)

lines = 10

line = [1]
for line_index in range(1,lines):
    print(line)
    line = create_pascal_line(line)
print(line)
