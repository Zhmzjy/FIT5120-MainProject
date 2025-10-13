DROP TABLE IF EXISTS yearly_wildlife_occurrences;

CREATE TABLE yearly_wildlife_occurrences (
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    state_territory VARCHAR(50) NOT NULL,
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255) NOT NULL,
    threat_status VARCHAR(50),
    occurrence_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_yearly_year ON yearly_wildlife_occurrences(year);
CREATE INDEX idx_yearly_common_name ON yearly_wildlife_occurrences(common_name);
CREATE INDEX idx_yearly_year_common ON yearly_wildlife_occurrences(year, common_name);
CREATE INDEX idx_yearly_state ON yearly_wildlife_occurrences(state_territory);
