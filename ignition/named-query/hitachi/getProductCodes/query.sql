SELECT
    product_code AS value,
    product_code AS label
FROM hitachi_messages
WHERE enabled = TRUE
ORDER BY product_code;