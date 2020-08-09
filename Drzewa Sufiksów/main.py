import string

from trie import *
from sufixtree import *
from suffixtree_mccreight import *
import time
import math
import random

test_set = ['bbb$', 'aabbabd', 'ababcd', 'abcbccd']


def check_unique_mark(text):
    if text.count(text[-1]) == 1:
        return text
    i = 0
    while True:
        marker = chr(ord('#') + i)
        if marker not in text:
            text = text + marker
            return text
        i += 1


def build_tree_schema(text):
    trie = Trie(text)
    for i in range(1, len(text)):
        suffix = text[i:]
        head = trie.find_head(suffix)
        suffix_end = suffix[head.depth:]
        head.graft(suffix_end)
    return trie


def test_trie():
    for word in test_set:
        start = time.perf_counter()
        trie = build_tree_schema(word)
        print(time.perf_counter() - start)
        for i in range(1, len(word)):
            if not search_trie_pattern(trie.root, word[i:]):
                print("Error")
    with open('1997_714.txt', 'r', encoding='UTF-8') as file:
        content = file.read()
        content = content[:5000]
        content = check_unique_mark(content)
        start = time.perf_counter()
        trie = build_tree_schema(content)
        print(time.perf_counter() - start)
        pattern = content[-150:]
        if not search_trie_pattern(trie.root, pattern):
            print("Error")


def build_suffix_tree_schema(text):
    suffix_tree = SuffixTree(text)
    for i in range(1, len(text)):
        suffix = text[i:]
        head = find_head(suffix_tree.root, suffix)
        # head = None when we have this suffix in tree
        if head:
            head.graft(suffix, suffix_tree)
    return suffix_tree


def test_suffix_tree():
    for text in test_set:
        start = time.perf_counter()
        tree = build_suffix_tree_schema(text)
        print(time.perf_counter() - start)
        for i in range(len(text)):
            if not search_suffix_pattern(text[i:], tree, tree.root):
                print("Error with " + text[i:])
    with open('1997_714.txt', 'r', encoding='UTF-8') as file:
        content = file.read()
        content = content[:10000]
        content = check_unique_mark(content)
        start = time.perf_counter()
        tree = build_suffix_tree_schema(content)
        print(time.perf_counter() - start)
        pattern = content[-150:]
        if not search_suffix_pattern(pattern, tree, tree.root):
            print("Error")


def build_mccreight_tree_schema(text):
    tree = Tree(text)
    head = tree.root
    node = tree.root
    leaf = node.graft((0, len(text) - 1), text[0])
    for i in range(1, len(text)):
        left_label = (i, len(text) - 1)
        if head == tree.root:
            node = tree.root
        else:
            to_head_label = head.parent.children[head.parent_first_letter].interval
            if head.parent == tree.root:
                to_head_label = (to_head_label[0] + 1, to_head_label[1])
                node = tree.root
            else:
                node = head.parent.link
            if to_head_label[1] >= to_head_label[0]:
                node = fast_find(node, to_head_label, text)
            left_label = (leaf.parent.children[leaf.parent_first_letter].interval[0], left_label[1])
        last_head = head
        head, left_label = slow_find(node, left_label, text)
        last_head.link = node
        leaf = head.graft(left_label, text[left_label[0]])
    return tree


def test_mccreight():
    for word in test_set:
        start = time.perf_counter()
        tree = build_mccreight_tree_schema(word)
        print(time.perf_counter() - start)
        for i in range(len(word)):
            if not tree.search_tree_pattern(word[i:]):
                print("Error with " + word[i:])
    with open('1997_714.txt', 'r', encoding='UTF-8') as file:
        content = file.read()
        content = content[:10000]
        content = check_unique_mark(content)
        start = time.perf_counter()
        tree = build_mccreight_tree_schema(content)
        print(time.perf_counter() - start)
        pattern = content[-150:]
        if not tree.search_tree_pattern(pattern):
            print("Error")


# TESTY
tree = build_tree_schema("ananas")
if not search_trie_pattern(tree.root, "nanas"):
    print("Error with " + "nanas")
if not search_trie_pattern(tree.root, "banas"):
    print("Error with banas in trie")

suffix_tree = build_suffix_tree_schema("ananas")
if not search_suffix_pattern("nanas", tree, tree.root):
    print("Error with " + "nanas")
if not search_suffix_pattern("banas", suffix_tree, suffix_tree.root):
    print("Error with banas in suffix tree")

tree = build_mccreight_tree_schema("ananas")
if not tree.search_tree_pattern("nanas"):
    print("Error with " + "nanas")
if not tree.search_tree_pattern("banas"):
    print("Error with banas in suffix tree with links")

for word in test_set:
    word = check_unique_mark(word)


test_trie()
test_suffix_tree()
test_mccreight()
