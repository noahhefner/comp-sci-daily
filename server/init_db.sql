-- PostgreSQL Database Initialization Script
-- Computer Science Daily Trivia Database

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create questions table
CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question TEXT NOT NULL,
    difficulty VARCHAR(50) NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on date for efficient today's question lookup
CREATE INDEX IF NOT EXISTS idx_questions_date ON questions(date);

-- Create choices table
CREATE TABLE IF NOT EXISTS choices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    choice_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on question_id for efficient choice lookup
CREATE INDEX IF NOT EXISTS idx_choices_question_id ON choices(question_id);

-- Create answers table
CREATE TABLE IF NOT EXISTS answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    answer VARCHAR(1) NOT NULL CHECK (answer IN ('A', 'B', 'C', 'D', 'E', 'F')),
    explanation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on question_id for efficient answer lookup
CREATE INDEX IF NOT EXISTS idx_answers_question_id ON answers(question_id);

-- Create users table (for future user tracking/analytics)
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    auth0_sub VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create user_answers table (for tracking user responses)
CREATE TABLE IF NOT EXISTS user_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    selected_answer VARCHAR(1) NOT NULL CHECK (selected_answer IN ('A', 'B', 'C', 'D', 'E', 'F')),
    is_correct BOOLEAN NOT NULL,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for user_answers
CREATE INDEX IF NOT EXISTS idx_user_answers_user_id ON user_answers(user_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_question_id ON user_answers(question_id);
CREATE INDEX IF NOT EXISTS idx_user_answers_answered_at ON user_answers(answered_at);

-- Create a view for user statistics (optional, for analytics)
CREATE OR REPLACE VIEW user_stats AS
SELECT 
    u.id,
    u.email,
    COUNT(DISTINCT ua.question_id) as total_questions_answered,
    SUM(CASE WHEN ua.is_correct THEN 1 ELSE 0 END) as correct_answers,
    ROUND(100.0 * SUM(CASE WHEN ua.is_correct THEN 1 ELSE 0 END) / 
        NULLIF(COUNT(DISTINCT ua.question_id), 0), 2) as accuracy_percentage
FROM users u
LEFT JOIN user_answers ua ON u.id = ua.user_id
GROUP BY u.id, u.email;

-- Insert sample data for development

-- Question 1: Easy - Big O Notation
INSERT INTO questions (question, difficulty, date) 
VALUES ('What is the time complexity of binary search?', 'easy', CURRENT_DATE)
RETURNING id INTO q1_id;

INSERT INTO choices (question_id, choice_text) 
SELECT q1_id, choice_text FROM (VALUES 
    ('O(n)'),
    ('O(log n)'),
    ('O(n²)'),
    ('O(n log n)'),
    ('O(2^n)')
) AS t(choice_text);

INSERT INTO answers (question_id, answer, explanation)
VALUES ((SELECT id FROM questions WHERE question = 'What is the time complexity of binary search?' LIMIT 1), 
        'B', 
        'Binary search divides the search space in half with each iteration, resulting in O(log n) time complexity. This is much more efficient than linear search which is O(n).');

-- Question 2: Medium - Database Indexing
INSERT INTO questions (question, difficulty, date) 
VALUES ('What is the primary advantage of using an index on a database column?', 'medium', CURRENT_DATE)
RETURNING id INTO q2_id;

INSERT INTO choices (question_id, choice_text) 
SELECT q2_id, choice_text FROM (VALUES 
    ('It reduces storage space'),
    ('It speeds up query performance'),
    ('It automatically backs up data'),
    ('It encrypts the data'),
    ('It enforces referential integrity')
) AS t(choice_text);

INSERT INTO answers (question_id, answer, explanation)
VALUES ((SELECT id FROM questions WHERE question = 'What is the primary advantage of using an index on a database column?' LIMIT 1), 
        'B', 
        'Database indexes create a separate data structure that allows the database engine to quickly locate rows without scanning the entire table. This significantly speeds up query performance for WHERE clauses and JOIN operations.');

-- Question 3: Hard - Algorithm Design
INSERT INTO questions (question, difficulty, date) 
VALUES ('Which sorting algorithm has the best average-case time complexity?', 'hard', CURRENT_DATE)
RETURNING id INTO q3_id;

INSERT INTO choices (question_id, choice_text) 
SELECT q3_id, choice_text FROM (VALUES 
    ('Bubble Sort'),
    ('Selection Sort'),
    ('Merge Sort'),
    ('Insertion Sort'),
    ('Counting Sort')
) AS t(choice_text);

INSERT INTO answers (question_id, answer, explanation)
VALUES ((SELECT id FROM questions WHERE question = 'Which sorting algorithm has the best average-case time complexity?' LIMIT 1), 
        'C', 
        'Merge Sort has O(n log n) average-case time complexity, which is optimal for comparison-based sorting algorithms. While Counting Sort can achieve O(n) for certain types of data, Merge Sort is the best general-purpose comparison-based sorting algorithm.');
