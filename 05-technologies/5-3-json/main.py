import json
import csv

with open('data.csv', 'r', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    result = []
    for row in reader:
        row = {k.strip(): v.strip() for k, v in row.items()}
        result.append(row)

print(json.dumps(result, indent=4, ensure_ascii=False))


def csv_to_json(csv_str: str, delimiter: str =",", eol_delimiter: str ="\n") -> str:
    rows = csv_str.strip().split(eol_delimiter)

    headers = rows[0].split(delimiter)
    result = []

    for row in rows[1:]:
        values = row.split(delimiter)

        row_dict = {}            
        for i in range(len(headers)):
            row_dict[headers[i].strip()] = values[i].strip()
        
        result.append(row_dict)

    return json.dumps(result, indent=4, ensure_ascii=False)


with open("data.csv", "r", encoding="utf-8") as f:
    csv_data = f.read()

print(csv_to_json(csv_data))
