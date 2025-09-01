import os
import csv
import json
from typing import List, Dict, Any

class CSVFallback:
    def __init__(self):
        self.outputs_dir = os.getenv('OUTPUTS_DIR', 'outputs')
        self.data_dir = os.path.join('data', 'dataset', 'Epic2')
    
    def _read_csv(self, filename: str) -> List[Dict[str, Any]]:
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            return []
        
        data = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except Exception:
            return []
        
        return data
    
    def get_season_kpi(self) -> List[Dict[str, Any]]:
        data = self._read_csv('season_kpi.csv')
        result = []
        for row in data:
            result.append({
                'season': row['season'],
                'active_species': int(row['active_species']),
                'total_observations': int(row['total_observations'])
            })
        return result
    
    def get_season_activity(self) -> List[Dict[str, Any]]:
        data = self._read_csv('season_activity_bins.csv')
        result = []
        for row in data:
            result.append({
                'season': row['season'],
                'time_bin': row['time_bin'],
                'count': int(row['count'])
            })
        return result
    
    def get_top_species(self, season: str) -> List[Dict[str, Any]]:
        data = self._read_csv('season_top_species.csv')
        result = []
        for row in data:
            if row['season'] == season:
                result.append({
                    'common_name': row['common_name'],
                    'scientific_name': row['scientific_name'],
                    'image_url': row['image_url'],
                    'total_count': int(row['total_count']),
                    'rank': int(row['rank'])
                })
        return sorted(result, key=lambda x: x['rank'])[:10]
    
    def get_species_trend(self, taxon_id: str) -> List[Dict[str, Any]]:
        data = self._read_csv('trends_per_species.csv')
        result = []
        for row in data:
            if row['taxon_id'] == taxon_id:
                result.append({
                    'month': int(row['month']),
                    'total_count': int(row['total_count'])
                })
        return sorted(result, key=lambda x: x['month'])
    
    def get_seasonal_trend(self, season: str) -> List[Dict[str, Any]]:
        season_months = {
            'Spring': [9, 10, 11],
            'Summer': [12, 1, 2],
            'Autumn': [3, 4, 5],
            'Winter': [6, 7, 8]
        }
        
        months = season_months.get(season, [])
        if not months:
            return []
        
        data = self._read_csv('trends_per_species.csv')
        monthly_totals = {month: 0 for month in months}
        
        for row in data:
            month = int(row['month'])
            if month in months:
                monthly_totals[month] += int(row['total_count'])
        
        result = []
        for month in months:
            result.append({
                'month': month,
                'total_count': monthly_totals[month]
            })
        
        return result
