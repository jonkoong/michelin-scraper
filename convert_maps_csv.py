import csv
from pathlib import Path

def convert_google_takeout_csv():
    """
    Convert Google Takeout saved places CSV to a format suitable for Google Maps import.
    Input: results/tw-saved.csv (Title, Note, URL)
    Output: results/tw-maps-import.csv (Name, Address)
    """

    input_file = Path("results/tw-saved.csv")
    output_file = Path("results/tw-maps-import.csv")

    if not input_file.exists():
        print(f"Error: {input_file} not found!")
        return

    places = []

    # Read the input CSV
    with open(input_file, "r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            title = row["Title"].strip()
            if title:  # Only process non-empty titles
                places.append({
                    "Name": title,
                    "Address": f"{title}, Taiwan"
                })

    # Write the output CSV
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        fieldnames = ["Name", "Address"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(places)

    print(f"Successfully converted {len(places)} places")
    print(f"Output saved to: {output_file}")
    print("\nFirst 5 entries:")
    for place in places[:5]:
        print(f"  - {place['Name']}")

if __name__ == "__main__":
    convert_google_takeout_csv()