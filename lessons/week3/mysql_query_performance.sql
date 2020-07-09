use employees;

-- This database contains 6 tables (and 2 views).
select table_name, table_rows from information_schema.TABLES
where table_schema = 'employees' and table_type = 'BASE TABLE'
order by table_rows desc;

-- This database's storage engine is "InnoDB".
-- (InnoDB became MySQL's default engine in December 2010, replacing "MyISAM".)
SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='employees'
and TABLE_TYPE = 'BASE TABLE';

-- Next, a series of queries for which Visual Explain selects different
-- display colours (as shown by pressing Control-Alt-x).

-- (WHICH COLOUR?):
select max(from_date) from salaries where emp_no = 18888;

-- (WHICH COLOUR?):
select * from departments where dept_no = 'd008';

-- (WHICH COLOUR?):
select * from salaries where emp_no = 18888;

-- (WHICH COLOUR?):
-- [I added this myself: CREATE FULLTEXT INDEX ft_idx_first_name ON employees(first_name);]
-- MATCH(...) ... AGAINST(...) is specifically for these specialised indexes.
select * from employees where match(first_name) against('Mary');

-- (WHICH COLOUR?):
select * from dept_manager where dept_no in ('d005', 'd008');  -- Either Sales or Research

-- (WHICH COLOUR?):
-- set profiling=1;  -- MySQL Workbench's Query Stats tab gives us friendlier outputs.
select emp_no from salaries where from_date between '1999-12-01' and '1999-12-31';
select max(hire_date) from employees;
-- show profile;     -- See above comment re: Query Stats.


-- Next, speeding up the three red and orange queries above.

-- A table scan, hence a "red query":
select max(hire_date) from employees;
create index idx_employees_hd ON employees(hire_date);
-- show indexes from employees;  -- "show indexes" is per table, not per DB.
-- drop index idx_employees_hd ON employees;  -- To undo

-- A full index scan, hence a "red query":
select emp_no from salaries where from_date between '1999-12-01' and '1999-12-31';
create index idx_salaries_fd_en on salaries(from_date, emp_no);
-- drop index idx_salaries_fd_en on salaries;

-- An index range scan, hence an "orange query":
select * from dept_manager where dept_no in ('d005', 'd008');


-- FYI, MySQL stores its basic cost assumptions in two tables.
select cost_name, default_value from mysql.server_cost
union
select cost_name, default_value from mysql.engine_cost
order by default_value desc;

-- Let's look at the internal statistics for this database.
SELECT * FROM INFORMATION_SCHEMA.STATISTICS WHERE table_name = 'salaries' AND table_schema = 'employees';
-- We have to run "analyze table" first to populate the column_statistics table:
analyze table salaries update histogram on emp_no, from_date;
SELECT * FROM INFORMATION_SCHEMA.COLUMN_STATISTICS;  -- Each histogram is stored as a blob of JSON.
SELECT TABLE_NAME, COLUMN_NAME,
	   HISTOGRAM->>'$."data-type"' AS 'data-type',
	   JSON_LENGTH(HISTOGRAM->>'$."buckets"') AS 'bucket-count'
FROM INFORMATION_SCHEMA.COLUMN_STATISTICS;
