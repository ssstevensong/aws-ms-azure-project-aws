CREATE DATABASE IF NOT EXISTS churn_project;

CREATE TABLE IF NOT EXISTS churn_project.telco_churn_clean (
  gender string,
  seniorcitizen int,
  partner int,
  dependents int,
  tenure int,
  phoneservice int,
  multiplelines string,
  internetservice string,
  onlinesecurity string,
  onlinebackup string,
  deviceprotection string,
  techsupport string,
  streamingtv string,
  streamingmovies string,
  contract string,
  paperlessbilling int,
  paymentmethod string,
  monthlycharges double,
  totalcharges double,
  churn int
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://YOUR_BUCKET_NAME/churn-project/processed/'
TBLPROPERTIES (
  'skip.header.line.count' = '1'
);

SELECT
  contract,
  COUNT(*) AS customers,
  ROUND(AVG(churn), 4) AS churn_rate
FROM churn_project.telco_churn_clean
GROUP BY contract
ORDER BY churn_rate DESC;
