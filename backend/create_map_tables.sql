CREATE TABLE wildlife_observations (
    id SERIAL PRIMARY KEY,
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255) NOT NULL,
    lat DECIMAL(10, 8) NOT NULL,
    lon DECIMAL(11, 8) NOT NULL,
    year INTEGER NOT NULL,
    state_territory VARCHAR(100),
    ibra_region VARCHAR(200),
    kingdom VARCHAR(100),
    conservation_status VARCHAR(100),
    occurrence_count INTEGER DEFAULT 1
);

CREATE TABLE species_taxonomy (
    taxon_id INTEGER PRIMARY KEY,
    scientific_name VARCHAR(255) NOT NULL,
    common_name VARCHAR(255) NOT NULL,
    rank VARCHAR(50),
    iconic_taxon_name VARCHAR(100),
    kingdom VARCHAR(100),
    observations_count INTEGER DEFAULT 0,
    wikipedia_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    extinct BOOLEAN DEFAULT FALSE
);

CREATE TABLE species_media (
    media_id INTEGER PRIMARY KEY,
    taxon_id INTEGER,
    square_url TEXT,
    medium_url TEXT,
    original_url TEXT,
    license_code VARCHAR(50),
    attribution TEXT
);

CREATE TABLE habitat_mapping (
    id SERIAL PRIMARY KEY,
    ibra_region VARCHAR(200),
    primary_habitat VARCHAR(100),
    secondary_habitat VARCHAR(100)
);

CREATE INDEX idx_wildlife_observations_lat_lon ON wildlife_observations(lat, lon);
CREATE INDEX idx_wildlife_observations_scientific_name ON wildlife_observations(scientific_name);
CREATE INDEX idx_wildlife_observations_common_name ON wildlife_observations(common_name);
CREATE INDEX idx_wildlife_observations_conservation_status ON wildlife_observations(conservation_status);
CREATE INDEX idx_wildlife_observations_kingdom ON wildlife_observations(kingdom);
CREATE INDEX idx_wildlife_observations_state ON wildlife_observations(state_territory);

CREATE INDEX idx_species_taxonomy_scientific_name ON species_taxonomy(scientific_name);
CREATE INDEX idx_species_taxonomy_common_name ON species_taxonomy(common_name);
CREATE INDEX idx_species_taxonomy_iconic_taxon_name ON species_taxonomy(iconic_taxon_name);

CREATE INDEX idx_species_media_taxon_id ON species_media(taxon_id);

CREATE INDEX idx_habitat_mapping_ibra_region ON habitat_mapping(ibra_region);
CREATE INDEX idx_habitat_mapping_primary_habitat ON habitat_mapping(primary_habitat);
