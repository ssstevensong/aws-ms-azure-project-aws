SELECT
  risk_level,
  COUNT(*) AS customers,
  ROUND(AVG(churn_probability), 4) AS avg_churn_probability,
  ROUND(AVG(actual_churn), 4) AS actual_churn_rate
FROM churn_project.customer_churn_scores
GROUP BY risk_level
ORDER BY
  CASE risk_level
    WHEN 'High' THEN 1
    WHEN 'Medium' THEN 2
    WHEN 'Low' THEN 3
    ELSE 4
  END;

SELECT
  risk_level,
  contract,
  COUNT(*) AS customers,
  ROUND(AVG(actual_churn), 4) AS actual_churn_rate
FROM churn_project.customer_churn_scores
GROUP BY risk_level, contract
ORDER BY risk_level, actual_churn_rate DESC;
