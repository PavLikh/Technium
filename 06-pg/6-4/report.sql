-- Задача 1.
-- Сформируйте список пользователей, которые:
-- 1. имеют хотя бы один ресурс в статусе In Progress,
-- 2. и имя пользователя:
	-- a. либо состоит только из цифр,
	-- b. либо содержит 3 одинаковых символа подряд (например, aaa, 111, ***)
SELECT * FROM users
WHERE id IN
(SELECT user_id FROM public.user_resource_progress
	WHERE status_id IN 
 	(SELECT id FROM dictionaries WHERE name = 'In Progress'))
AND name ~ '\d|(.)\1{2}';


-- Задача 2. Анализ прогресса с оконными функциями
-- Для каждого пользователя рассчитайте:
-- 1. количество всех ресурсов,
-- 2. средний прогресс,
-- 3. номер по порядку ресурса внутри полþзователā (по убыванию прогресса),
-- 4. разницу между прогрессом текушего ресурса и предыдушего (если есть)
SELECT user_id, resource_id, progress_percent,
	AVG(resource_id) OVER (PARTITION BY user_id),
	COUNT(resource_id) OVER (PARTITION BY user_id),
	ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY progress_percent DESC),
	LAG(progress_percent) OVER (PARTITION BY user_id) - progress_percent AS diff_from_prev
FROM user_resource_progress;


-- Задача 3. Представление с использованием CTE
-- Создайте представление user_progress_overview, в котором с помоûþĀ
-- WITH-CTE длā каждого полþзователā рассùитýваĀтсā:
-- 1. обûее колиùество ресурсов,
-- 2. колиùество заверúённýх (status_id = 7),
-- 3. средний проøент прогресса (с округлением до 1 знака).
CREATE VIEW user_progress_overview AS
WITH user_stats AS (
    SELECT
        user_id,
        COUNT(*) AS total_by_user,
        COUNT(*) FILTER (WHERE status_id = 7) AS completed,
        AVG(progress_percent) AS avg_progress_by_user
    FROM user_resource_progress
    GROUP BY user_id
)
SELECT
	user_id,
    total_by_user,
    completed,
    ROUND(avg_progress_by_user, 1) AS avg_progress_percent
FROM user_stats;
