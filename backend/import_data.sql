INSERT INTO species (taxon_id, common_name, scientific_name, image_url)
SELECT DISTINCT
    taxon_id,
    common_name,
    scientific_name,
    image_url
FROM (
    SELECT taxon_id, common_name, scientific_name, image_url FROM wildlife_counts_temp
    UNION
    SELECT taxon_id, common_name, scientific_name, image_url FROM season_top_species_temp
    UNION
    SELECT taxon_id, common_name, scientific_name, image_url FROM trends_per_species_temp
) AS all_species
ON CONFLICT (taxon_id) DO NOTHING;

INSERT INTO species_counts (taxon_id, year, month, count)
SELECT taxon_id, year, month, count
FROM wildlife_counts_temp;

INSERT INTO season_kpi (season, active_species, total_observations)
SELECT season::season_enum, active_species, total_observations
FROM season_kpi_temp;

INSERT INTO season_top_species (season, rank, taxon_id, total_count)
SELECT season::season_enum, rank, taxon_id, total_count
FROM season_top_species_temp;

INSERT INTO trends_per_species (taxon_id, month, total_count)
SELECT taxon_id, month, total_count
FROM trends_per_species_temp;

INSERT INTO season_activity_bins (season, time_bin, count)
SELECT season::season_enum, time_bin::time_bin_enum, count
FROM season_activity_bins_temp;

INSERT INTO month_activity_bins (month, time_bin, count)
SELECT month, time_bin::time_bin_enum, count
FROM month_activity_bins_temp;
