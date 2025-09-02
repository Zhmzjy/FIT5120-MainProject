#!/bin/bash

DB_NAME="wildlife_db"
DB_USER="zhujunyi"
DATA_DIR="/Users/zhujunyi/FIT5120-MainProject/backend/data/dataset/Epic2"

echo "Creating temporary tables..."
psql -h localhost -U $DB_USER -d $DB_NAME -f create_temp_tables.sql

echo "Importing CSV data..."

echo "Importing wildlife_counts.csv..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY wildlife_counts_temp(taxon_id, common_name, scientific_name, image_url, year, month, count) FROM '$DATA_DIR/wildlife_counts.csv' WITH (FORMAT CSV, HEADER);"

echo "Importing season_kpi.csv..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY season_kpi_temp(season, active_species, total_observations) FROM '$DATA_DIR/season_kpi.csv' WITH (FORMAT CSV, HEADER);"

echo "Importing season_top_species.csv..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY season_top_species_temp(season, taxon_id, common_name, scientific_name, image_url, total_count, rank) FROM '$DATA_DIR/season_top_species.csv' WITH (FORMAT CSV, HEADER);"

echo "Importing trends_per_species.csv..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY trends_per_species_temp(taxon_id, common_name, scientific_name, image_url, month, total_count) FROM '$DATA_DIR/trends_per_species.csv' WITH (FORMAT CSV, HEADER);"

echo "Importing season_activity_bins.csv..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY season_activity_bins_temp(season, time_bin, count) FROM '$DATA_DIR/season_activity_bins.csv' WITH (FORMAT CSV, HEADER);"

echo "Importing month_activity_bins.csv..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "\COPY month_activity_bins_temp(month, time_bin, count) FROM '$DATA_DIR/month_activity_bins.csv' WITH (FORMAT CSV, HEADER);"

echo "Transferring data to main tables..."
psql -h localhost -U $DB_USER -d $DB_NAME -f import_data.sql

echo "Cleaning up temporary tables..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "DROP TABLE wildlife_counts_temp, season_kpi_temp, season_top_species_temp, trends_per_species_temp, season_activity_bins_temp, month_activity_bins_temp;"

echo "Data import completed!"

echo "Verifying data..."
psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) as total_species FROM species;"
psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) as total_observations FROM species_counts;"
psql -h localhost -U $DB_USER -d $DB_NAME -c "SELECT * FROM season_kpi;"
