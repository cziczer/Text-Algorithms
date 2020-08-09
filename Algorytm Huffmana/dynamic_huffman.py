from bitmask_helper import *


class Node:
    def __init__(self, letter=None, cost=0):
        self.letter = letter
        self.cost = cost
        self.left = None
        self.right = None
        self.parent = None

    def insert_left(self, node):
        self.left = node
        node.parent = self

    def insert_right(self, node):
        self.right = node
        node.parent = self

    def code(self):
        if self.parent is None:
            return bitarray()
        if self == self.parent.left:
            return self.parent.code() + bitarray('0')
        else:
            return self.parent.code() + bitarray('1')

    def nodes_on_level(self, level):
        if level == 0:
            return self
        if self.left is not None:
            found = self.left.nodes_on_level(level + 1)
            if found is not None:
                return found
            return self.right.nodes_on_level(level + 1)

    def swap(self, node):
        self.parent, node.parent = node.parent, self.parent
        if self.parent is not None:
            if self.parent.left == node:
                self.parent.left = self
            else:
                self.parent.right = self
        if node.parent is not None:
            if node.parent.left == self:
                node.parent.left = node
            else:
                node.parent.right = node

    def right_sibling(self):
        current_node = self
        level = 0
        while current_node.parent is not None:
            if current_node == current_node.parent.left:
                found = current_node.parent.right.nodes_on_level(level)
                if found is not None:
                    return found
            current_node = current_node.parent
            level -= 1
        current_node = self
        level = 0
        while current_node.parent is not None:
            current_node = current_node.parent
            level += 1
        return current_node.nodes_on_level(-level + 1)

    def increment(self):
        self.cost += 1
        if self.parent is not None:
            right_sibling = self.right_sibling()
            if right_sibling.cost < self.cost:
                while True:
                    next_sib = right_sibling.right_sibling()
                    if next_sib is None or right_sibling.cost != next_sib.cost:
                        break
                    else:
                        right_sibling = next_sib
                if right_sibling != self.parent:
                    self.swap(right_sibling)
            self.parent.increment()


def encode(text):
    encoded = bitarray()
    nodes = {"": Node("")}
    for letter in text:
        if letter in nodes:
            node = nodes[letter]
            encoded += node.code()
            node.increment()
        else:
            updated_node = nodes[""]
            encoded += updated_node.code()
            encoded.fromstring(letter)
            node = Node(letter, cost=1)
            nodes[letter] = node
            zero_node = Node("")
            updated_node.insert_left(zero_node)
            updated_node.insert_right(node)
            nodes[""] = zero_node
            updated_node.increment()
    return encoded


def decode(code):
    result = ""
    nodes = {"": Node("")}
    current_node = root = nodes[""]
    index = 0
    while index <= len(code):
        if current_node.left is None:
            if current_node.letter != "":
                result += current_node.letter
            else:
                letter = code[index:index + 8].tostring()
                result += letter
                node = Node(letter, cost=1)
                nodes[letter] = node
                zero_node = Node("")
                current_node.insert_left(zero_node)
                current_node.insert_right(node)
                nodes[""] = zero_node
                index += 8
            current_node.increment()
            current_node = root
        if index < len(code):
            current_node = current_node.right if code[index] else current_node.left
        index += 1
    return result


def compress_file(file):
    result = file + ".dhuff"
    with open(file) as f:
        encoded = encode(f.read())
        with open(result, "wb") as res:
            encoded.tofile(res)
