CREATE OR REPLACE FUNCTION check_task() RETURNS bool
AS
$$
    DECLARE
        rows_count INT;
    BEGIN
        rows_count = (SELECT count(*) FROM orders);
        IF rows_count = 4 THEN
            RETURN true;
        ELSE
            RETURN false;
        end if;
END;$$
LANGUAGE plpgsql;

SELECT check_task();
