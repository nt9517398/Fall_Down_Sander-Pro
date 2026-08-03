DELETE FROM downfall_table
WHERE downfall_table_ndx = (
    SELECT downfall_table_ndx
    FROM downfall_table
    ORDER BY t_stamp DESC
    LIMIT 1
);
