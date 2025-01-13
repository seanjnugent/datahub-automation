-- Update the nino column with randomly generated valid NINOs
WITH generate_nino AS (
    SELECT 
        CHR(ASCII('A') + (FLOOR(RANDOM() * 20))::INT) AS first_letter,  -- A-CEGHJ-PR-TW-Z
        CHR(ASCII('A') + (FLOOR(RANDOM() * 20))::INT) AS second_letter, -- A-CEGHJ-NPR-TW-Z
        LPAD((FLOOR(RANDOM() * 1000000))::TEXT, 6, '0') AS digits,     -- 000001-999999
        CHR(ASCII('A') + (FLOOR(RANDOM() * 4))::INT) AS suffix          -- A-D
)
UPDATE test_data
SET nino = (
    SELECT 
        first_letter || second_letter || digits || suffix
    FROM generate_nino
)
WHERE nino IS NULL; -- Update only rows where nino is NULL
