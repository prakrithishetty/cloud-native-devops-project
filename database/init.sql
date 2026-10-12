
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    role VARCHAR(100) NOT NULL DEFAULT 'User',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS deployments (
    id SERIAL PRIMARY KEY,
    version VARCHAR(50) NOT NULL,
    environment VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email, role)
VALUES
    ('Admin User', 'admin@example.com', 'Admin'),
    ('DevOps Engineer', 'devops@example.com', 'Engineer')
ON CONFLICT (email) DO NOTHING;

INSERT INTO deployments (version, environment, status)
VALUES
    ('v1.0.0', 'Development', 'SUCCESS'),
    ('v0.9.0', 'Development', 'SUCCESS'),
    ('v0.8.0', 'Development', 'FAILED');
