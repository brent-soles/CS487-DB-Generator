#!/usr/bin/env python3

import random
import string
import math
import sys
import argparse

##### Functions for generating rows/tuples ######


def compute_tailing_characters():
    """
    Args:
      None

    Purpose of this function is to provide a compact
    way of adding the trailing characters to the 
    strings in the schema
    """
    trailing_chars = ""
    for _ in range(5):
        trailing_chars += "xxxxxxxx"
    return trailing_chars


def compute_cyclic_str_key(index):
    mod_value = index % 4
    return ''.join([chr(65 + mod_value * 7)] * 7)


def compute_unique_str_key(unique_val):
    """
      This function is pulled from the Wisconsin Benchmark paper
      and formats the first 7 characters in the resulting
      strings. 

      This function is used in conjunction with:
        compute_tailing_characters
    """
    unq = unique_val
    key = ['A', 'A', 'A', 'A', 'A', 'A', 'A']
    incr = 6

    while unq > 0:
        remainder = unq % 26
        key[incr] = chr(65 + remainder)
        unq = math.floor(unq / 26)
        incr -= 1

    # Creates the correct string,
    # The alogrithm originally right aligns,
    # then left justifies (i.e. reverse the list
    # from its reversed state)
    key.reverse()
    return ''.join(key)


def create_table_data_of_size(num_of_tuples):
    """
    Args:
        num_of_tuples (integer): # of tuples/rows to create

        This functions creates the rows specified in the
        Wisconsin benchmark paper.
    """
    rows = []
    unique_set = random.sample(range(num_of_tuples), num_of_tuples)
    trailing_characters = compute_tailing_characters()
    for incr in range(num_of_tuples):
        # All the 'static' values
        unique1 = unique_set[incr]
        unique2 = incr
        two = unique1 % 2
        four = unique1 % 4
        ten = unique1 % 10
        twenty = unique1 % 20
        one_percent = unique1 % 100
        ten_percent = unique1 % 10
        twenty_percent = unique1 % 5
        fifty_percent = unique1 % 2
        unique3 = unique1
        even_one_percent = one_percent * 2
        odd_one_percent = one_percent * 2 + 1

        # Need to compute the unique string
        # which will help in string comparisons/
        # joins when input into the DB
        ustr1 = compute_unique_str_key(unique1)
        ustr2 = compute_unique_str_key(unique2)
        str4 = compute_cyclic_str_key(incr)

        rows.append('{u1},{u2},{two},{four},{ten},{twenty},{one_p},{ten_p},{tw_p},{fi_p},{u3},{e_o},{o_o},{ustr1},{ustr2},{str4}\n'.format(
            u1=unique1,
            u2=unique2,
            two=two,
            four=four,
            ten=ten,
            twenty=twenty,
            one_p=one_percent,
            ten_p=ten_percent,
            tw_p=twenty_percent,
            fi_p=fifty_percent,
            u3=unique3,
            e_o=even_one_percent,
            o_o=odd_one_percent,
            ustr1=ustr1 + trailing_characters,
            ustr2=ustr2 + trailing_characters,
            str4=str4 + trailing_characters
        ))
    return rows

##### End Functions for generating rows/tuples ######

##### Functions for main script #####


def write_tuples_to_file(file, tuples):
    """
    Args:
      file:     file specified by the user.
      tuples:   array with each index being a string to input into
                the specified file.

      This functions opens (creates one if it doesn't exist),
      then proceeds to write to the file. This is destructive,
      as it overwrites any data that is previously in the file.
    """
    with open(file, 'w+') as user_file:
        for each_row in tuples:
            user_file.write(each_row)

##### End Functions for main script #####


if __name__ == '__main__':
    # Need to have user have some sort
    # of control over what to output
    argsparser = argparse.ArgumentParser(
        description='Generate a file for conducting the Wisconsin Benchmark')
    argsparser.add_argument('--tuples', '-t', type=int, required=True)
    argsparser.add_argument('--file', '-f', type=str, required=True)

    # Omits the first element in the argv
    # passes it to the parser
    args = argsparser.parse_args(sys.argv[1:])

    # Extract args for readability
    user_file_name = args.file
    tuples = create_table_data_of_size(args.tuples)

    # Compute and write out the file
    write_tuples_to_file(user_file_name, tuples)
    print('Wrote', len(tuples), 'lines to:', args.file, sep=' ')
