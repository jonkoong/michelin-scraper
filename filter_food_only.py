import csv

# List of non-food places to remove
non_food_places = [
    "MINI HOTELS 台中火車站館",
    "RedDot Hotel & Culture",
    "89.5k觀景台",
    "Ali-Shan Kaofeng Hotel",
    "Hotel HI- Branch Chui-Yang",
    "Wenwu Temple",
    "Fenchihu Hotel",
    "Taipei Public Library Beitou Branch",
    "Eslite Spectrum Nanxi",
    "Eslite Spectrum Songyan",
    "Alishan Transport Station",
    "Yongkang St, Da'an District",
    "Remains of Longteng Bridge",
    "Shengxing Station",
    "Yizhong St, North District",
    "Sun Moon Lake Ropeway Station",
    "Xiangshan Visitor Center",
    "Gaomei Wetlands",
    "921 Earthquake Museum of Taiwan",
    "Lukang Old Street",
    "中社觀光花市",
    "National Taiwan University",
    "Shifen Waterfall",
    "Jioufen",
    "Sun-Link-Sea",
    "Hehuanshan",
    "Sun Moon Lake"
]

# Read the current file and filter out non-food places
food_places = []
with open("results/tw-maps-import.csv", "r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)

    for row in reader:
        if row["Name"] not in non_food_places:
            food_places.append(row)

# Write the filtered data back
with open("results/tw-maps-import.csv", "w", newline="", encoding="utf-8") as outfile:
    fieldnames = ["Name", "Address"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(food_places)

print(f"Filtered out {27} non-food places")
print(f"Remaining food places: {len(food_places)}")
print("\nRemoved places:")
for place in non_food_places:
    print(f"  - {place}")