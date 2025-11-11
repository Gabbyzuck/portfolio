import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    data = load_json('data/properties.json')
    for property in data:
        print("")

def get_investor_profile():
    investor_profile = {
        'investment_type': input('Enter risk appetite (core, core-plus, opportunistic, value-add): '),
        'size': float(input('Enter min asset size: ')),
        'min_cap': float(input('Enter min cap rate (0.00 - 1.00): ')),
    }
    return investor_profile

def match_investment(investor_profile, data):
    matches = []
    investment_type_match = {
        'core': ['A'],
        'core-plus': ['A', 'B'],
        'value-add': ['B', 'C'],
        'opportunistic': ['C']
    }

    preferred_classes = investment_type_match.get(investor_profile['investment_type'], [])
    
    for property in data:
        property_cap_rate = property['noi'] / property['sale_price']

        if (property['square_feet'] >= investor_profile['size'] and
            property_cap_rate >= investor_profile['min_cap'] and
            property['property_class'] in preferred_classes):
            matches.append(property)
    
    with open('cre_matchmaker_output.json', 'w') as file:
        json.dump(matches, file, indent=4)
    print(f"Number of matches: {len(matches)}")

    return matches

if __name__ == "__main__":
    data = load_json('data/properties.json')
    investor_profile = get_investor_profile()
    matches = match_investment(investor_profile, data)

    if matches:
        print("Matching properties:")
        for match in matches:
            print(f"Property Name: {match['name']}, Size: {match['square_feet']}, Sale Price: {match['sale_price']}")
    else:
        print("No matching properties found.")