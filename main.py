import json
from datetime import datetime
from collections import Counter

# Load dataset
file_path = '/mnt/data/DataEngineeringQ2.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Question 1: Share percentage of missing values for firstName, lastName, and DOB
columns = ["firstName", "lastName", "birthDate"]
missing_percentages = {}
total_records = len(data)
for column in columns:
    missing_count = sum(1 for record in data if not record["patientDetails"].get(column))
    missing_percentages[column] = (missing_count / total_records) * 100

# Question 2: Percentage of female gender after imputing with mode
genders = [record['patientDetails'].get('gender', '').upper() for record in data if record['patientDetails'].get('gender')]
mode_gender = max(set(genders), key=genders.count) if genders else None

# Impute missing genders with mode
total_female = 0
for record in data:
    if not record['patientDetails'].get('gender'):
        record['patientDetails']['gender'] = mode_gender
    if record['patientDetails']['gender'] == 'F':
        total_female += 1
percentage_female = (total_female / total_records) * 100

# Question 3: Add ageGroup column and count Adults
age_groups = {"Child": 0, "Teen": 0, "Adult": 0, "Senior": 0}
current_year = datetime.now().year

def calculate_age_group(birth_date):
    if not birth_date:
        return None
    birth_year = datetime.fromisoformat(birth_date.replace("Z", "")).year
    age = current_year - birth_year
    if age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teen"
    elif 20 <= age <= 59:
        return "Adult"
    else:
        return "Senior"

for record in data:
    birth_date = record["patientDetails"].get("birthDate")
    age_group = calculate_age_group(birth_date)
    record["ageGroup"] = age_group
    if age_group:
        age_groups[age_group] += 1
adult_count = age_groups.get("Adult", 0)

# Question 4: Average number of medicines prescribed
medicine_counts = [len(record.get("consultationData", {}).get("medicines", [])) for record in data]
average_medicines = sum(medicine_counts) / len(medicine_counts) if medicine_counts else 0

# Question 5: 3rd most frequently prescribed medicineName
all_medicines = [medicine["medicineName"] for record in data for medicine in record.get("consultationData", {}).get("medicines", [])]
medicine_frequency = Counter(all_medicines)
third_most_frequent_medicine = medicine_frequency.most_common(3)[-1][0] if len(medicine_frequency) >= 3 else None

# Question 6: Percentage distribution of active and inactive medicines
total_active, total_inactive = 0, 0
for record in data:
    medicines = record.get("consultationData", {}).get("medicines", [])
    for medicine in medicines:
        if medicine.get("isActive"):
            total_active += 1
        else:
            total_inactive += 1

total_medicines = total_active + total_inactive
active_percentage = (total_active / total_medicines) * 100 if total_medicines else 0
inactive_percentage = (total_inactive / total_medicines) * 100 if total_medicines else 0

# Question 7: Add isValidMobile column and count valid phone numbers
def is_valid_phone_number(phone_number):
    if phone_number.startswith('+91'):
        phone_number = phone_number[3:]
    elif phone_number.startswith('91'):
        phone_number = phone_number[2:]
    return phone_number.isdigit() and len(phone_number) == 10 and 6000000000 <= int(phone_number) <= 9999999999

valid_phone_count = 0
for record in data:
    phone_number = record.get('phoneNumber', '')
    is_valid = is_valid_phone_number(phone_number)
    record['isValidMobile'] = is_valid
    if is_valid:
        valid_phone_count += 1

# Question 8: Pearson correlation between number of medicines and age
ages, medicines = [], []
def calculate_age(birth_date):
    if not birth_date:
        return None
    birth_year = datetime.fromisoformat(birth_date.replace("Z", "")).year
    return current_year - birth_year

for record in data:
    num_medicines = len(record.get("consultationData", {}).get("medicines", []))
    age = calculate_age(record["patientDetails"].get("birthDate"))
    if age is not None:
        ages.append(age)
        medicines.append(num_medicines)

pearson_correlation = (sum((x - sum(ages)/len(ages)) * (y - sum(medicines)/len(medicines)) for x, y in zip(ages, medicines)) /
                      (len(ages) * (sum((x - sum(ages)/len(ages))**2 for x in ages)**0.5) * (sum((y - sum(medicines)/len(medicines))**2 for y in medicines)**0.5))) if ages else None

# Prepare outputs
outputs = {
    "missing_percentages": missing_percentages,
    "percentage_female": percentage_female,
    "adult_count": adult_count,
    "average_medicines": average_medicines,
    "third_most_frequent_medicine": third_most_frequent_medicine,
    "active_percentage": active_percentage,
    "inactive_percentage": inactive_percentage,
    "valid_phone_count": valid_phone_count,
    "pearson_correlation": pearson_correlation
}

outputs
