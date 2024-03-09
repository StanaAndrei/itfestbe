import requests
import json
import time

# Definește nutrienții de interes
nutrients_of_interest = ['energy_100g', 'proteins_100g', 'carbohydrates_100g', 'sugars_100g', 'fat_100g', 'saturated-fat_100g', 'fiber_100g', 'salt_100g']

def nutriscore_to_number(nutriscore_grade):
    mapping = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
    return mapping.get(nutriscore_grade.lower(), 0)

def extract_filtered_products(num_products):
    filtered_products = []  # Lista pentru a stoca produsele filtrate
    page_size = 50
    num_pages = (num_products + page_size - 1) // page_size

    for page in range(1, num_pages + 1):
        url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms=&search_simple=1&action=process&json=1&page_size={page_size}&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break
        data = response.json()
        
        for product in data.get('products', []):
            if 'nutriments' in product:
                nutrients_data = {nutrient: product['nutriments'].get(nutrient, 0) for nutrient in nutrients_of_interest}
                health_score = product.get('nutriscore_grade', '').lower()
                numeric_health_score = nutriscore_to_number(health_score)
                product_info = {
                    'nutrients': nutrients_data,
                    'health_score': numeric_health_score
                }
                filtered_products.append(product_info)
                
                if len(filtered_products) >= num_products:
                    return filtered_products

        time.sleep(1)

    return filtered_products[:num_products]

num_products = 2000
filtered_products = extract_filtered_products(num_products)

with open('products.json', 'w') as f:
    json.dump(filtered_products, f, indent=4)

print(f"Salvat {len(filtered_products)} produse filtrate în 'filtered_products_2000_uniform_nutrients.json'")
