import os
from lib.db import DatabaseHelper

db = DatabaseHelper()

print("Fixing animal names in animal_details table...")

updates = [
    ("UPDATE animal_details SET common_name = 'Rabbit' WHERE common_name LIKE 'Rabbit%'", "Rabbit"),
    ("UPDATE animal_details SET common_name = 'Red Fox' WHERE common_name LIKE 'Red Fox%'", "Red Fox"),
]

for query, name in updates:
    try:
        db.execute_query(query)
        print(f"Updated {name}")
    except Exception as e:
        print(f"Error updating {name}: {e}")

missing_animals = [
    {
        'name': 'Eastern Grey Kangaroo',
        'scientific': 'Macropus giganteus',
        'description': 'The Eastern Grey Kangaroo is a marsupial found in eastern Australia. They are one of the largest kangaroo species.',
        'habitat': 'Open forests, woodlands, and grasslands',
        'diet': 'Herbivore - grasses, herbs, and leaves',
        'conservation': 'Least Concern',
        'fun_fact': 'They can hop at speeds up to 56 km/h and leap up to 9 meters in a single bound!'
    },
    {
        'name': 'Agile Antechinus',
        'scientific': 'Antechinus agilis',
        'description': 'A small carnivorous marsupial with a pointed snout and dark brown fur.',
        'habitat': 'Forests and woodlands',
        'diet': 'Carnivore - insects, spiders, and small vertebrates',
        'conservation': 'Least Concern',
        'fun_fact': 'Males die after their first mating season due to stress!'
    },
    {
        'name': 'Bush Stone-curlew',
        'scientific': 'Burhinus grallarius',
        'description': 'A large ground-dwelling bird with distinctive large yellow eyes and cryptic plumage.',
        'habitat': 'Open woodlands and grasslands',
        'diet': 'Carnivore - insects, small reptiles, and seeds',
        'conservation': 'Least Concern',
        'fun_fact': 'They are nocturnal and make eerie wailing calls at night!'
    },
    {
        'name': 'Burrowing Bettong',
        'scientific': 'Bettongia lesueur',
        'description': 'A small marsupial that was once widespread but is now critically endangered.',
        'habitat': 'Semi-arid grasslands and woodlands',
        'diet': 'Herbivore - fungi, roots, and seeds',
        'conservation': 'Critically Endangered',
        'fun_fact': 'They build complex burrow systems that can house multiple families!'
    },
    {
        'name': 'Bare-nosed Wombat',
        'scientific': 'Vombatus ursinus',
        'description': 'A stocky, burrowing marsupial with a bare nose and powerful claws.',
        'habitat': 'Forests, mountains, and heathlands',
        'diet': 'Herbivore - grasses, sedges, and roots',
        'conservation': 'Least Concern',
        'fun_fact': 'Their droppings are cube-shaped to prevent them from rolling away!'
    }
]

for animal in missing_animals:
    try:
        query = """
            INSERT INTO animal_details (common_name, scientific_name, description, habitat, diet, conservation_status, fun_fact)
            VALUES (:name, :scientific, :description, :habitat, :diet, :conservation, :fun_fact)
            ON CONFLICT (common_name) DO UPDATE SET
                scientific_name = EXCLUDED.scientific_name,
                description = EXCLUDED.description,
                habitat = EXCLUDED.habitat,
                diet = EXCLUDED.diet,
                conservation_status = EXCLUDED.conservation_status,
                fun_fact = EXCLUDED.fun_fact
        """
        db.execute_query(query, animal)
        print(f"Added/Updated {animal['name']}")
    except Exception as e:
        print(f"Error adding {animal['name']}: {e}")

print("\nVerifying matches between tables...")
verify_query = """
    SELECT 
        asound.common_name as sound_name,
        ad.common_name as detail_name,
        CASE WHEN ad.common_name IS NULL THEN 'MISSING' ELSE 'OK' END as status
    FROM animal_sounds asound
    LEFT JOIN animal_details ad ON asound.common_name = ad.common_name
    ORDER BY asound.common_name
"""

try:
    results = db.execute_query(verify_query)
    print("\nMatching status:")
    for row in results:
        print(f"  {row['sound_name']}: {row['status']}")
except Exception as e:
    print(f"Error verifying: {e}")

print("\nDone!")

