class SuffixTreeNode:
    def __init__(self, depth, parent, interval, char):
        self.depth = depth
        self.parent = parent
        self.interval = interval
        self.v = char
        self.children = []

    def graft(self, suffix, tree):
        if self.v != suffix[self.depth-1]:
            node = SuffixTreeNode(self.depth + 1, self, None, suffix[self.depth])
            self.children.append(node)
            node.children.append(SuffixTreeNode(node.depth + 1, node, (tree.text.find(suffix[1:])+1, len(tree.text))
                                                , None))
        else:
            self.children.append(SuffixTreeNode(self.depth + 1, self, (tree.text.find(suffix[1:]) + 1, len(tree.text)),
                                                None))


class SuffixTree:
    def __init__(self, text):
        self.root = SuffixTreeNode(0, None, None, None)
        self.text = text
        self.root.graft(text, self)


def find_head(head, suffix):
    for child in head.children:
        if not child.v:
            return None     # we have this word in tree
        if child.v is not None and child.v == suffix[0]:
            head = child
    return head


def search_suffix_pattern(pattern, tree, current_node):
    if len(pattern) == 0:
        return True
    for child in current_node.children:
        if child.v is not None and child.v == pattern[0]:
            if len(pattern) == 1:
                return True
            return search_suffix_pattern(pattern[1:], tree, child)
    if current_node == tree.root:
        return False
    return search_suffix_pattern(pattern[1:], tree, tree.root)
