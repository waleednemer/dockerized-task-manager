CREATE TABLE IF NOT EXISTS tasks (
    id         SERIAL PRIMARY KEY,
    title      VARCHAR(200) NOT NULL,
    status     VARCHAR(10)  NOT NULL DEFAULT 'todo'   CHECK (status IN ('todo','doing','done')),
    priority   VARCHAR(10)  NOT NULL DEFAULT 'medium' CHECK (priority IN ('low','medium','high')),
    due_date   DATE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
INSERT INTO tasks (title, priority, due_date) VALUES
 ('مراجعة ملف الـ Dockerfile', 'high', CURRENT_DATE + 1),
 ('كتابة اختبارات للـ API', 'medium', NULL);
