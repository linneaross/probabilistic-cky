import sys
#from nltk.tree import Tree

grammar = open(sys.argv[1])
sentence = open(sys.argv[2])

class Node:

    def __init__(self, data, prob=0.0, left=None, down=None):
        #add further probabilities??
        self._data = data
        self._prob = prob
        self._left = left
        self._down = down

    def __repr__(self):
        if self._left == None and self._down == None:
            return self._data
        result = "( %s" % self._data
        if self._left:
            result += " %r" % self._left
        if self._down:
            result += " %r" % self._down
        result += " )"
        return result

    def data(self):
        return self._data

    def prob(self):
        return self._prob

    def left(self):
        return self._left

    def down(self):
        return self._down


def analyze_grammar(grammar):
    result = {}
    for line in grammar:
        rule = line.split()
        if len(rule) > 0:
            # breaks rule into a list of items
            prob = float(rule[0])
            left = rule[1]
            right = rule[2:]
            # stores values as variables which help keep track of rule info
            if left in result:
                # if there is already a list of rules associated with the left side
                result[left].append({'prob': prob, 'left': left, 'right': right})
            else:
                #if there is no list containing rules associated with the left side
                result[left] = [{'prob': prob, 'left': left, 'right': right}]
    return result

def analyze_sentence(sentence):
    result = []
    for line in sentence:
        #adds and returns each sentence as a list into the greater list
        sent = line.split()
        result.append(sent)
    return result

def get_parent_unary(grammar, child_node):
    result = []
    prob = 0.0
    for key in grammar:
        for item in range(len(grammar[key])):
            if child_node.data() in grammar[key][item]['right']:
                result.append(Node(grammar[key][item]['left'], grammar[key][item]['prob']+ child_node.prob(), child_node))
    return result

def get_parent_binary(grammar,left_node,down_node):
    result = []
    prob = 0.0
    for key in grammar:
        for item in range(len(grammar[key])):
            if len(grammar[key][item]['right']) == 2:
                if (left_node.data() == grammar[key][item]['right'][0]) and (down_node.data() == grammar[key][item]['right'][1]):
                    result.append(Node(grammar[key][item]['left'], grammar[key][item]['prob'] + left_node.prob() + down_node.prob(), left_node, down_node))
    return result

def cky(grammar, sentence):
    length = len(sentence)
    sent = ''
    for beep in range(len(sentence)):
        sent += sentence[beep] +' '
    table = []

    #create the matrix according to the amount of constituent parts
    for i in range(length):
        table.append([])
        for j in range(length):
            table[i].append([])

    #master loop - does the whole darn thing
    for col in range(length):
        for row in reversed(range(col+1)):
            if (row == col):
                table[col][row] += get_parent_unary(grammar, Node(sentence[col]))
            else:
                for k in range(col):
                    left_col = k
                    down_row = k+1
                    for left_node in table[left_col][row]:
                        for down_node in table[col][down_row]:
                            table[col][row] += get_parent_binary(grammar,left_node,down_node)

    return table[length - 1][0]

def main():
    if len(sys.argv) != 3:
        return 'Invalid arguments'
    gram = analyze_grammar(grammar)
    print("%r" % gram["ROOT"])
    sent = analyze_sentence(sentence)
    for item in sent:
        print("PARSING:: %r" % item)
        result = cky(gram,item)
        for parse in result:
            if parse.data() == "ROOT":
                print("======")
                print("Prob: %f" % parse.prob())
                print("%r" % parse)
                print("======\n")
    return

if __name__ == '__main__':
    main()
