def parse_transit_corridor(corridor_code):
    if not isinstance(corridor_code, str):
        return "Invalid input: Corridor code must be a string"
    parts = corridor_code.strip().split('-')
    if len(parts) != 3:
        return "Invalid format: Expected ORIGIN-DESTINATION-ZONES (e.g., DT-UP-3)"
    orig, dest, zones_str = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if not orig or not dest:
        return "Invalid route: Origin and destination must not be empty"
    try:
        zones = int(zones_str)
        if zones < 0:
            return "Invalid zones: Zone count cannot be negative"
    except (ValueError, TypeError):
        return "Invalid zones: Zone count must be a valid integer"
    base_fare = 2.50 + (zones * 0.75)
    return f"Route {orig.upper()}->{dest.upper()}: {zones} Zones, Fare ${base_fare:.2f}"

def lookup_concession_discount(category_name):
    if not isinstance(category_name, str):
        return 1.00
    category = category_name.strip().upper()
    discounts = {
        "STANDARD": 1.00,
        "STUDENT": 0.50,
        "SENIOR": 0.35,
        "MILITARY": 0.20,
        "CHILD": 0.00
    }
    return discounts.get(category, 1.00)

def compute_passenger_density(occupancy_ratio_str):
    if not isinstance(occupancy_ratio_str, str):
        return 0.0
    parts = occupancy_ratio_str.split('/')
    if len(parts) != 2:
        return 0.0
    try:
        passengers = float(parts[0].strip())
        km = float(parts[1].strip())
        if km <= 0 or passengers < 0:
            return 0.0
        density = passengers / km
        return round(density, 2)
    except (ValueError, ZeroDivisionError, OverflowError, TypeError):
        return 0.0

def main():
    print("==== Running parse_transit_corridor ====")
    c_input = input("Enter corridor (e.g. DT-UP-3): ")
    print(parse_transit_corridor(c_input))

    print("\n==== Running lookup_concession_discount ====")
    cat_input = input("Enter concession category (e.g. STUDENT, SENIOR): ")
    print("Multiplier:", lookup_concession_discount(cat_input))

    print("\n==== Running compute_passenger_density ====")
    d_input = input("Enter passengers/km (e.g. 50/10.0): ")
    print("Density:", compute_passenger_density(d_input))

if __name__ == "__main__":
    main()
