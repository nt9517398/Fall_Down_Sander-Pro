SELECT COUNT(*) AS "2A_Count"
FROM downfall_table
WHERE "Description" = :description
  AND "Documentation" = :documentation
  AND "ClassA" = :classa
  AND "t_stamp" >= :loginTime;


