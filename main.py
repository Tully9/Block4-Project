CompanyPositions = {
    "Stripe": 2,
    "AWS": 6,
    "J&J": 2,
    "CloudCards": 2,
    "Dogpatch labs": 2,
    "Patch": 2,
    "Fidelity": 2,
    "Transact Campus": 1
}

StudentList = [
    "24412155", "24486331", "24810385", "24123443",
    "24900042", "24154365", "24777666", "24555555"
]

# Student preferences in order (can be customized further)
StudentPreferences = {
    "24412155": ["AWS", "Stripe", "J&J", "Patch", "CloudCards"],
    "24486331": ["Stripe", "Patch", "CloudCards", "Dogpatch labs"],
    "24810385": ["J&J", "AWS", "Stripe"],
    "24123443": ["CloudCards", "Dogpatch labs", "Fidelity"],
    "24900042": ["AWS", "Fidelity", "Transact Campus"],
    "24154365": ["Transact Campus", "J&J", "Dogpatch labs"],
    "24777666": ["Patch", "Fidelity", "Stripe", "AWS"],
    "24555555": ["Stripe", "AWS", "J&J", "Fidelity"]
}

StudentAllocations = {}

for student in StudentList:
    prefs = StudentPreferences.get(student, [])
    allocated = []
    
    for pref in prefs:
        if len(allocated) >= 3:
            break
        if CompanyPositions.get(pref, 0) > 0:
            allocated.append(pref)
            CompanyPositions[pref] -= 1
    
    # Fill in empty spots with None
    while len(allocated) < 3:
        allocated.append(None)
    
    StudentAllocations[student] = allocated

# 🖨️ Nicely formatted output
print("student_id | pref1           | pref2           | pref3")
print("-----------+-----------------+-----------------+-----------------")
for student, prefs in StudentAllocations.items():
    print(f"{student} | {prefs[0] or 'None':<15} | {prefs[1] or 'None':<15} | {prefs[2] or 'None':<15}")
