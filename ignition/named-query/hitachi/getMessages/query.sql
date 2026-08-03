SELECT
    message1_line1,
    message1_line2,
    message2_line1,
    message2_line2,
    message3_line1,
    message3_line2,
    message4_line1,
    message4_line2
FROM hitachi_messages
WHERE product_description = :productDescription
  AND enabled = TRUE
LIMIT 1;