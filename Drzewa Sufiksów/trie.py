class Node:
    def __init__(self, depth, parent, char):
        self.depth = depth
        self.parent = parent
        self.v = char
        self.children = []

    def go_to_child(self, char):
        for child in self.children:
            if child.v == char:
                return child
        return None

    def graft(self, suffix_end):
        parent = self
        running_depth = self.depth + 1
        for char in suffix_end:
            child = Node(running_depth, parent, char)
            parent.children.append(child)
            running_depth += 1
            parent = child
        return parent


class Trie:
    def __init__(self, text):
        self.root = Node(0, None, None)
        self.root.graft(text)

    def find_head(self, suffix):
        head = self.root
        for char in suffix:
            child = head.go_to_child(char)
            if child is None:
                break
            else:
                head = child
        return head


def search_trie_pattern(node, pattern):
    if len(pattern) <= 0:
        return True
    child = node.go_to_child(pattern[0])
    if child is None:
        return False
    else:
        return search_trie_pattern(child, pattern[1:])