# encoding=utf8
import sys
import os
import re

if (len(sys.argv) != 3):
    print "You must provide 2 arguments: " + """program takes two paths as parameters:
    path to the candidate translation (single file),
    a path reference translations (single file, or a directory if there are multiple reference translations)"""
    print "\nUsage: python calculatebleu.py /path/to/candidate /path/to/reference"
    exit(1)

ref_path = sys.argv[2]
list_ref_files = []

if os.path.isdir(ref_path):
    for f in os.listdir(ref_path):
        f_full_path = os.path.join(ref_path, f)
        if os.path.isfile(f_full_path):
            list_ref_files.append(f_full_path)

else:
    list_ref_files.append(ref_path)

print list_ref_files
exit(0)

# with open(sys.argv[1], 'rb') as f_cand, open(sys.argv[2], 'rb') as f_ref:


def tokenize(sentence):
    tokens = re.sub('[\W_]+', ' ', sentence, flags=re.UNICODE).lower().split()
    return tokens

def concat_tokens(list_tokens):
    str = list_tokens[0]
    for token in list_tokens[1:]:
        str += "-" + token
    return str


def compute_grams(tokens, N = 4):
    grams = [concat_tokens( tokens[i:i + N] ) for i in xrange(len(tokens) - (N - 1))]
    return grams

def create_words_dict(tokens):
    dict = {}
    for token in tokens:
        if token not in dict:
            dict[token] = 1
        else:
            dict[token] += 1

    return dict

def sum_clip_counts(dict_cand, list_dict_refs):
    sum = 0
    for word in dict_cand:
        max_count_word_occurrences = 0

        for dict_ref in list_dict_refs:
            if word in dict_ref:
                count_word_occurrences = min(dict_cand[word], dict_ref[word])
                if count_word_occurrences > max_count_word_occurrences:
                    max_count_word_occurrences = count_word_occurrences

        sum += max_count_word_occurrences

    return sum


def modified_precision(cand_tokens, list_ref_tokens):
    dict_cand = create_words_dict(cand_tokens)
    list_dict_ref = [create_words_dict(ref_tokens) for ref_tokens in list_ref_tokens]
    # print list_dict_ref

    return float(sum_clip_counts(dict_cand, list_dict_ref)) / float(len(cand_tokens))  #total_num_candidate_words = len(cand_tokens)

# Example 1
candidate1 = "It is a guide to action which ensures that the military always obeys the commands of the party."
candidate2 = "It is to insure the troops forever hearing the activity guidebook that party direct."
reference1 = "It is a guide to action that ensures that the military will forever heed Party commands."
reference2 = "It is the guiding principle which guarantees the military forces always being under the command of the Party."
reference3 = "It is the practical guide for the army always to heed the directions of the party."
list_cand = [candidate1, candidate2]
list_refs = [reference1, reference2, reference3]

# Example 2
# candidate1 = "the the the the the the the."
# reference1 = "The cat is on the mat."
# reference2 = "There is a cat on the mat."
# list_cand = [candidate1]
# list_refs = [reference1, reference2]


N = 4
for candidate in list_cand:
    cand_tokens = compute_grams(tokenize(candidate), N)

    list_ref_tokens = [compute_grams(tokenize(ref), N) for ref in list_refs]
    # print list_ref_tokens
    print modified_precision(cand_tokens, list_ref_tokens)

    # print compute_4grams(cand_tokens)



