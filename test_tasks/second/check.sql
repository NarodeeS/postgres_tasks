CREATE FUNCTION check_task() RETURNS bool
AS
$$
    DECLARE
        rows_count INT;
        fk_checker INT;
    BEGIN
        rows_count := (SELECT count(*) FROM orders);
        fk_checker := (SELECT COUNT(1) FROM information_schema.table_constraints WHERE constraint_name='orders_book_id_fkey' AND table_name='orders');
        IF rows_count = 3 AND fk_checker = 1 THEN
            RETURN true;
        ELSE
            RETURN false;
        end if;
END;$$
LANGUAGE plpgsql;

SELECT check_task();