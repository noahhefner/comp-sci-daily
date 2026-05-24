-- Computer Science Daily Trivia Database

-- Create questions table
CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    question TEXT NOT NULL,
    date DATE NOT NULL UNIQUE  -- Only one question allowed per day
);

-- Create index on date for efficient today's question lookup
CREATE INDEX IF NOT EXISTS idx_questions_date ON questions(date);

-- Create choices table
CREATE TABLE IF NOT EXISTS choices (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    choice_text TEXT NOT NULL
);

-- Create index on question_id for efficient choice lookup
CREATE INDEX IF NOT EXISTS idx_choices_question_id ON choices(question_id);

-- Create answers table
CREATE TABLE IF NOT EXISTS answers (
    id UUID PRIMARY KEY DEFAULT uuidv7(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    choice_id UUID NOT NULL REFERENCES choices(id) ON DELETE CASCADE,
    explanation TEXT NOT NULL
);

-- Create index on question_id for efficient answer lookup
CREATE INDEX IF NOT EXISTS idx_answers_question_id ON answers(question_id);