CREATE TYPE season_enum AS ENUM ('Spring', 'Summer', 'Autumn', 'Winter');
CREATE TYPE time_bin_enum AS ENUM ('Morning', 'Afternoon', 'Evening', 'Night');

CREATE TABLE species (
    taxon_id INTEGER PRIMARY KEY,
    common_name VARCHAR(255) NOT NULL,
    scientific_name VARCHAR(255) NOT NULL,
    emoji VARCHAR(10),
    image_url TEXT
);

CREATE TABLE species_counts (
    id SERIAL PRIMARY KEY,
    taxon_id INTEGER NOT NULL REFERENCES species(taxon_id),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
    count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE season_kpi (
    season season_enum PRIMARY KEY,
    active_species INTEGER NOT NULL DEFAULT 0,
    total_observations INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE season_top_species (
    season season_enum NOT NULL,
    rank INTEGER NOT NULL CHECK (rank > 0),
    taxon_id INTEGER NOT NULL REFERENCES species(taxon_id),
    total_count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (season, rank)
);

CREATE TABLE trends_per_species (
    taxon_id INTEGER NOT NULL REFERENCES species(taxon_id),
    month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
    total_count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (taxon_id, month)
);

CREATE TABLE season_activity_bins (
    season season_enum NOT NULL,
    time_bin time_bin_enum NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (season, time_bin)
);

CREATE TABLE month_activity_bins (
    month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
    time_bin time_bin_enum NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (month, time_bin)
);

CREATE INDEX idx_species_counts_taxon_id ON species_counts(taxon_id);
CREATE INDEX idx_species_counts_year ON species_counts(year);
CREATE INDEX idx_species_counts_month ON species_counts(month);
CREATE INDEX idx_species_counts_year_month ON species_counts(year, month);
CREATE INDEX idx_species_counts_taxon_year_month ON species_counts(taxon_id, year, month);

CREATE INDEX idx_season_top_species_season ON season_top_species(season);
CREATE INDEX idx_season_top_species_taxon_id ON season_top_species(taxon_id);

CREATE INDEX idx_trends_per_species_month ON trends_per_species(month);
CREATE INDEX idx_trends_per_species_taxon_id ON trends_per_species(taxon_id);

CREATE INDEX idx_season_activity_bins_season ON season_activity_bins(season);
CREATE INDEX idx_month_activity_bins_month ON month_activity_bins(month);
