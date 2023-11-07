import yaml

def account_risk(user_input_address = "0x48549a34ae37b12f6a30566245176994e17c6b4a"):

    risk_rating = {"terrorist entity": 4, "Phishing": 3, "Scamming": 2, "New_account": 1}
    # Load the YAML data from the file
    with open('etherscamdb.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # Define a function to search for objects with matching addresses
    def search_by_address(address):
        matching_objects = []
        for item in data:
            if 'addresses' in item and isinstance(item['addresses'], list):
                for addr in item['addresses']:
                    if addr == address:
                        matching_objects.append(item)
        return matching_objects

    # Get user input for the address to search
    #user_input_address = input("Enter an address: ")
    

    # Search for matching objects
    matching_results = search_by_address(user_input_address)

    # Display the matching objects
    if matching_results:
        print("Matching objects:")
        for result in matching_results:
            print(result)
            address = result['addresses']
            category = result['category']
            print(type(result))
            risk_score = risk_rating[category]
            # do a extra check if an account is associated different categories
    else:
        print("No matching objects found.")
        risk_score = risk_rating["New_account"]


    print(risk_score)
    return risk_score
    
