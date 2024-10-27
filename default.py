import json

file = open("{}.txt".format("叮哥"), "r", encoding="utf-8")
lines = file.readlines()
ls = []
for i in range(1, len(lines), 4):
    ls.append([lines[i], int(lines[i + 1]), int(lines[i + 2]), list(lines[i + 3])])


def add_item(a):
    """Prompt the user to add a new item to the menu."""
    medium_price = ls[a][1]
    large_price = ls[a][2]
    bottle_price = input("Enter bottle price (leave empty if not available): ")
    name = ls[a][0]
    # Convert prices to integers if provided
    medium_price = int(medium_price) if medium_price != 0 else None
    large_price = int(large_price) if large_price != 0 else None
    bottle_price = int(bottle_price) if bottle_price else None

    # Options for the item
    custom_sugar = ls[a][3][0].strip().lower() == "0"
    custom_ice = ls[a][3][2].strip().lower() == "0"
    hot_available = ls[a][3][1].strip().lower() == "1"

    return {
        "name": name.replace("\n", ""),
        "medium_price": medium_price,
        "large_price": large_price,
        "bottle_price": bottle_price,
        "options": {
            "custom_sugar": custom_sugar,
            "custom_ice": custom_ice,
            "hot_available": hot_available,
        },
    }


def add_category(b):
    """Prompt the user to add a new category to the menu."""
    items = []

    while True:
        name = input("yes or no")
        if name != "n":
            print(add_item(b))
            items.append(add_item(b))
            b += 1
        else:
            print("exit")
            break
    return items, b


def main():
    menu = {}
    b = 0
    while True:
        category_name = input("category_name")
        if category_name != "a":
            items, b = add_category(b)
            menu[category_name] = items
        else:
            break
    # Save menu to JSON file
    with open("menu.json", "w", encoding="utf-8") as file:
        json.dump(menu, file, ensure_ascii=False, indent=4)

    print("Menu saved to menu.json!")


if __name__ == "__main__":
    main()
