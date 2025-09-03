import os
import time
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool

class DatabaseHelper:
    def __init__(self):
        self.engine = None
        self.connect()
    
    def connect(self):
        try:
           
            database_url = os.getenv(
                'DATABASE_URL',
                'postgresql://main_db_user:password@dpg-xxxx.oregon-postgres.render.com/main_db?sslmode=require'
            )

            self.engine = create_engine(
                database_url,
                poolclass=QueuePool,
                pool_size=5,
                max_overflow=10,
                pool_pre_ping=True,
                pool_recycle=300,
                connect_args={
                    "connect_timeout": 10,
                    "application_name": "wildlife_academy"
                }
            )
        except Exception:
            self.engine = None
    
    def execute_query(self, query, params=None, retries=3):
        if not self.engine:
            return None
        
        for attempt in range(retries):
            try:
                with self.engine.connect() as connection:
                    if params is None:
                        result = connection.execute(text(query))
                    elif isinstance(params, dict):
                        result = connection.execute(text(query), params)
                    elif isinstance(params, (list, tuple)):
                        converted_params = {}
                        param_count = 0
                        converted_query = query
                        while '%s' in converted_query:
                            if param_count < len(params):
                                param_name = f'param_{param_count}'
                                converted_params[param_name] = params[param_count]
                                converted_query = converted_query.replace('%s', f':{param_name}', 1)
                                param_count += 1
                            else:
                                break
                        result = connection.execute(text(converted_query), converted_params)
                    else:
                        result = connection.execute(text(query), params)

                    return [dict(row._mapping) for row in result]
            except SQLAlchemyError as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(0.5 * (attempt + 1))
                self.connect()
            except Exception as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(0.5 * (attempt + 1))

    def test_connection(self):
        if not self.engine:
            return False
        
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                return True
        except SQLAlchemyError:
            return False
    
    def get_season_kpi(self):
        query = """
        SELECT season, active_species, total_observations 
        FROM season_kpi 
        ORDER BY 
            CASE season 
                WHEN 'Spring' THEN 1 
                WHEN 'Summer' THEN 2 
                WHEN 'Autumn' THEN 3 
                WHEN 'Winter' THEN 4 
            END
        """
        return self.execute_query(query)
    
    def get_season_activity(self):
        query = """
        SELECT season, time_bin, count 
        FROM season_activity_bins 
        ORDER BY 
            CASE season 
                WHEN 'Spring' THEN 1 
                WHEN 'Summer' THEN 2 
                WHEN 'Autumn' THEN 3 
                WHEN 'Winter' THEN 4 
            END, 
            CASE time_bin 
                WHEN 'Morning' THEN 1 
                WHEN 'Afternoon' THEN 2 
                WHEN 'Evening' THEN 3 
                WHEN 'Night' THEN 4 
            END
        """
        return self.execute_query(query)
    
    def get_top_species(self, season):
        query = """
        SELECT sts.taxon_id, s.common_name, s.scientific_name, s.image_url, sts.total_count, sts.rank
        FROM season_top_species sts
        JOIN species s ON sts.taxon_id = s.taxon_id
        WHERE sts.season = :season
        ORDER BY sts.rank
        LIMIT 10
        """
        return self.execute_query(query, {'season': season})
    
    def get_species_trend(self, taxon_id):
        query = """
        SELECT month, total_count
        FROM trends_per_species
        WHERE taxon_id = :taxon_id
        ORDER BY month
        """
        return self.execute_query(query, {'taxon_id': taxon_id})
    
    def get_seasonal_trend(self, season):
        season_months = {
            'Spring': [9, 10, 11],
            'Summer': [12, 1, 2],
            'Autumn': [3, 4, 5],
            'Winter': [6, 7, 8]
        }
        
        months = season_months.get(season, [])
        if not months:
            return None
        
        placeholders = ','.join([str(m) for m in months])
        query = f"""
        SELECT month, SUM(total_count) as total_count
        FROM trends_per_species
        WHERE month IN ({placeholders})
        GROUP BY month
        ORDER BY month
        """
        return self.execute_query(query)
