import static_huffman
import dynamic_huffman
import os
import time


test_set = ["1kBFile.txt", "10kBFile.txt", "100kBFile.txt", "1MBFile.txt"]


def compression(file, compressed):
    return 1 - os.path.getsize(compressed) / os.path.getsize(file)


def static_huffman_test(file):
    with open(file) as f:
        content = f.read()
        codes, encoded = static_huffman.encode(content)
        decrypted = static_huffman.decode(encoded, static_huffman.generate_tree(codes))
        if decrypted == content:
            print("Huffman code correct")
        else:
            print("ERROR")
    start = time.perf_counter()
    static_huffman.compress_file(file)
    print("Compression time: " + str(time.perf_counter() - start))
    start = time.perf_counter()
    decrypted = static_huffman.decode_file(file + ".shuff")
    print("Decompression time: " + str(time.perf_counter() - start))
    if decrypted == content:
        print("Compression to file correct!")
    else:
        print("ERROR")
    print("Compression level: " + str(compression(file, file + ".shuff")))


def dynamic_huffman_test(file):
    with open(file) as f:
        content = f.read()
        encoded = dynamic_huffman.encode(content)
        decrypted = dynamic_huffman.decode(encoded)
        if decrypted == content:
            print("Huffman code correct")
        else:
            print("ERROR")
    start = time.perf_counter()
    dynamic_huffman.compress_file(file)
    print("Compression time: " + str(time.perf_counter() - start))
    print("Compression level: " + str(compression(file, file + ".dhuff")))


for test in test_set:
    print(test + " test")
    print("Results for static Huffman: ")
    static_huffman_test(test)
    print("Results for dynamic Huffman: ")
    dynamic_huffman_test(test)


