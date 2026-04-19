task 1

v1
SELECT * FROM EMPLOYEES;

SELECT LAST_NAME, COUNT(*) as cnt
FROM EMPLOYEES
GROUP BY LAST_NAME
HAVING COUNT(*) > 1;


DELETE FROM EMPLOYEES
WHERE ctid NOT IN (
    SELECT MAX(ctid)
    FROM EMPLOYEES
    GROUP BY LAST_NAME
);



v2
SELECT * FROM EMPLOYEES;

SELECT LAST_NAME, COUNT(*) as cnt
FROM EMPLOYEES
GROUP BY LAST_NAME
HAVING COUNT(*) > 1;


DELETE FROM EMPLOYEES
WHERE ctid IN (
    SELECT ctid FROM (
        SELECT ctid,
               ROW_NUMBER() OVER (
                   PARTITION BY LAST_NAME
                   ORDER BY ctid DESC
               ) as rn
        FROM EMPLOYEES
    ) sub
    WHERE rn > 1
);





----------------------------------------------------------------------------------
task 2


SELECT e.LAST_NAME, e.DEPARTMENT_ID, d.DEPARTMENT_NAME
FROM EMPLOYEES e
LEFT JOIN DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID;


SELECT d.DEPARTMENT_NAME, AVG(e.SALARY) as avg_salary
FROM EMPLOYEES e
LEFT JOIN DEPARTMENTS d ON e.DEPARTMENT_ID = d.DEPARTMENT_ID
GROUP BY d.DEPARTMENT_NAME;





----------------------------------------------------------------------------------
task 3


SELECT DEPT_ID,
    MIN(SALARY) as min_salary,
    MAX(SALARY) as max_salary
FROM EMPLOYEES
GROUP BY DEPT_ID
HAVING MIN(SALARY) < 5000 AND MAX(SALARY) > 15000;





----------------------------------------------------------------------------------
task 4


Запит завершиться помилкою.
PostgreSQL не дозволить видалити запис із DEPARTMENTS, доки в таблиці EMPLOYEES є співробітники,
які посилаються на цей відділ.
Це поведінка таблиць із налаштуванням ON DELETE RESTRICT - забороняє видалення,
якщо є пов’язані записи




----------------------------------------------------------------------------------
task 5


Запит завершиться синтаксичною помилкою
DELETE видаляє рядок повністю
До перевірки NOT NULL та пошуку dept_id = 90 справа взагалі не дійде

