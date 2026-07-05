INSERT INTO users (name, email)
VALUES ('Sidor Sidorov', 'sidor.sidorov@example.com');

INSERT INTO user_skills (user_id, skill_id, level, updated_at)
SELECT u.id, s.id, lvl.level, CURRENT_DATE
FROM users u
JOIN skills s ON s.name IN ('SQL', 'Time Management', 'Python')
JOIN (VALUES (4), (3), (4)) AS lvl(level) ON TRUE
WHERE u.name = 'Sidor Sidorov';

-- Найдите всех пользователей, чьи имена начинаются на "A" или заканчиваются на "ov", и у которых email не пустой.
SELECT * FROM users WHERE (name LIKE 'A%' OR name LIKE '%ov') AND email IS NOT NULL;

-- Получите 3 последних ресурса по id и отсортируйте их по title в алфавитном порядке.
SELECT * FROM resources
ORDER BY id DESC, title ASC
LIMIT 3;

-- Покажите user_id и количество навыков (user_skills), только для тех пользователей, у которых больше 2 навыков
SELECT user_id, csi FROM
	(SELECT user_id, COUNT(skill_id) AS csi FROM user_skills
	GROUP BY user_id) us
WHERE us.csi > 2;

-- Посчитайте:
-- ○ Сколько всего пользователей в таблице
SELECT COUNT(*) FROM users;
-- ○ Сколько пользователей указали email
SELECT COUNT(email) FROM users;
-- ○ Среднюю длину email (используйте LENGTH(email) и AVG)
SELECT AVG(LENGTH(email)) FROM users;
