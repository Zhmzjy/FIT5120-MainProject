#!/bin/bash

DB_NAME="wildlife_db"
DB_USER="zhujunyi"
DATA_DIR="/Users/zhujunyi/FIT5120-MainProject/backend/data/dataset/Epic1"

echo "Creating temporary tables for Epic1 data..."

psql -h localhost -U $DB_USER -d $DB_NAME -c "
CREATE TABLE wildlife_observations_temp (
    year INTEGER,
    stateTerritory VARCHAR(100),
    ibraRegion VARCHAR(200),
    ScientificName VARCHAR(255),
    CommonName VARCHAR(255),
    Kingdom VARCHAR(100),
    griisStatus VARCHAR(100),
    capadStatus VARCHAR(100),
    EPBCThreatStatus VARCHAR(100),
    occurrenceCount INTEGER,
    IBRA_REG_N VARCHAR(200),
    STATE VARCHAR(100),
    lat DECIMAL(10, 8),
    lon DECIMAL(11, 8),
    CommonName_clean VARCHAR(255)
);

CREATE TABLE species_taxonomy_temp (
    taxon_id INTEGER,
    scientific_name VARCHAR(255),
    common_name VARCHAR(255),
    rank VARCHAR(50),
    iconic_taxon_name VARCHAR(100),
    observations_count INTEGER,
    wikipedia_url TEXT,
    is_active VARCHAR(10),
    extinct VARCHAR(10)
);

CREATE TABLE species_media_temp (
    media_id INTEGER,
    taxon_id INTEGER,
    square_url TEXT,
    medium_url TEXT,
    original_url TEXT,
    license_code VARCHAR(50),
    attribution TEXT
);
"

echo "Importing Epic1 CSV data..."

echo "Importing wildlife observations..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY wildlife_observations_temp FROM '$DATA_DIR/wildlife_occurrences_with_location_end_status_v2_w_lat_long (2).csv' WITH (FORMAT CSV, HEADER);"

echo "Importing species taxonomy..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY species_taxonomy_temp FROM '$DATA_DIR/taxa.csv' WITH (FORMAT CSV, HEADER);"

echo "Importing species media..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY species_media_temp FROM '$DATA_DIR/media.csv' WITH (FORMAT CSV, HEADER);"

echo "Transferring data to main tables..."

psql -h localhost -U $DB_USER -d $DB_NAME -c "
INSERT INTO wildlife_observations (scientific_name, common_name, lat, lon, year, state_territory, ibra_region, kingdom, conservation_status, occurrence_count)
SELECT ScientificName, CommonName, lat, lon, year, stateTerritory, ibraRegion, Kingdom, EPBCThreatStatus, occurrenceCount
FROM wildlife_observations_temp
WHERE lat IS NOT NULL AND lon IS NOT NULL;

INSERT INTO species_taxonomy (taxon_id, scientific_name, common_name, rank, iconic_taxon_name, observations_count, wikipedia_url, is_active, extinct)
SELECT taxon_id, scientific_name, common_name, rank, iconic_taxon_name, observations_count, wikipedia_url, 
       CASE WHEN is_active = 'TRUE' THEN TRUE ELSE FALSE END,
       CASE WHEN extinct = 'TRUE' THEN TRUE ELSE FALSE END
FROM species_taxonomy_temp
ON CONFLICT (taxon_id) DO NOTHING;

INSERT INTO species_media (media_id, taxon_id, square_url, medium_url, original_url, license_code, attribution)
SELECT media_id, taxon_id, square_url, medium_url, original_url, license_code, attribution
FROM species_media_temp;
"

echo "Creating basic habitat mapping..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "
INSERT INTO habitat_mapping (ibra_region, primary_habitat, secondary_habitat) VALUES
('Australian Alps', 'Mountains', 'Forest'),
('Sydney Basin', 'Forest', 'Urban'),
('South Eastern Highlands', 'Forest', 'Mountains'),
('NSW North Coast', 'Forest', 'Ocean'),
('Murray Darling Depression', 'Grassland', 'River'),
('Brigalow Belt South', 'Grassland', 'Forest'),
('New England Tablelands', 'Mountains', 'Forest'),
('Nandewar', 'Mountains', 'Grassland'),
('NSW South Western Slopes', 'Grassland', 'Forest'),
('Riverina', 'Grassland', 'River');
"

echo "Cleaning up temporary tables..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "DROP TABLE wildlife_observations_temp, species_taxonomy_temp, species_media_temp;"

echo "Epic1 import completed!"

echo "Verifying data..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "
SELECT COUNT(*) as total_observations FROM wildlife_observations;
SELECT COUNT(*) as total_taxonomy FROM species_taxonomy;
SELECT COUNT(*) as total_media FROM species_media;
SELECT COUNT(*) as total_habitats FROM habitat_mapping;
"
