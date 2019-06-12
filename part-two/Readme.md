
### Query 1
```sql
SELECT * 
FROM TENKTUP1 
WHERE unique2 BETWEEN 3792 AND 18764;
```

What perf metrics does this query test:
* Projection of large range of elements
* Tests raw efficiency of plan, due to an index not having an effect (need to scan whole table)


### Query 2
```sql
SELECT two, ten, stringu1 
FROM TENKTUP1 
WHERE unique1 BETWEEN 5400 AND 79999;
```
What perf metrics does this query test:
* 



### Query 3
```sql
SELECT * 
FROM TENKTUP1, TENKTUP2 
WHERE (TENKTUP1.unique2 = TENKTUP2 .unique2);
```


### Query 4
```sql
SELECT * FROM TENKTUP1, TENKTUP2 
WHERE (TENKTUP1.unique1 = TENKTUP2 .unique1) AND (TENKTUP1.unique1<4532)
```


### Query 5
```sql
SELECT tenktup1.unique2, COUNT(*)
FROM tenktup1 JOIN tenktup2 on tenktup1.unique2 = tenktup2.odd100
GROUP BY tenktup1.unique2
ORDER BY tenktup1.unique2;
```
