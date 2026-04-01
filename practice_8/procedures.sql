CREATE OR REPLACE PROCEDURE upsert(p_names VARCHAR,p_phones VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    
    IF EXISTS(
        SELECT 1
        FROM basement
        WHERE first_name=p_names
    )
    THEN 
        UPDATE basement
        SET phone=p_phones
        WHERE first_name=p_names;
    ELSE
        INSERT INTO basement(first_name,phone) 
        VALUES(p_names,p_phones);

    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_phone(
    names TEXT[],
    phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1)
    LOOP

        IF phones[i] !~ '^\+\d{10,15}$' THEN
            RAISE NOTICE 'Invalid phone: %', phones[i];
        ELSE
            INSERT INTO phone(first_name, phone)
            VALUES (names[i], phones[i])
            ON CONFLICT (phone) DO NOTHING;
        END IF;

    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_user(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    DELETE FROM basement
    WHERE first_name = p_value
       OR phone = p_value;

END;
$$;
