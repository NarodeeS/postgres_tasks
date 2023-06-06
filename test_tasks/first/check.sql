CREATE OR REPLACE FUNCTION check_task_function() RETURNS bool
AS
$$
    DECLARE
        all_money MONEY;
        avg_money MONEY;
    BEGIN
        all_money = (SELECT all_money FROM hero_money_table LIMIT 1);
        avg_money = (SELECT avg_money FROM hero_money_table LIMIT 1);
        IF all_money = 112.2 AND avg_money = 56.1 THEN
            RETURN true;
        ELSE
            RETURN false;
        end if;
END;$$
LANGUAGE plpgsql;

SELECT check_task_function();
