CREATE TABLE hero_money_table AS (
    SELECT SUM(heroMoney) AS all_money, AVG(heroMoney) AS avg_money FROM hero
);