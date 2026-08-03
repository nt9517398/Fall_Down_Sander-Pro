WITH total_production AS (
    SELECT COUNT(*) AS total_boards
    FROM production
    WHERE "t_stamp" >= :startDate
      AND "t_stamp" < :endDate
)

SELECT 
    d."Description",
    COUNT(d.downfall_table_ndx) AS downfall_count,
    ROUND(
        (COUNT(d.downfall_table_ndx) * 100.0 / t.total_boards),
        2
    ) AS percent_of_total,
    t.total_boards
FROM downfall_table d
CROSS JOIN total_production t
WHERE d."t_stamp" >= :startDate
  AND d."t_stamp" < :endDate
GROUP BY d."Description", t.total_boards
ORDER BY downfall_count DESC;
