class Node:
    def __init__(self, parent, parent_first_letter):
        self.parent = parent
        self.parent_first_letter = parent_first_letter
        self.children = {}
        self.link = None

    def add_child(self, letter, edge):
        self.children[letter] = edge

    def graft(self, interval, first_letter):
        node = Node(self, first_letter)
        edge = Edge(interval, node)
        self.add_child(first_letter, edge)
        return node

    def split_edge(self, interval, text):
        edge = self.children[text[interval[0]]]
        node = Node(self, text[interval[0]])
        edge_from_parent = Edge(interval, node)
        self.children[text[interval[0]]] = edge_from_parent
        bottom_interval = (interval[1] + 1, edge.interval[1])
        bottom_edge = Edge(bottom_interval, edge.node)
        node.add_child(text[interval[1] + 1], bottom_edge)
        edge.node.parent = node
        edge.node.parent_first_letter = text[interval[1] + 1]


class Edge:
    def __init__(self, interval, node):
        self.interval = interval
        self.node = node


class Tree:
    def __init__(self, text):
        self.root = Node(None, "")
        self.word = text

    def search_tree_pattern(self, pattern):
        curr_letter = 0
        node = self.root
        while curr_letter < len(pattern):
            # checking if common part of word to find and text represented by the tree ended in the current node
            if pattern[curr_letter] not in node.children:
                return False
            edge = node.children[pattern[curr_letter]]
            interval = edge.interval
            text_interval = interval[0]
            while text_interval <= interval[1]:
                if curr_letter == len(pattern):
                    return True
                if self.word[text_interval] != pattern[curr_letter]:
                    return False
                curr_letter += 1
                text_interval += 1
            node = edge.node
        return True


def label_size(label):
    return label[1] - label[0] + 1


def fast_find(node, label, text):
    edge = node.children[text[label[0]]]
    while label_size(label) > label_size(edge.interval):
        node = edge.node
        label = (label[0] + label_size(edge.interval), label[1])
        edge = node.children[text[label[0]]]
    if label_size(label) == label_size(edge.interval):
        return edge.node
    else:
        node_top = (edge.interval[0], edge.interval[0] + label_size(label) - 1)
        node.split_edge(node_top, text)
        node = node.children[text[label[0]]].node
        return node


def slow_find(node, label, text):
    label_letter = label[0]
    if not text[label_letter] in node.children:
        return node, label
    edge = node.children[text[label_letter]]
    edge_letter = edge.interval[0]
    while text[label_letter] == text[edge_letter]:
        if edge_letter == edge.interval[1]:
            node = edge.node
            label_letter += 1
            if not text[label_letter] in node.children:
                return node, (label_letter, label[1])
            edge = node.children[text[label_letter]]
            edge_letter = edge.interval[0]
        else:
            label_letter += 1
            edge_letter += 1
    node_top = (edge.interval[0], edge_letter - 1)
    node.split_edge(node_top, text)
    left_label = (label_letter, label[1])
    return node.children[text[edge.interval[0]]].node, left_label