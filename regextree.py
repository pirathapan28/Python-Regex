"""
# Copyright Nick Cheng, Brian Harrington, Danny Heap, Pirathapan Nagendrajah
# 2013, 2014, 2015, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2016
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from regextree import RegexTree, StarTree, DotTree, BarTree, Leaf

# Do not change anything above this comment except for the copyright
# statement

# Student code below this comment.

# Global Variable
ZERO = '0'
ONE = '1'
TWO = '2'
E = 'e'
STAR = '*'
OB = '('   # OB - Open Bracket
CB = ')'   # CD - Close Bracket
DOT = '.'
BAR = '|'


def is_regex(s):
    '''(str) -> bool
    Takes a string s, and returns True if it is a regular expression
    or else it will return False
    >>>is_regex('10')
    False
    >>>is_regex('isRegex')
    False
    >>>is_regex('e*')
    True
    >>>is_regex('(0|2)')
    True
    >>>is_regex('((0.(e|0)*).1)')
    True
    >>>is_regex('3|0')
    False
    '''
    # Base Case, if s is empty
    if s == '':
        return False
    # Check if s has '0', '1', '2', or 'e'
    if len(s) == 1:
        if (s == ZERO or s == ONE or s == TWO or s == E):
            return True
        return False
    # Checks if the * is at the end
    elif s[-1] == STAR:
        return is_regex(s[:-1])
    # checks if the regax's has brackets at the begininng and end
    elif s[0] == OB and s[-1] == CB:
        locator = operationLocator(s)
        if locator == 0:
            return False
        # recurse by splitting them and returns True if they are both True
        return is_regex(s[1:locator]) and is_regex(s[locator + 1:len(s) - 1])
    else:
        return False


def bracket(s, counter=0):
    '''(str) -> int
    HELPER FUNCTION
    Finds the closing bracket index to the respective opening bracket
    REQ: first element has to be '('
    >>>bracket('(e|1*)')
    5
    >>>bracket('((1.e).(e*|0))')
    13
    >>>bracket('(((1|0).(2.0)))')
    14
    '''
    # If empty return 0
    if len(s) == 0:
        return 0
    # If the first element is a open bracket then recurses it to find the next
    if s[0] == OB:
        return 1 + bracket(s[1:], counter + 1)
    # If it's not a closing bracket then continue with the recurrsion
    if s[0] != CB:
        return 1 + bracket(s[1:], counter)
    # When the closing bracket is found, return the index of the bracket
    elif s[0] == CB:
        # If the bracket is at the end, return 0
        if counter - 1 == 0:
            return 0
        # return the index when the closing bracket is not at the end
        return 1 + bracket(s[1:], counter - 1)


def operationLocator(s, counter=0, copyLen=0):
    '''(str) -> int
    HELPER FUNCTION
    Returns the location of the operation, the operation consist of dot or bar
    >>>operationLocator('1')
    0
    >>>operationLocator('1.2')
    1
    >>>operationLocator('(1|2)')
    2
    >>>operationLocator('((1*|2)*.e*)')
    8
    '''
    if len(s) == 0:
        return 0
    # Keeping a copy of len(s) to keep track
    if copyLen == 0:
        copyLen = len(s) - 1
    # If the len is equal then we know it's a valid regex expression
    if len(s) == 1:
        return 0
    # If the counter is equal to the len(copyLen) then we know that the counter
    # went thru the expression to find no operation
    if counter == copyLen:
        return 0
    # If theres a bracket in the regex expression, call bracket to find the
    # last bracket
    if s[1] == OB:
        temp = bracket(s[1:])
        # If temp == 0 then this expression is not a regex
        if temp == 0:
            return 0
        counter += temp + 1
        return operationLocator(s[counter:], counter, copyLen)
    # If the next element is not . or | then find the . or |, more recurrsion
    elif s[1] != DOT and s[1] != BAR:
        return operationLocator(s[1:], counter + 1, copyLen)
    # we found the operator now return the index of the operator
    else:
        return counter + 1


def perms(s):
    '''(str) -> set of str
    Takes in a str and returns the permutation of the str in a set of str
    >>>perms('abc')
    {'abc', 'bca', 'bac', 'acb', 'cba', 'cab'}
    >>>perms('ab')
    {'ba', 'ab'}
    >>>perms('abcd')
    {'cadb', 'cbad', 'dacb', 'acbd', 'bdac', 'abdc', 'abcd', 'bdca', 'dcba',
    'adbc', 'cdba', 'cabd', 'dcab', 'acdb', 'cbda', 'bacd', 'dbca', 'bcad',
    'dbac', 'cdab', 'badc', 'bcda', 'dabc', 'adcb'}

    Takes in a regular regex expression and returns the set of all permutations
    of the charcters in s that form valid regular expressions

    '''
    # Base case: if s is 1 character or shorter,
    # it has only one permutation (itself)
    if (len(s) <= 1):
        return set(s)
    # Recursive decomposition: n-1 approach
    # Permutations of s consist of each character in s plus each permutation
    # of s minus that character
    else:
        # New set for storing the permutations
        result = set()
        # For each character in s,
        # find the permutations of s minus that character.
        # Add s to the begining of each permutation, and add to result set
        for i in range(len(s)):
            char = s[i]
            # String of characters in s other than the current char
            s_minus = s[:i] + s[i+1:]
            # Set of permutations of s_minus
            perms_minus = perms(s_minus)
            # Add char to the begining of each permutation of s_minus,
            # and update result set to include these results.
            for p in perms_minus:
                result.update({(char + p)})
        return result


def all_regex_permutations(s):
    '''(str) -> set of str
    Takes in a str and returns all the permuatation of str that is a
    valid regex expression
    >>>all_regex_permutations('(1.0)')
    {'(0.1)', '(1.0)'}
    >>>all_regex_permutations('(1.0*)')
    {'(1*.0)', '(1.0*)', '(0.1)*', '(0.1*)', '(1.0)*', '(0*.1)'}
    >>>all_regex_permutations('(1.0).2*')
    set()
    >>>all_regex_permutations('((1.0).2*)')
    {'((2.0*).1)', '((1.0).2*)', '((1.2*).0)', '(0.(2.1*))', '(0.(2.1))*',
    '(2.(1.0)*)', '(1.(2.0)*)', '((0*.2).1)', '((0*.1).2)', '(0.(1.2*))',
    '((0.1*).2)', '((1.2).0)*', '((2.0).1*)', '((2.1*).0)', '((2.1)*.0)',
    '(2.(0*.1))', '((0.1).2*)', '((2*.0).1)', '(2.(0.1))*', '(1.(0.2*))',
    '((1.2).0*)', '(1.(2.0))*', '((0.1)*.2)', '(1.(2*.0))', '(2.(1.0*))',
    '((1.2)*.0)', '((1.0)*.2)', '(0.(1.2))*', '(1.(2.0*))', '((2*.1).0)',
    '(2.(1.0))*', '((2.1).0*)', '((0.2).1*)', '(2.(1*.0))', '(2.(0.1*))',
    '((2.0)*.1)', '((2.0).1)*', '(0*.(1.2))', '(1.(0.2))*', '((2.1).0)*',
    '(0*.(2.1))', '(2*.(0.1))', '(2*.(1.0))', '(0.(2*.1))', '((0.2*).1)',
    '((1.0).2)*', '((0.2)*.1)', '((1.0*).2)', '(0.(2.1)*)', '(2.(0.1)*)',
    '(1*.(0.2))', '(0.(1*.2))', '(0.(1.2)*)', '((1*.2).0)', '(1.(0*.2))',
    '(1.(0.2)*)', '(1*.(2.0))', '((1*.0).2)', '((0.2).1)*', '((0.1).2)*'}
    >>>all_regex_permutations('(**1.0)')
    {'(0.1*)*', '(1.0*)*', '(0*.1)*', '(0.1**)', '(0*.1*)', '(1.0)**',
    '(1*.0)*', '(0.1)**', '(1*.0*)', '(1**.0)', '(0**.1)', '(1.0**)'}
    >>>all_regex_permutations('**1*')
    {'1***'}
    '''
    # Calling perms Helper Function
    permSet = perms(s)
    regexPerms = set()
    # Using elemental loop, for every element in the permsList
    for element in permSet:
        # Removing invalid regex to make it more efficient
        # removing if star is at the beginning
        # if the closing bracket is in the beginning
        # if the operation is at the beginning
        if (element[0] == STAR or element[0] == CB or element[0] == DOT or
            element[0] == BAR) or (element[-1] == OB or element[-1] == DOT or
                                   element[-1] == BAR):
            pass
        # Case 2 of removing invalid regex
        elif len(element) > 1 and element[1] != STAR and (element[0] == ZERO or
                                                          element[0] == ONE or
                                                          element[0] == TWO or
                                                          element[0] == E):
            pass
        # Case 3 of removing invalid regex
        elif len(element) > 1 and (element[-1] == ZERO or element[-1] == ONE or
                                   element[-1] == TWO or element[-1] == E):
            pass
        # last condition, if the element is regex then add it to the list
        # If the expression is a valid regex, add it to the regexPerms
        elif is_regex(element) == True:
            regexPerms.add(element)

    return regexPerms


def regex_match(r, s):
    '''(RegexTree, str) -> bool
    Takes in a RegexTree and a str and checks if the str maches the regex
    if matches, return true else, return false
    >>>regex_match(build_regex_tree("(0|1*)"), "")
    True
    >>>regex_match(build_regex_tree("(0|1*)"), "1111")
    True
    >>>regex_match(build_regex_tree("(0|1*)"), "0")
    True
    >>>regex_match(build_regex_tree("(0|1*)"), "000")
    False
    >>>regex_match(build_regex_tree("((0|1*).(1.0))"), "010")
    True
    >>>regex_match(build_regex_tree("((0|1*).(1.0))"), "10")
    True
    >>>regex_match(build_regex_tree("((0|1*).(1.0))"), "111110")
    True
    >>>regex_match(build_regex_tree("((0|1*)|((2*.1*).(e*.0)))"), "210")
    True
    '''
    # To check if s is a len of 1 and which means it's a Leaf
    if isinstance(r, Leaf):
        # if the symbol equals to 'e' or '*'
        if r.get_symbol() == E or r.get_symbol() == STAR:
            if s == '':
                return True
            else:
                return False
        # if the symbol is equal to s
        elif r.get_symbol() == s:
            return True
        else:
            return False
    # To check if the tree has a '*'
    elif isinstance(r, StarTree):
        # If the s is empty then its True because '*' can have empty str
        if s == '':
            return True
        # Base case
        elif regex_match(r.get_child(), s):
            return True
        # If the operation is dot, and has star outside the bracket
        elif isinstance(r.get_child(), DotTree):
            # Slicing the string up from every index and sends it through to
            # the left side and right right of the dot operation to check if
            # they are both are present then it returns True
            for i in range(len(s) + 1):
                starValid = regex_match(r.get_child(), s[:i]) and regex_match(
                    r, s[i:])
                if starValid:
                    return True
            return False
        # Slicing the str to see the str has more than 1 repeated str
        else:
            return bool(regex_match(r.get_child(), s[:1]) and
                        regex_match(r, s[1:]))
    # To check if the tree has a '|'
    elif isinstance(r, BarTree):
        # Getting the left side of the bar
        left = regex_match(r.get_left_child(), s)
        # Getting the right side of the bar
        right = regex_match(r.get_right_child(), s)
        # Because bar == or, if left or right is present then it returns True
        return bool(left or right)
    # To check if the tree has a '.'
    elif isinstance(r, DotTree):
        # slicing the string up from every index and sends it through to the
        # left side and right right of the dot operation to check if they are
        # both are present then it returns True
        for i in range(len(s) + 1):
            dotValid = regex_match(r.get_left_child(), s[:i]) and regex_match(
                r.get_right_child(), s[i:])
            # if both the left child and right child are present then it
            # returns true
            if dotValid:
                return True
        return False
    else:
        return False


def build_regex_tree(regex):
    '''(str) -> RegexTree
    REQ: str must be a valid regex
    Takes in a str that is a valid regex and creates a RegexTree for the regex
    and returns the root of it
    >>>build_regex_tree('1*')
    StarTree(Leaf('1'))
    >>>build_regex_tree('(1|0)*')
    StarTree(BarTree(Leaf('1'), Leaf('0')))
    >>>build_regex_tree('(2*.0)')
    DotTree(StarTree(Leaf('2')), Leaf('0'))
    >>>build_regex_tree('e*')
    StarTree(Leaf('e'))
    >>>build_regex_tree('((1.0)|(2.1))')
    BarTree(DotTree(Leaf('1'), Leaf('0')), DotTree(Leaf('2'), Leaf('1')))
    >>>build_regex_tree("((0|1*)|((2*.1*).(e*.0)))")
    BarTree(BarTree(Leaf('0'), StarTree(Leaf('1'))),
    DotTree(DotTree(StarTree(Leaf('2')), StarTree(Leaf('1'))),
    DotTree(StarTree(Leaf('e')), Leaf('0'))))
    '''
    # Checks if the len is 0, 1, 2, or e
    if len(regex) == 1:
        # Calling Leaf function from RegexTree because regex has no children
        return Leaf(regex)
    # To check if the regex has a '*' at the end
    elif regex[-1] == STAR:
        # Calling StarTree function from RegexTree because Regex ends with '*'
        return StarTree(build_regex_tree(regex[:len(regex)-1]))
    else:
        # Calling operationLocator helper function to determine what index
        # the operation is located at
        operation = operationLocator(regex)
        # If the main operation is a bar, it will call BarTree from RegexTree
        # because the index of the operation is a bar
        if regex[operation] == BAR:
            return BarTree(build_regex_tree(regex[1:operation]),
                           build_regex_tree(regex[operation+1:len(regex)-1]))
        # This case checks if the operation is a dot, it will call DotTree
        # from RegexTree because the index of the operation is a dot
        else:
            return DotTree(build_regex_tree(regex[1:operation]),
                           build_regex_tree(regex[operation+1:len(regex)-1]))
