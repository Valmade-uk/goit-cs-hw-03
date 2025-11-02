-- task1_postgres/queries.sql

-- 1. Отримати всі завдання певного користувача (за user_id = 1)
SELECT t.*
FROM tasks t
WHERE t.user_id = 1;

-- 2. Вибрати завдання за певним статусом (наприклад 'new')
SELECT t.*
FROM tasks t
WHERE t.status_id = (
    SELECT s.id FROM status s WHERE s.name = 'new'
);

-- 3. Оновити статус конкретного завдання (id = 5) на 'in progress'
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 5;

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT u.*
FROM users u
WHERE u.id NOT IN (
    SELECT DISTINCT t.user_id FROM tasks t
);

-- 5. Додати нове завдання для конкретного користувача (user_id = 2)
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'New task for user 2',
    'Some description',
    (SELECT id FROM status WHERE name = 'new'),
    2
);

-- 6. Отримати всі завдання, які ще не завершено (status != 'completed')
SELECT t.*
FROM tasks t
JOIN status s ON t.status_id = s.id
WHERE s.name <> 'completed';

-- 7. Видалити конкретне завдання (id = 10)
DELETE FROM tasks
WHERE id = 10;

-- 8. Знайти користувачів з певною електронною поштою (наприклад, що містить 'gmail')
SELECT *
FROM users
WHERE email LIKE '%gmail%';

-- 9. Оновити ім'я користувача (id = 3)
UPDATE users
SET fullname = 'Updated User Name'
WHERE id = 3;

-- 10. Отримати кількість завдань для кожного статусу
SELECT s.name AS status, COUNT(t.id) AS tasks_count
FROM status s
LEFT JOIN tasks t ON t.status_id = s.id
GROUP BY s.name
ORDER BY tasks_count DESC;

-- 11. Отримати завдання, які призначені користувачам з певною доменною частиною
-- (наприклад, '@example.com')
SELECT t.*
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@example.com';

-- 12. Отримати список завдань, що не мають опису
SELECT *
FROM tasks
WHERE description IS NULL OR description = '';

-- 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
SELECT u.fullname, u.email, t.title, t.description
FROM users u
JOIN tasks t ON u.id = t.user_id
JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress';

-- 14. Отримати користувачів та кількість їхніх завдань
SELECT u.id,
       u.fullname,
       u.email,
       COUNT(t.id) AS tasks_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.id, u.fullname, u.email
ORDER BY tasks_count DESC;
