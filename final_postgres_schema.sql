
-- SCHEMA GENERATED ON 2025-05-24 15:43:42

-- STUDENTS TABLE
CREATE TABLE students (
    student_id CHAR(8) PRIMARY KEY,
    name VARCHAR(100),
    year_group INTEGER CHECK (year_group BETWEEN 1 AND 4),
    placement_status VARCHAR(20) DEFAULT 'unmatched'
);

-- COMPANIES TABLE
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    logo_url TEXT,
    description TEXT,
    tech_stack TEXT,
    location TEXT,
    salary INTEGER,
    working_block VARCHAR(10),
    positions_available INTEGER,
    requires_cv BOOLEAN DEFAULT FALSE,
    is_charity BOOLEAN DEFAULT FALSE,
    is_private BOOLEAN DEFAULT FALSE  -- for hidden/1-to-1 companies
);

-- STUDENT-COMPANY VISIBILITY (for private jobs)
CREATE TABLE student_company_visibility (
    id SERIAL PRIMARY KEY,
    student_id CHAR(8) REFERENCES students(student_id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE
);

-- PLACEMENT BLOCKS TABLE
CREATE TABLE placement_blocks (
    id SERIAL PRIMARY KEY,
    block_code VARCHAR(10) UNIQUE,
    year_group INTEGER,
    starts_on DATE,
    rounds INTEGER DEFAULT 3,
    notes TEXT
);

-- CV SUBMISSIONS TABLE
CREATE TABLE cv_submissions (
    id SERIAL PRIMARY KEY,
    student_id CHAR(8) REFERENCES students(student_id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    round INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cv_file_path TEXT NOT NULL
);

-- INTERVIEWS TABLE
CREATE TABLE interviews (
    id SERIAL PRIMARY KEY,
    student_id CHAR(8) REFERENCES students(student_id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    round INTEGER,
    interview_date DATE,
    student_rank INTEGER,
    company_rank INTEGER,
    UNIQUE(student_id, company_id, round)
);

-- MATCHES TABLE
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    student_id CHAR(8) REFERENCES students(student_id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    round INTEGER,
    match_type VARCHAR(20), -- standard, open_marketplace, lottery, non_profit, self-arranged
    match_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    placement_block VARCHAR(10),
    CHECK (match_type IN ('standard', 'open_marketplace', 'lottery', 'non_profit', 'self-arranged'))
);

-- Prevent student from working at same company more than once (except for block 5)
CREATE UNIQUE INDEX unique_placements_per_block_except_5
ON matches(student_id, company_id)
WHERE placement_block != '5';

-- SELF-ARRANGED JOBS TABLE (links student to a company they brought in)
CREATE TABLE self_arranged_jobs (
    id SERIAL PRIMARY KEY,
    student_id CHAR(8) REFERENCES students(student_id) ON DELETE CASCADE,
    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    approved BOOLEAN DEFAULT FALSE
);

-- ACCOUNTS TABLE
CREATE TABLE accounts (
    student_email VARCHAR(100),
    staff_email VARCHAR(100),
    partner_email VARCHAR(100),
    password VARCHAR(100)
);
