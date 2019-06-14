# CS487/587 Spring 2019
## Project Part II
### By: Mingjue Wang & Brent Daniels-Soles

## Part II Overview

Given our initial experiments with MySQL and Postgres, it was decided the best course of action would be to compare MySQL and Postgres. The reason being, is we think our benchmark experiments will give some idea of how each of the respective systems perfrom without any given configuration.

The real world application of this, is for most side and hobby projects, people will use the standard install of Postgres/MySQL, rather than fine tuning it before they begin building their applications. We hope to exposed, through our experiments, which system may be better for building a performant application withouth having to tune various settings. In addition, we generated data for a table which has 1,000,000 rows, using the Wisconsin Benchmark data generation guidelines. The reason we added this extra table to use in our test, is to have an idea of how each would perform when there are non-trivial amounts of data to deal with.


### Hypothesis
The hypothesis we have for these experiments is for MySQL and Postrgres to have similar performance. I do not think we will be able to pick a clear "winner", but be able to see where each of the systems shine, and where they struggle.

---
## System Research

The following information is taken from the office Postgres and MySQL docs.
Below are the respective links to each of the documentation pages:
* MySQL: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
* PosgreSQL: [https://www.postgresql.org/docs/9.1/ ](https://www.postgresql.org/docs/9.1/ )

For each of the respective databases, we tried to dig into how a query plan could be structred from the query feature set of each of the systems.

The subsections represent how indicies, projection, joins, etc... are handled in each of the systems.

### Indices
#### Postgres
Posgres has a few different index 'types' which can be utilized. They are as follows:
* B-Tree (more commonly known as B+ Tree)
* Hash Indices
* GiST (Acronym for 'Generalized Search Tree')
* GIN (Acronym for 'Generalized Inverted Index', commonly used for indexing composite values)

In our experiments, the index type used is the 'B-Tree' type. The reason being, is this is the default index type when constructing a primary key/index on a column in a table. And since this is one of the most common data structures used for indexing, we think it is good to measure if an index on certain tables for certain query types will increase the speed of execution.

#### MySQL
MySQL has similar index types, however, we were not able to find many 'specialized' index types. Specialized in this case, refer to different index types which could be utilized for less common scenarios (ref. GiST and GIN in Posgres section). The following are the types of indicies available in MySQL:
* B-Tree (or B+ Tree)
* Hash Indicies
* R-Tree (index type for spacial data)

Again, in our experiments, we used the 'B-Tree' as it is one of the more commone index types.


### Joins
#### Postgres
During research, we had a tough time finding specifics about the types of joins Postgres implements. However, we were able to find imformation that details (at a high level) how the DBMS constructs a query. At a high leve, Postgres constructs queries based off of what indices are defined for the tables involved in the relation, and from there, conducts a near-exhaustive search of various query plans in order to derive the best one. However, the near-exhaustive search is only conducted when querying smaller amounts of data, as there can be huge, system-wide ramifications if performing a near-exhaustive search on large data sets. When joining big data together, Postgres uses what is called a “genetic algorithm” to attempt to discern the best query plan for large/many join operations, these optimizations are mainly based upon heuristics which operate off of some form of randomization.

#### MySQL
In the documentation for MySQL, specifically in the introductary chapter (1.3.2), it is specified MySQL utilizes an optimized nested loop join algorithm. After further digging in, MySQL currently implements two types of nested loop joins, they are:

* Nested Loop Join
* Block Nested Loop Join

The Nested Loop Join is pretty straightforward: for each row in TableA, loop over TableB and see if the join predicate is satisfied.

The Block Nested Loop Join is similar to the Nested Loop Join, however, works a bit differently, What this join algorithm does, is once a row is read for the outer table, it is sent to a buffer called the 'join_buffer'. Given the example above with TableA and TableB: for each row in TableA, TableB is looped over, however, TableB is in the 'join_buffer', so the access to each row is already in memory. This makes accessing each row have a lower overhead than making calls to the Disk Manager/Buffer pool. 


### Buffer Pools
#### Postgres
For this section, I reference the following articles:

* Postgres buffer manager: http://www.interdb.jp/pg/pgsql08.html

The Postgres buffer pool is constructed from what are called ‘slots’. A slot is the equivalent of a page in any other DBMS. Each slot holds 8KB of data; the same amount as a page in memory. Once data has been loaded into a slot in the buffer pool, the algorithm that manages which pages are evicted, is the clock algorithm. In addition when Postgres detects it is set to read large amounts of data, the system will allocate a Ring buffer on the side (basically an on-demand small amount of data to store temporary data) in order to improve buffer performance.

#### MySQL
Digging through the MySQL docs, we were unable to land on a definite answer for the default size of pages or the default size of memory MySQL is allocated. The docs mentioned this aspect is left up to user discretion. Despite this, the docs go on to detail MySQL uses a variation of the Least Recently Used algorithm. The LRU algorithm employed by MySQL uses a head and tail pointer to memory to track older/inactive pages not really used, and newer/active pages, respectively. Everything the the ‘old’ list is candidate for eviction when a need arises.

--- 
## Performance Experiment Design
### Overview

---
## Data Used In Tests

---
## Perf. Hypothesis

---
### Experiment Queries

#### Query 1
```sql
SELECT * 
FROM TENKTUP1 
WHERE unique2 BETWEEN 3792 AND 18764;
```

What perf metrics does this query test:
* Projection of large range of elements
* Tests raw efficiency of plan, due to an index not having an effect (need to scan whole table)


#### Query 2
```sql
SELECT two, ten, stringu1 
FROM TENKTUP1 
WHERE unique1 BETWEEN 5400 AND 79999;
```
What perf metrics does this query test:
* 


#### Query 3
```sql
SELECT * 
FROM TENKTUP1, onemiltup 
WHERE (TENKTUP1.unique2 = onemiltup .unique2);
```


#### Query 4
```sql
SELECT * FROM TENKTUP1, onemiltup 
WHERE (TENKTUP1.unique1 = onemiltup .unique1) AND (TENKTUP1.unique1<4532)
```


#### Query 5
```sql
SELECT tenktup1.unique2, COUNT(*)
FROM tenktup1 JOIN onemiltup on tenktup1.unique2 = onemiltup.odd100
GROUP BY tenktup1.unique2
ORDER BY tenktup1.unique2;
```


## Lessons Learned
