CREATE OR REPLACE FUNCTION search_phone(pattern TEXT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name,c.phone
    FROM basement c
    WHERE c.first_name ILIKE '%' || pattern || '%'
       OR c.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_phone_paginated(limit_val INT, offset_val INT)
RETURNS TABLE (
    id INT,
    first_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM basement
    ORDER BY id
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;