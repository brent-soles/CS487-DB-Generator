# CS487/587 Spring 2019
## Project Part II
### By: Mingjue Wang & Brent Daniels-Soles

# Part II Overview

Given our initial experiments with MySQL and Postgres, it was decided the best course of action would be to compare MySQL and Postgres for the benchmark segment of this project. The reason being, is we wanted to structure our benchmark experiments to give an idea of how each of the respective systems perfrom out of the box.

The reason for leaving each system in their default configuration is because of the fact most side and hobby projects, and possibly startups, use these systems in their default state rather than fine tuning it before beginning to build any application. With our benchmark, we hope to examine which system may be better for building a performant application withouth having to adjust any settings. In addition, our benchmark aims to test the consistency of each platform by running each test in the benchmark multiple times.

## Hypothesis
The hypothesis we have for the experiments in this benchmark is: MySQL and Postrgres should have similar performance for the simpler queries of the benchmark. However, once they systems are executing `JOIN` statements, we think Postgres will be more performant than MySQL, due to MySQL only implementing nested loop joins (See 'Joins' in 'System Research' section for more information).

---
# System Research

The following information about each of the systems is sourced from the offical Postgres and MySQL docs.
Below are the respective links to each of the documentation pages:
* MySQL: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
* PosgreSQL: [https://www.postgresql.org/docs/9.1/ ](https://www.postgresql.org/docs/9.1/ )

For each of the databases, we tried to dig into the features which would be involved in our tests.

The subsections represent how indicies, joins, and the buffer pool are used in each of the systems.

## Indices
#### Postgres
Posgres has a few different index 'types' (types in this case referring to data structures) which can be utilized in relations. They are as follows:
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

At a high level, Postgres constructs queries based off of the indices currently defined on the relation, and from there, conducts a near-exhaustive search of various query plans in order to derive the best one. However, the near-exhaustive search is only conducted when querying smaller amounts of data, as there can be huge, system-wide ramifications when performing a near-exhaustive search on large data sets. When joining big data together, Postgres uses what is called a “genetic algorithm” to attempt to discern the best query plan for large/join heavy operations. The optimizations made for computationally expensive queries are mainly based upon heuristics which are determined by a form of randomization.

#### MySQL
In the documentation for MySQL, specifically in the introductary chapter (1.3.2), it is specified MySQL utilizes an optimized nested loop join algorithm and another variant of the nested loop join. No other type of `JOIN` algorithm(for example: Hash Join), is implemented in MySQL.

Currently, the two types of nested loop joins MySQL implements are:

* Nested Loop Join
* Block Nested Loop Join

The Nested Loop Join is pretty straightforward: for each row in TableA, loop over TableB and see if the join predicate is satisfied. If the join predicate is satisfied, then add the combination of each of the rows to the output.

The Block Nested Loop Join is similar to the Nested Loop Join, however, works a bit differently, What Block Nested Loop Join does, is once a row is read from the outer table, it is sent to a buffer called the 'join_buffer'. The 'join_buffer' acts as an in-memory cache of each row seen for a given `JOIN` query. This prevents the DBMS from having to constantly make calls to the buffer pool/Disk Manage, and allows for the query engine to access the buffer for rows that have already been seen. Given the example above with TableA and TableB: for each row in TableA, TableB is looped over, however, TableB is in the 'join_buffer', so the access to each row is already in memory. This makes accessing each row have a lower overhead, instead of constantly making calls to the Disk Manager/Buffer pool for rows that have already been seen. 


## Buffer Pools
#### Postgres
For this section, I reference the following articles:

* Postgres buffer manager: http://www.interdb.jp/pg/pgsql08.html

The Postgres buffer pool is constructed from what are called ‘slots’. A slot is the equivalent of a page in any other DBMS. Each slot holds 8KB of data; the same amount as a page in memory. Once data has been loaded into a slot in the buffer pool, the algorithm that manages which pages are evicted, is the clock algorithm. In addition when Postgres detects it is set to read large amounts of data, the system will allocate a Ring buffer on the side (basically an on-demand small amount of data to store temporary data) in order to improve buffer performance.

#### MySQL
Digging through the MySQL docs, we were unable to land on a definite answer for the default size of pages or the default size of memory MySQL is allocated. The docs mentioned this aspect is left up to user discretion. Despite the documentation being vauge about the storage size, the docs go on to detail MySQL uses a variation of the Least Recently Used algorithm in order to determine which pages will be evicted from the buffer pool. The LRU algorithm employed by MySQL uses a head and tail pointer to track older/inactive pages and newer/active pages, respectively. Everything the the ‘old’ list is candidate for eviction when a need for space arises.

--- 
# Performance Experiment Design
## Overview

For each of the tests, we wanted to see how the systems would perform for small, medium and large sets of data. Given some of the insights gained from the class about how databases behave when constructing query plans, we structured the query tests to first get a baseline as to how the respective system perform with *'smaller'* relations, with each query getting more complex and computationally expensive. The first two queries are basic `SELECT` statements, and the rest are focused on analyzing the performance of each systems `JOIN` algorithm.

The main part of this benchmark is centered around each systems `JOIN` execution. The reason we decided to have this benchmark focus mainly on `JOIN`'s, is becuase they are historically the most expensive query type to execute and because of the variance between the two systems in the way they implement `JOIN`'s.

## Data Used In Tests

There are three tables that we use in these tests, each being generated using the guidelines set forth in the Wisconsin Benchmark paper. The following tables are:

* TENKTUP1 (10,000 rows of data)
* TENKTUP2 (10,000 rows of data)
* ONEMILTUP (1,000,000 rows of data)

Originally, the benchmark did not exceed 10,000 relations for any given table, and did not included the ONEMILTUP as part of the benchmark. The reason we decided to include this table, was to mock a system which deals with amount of data one would see in industry. 

---
### Experiment Queries
Below are each of the queries


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




#### Query 5 - JOIN With Small & Large tables + GROUP/SORT + Aggregate
```sql
SELECT TENKTUP1.unique2, COUNT(*)
FROM TENKTUP1 JOIN ONEMILTUP on TENKTUP1.unique2 = ONEMILTUP.odd100
GROUP BY TENKTUP1.unique2
ORDER BY TENKTUP1.unique2;
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

### Performance Section Conclusion

For smaller queries MySQL does outperform Posgres by a decent margin (~.5-.6ms), which is what we hypothesized would happen. However, where we were off slightly on our hypothesis, is MySQL being less performant for `JOIN` operations. While MySQL did have some slow queries for larger sets of data, the `JOIN` operation proved to be very quick once relations were loaded into the join_buffer.

## Lessons Learned

One of the big lessons learned throught this portion of the project, has been critically analyzing a DBMS as a whole rather than taking a system such as Postgres or MySQL at face value. Part of the analysis process was identifying each system's tradeoffs. For instance, a tradeoff with MySQL is the potential to have occasional long running queries at the benefit of a large portion of queries executing efficiently (less query execution consistency). In comparison, a tradeoff with Postgres would be having consistently slower queries, but having each of those querys execute in a fairly consistent manner.

Finally, we learned that when it comes to building a performant application, it is about using the right tool for the right job. If speed is necessary, use a DBMS which is know to be performant. If consistency and resiliance is desired for your application, choose one which will fit that need, rather than trying to get another technology to fit into a use case it was not designed for.