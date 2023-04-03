CREATE DATABASE IF NOT EXISTS open_datadb
COMMENT 'This database contains information about salaries from Chicago';

USE open_datadb;

CREATE EXTERNAL TABLE IF NOT EXISTS employee (
  name STRING,
  job_titles STRING,
  department STRING,
  full_or_part_time STRING,
  salary_or_hourly STRING,
  typical_hours INT,
  annual_salary DOUBLE,
  hourly_rate DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE;