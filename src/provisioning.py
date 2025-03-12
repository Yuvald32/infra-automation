from jsonschema import validate, exceptions as jsonschema_exceptions
import json
import os


# Define the validation schema
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "OS": {"type": "string", "enum": ["Ubuntu", "CentOS", "Windows"]},
        "CPU": {"type": "integer", "enum": [1, 2, 4]},
        "RAM": {"type": "integer", "enum": [2, 4, 8]}
    },
    "required": ["name", "OS", "CPU", "RAM"]
}

def get_validated_input(prompt, field, allowed_values=None):
    """Prompt user until a valid input is entered."""
    while True:
        user_input = input(prompt).strip()
        
        # Convert to integer if needed
        if field in ["CPU", "RAM"]:
            try:
                user_input = int(user_input)
            except ValueError:
                print(f"❌ Error: {field} must be a number. Try again.")
                continue

        # Check allowed values
        if allowed_values and user_input not in allowed_values:
            print(f"❌ Error: Invalid {field}. Allowed values: {allowed_values}. Try again.")
            continue
        
        return user_input

def get_user_input():
    """Prompts user for machine details and ensures valid input."""
    machine = {}

    machine["name"] = get_validated_input("Enter machine name: ", "name")
    machine["OS"] = get_validated_input("Enter OS (Ubuntu, CentOS, Windows): ", "OS", ["Ubuntu", "CentOS", "Windows"])
    machine["CPU"] = get_validated_input("Enter CPU cores (1, 2, 4): ", "CPU", [1, 2, 4])
    machine["RAM"] = get_validated_input("Enter RAM in GB (2, 4, 8): ", "RAM", [2, 4, 8])

    # Validate input using JSON schema (final check)
    try:
        validate(instance=machine, schema=schema)
    except jsonschema_exceptions.ValidationError as err:
        print(f"❌ Validation Error: {err.message}. Restarting input...")
        return get_user_input()  # Restart input if there's an issue

    return machine

def save_config(machine):
    """Saves machine details to a JSON file."""
    config_path = "configs/instances.json"

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            machines = json.load(f)
    else:
        machines = []

    machines.append(machine)

    with open(config_path, "w") as f:
        json.dump(machines, f, indent=4)

if __name__ == "__main__":
    machine = get_user_input()
    if machine:
        save_config(machine)
        print("Machine configuration saved successfully!")