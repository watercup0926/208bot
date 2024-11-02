import json


def add_item(name):
    """Prompt the user to add a new item to the menu."""
    #medium_price = input("Enter medium price (leave empty if not available): ")
    large_price = input("Enter large price (leave empty if not available): ")
    bottle_price = input("Enter bottle price (leave empty if not available): ")

    # Convert prices to integers if provided
    #medium_price = int(medium_price) if medium_price else None
    large_price = int(large_price) if large_price else None
    bottle_price = int(bottle_price) if bottle_price else None
    
    #bottle_price = None
    # Options for the item
    medium_price = None
    custom_sugar = input("Can customize sugar level? (yes/no): ").strip().lower() == "y"
    custom_ice = input("Can customize ice level? (yes/no): ").strip().lower() == "y"
    hot_available = input("Available hot? (yes/no): ").strip().lower() == "y"

    return {
        "name": name,
        "medium_price": medium_price,
        "large_price": large_price,
        "bottle_price": bottle_price,
        "options": {
            "custom_sugar": custom_sugar,
            "custom_ice": custom_ice,
            "hot_available": hot_available,
        },
    }


def add_category():
    """Prompt the user to add a new category to the menu."""
    items = []

    while True:
        name = input("enter name: ")
        if name != "a":
            items.append(add_item(name))
        else:
            print()
            break
    return items


def main():
    menu = {}

    while True:
        category_name = input("category_name: ")
        if category_name != "a":
            items = add_category()
            menu[category_name] = items
        else:
            break
    # Save menu to JSON file
    with open("menu.json", "w", encoding="utf-8") as file:
        json.dump(menu, file, ensure_ascii=False, indent=4)

    print("Menu saved to menu.json!")


if __name__ == "__main__":
    main()
