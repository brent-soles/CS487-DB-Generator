# CS487-DB-Generator
##DB generator implementation of Wisconsin Benchmark

Here is where we will draft the desgin document.

Purpose of this document is have a reference of the steps that must be taken to implement a program which produces a vaild Wisconsin Benchmark schema.

The following document will use Python as the primary language, and where applicable, will use psuedo-code with a syntax similar to python.

# Relations

## Overview

As stated in section 2.1.1 of the Wisconsin Benchmark paper, the original benchmark has three relations: ONEKTUP, TENKTUP1 and TENKTUP2. Their differences are as follows:

* ONEKTUP, means there are 1,000 tuples in a table
* TENKTUP1, TENKTUP2 have 10,000 respectively

Where they each are the same is in the type of data that lives in the table, which is as follows:

* 13 integer attributes (where an integer is 4 bytes)
* 3 52-byte strings

### Environment
We will use two different relation database to do the performance comparison
* MYSQL
* Postgresql


#### Schema Definition

Note: This is copied directly from the Wisconsin Benchmark paper.

```sql
CREATE TABLE TUP
(
  unique1   integer NOT NULL,             # Random 0..9999
  unique2   integer NOT NULL PRIMARY KEY, # Random 0..9999
  two       integer NOT NULL,             # Cyclic 0..1
  four      integer NOT NULL,             # Cyclic 0..3
  ten       integer NOT NULL,             # Cyclic 0..9
  twenty    integer NOT NULL,             # Cyclic 0..19
  hundred   integer NOT NULL,             # Cyclic 0..99
  thousand  integer NOT NULL,             # Cyclic 0..999
  twothous  integer NOT NULL,             # Cyclic 0..1999
  fivethous integer NOT NULL,             # Cyclic 0..4999
  tenthous  integer NOT NULL,             # Cyclic 0..9999
  odd100    integer NOT NULL,             # Cyclic 1..99, where n % 3 == 0
  even100   integer NOT NULL,             # Cyclic 2..100, where n % 2 == 0
  stringu1  char(52) NOT NULL,            # See below
  stringu2  char(52) NOT NULL,            # ""
  string4   char(52) NOT NULL,            # ""
)
```
#### String definition

The string to be used in each of the the string attributes of the schema is:

```$xxxxxxxxxxxxxxxxxxxxxxxxx$xxxxxxxxxxxxxxxxxxxxxxxx$```

Where the `$` will be replaced by an uppercase character in the range of A..V

### Function Desgin

Goal: to see if we can fit all of this computation into a single loop.

Known metrics:

* unique2 MUST be uniqe. This will require some sort of memoization. Solutions can involve utilizing an array and flipping a bit at an index of a number that has been computed. For example, if 100 was computed as a value of unique2, then cache[100] == 1, whereas if 80 had not been computed, then cache[80] == 0.

* We know which indicies of the strings will need to be replaced, these will be: 0, 25, and 51

* We can utilize the modulo operator for each of the Cyclic integers, where the iterator will be set agains the modulus of targe range. For example, the `hundred` will be derived with: i % 99

```python
import random

# Inputs: number of tuples (rows) we want to
#   generate.
def generate_benchmark_data(number_of_tuples):
    # Need to keep track of wich values have been
    # computed and output
    cache = [0] * number_of_tuples
    odd_val = 1
    even_val = 2
    for i in range(number_of_tuples):
      unique1 = random.randrange(number_of_tuples)
      if (cache[unique2]):
        while(cache[unique2]):
          unique2 = random.randrange(number_of_tuples)

      cache[unique2] = 1 # Register this value is in table

      unique2 = i

      two = i % 2
      four = i % 4
      ten = i % 10
      twenty = i % 20
      hundred = i % 100
      thousand = i % 1000
      twothous = i % 2000
      fivethous = 1 % 5000
      tenthous = i % 10000
      odd_one_hun = odd_val
      odd_val += 2
      # ternary to reset odd_val
      even_one_hun = even_val
      even_val += 2
      # ternary to reset even_val
      # String computations

```