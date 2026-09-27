-- Задача 1. Хранимая процедура
CREATE OR REPLACE PROCEDURE update_progress_bulk (
	IN p_resource_id INT,
	IN p_increment INT
)
LANGUAGE plpgsql
AS $$
DECLARE
	rows_updated INTEGER;
BEGIN
	UPDATE public.user_resource_progress
	SET progress_percent = LEAST(progress_percent + p_increment, 100)
	WHERE resource_id = p_resource_id
		AND progress_percent < 100;
	GET DIAGNOSTICS rows_updated = ROW_COUNT;
		
	RAISE NOTICE '% rows has updated', rows_updated;
END;
$$;

-- Задача 2. Пользовательская функция
CREATE OR REPLACE FUNCTION get_user_skill_level(f_user_id INT, f_skill_id INT)
RETURNS INT
AS $$
	SELECT level
	FROM public.user_skills
	WHERE user_id = f_user_id
		AND skill_id = f_skill_id;
$$ LANGUAGE sql;

-- Задача 3. Триггер
CREATE TABLE IF NOT EXISTS user_skills_log (
	id SERIAL PRIMARY KEY,
	user_id int NOT NULL,
	skill_id int NOT NULL,
	level int NOT NULL,
	updated_at date NOT NULL,
	operation TEXT
);

CREATE OR REPLACE FUNCTION after_log_user_skills_change()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        INSERT INTO user_skills_log (user_id, skill_id, level, updated_at, operation)
        VALUES (
            NEW.user_id,
            NEW.skill_id,
            NEW.level,
            CURRENT_DATE,
            'update'
        );
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO user_skills_log (user_id, skill_id, level, updated_at, operation)
        VALUES (
            NEW.user_id,
            NEW.skill_id,
            NEW.level,
            CURRENT_DATE,
            'insert'
        );
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_user_skills_log
AFTER INSERT OR UPDATE ON user_skills
FOR EACH ROW
EXECUTE FUNCTION after_log_user_skills_change();

-- Проверка
-- UPDATE user_skills SET
-- level = 2
-- WHERE id = 20;

-- INSERT INTO user_skills (user_id,skill_id,level, updated_at)
-- VALUES (1,10,100,NOW());

-- SELECT * FROM user_skills;
-- SELECT * FROM user_skills_log;

-- Задача 4.
-- 1 SELECT * FROM user_skills WHERE user_id = ?;
CREATE INDEX idx_user_id ON user_skills(user_id);

-- 2 SELECT * FROM user_skills WHERE user_id = ? AND skill_id = ?;
CREATE INDEX idx_user_skill ON user_skills(user_id, skill_id);

-- 3 SELECT * FROM user_resource_progress WHERE resource_id = ? AND progress_percent < 100;
CREATE INDEX idx_user_in_process ON user_resource_progress(resource_id)
	WHERE progress_percent < 100;

-- 4 SELECT * FROM users WHERE LOWER(email) = 'some@email.com';
CREATE INDEX idx_lower_email ON users (LOWER(email));

-- 5 SELECT user_id, progress_percent FROM user_resource_progress WHERE resource_id = ?;
CREATE INDEX idx ON user_resource_progress(user_id)
	INCLUDE (resource_id);
