import time
import re


def naive_string_matching(text, pattern):
    shifts = []
    start = time.perf_counter()
    for s in range(0, len(text) - len(pattern) + 1):
        if pattern == text[s:s + len(pattern)]:
            shifts.append(s)
    stop = time.perf_counter()
    return stop - start, shifts


def transition_table(pattern):
    alphabet = []
    for i in pattern:
        if i not in alphabet:
            alphabet.append(i)
    result = []
    for q in range(len(pattern)+1):
        result.append({})
        for a in alphabet:
            k = min(len(pattern) + 1, q + 2)
            while True:
                k = k - 1
                if re.search(f"{pattern[:k]}$", pattern[:q] + a):
                    break
            result[q][a] = k
    return result


def fa_string_matching(text, delta):
    start = time.perf_counter()
    shifts = []
    q = 0
    for s in range(0, len(text)):
        if text[s] in delta[q]:
            q = delta[q][text[s]]
            if q == len(delta) - 1:
                q = 0
                shifts.append(s)
        else:
            q = 0
    stop = time.perf_counter()
    return stop - start, shifts


def prefix_function(pattern):
    pi = [0 for _ in range(len(pattern))]

    last_prefix = 0
    for i in range(1, len(pattern)):
        while last_prefix > 0 and pattern[last_prefix] != pattern[i]:
            last_prefix = pi[last_prefix - 1]

        if pattern[last_prefix] == pattern[i]:
            last_prefix += 1

        pi[i] = last_prefix

    return pi


def kmp_string_matching(s, pattern):
    pi = prefix_function(pattern)
    start = time.perf_counter()
    shifts = []
    last_prefix = 0
    m = len(pattern)
    for idx, a in enumerate(s):
        while last_prefix > 0 and pattern[last_prefix] != a:
            last_prefix = pi[last_prefix - 1]

        if pattern[last_prefix] == a:
            last_prefix += 1

            if last_prefix == m:
                shifts.append(idx + 1 - m)
                last_prefix = pi[last_prefix - 1]
    stop = time.perf_counter()
    return stop - start, shifts


with open('1997_714.txt', ) as f:
    article = f.read()
# with open('wikipedia.txt', ) as f:
#     article = f.read()

naive_time, naive_shifts = naive_string_matching(article, "art")
print("Time for naive algorithm: " + str(naive_time))

kmp_time, kmp_shifts = kmp_string_matching(article, "art")
print("Time for kmp algorithm: " + str(kmp_time))

table = transition_table("art")
fa_time, fa_shifts = fa_string_matching(article, table)
print("Time for fa: " + str(fa_time))

print(str(len(naive_shifts)) + " " + str(len(kmp_shifts)) + " " + str(len(fa_shifts)))

pattern_match = "qwertyuiopasdfghjklzxcvbnm"

kmp_timer = time.perf_counter()
prefix_function(pattern_match)
kmp_timer = time.perf_counter() - kmp_timer

fa_timer = time.perf_counter()
transition_table(pattern_match)
fa_timer = time.perf_counter() - fa_timer


print(str(fa_time) + "fa transition table" + " vs " + str(kmp_timer ) + " kmp prefix funtion")

pattern_match2 = "The quick brown fox jumps over the lazy dog"

kmp_timer2 = time.perf_counter()
prefix_function(pattern_match2)
kmp_timer2 = time.perf_counter() - kmp_timer2

fa_timer2 = time.perf_counter()
transition_table(pattern_match2)
fa_timer2 = time.perf_counter() - fa_timer2


print(str(fa_time) + " fa transition table" + " vs " + str(kmp_timer2) + " kmp prefix funtion")

text = 'd'*450000
pattern = 'd' * 10000 + 'a'

naive_time2, naive_shifts2 = naive_string_matching(text, pattern)
print("Time for naive algorithm: " + str(naive_time2))

kmp_time2, kmp_shifts2 = kmp_string_matching(text, pattern)
print("Time for kmp algorithm: " + str(kmp_time2))

# table2 = transition_table(pattern)
# fa_time2, fa_shifts2 = fa_string_matching(text, table2)
# print("Time for fa: " + str(fa_time2)) # nie skończyło się wykonowywać

