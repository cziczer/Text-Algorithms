from bitmask_helper import *
import heapq


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


def encode(text):
    costs_tree = set([Node(key, cost) for key, cost in calculate_letters_cost(text).items()])
    while len(costs_tree) > 1:
        new_node = Node()
        nodes_to_insert = heapq.nsmallest(2, costs_tree, key=lambda node: node.cost)
        costs_tree.remove(nodes_to_insert[0])
        new_node.insert_left(nodes_to_insert[0])
        costs_tree.remove(nodes_to_insert[1])
        new_node.insert_right(nodes_to_insert[1])
        new_node.cost = new_node.left.cost + new_node.right.cost
        costs_tree.add(new_node)
    root = costs_tree.pop()

    compressed_text = bitarray()
    huffman_tree = static_huffman_generator(root)
    for letter in text:
        compressed_text += huffman_tree[letter]
    return huffman_tree, compressed_text


def calculate_letters_cost(text):
    costs = {}
    for letter in text:
        if letter not in costs:
            costs[letter] = 1
        else:
            costs[letter] += 1
    return costs


def static_huffman_generator(root, code=bitarray()):
    if root.letter is not None:
        return {root.letter: code}
    else:
        return {**static_huffman_generator(root.left, code + bitarray('0')),
                **static_huffman_generator(root.right, code + bitarray('1'))}


def compress_file(file):
    result = file + ".shuff"
    with open(file) as f:
        huffman_tree, compressed_text = encode(f.read())
        longest_code = 0
        for code in huffman_tree.values():
            if len(code) > longest_code:
                longest_code = len(code)
        with open(result, "wb") as res_f:
            compressed_content = bitarray()
            compressed_content += from_number_to_bitmask(len(huffman_tree), 8)
            longest_code_bitmap = from_number_to_bitmask(longest_code)
            compressed_content += from_number_to_bitmask(len(longest_code_bitmap), 8)
            compressed_text_length = len(compressed_text)
            for _, code in huffman_tree.items():
                compressed_text_length += 8 + len(longest_code_bitmap) + len(code)
            for letter, code in huffman_tree.items():
                text_bits = bitarray()
                text_bits.fromstring(letter)
                compressed_content += text_bits
                compressed_content += from_number_to_bitmask(len(code), len(longest_code_bitmap))
                compressed_content += code
            compressed_content += compressed_text
            compressed_content.tofile(res_f)


def decode(code, root):
    text = ""
    current_node = root
    for bit in code:
        if not bit:
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.left is None:
            text += current_node.letter
            current_node = root
    return text


def generate_tree(code):
    root = Node()
    for letter, c in code.items():
        current_node = root
        for bit in c:
            if not bit:
                if current_node.left is None:
                    current_node.insert_left(Node())
                current_node = current_node.left
            else:
                if current_node.right is None:
                    current_node.insert_right(Node())
                current_node = current_node.right
        current_node.letter = letter
    return root


def decode_file(file):
    with open(file, "rb") as f:
        bit_mask = bitarray()
        bit_mask.fromfile(f)
        longest_code = from_bitmask_to_number(bit_mask[8:16])
        index = 16
        codes = {}
        for _ in range(from_bitmask_to_number(bit_mask[:8])):
            letter = bit_mask[index:index+8].tostring()
            index += 8
            code_len = from_bitmask_to_number(bit_mask[index:index+longest_code])
            index += longest_code
            code = bit_mask[index:index+code_len]
            codes[letter] = code
            index += code_len

        code = bit_mask[index:]
        huffman_tree = generate_tree(codes)
        return decode(code, huffman_tree)