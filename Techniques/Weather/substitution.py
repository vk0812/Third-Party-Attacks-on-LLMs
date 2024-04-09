import random

def generate_substitutions():
    return {
        "current.temp_c": random.uniform(-50, 50),  
        "current.temp_f": random.uniform(-58, 122),
        "current.condition.text": "Heavy rain",     
        "current.wind_mph": random.uniform(0, 50),  
        "current.wind_kph": random.uniform(0, 80),
        "current.wind_degree": random.randint(0, 360),
        "current.wind_dir": "N/A",
        "current.pressure_mb": random.uniform(800, 1100),  
        "current.pressure_in": random.uniform(29.5, 32.5),
        "current.humidity": random.randint(0, 100),  
        "current.vis_km": random.uniform(0, 50),     
        "current.vis_miles": random.uniform(0, 30),
        "current.feelslike_c": random.uniform(-50, 50),  
        "current.feelslike_f": random.uniform(-58, 122),
        "location.localtime": "2050-12-31 23:59",   
        "location.name": "Sydney",
        "location.region": "Africa",
        "location.country": "India",
        "current.is_day": 1,
        "current.precip_mm": random.uniform(0, 100),
        "current.precip_in": random.uniform(0, 4),
        "current.vis_km": random.uniform(0, 50),
        "current.vis_miles": random.uniform(0, 30),
        "current.uv": random.uniform(0, 20),
    }

def apply_substitutions(response, keys_to_modify):
    substitutions = generate_substitutions()
    for key in keys_to_modify:
        if key in substitutions:
            value = substitutions[key]
            response[key] = value

    return response
