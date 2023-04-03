CREATE DATABASE IF NOT EXISTS open_datadb
COMMENT 'This database contains information about salaries from Chicago';

USE open_datadb;


DROP TABLE IF EXISTS employee;

CREATE EXTERNAL TABLE IF NOT EXISTS employee (
  name STRING,
  job_titles STRING,
  department STRING,
  full_or_part_time STRING,
  salary_or_hourly STRING,
  typical_hours STRING,
  annual_salary STRING,
  hourly_rate STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
TBLPROPERTIES("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH './workspace/data.csv' OVERWRITE INTO TABLE employee;



