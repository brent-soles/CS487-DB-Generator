#!/usr/bin/python3.7

import random
import string
import math

def compute_tailing_characters():
  trailing_chars = ""
  for i in range(5):
    trailing_chars += "xxxxxxxx"
  return trailing_chars

def compute_cyclic_str_key(index):
  mod_value = index % 4
  return ''.join( [chr(65 + mod_value * 7)] * 7 )


def compute_unique_str_key(unique_val):
  """
    This function is pulled from the Wisconsin Benchmark paper
  """
  unq = unique_val
  key = ['A','A','A','A','A','A','A']
  incr = 6
  
  while unq > 0:
    remainder = unq % 26
    key[incr] = chr(65 + remainder)
    unq = math.floor(unq / 26)
    incr -= 1

  return ''.join(key)

def create_table_data_of_size(table_size):
    
    unique_set = random.sample(range(table_size), table_size)
    trailing_characters = compute_tailing_characters()
    for incr in range(table_size):
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

        ustr1 = compute_unique_str_key(unique1)
        ustr2 = compute_unique_str_key(unique2)
        str4 = compute_cyclic_str_key(incr)

        print('{u1}\t{u2}\t{two}\t{four}\t{ten}\t{twenty}\t{one_p}\t{ten_p}\t{tw_p}\t{fi_p}\t{u3}\t{e_o}\t{o_o}\t{ustr1}\t{ustr2}\t{str4}'.format(
          u1 = unique1,
          u2 = unique2,
          two = two,
          four = four,
          ten = ten,
          twenty = twenty,
          one_p = one_percent,
          ten_p = ten_percent,
          tw_p = twenty_percent,
          fi_p = fifty_percent,
          u3 = unique3,
          e_o = even_one_percent,
          o_o = odd_one_percent,
          ustr1 = ustr1 + trailing_characters,
          ustr2 = ustr2 + trailing_characters,
          str4 = str4 + trailing_characters
        ))


create_table_data_of_size(1000)