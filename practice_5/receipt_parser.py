import re
import json
with open("Practice5/raw.txt", "r", encoding="utf-8") as f:
    text = f.read()
company = re.search(r"Филиал ТОО\s+(.+)", text)
company = company.group(1) if company else None

receipt_number = re.search(r"Чек №(\d+)", text)
receipt_number = receipt_number.group(1) if receipt_number else None

cashier = re.search(r"Кассир\s+(.+)", text)
cashier = cashier.group(1) if cashier else None

pattern = re.compile(
    r"\d+\.\s*\n"            
    r"(.+?)\n"               
    r"(\d+,\d+)\s*x\s*(\d+,\d+)\n"  
    r"(\d+,\d+)",            
    re.MULTILINE
)

products = []
total_sum = 0

for match in pattern.finditer(text):
    name = match.group(1).strip()
    quantity = float(match.group(2).replace(',', '.'))
    price = float(match.group(3).replace(',', '.'))
    total = float(match.group(4).replace(',', '.'))

    total_sum += total

    products.append({
        "name": name,
        "quantity": quantity,
        "price_per_unit": price,
        "total": total
    })

result = {
    "company": company,
    "receipt_number": receipt_number,
    "cashier": cashier,
    "products": products,
    "calculated_total": total_sum
}

print(json.dumps(result, indent=4, ensure_ascii=False))
