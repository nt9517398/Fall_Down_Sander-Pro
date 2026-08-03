SELECT
    COUNT(*) FILTER (WHERE "ClassA" IN (1, 2)) AS non_structural,
    COUNT(*) FILTER (WHERE "ClassA" IN (3, 4)) AS pallet_grade,
    COUNT(*) FILTER (WHERE "ClassA" = 5) AS rejects
FROM downfall_table
WHERE "t_stamp" >= :loginTime
  AND "t_stamp" <= CURRENT_TIMESTAMP;