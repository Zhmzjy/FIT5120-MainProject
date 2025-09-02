CREATE TABLE wildlife_counts_temp (
    taxon_id INTEGER,
    common_name VARCHAR(255),
    scientific_name VARCHAR(255),
    image_url TEXT,
    year INTEGER,
    month INTEGER,
    count INTEGER
);

CREATE TABLE season_kpi_temp (
    season VARCHAR(50),
    active_species INTEGER,
    total_observations INTEGER
);

CREATE TABLE season_top_species_temp (
    season VARCHAR(50),
    taxon_id INTEGER,
    common_name VARCHAR(255),
    scientific_name VARCHAR(255),
    image_url TEXT,
    total_count INTEGER,
    rank INTEGER
);

CREATE TABLE trends_per_species_temp (
    taxon_id INTEGER,
    common_name VARCHAR(255),
    scientific_name VARCHAR(255),
    image_url TEXT,
    month INTEGER,
    total_count INTEGER
);

CREATE TABLE season_activity_bins_temp (
    season VARCHAR(50),
    time_bin VARCHAR(50),
    count INTEGER
);

CREATE TABLE month_activity_bins_temp (
    month INTEGER,
    time_bin VARCHAR(50),
    count INTEGER
);
