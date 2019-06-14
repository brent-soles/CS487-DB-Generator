# CS487/587 Spring 2019
## Project Part II
### By: Mingjue Wang & Brent Daniels-Soles

# Part II Overview

Given our initial experiments with MySQL and Postgres, it was decided the best course of action would be to compare MySQL and Postgres for the benchmark segment of this project. The reason being, is we wanted to structure our benchmark experiments to give an idea of how each of the respective systems perfrom out of the box.

The reason for leaving each system in their default configuration is because of the fact most side and hobby projects, and possibly startups, use these systems in their default state rather than fine tuning it before they beginning to build their applications. With our benchmark, we hope to examine which system may be better for building a performant application withouth having to adjust any settings. In addition, our benchmark aims to highlight the consistency of each platform, as each query in the benchmark will be run mulitple times.

## Hypothesis
The hypothesis we have for these experiments is for MySQL and Postrgres to have similar performance for the simpler queries of the benchmark. However, once they systems are executing `JOIN` statements, we think Postgres will be more performant than MySQL, due to MySQL only implementing Nested Loop Joins (See 'Join' in 'System Research' section for more information).

---
# System Research

The following information about each of the systems is sourced from the offical Postgres and MySQL docs.
Below are the respective links to each of the documentation pages:
* MySQL: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
* PosgreSQL: [https://www.postgresql.org/docs/9.1/ ](https://www.postgresql.org/docs/9.1/ )

For each of the databases, we tried to dig into the features which would be involved in our tests.

The subsections represent how indicies, projection, joins, and the buffer pool are used in each of the systems.

## Indices
#### Postgres
Posgres has a few different index 'types' which can be utilized. They are as follows:
* B-Tree (more commonly known as B+ Tree)
* Hash Indices
* GiST (Acronym for 'Generalized Search Tree')
* GIN (Acronym for 'Generalized Inverted Index', commonly used for indexing composite values)

In our experiments, the index type used is the 'B-Tree'. The reason being, is this is the default index type when constructing a primary key/index on a column in a table. And since this is one of the most common indexing strategies (and a default of the system), we decided to use this type of index on our data.

#### MySQL
MySQL has similar index types, however, we were not able to find many 'specialized' index types. Specialized in this case, refers to different index types which could be utilized for less common scenarios (ref. GiST and GIN in previous Postgres section). The following are the types of indicies available in MySQL:
* B-Tree (or B+ Tree)
* Hash Indicies
* R-Tree (index type for spacial data)

Again, in our experiments, we used the 'B-Tree' as it is one of the more commone index types (see above section for further details about using the 'B-Tree' in this benchmark).

## Joins
#### Postgres
During research, we were unfruitful in finding specifics about the types of `JOIN`'s Postgres implements. However, we were able to find information that details (at a high level) how a query is constructed. 

At a high level, Postgres constructs queries based off of the indices currently defined on the relation, and from there, conducts a near-exhaustive search of various query plans in order to derive the best one. However, the near-exhaustive search is only conducted when querying smaller amounts of data, as there can be huge, system-wide ramifications when performing a near-exhaustive search on large data sets. When joining big data together, Postgres uses what is called a “genetic algorithm” to attempt to discern the best query plan for large/join heavy operations, these optimizations are mainly based upon heuristics which are determined by a form of randomization.

#### MySQL
In the documentation for MySQL, specifically in the introductary chapter (1.3.2), it is specified MySQL utilizes an optimized nested loop join algorithm. No other type of `JOIN` (as far as I know), is implemented in MySQL (besides a variant of the Nested Loop Join). 

After further digging, MySQL currently implements two types of the Nested Loop Join algorithm, they are:

* Nested Loop Join
* Block Nested Loop Join

The Nested Loop Join is pretty straightforward: for each row in TableA, loop over TableB and see if the join predicate is satisfied. If the join predicate is satisfied, then add the combination of each of the rows to the output.

The Block Nested Loop Join is similar to the Nested Loop Join, however, works a bit differently, What Block Nested Loop Join does, is once a row is read from the outer table, it is sent to a buffer called the 'join_buffer'. The 'join_buffer' acts as an in memory cache of each row seen for a given `JOIN` query. This prevents the DBMS from having to constantly make calls to the buffer pool/Disk Manager, and allows for the query engine to access the buffer for rows that have already been seen. Given the example above with TableA and TableB: 

For each row in TableA, TableB is looped over and checked against the join predicate. If the join predicate is satisfied, the combination of the rows is added to the output. From there, the row in TableA and TableB are added to the join buffer. On the next pass, the query engine will check if the row needed is in the 'join_buffer' and if so, grab the row data from the buffer. If not, it will need to make a call to the system to grab that row off disk. This is then repeated for the remainder of the algorithm. In short, what the Block Nested Loop Join aims to do is make accessing each row have a lower overhead than making calls to the Disk Manager/Buffer pool. 


## Buffer Pools
#### Postgres
For this section, I reference the following articles:

* Postgres buffer manager: http://www.interdb.jp/pg/pgsql08.html

The Postgres buffer pool is constructed from what are called ‘slots’. A slot is the equivalent of a page in any other DBMS. Each slot holds 8KB of data; the same amount as a page in memory. Once data has been loaded into a slot in the buffer pool, the algorithm that manages which pages are evicted, is the clock algorithm. In addition when Postgres detects it is set to read large amounts of data, the system will allocate a Ring buffer on the side (basically an on-demand small amount of memory to store temporary data) in order to improve buffer performance.

#### MySQL
Digging through the MySQL docs, we were unable to land on a definite answer for the default size of pages or the default size of memory MySQL is allocated. The docs mentioned this aspect is left up to user discretion. Despite this, the docs go on to detail MySQL uses a variation of the Least Recently Used algorithm. The LRU algorithm employed by MySQL uses a head and tail pointer to memory to track older/inactive pages not really used, and newer/active pages, respectively. Everything the the ‘old’ list is candidate for eviction when a need arises.

--- 
# Performance Experiment Design
## Overview

For each of the tests, we wanted to see how the systems would perform for small, medium and large sets of data. Given some of the insights gained from the class about how databases behave when constructing query plans, we structured the query tests to first get a baseline as to how the respective system perform with *'smaller'* data tables, with each query getting more complex and more computationally expensive. The first two queries are basic `SELECT` statements, and three through five are focused on analyzing the performance of each systems `JOIN` algorithm.

The main part of this benchmark is centered around each systems `JOIN` execution. The reason we decided to have this benchmark focus mainly on `JOIN`'s, is becuase they are historically the most expensive query type to execute and because of the variance between the two systems in the way they implement joins.

## Data Used In Tests

There are three tables that we use in these tests, each being generated using the guidelines set forth in the Wisconsin Benchmark paper. The following tables are:

* TENKTUP1 (10,000 rows of data)
* TENKTUP2 (10,000 rows of data)
* ONEMILTUP (1,000,000 rows of data)

Originally, the benchmark did not exceed 10,000 rows of data, and by implication did not include the ONEMILTUP as part of the benchmark. The reason we decided to include this table, was to mock a table of a system which deals with an amount of data/rows one would see in industry. 

---
## Experiment Queries

### Testing methods
For each of the queries listed below, we used the following steps to get the performance data listed below. The steps are:
1. Run each query 5 times
2. Drop the slowest/fastest times for the given query*
3. Display the low/mid/high range of time and the average of those three times

> \*Some of the query's contain a footnote. This footnote is to give indication of queries ran for systems which had odd behavior for a given query run.

#### Query 1 - Basic SELECT
```sql
SELECT * 
FROM TENKTUP1 
WHERE unique2 BETWEEN 3792 AND 18764;
```

Performance metrics this query aims to test:
* Projection of large range of elements
* Measure raw efficiency of plan, due to an index not having an effect when > 10% of data is needed to be searched. 

Results:

|Times | Postgres  |   MySQL   |
|------|:---------:|:---------:|
| low  |  .862ms   |  .3ms     |
| mid  |  .870ms   |  .4ms     |
| high |  .924ms   |  .4ms     |
| avg: |  .885ms   |  .36ms    |



#### Query 2 - Basic SELECT & Projection
```sql
SELECT two, ten, stringu1 
FROM TENKTUP1 
WHERE unique1 BETWEEN 5400 AND 79999;
```

Performance metrics this query aims to test:
* Project for few attributes over a smaller range
* Measure raw efficiency of plan, due to an index not having an effect when > 10% of data is needed to be searched. 

Results:

|Times | Postgres  |   MySQL   |
|------|:---------:|:---------:|
| low  |  .871ms   |  .3ms     |
| mid  |  .949ms   |  .3ms     |
| high |  .953ms   |  .3ms     |
| avg: |  .924ms   |  .3ms     |



#### Query 3 - JOIN With Small & Large Tables
```sql
SELECT * 
FROM TENKTUP1, ONEMILTUP
WHERE (TENKTUP1.unique2 = ONEMILTUP.unique2);
```

Performance metrics this query aims to test:
* Efficiency of `JOIN` operation between a small data set and large data set
* Ability of DBMS to construct an effcient plan consistently
* Measure if caching is happening for either DBMS/Efficiency of buffer pool.

Results:

|Times | Postgres  |   MySQL   |
|------|:---------:|:---------:|
| low  |  1.38ms   |  1.5ms    |
| mid  |  1.52ms   |  1.5ms    |
| high |  1.56ms   |  1.6ms    |
| avg: |  1.48ms   |  1.56ms   |

> Note: For MySQL, the slowest query was the first which took 31.1ms to complete, whereas Postgres' slowest was 2.274ms on the fourth round.


#### Query 4 - JOIN With Small & Large tables + Match Predicate
```sql
SELECT * FROM TENKTUP1, ONEMILTUP 
WHERE (TENKTUP1.unique1 = ONEMILTUP.unique1) AND (TENKTUP1.unique1<4532)
```

Performance metrics this query aims to test:
* Efficiency of `JOIN` operation between a small data set and large data set with added predicate
* Ability of DBMS to construct an effcient plan consistently
* Measure if caching is happening for either DBMS/Efficiency of buffer pool.

Results:

| Times| Postgres  |   MySQL   |
|------|:---------:|:---------:|
| low  |  1.34ms   |  1.4ms    |
| mid  |  1.35ms   |  1.5ms    |
| high |  1.38ms   |  1.5ms    |
| avg: |  1.36ms   |  1.46ms   |

> Note: MySQL did not have a significantly slower time of execution for the first round, which has been common for the `JOINS` in the tests.




#### Query 5
```sql
SELECT tenktup1.unique2, COUNT(*)
FROM tenktup1 JOIN onemiltup on tenktup1.unique2 = onemiltup.odd100
GROUP BY tenktup1.unique2
ORDER BY tenktup1.unique2;
```

Performance metrics this query aims to test:
* Efficientcy of `JOIN` with aggregate and sort applied
* Efficiency of `JOIN` operation between a small data set and large data set with added predicate
* Ability of DBMS to construct an effcient plan consistently
* Measure if caching is happening for either DBMS/Efficiency of buffer pool.

Results:

|Times | Postgres  |   MySQL   |
|------|:---------:|:---------:|
| low  |  1.77ms   |  .8ms    |
| mid  |  1.88ms   |  .9ms    |
| high |  2.11ms   |  .9ms    |
| avg: |  1.92ms   |  .86ms   |


> Note: For MySQL, the slows was the first which took 2.92 seconds to complete, whereas Postgres' slowest was 4.724ms in the last round. 

## Lessons Learned
