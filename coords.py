import json

def get_coordinates(facility_id):
    # Prompt user for facility_id, longitude, and latitude
    longitude = input("Enter longitude: ")
    latitude = input("Enter latitude: ")
    
    # Create a dictionary to store the input values
    coordinates = {
        'facility_id': facility_id,
        'longitude': longitude,
        'latitude': latitude
    }
    
    return coordinates

def main():
    # Get the range of facility_ids
    start_id = int(input("Enter the starting facility ID: "))
    end_id = int(input("Enter the ending facility ID: "))
    
    # Initialize a list to store the coordinates
    coordinates_list = []
    
    # Loop through the range of facility_ids and get coordinates
    for facility_id in range(start_id, end_id + 1):
        print(f"\nCoordinates for facility ID {facility_id}:")
        coordinates = get_coordinates(facility_id)
        coordinates_list.append(coordinates)
    
    # Write the coordinates list to a JSON file
    with open('coords.json', 'w') as json_file:
        json.dump(coordinates_list, json_file, indent=4)
    
    print("Coordinates saved to coords.json")

if __name__ == "__main__":
    main()
