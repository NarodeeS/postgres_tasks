CREATE OR REPLACE FUNCTION check_task_function() RETURNS bool
AS
$$
    DECLARE
        all_money_check NUMERIC;
        avg_money_check NUMERIC;
    BEGIN
        all_money_check := (SELECT all_money FROM hero_money_table LIMIT 1);
        avg_money_check := (SELECT avg_money FROM hero_money_table LIMIT 1);
        IF all_money_check = 112.2 AND avg_money_check = 56.1 THEN
            RETURN true;
        ELSE
            RETURN false;
        end if;
END;$$
LANGUAGE plpgsql;

SELECT check_task_function();