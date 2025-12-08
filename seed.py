from flask import Flask
from faker import Faker
import random
from datetime import date, timedelta,datetime

from models import db,  Department, Doctor, Patient, Slot, Appointment, AppointmentStatus, Treatment, Admin,Sessions

TEST = False

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api_database1.sqlite3" if TEST else "sqlite:///api_database.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

fake = Faker()




NO_OF_PATIENTS = 4 if TEST else 50
NO_OF_DOCTORS = 2 if TEST else 15
NO_OF_APPOINTMENTS_PER_DOCTOR = 1 if TEST else 4
NO_OF_PAST_DAYS = 1 if TEST else 30
NO_OF_FUTURE_DAYS = 3 if TEST else 30
START_DATE = date.today() - timedelta(days=NO_OF_PAST_DAYS)
END_DATE = date.today() + timedelta(days=NO_OF_FUTURE_DAYS)

def seed_database():
    db.drop_all()
    db.create_all()
    print("  Tables dropped & recreated")

    # -----------------
    # 1 Admin
    # -----------------
    admin = Admin(
        name="Baskaran",
        last_name="Nadar",
        email="admin@example.com",
        password="123",
        type ="admin",
        role="admin",
        dob=datetime.strptime("1951-04-03", "%Y-%m-%d").date(),
        phone="+919876543210",
        address=f"{'C602, Dheeraj Residency'}, {'Goregaon West'}, {'Mumbai'}",
    )
    db.session.add(admin)

    # -----------------
    # 10 Departments
    # -----------------
    dept_names = [
        "Cardiology", "Neurology", "Orthopedics", "Pediatrics", "Oncology",
        "Dermatology", "Gastroenterology", "ENT", "Urology", "Endocrinology"
    ]
    male_names = [
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Krishna", "Ishaan", "Shaurya",
        "Rahul", "Amit", "Suresh", "Ramesh", "Vijay", "Karthik", "Sanjay", "Deepak", "Manoj", "Arvind",
        "Ram", "Murugan", "Chandran"
    ]

    female_names = [
        "Ananya", "Diya", "Aadhya", "Pari", "Avni", "Anika", "Navya", "Myra", "Ira", "Kiara",
        "Lakshmi", "Priya", "Rani", "Kavya", "Pooja", "Sneha", "Nisha", "Radha", "Divya", "Meera",
        "Sunita", "Geeta", "Seema", "Lata", "Rekha", "Neha", "Shreya", "Aarti", "Payal", "Jyoti",
        "Devika"
    ]

    names = [
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Krishna", "Ishaan", "Shaurya",
        "Ananya", "Diya", "Aadhya", "Pari", "Avni", "Anika", "Navya", "Myra", "Ira", "Kiara",
        "Lakshmi", "Priya", "Rani", "Kavya", "Pooja", "Sneha", "Nisha", "Radha", "Divya", "Meera",
        "Rahul", "Amit", "Suresh", "Ramesh", "Vijay", "Karthik", "Sanjay", "Deepak", "Manoj", "Arvind",
        "Sunita", "Geeta", "Seema", "Lata", "Rekha", "Neha", "Shreya", "Aarti", "Payal", "Jyoti",
        "Ram", "Murugan", "Chandran", "Devika"
    ]

    surnames = [
        "Sharma", "Reddy", "Iyer", "Nair", "Singh", "Mehta", "Gupta", "Rao", "Pillai", "Das",
        "Chatterjee", "Bose", "Patel", "Menon", "Varma", "Kulkarni", "Desai", "Ghosh", "Mishra", "Malhotra"
    ]

    # Sample addresses in Indian cities
    streets = [
        "5th Cross Road", "MG Road", "Park Street", "Anna Salai", "Connaught Place",
        "Sector 18", "Baner Road", "Banjara Hills", "Civil Lines", "Lalbagh Road",
        "Brigade Road", "Linking Road", "Camac Street", "Cathedral Road", "Karol Bagh Main Road",
        "Golf Course Road", "FC Road", "Hitech City Road", "MI Road", "Hazratganj Road",
        "Nungambakkam High Road", "Russel Street", "Colaba Causeway", "Commercial Street", "Connaught Lane"
    ]

    locations = [
        "Goregaon West", "Indiranagar", "Park Circus", "Teynampet", "Connaught Circle",
        "Atta Market", "Aundh", "Jubilee Hills", "C-Scheme", "Hazratganj",
        "Ashok Nagar", "Bandra West", "Elgin", "Gopalapuram", "Karol Bagh",
        "DLF Phase 1", "Deccan Gymkhana", "Madhapur", "Civil Lines", "Kaiserbagh",
        "Adyar", "Shakespeare Sarani", "Fort", "Shivaji Nagar", "Janpath"
    ]

    cities = [
        "Mumbai", "Bangalore", "Kolkata", "Chennai", "New Delhi",
        "Noida", "Pune", "Hyderabad", "Jaipur", "Lucknow",
        "Mysore", "Thane", "Chandigarh", "Coimbatore", "Bhopal",
        "Gurgaon", "Nagpur", "Visakhapatnam", "Udaipur", "Kanpur",
        "Madurai", "Patna", "Ahmedabad", "Mangalore", "Ranchi"
    ]
    doctors = [
        # Cardiology
        {"name": "Aarav", "surn": "Sharma", "dep": "Cardiology", "desc": "Specializes in treating heart diseases with over a decade of experience."},
        {"name": "Lakshmi", "surn": "Reddy", "dep": "Cardiology", "desc": "Focuses on preventive cardiology and patient rehabilitation."},

        # Pediatrics
        {"name": "Ananya", "surn": "Nair", "dep": "Pediatrics", "desc": "Dedicated to child healthcare and vaccinations."},
        {"name": "Rahul", "surn": "Gupta", "dep": "Pediatrics", "desc": "Expert in managing childhood growth and nutrition issues."},

        # Orthopedics
        {"name": "Vihaan", "surn": "Menon", "dep": "Orthopedics", "desc": "Specialist in bone fractures and sports injuries."},
        {"name": "Sneha", "surn": "Kulkarni", "dep": "Orthopedics", "desc": "Experienced in joint replacement and spinal care."},

        # Dermatology
        {"name": "Diya", "surn": "Singh", "dep": "Dermatology", "desc": "Provides treatment for skin allergies and acne care."},
        {"name": "Ramesh", "surn": "Patel", "dep": "Dermatology", "desc": "Focuses on cosmetic dermatology and laser treatments."},

        # Neurology
        {"name": "Aditya", "surn": "Iyer", "dep": "Neurology", "desc": "Treats epilepsy and other neurological disorders."},
        {"name": "Shreya", "surn": "Das", "dep": "Neurology", "desc": "Experienced in headache and migraine management."},

        # Gynecology
        {"name": "Navya", "surn": "Bose", "dep": "Gynecology", "desc": "Specializes in maternity and prenatal care."},
        {"name": "Deepak", "surn": "Varma", "dep": "Gynecology", "desc": "Focuses on reproductive health and infertility treatment."},

        # Ophthalmology
        {"name": "Myra", "surn": "Chatterjee", "dep": "Ophthalmology", "desc": "Provides advanced eye care and cataract surgeries."},
        {"name": "Vijay", "surn": "Mishra", "dep": "Ophthalmology", "desc": "Specialist in vision correction and glaucoma management."},

        # Psychiatry
        {"name": "Ishaan", "surn": "Rao", "dep": "Psychiatry", "desc": "Helps patients with stress, depression, and anxiety disorders."},
        {"name": "Priya", "surn": "Desai", "dep": "Psychiatry", "desc": "Focuses on adolescent and women’s mental health."},

        # Gastroenterology
        {"name": "Arjun", "surn": "Malhotra", "dep": "Gastroenterology", "desc": "Specialist in digestive system and liver diseases."},
        {"name": "Radha", "surn": "Mehta", "dep": "Gastroenterology", "desc": "Focuses on endoscopy and dietary management of gut health."},

        # General Medicine
        {"name": "Karthik", "surn": "Ghosh", "dep": "General Medicine", "desc": "Provides primary care and chronic disease management."},
        {"name": "Seema", "surn": "Pillai", "dep": "General Medicine", "desc": "Specializes in preventive medicine and patient wellness."}
    ]


    complaints = [
        "Headache", "Fever", "Cough", "Cold", "Sore throat",
        "Stomach pain", "Back pain", "Neck pain", "Chest pain", "Joint pain",
        "Shortness of breath", "Fatigue", "Dizziness", "Nausea", "Vomiting",
        "Diarrhea", "Constipation", "Acidity", "Indigestion", "Gas",
        "Skin rash", "Itching", "Acne", "Hair fall", "Dandruff",
        "Eye pain", "Blurred vision", "Red eyes", "Watery eyes", "Dry eyes",
        "Ear pain", "Hearing loss", "Ringing in ears", "Blocked nose", "Runny nose",
        "Swollen glands", "Mouth ulcers", "Toothache", "Bleeding gums", "Bad breath",
        "Palpitations", "High blood pressure", "Low blood pressure", "High sugar", "Frequent urination",
        "Burning urination", "Blood in urine", "Kidney pain", "Swelling in legs", "Varicose veins",
        "Difficulty walking", "Muscle cramps", "Weakness", "Tremors", "Numbness",
        "Anxiety", "Depression", "Insomnia", "Loss of appetite", "Weight loss",
        "Weight gain", "Obesity", "Thyroid issues", "Excessive sweating", "Chills",
        "Allergy", "Asthma attack", "Wheezing", "Cough with phlegm", "Blood in sputum",
        "Heartburn", "Hiccups", "Difficulty swallowing", "Loss of taste", "Loss of smell",
        "Menstrual pain", "Irregular periods", "Heavy bleeding", "Pregnancy checkup", "Menopause symptoms",
        "Low back stiffness", "Shoulder pain", "Knee pain", "Ankle swelling", "Wrist pain",
        "Cuts", "Bruises", "Burns", "Wounds not healing", "Insect bite",
        "Food poisoning", "Jaundice", "Liver pain", "Pancreatic pain", "Gallstones",
        "Chest tightness", "Cold hands and feet", "Fainting", "Seizures", "Memory loss"
    ]
    female_specific = [
        "Menstrual pain", "Irregular periods", "Heavy bleeding", "Pregnancy checkup", "Menopause symptoms"
    ]
    tests = [
    "Complete Blood Count", "Blood Sugar", "Lipid Profile", "Liver Function Test",
    "Kidney Function Test", "Thyroid Function Test", "Urine Analysis", "ECG",
    "Chest X-Ray", "Ultrasound Abdomen", "MRI Brain", "CT Scan Chest",
    "Vitamin D Test", "Iron Studies", "Electrolyte Panel", "HbA1c",
    "Prothrombin Time", "Stool Test", "Echocardiography", "Pulmonary Function Test"
    ]
    medicines = [
    "Paracetamol", "Ibuprofen", "Amoxicillin", "Cefixime", "Azithromycin",
    "Metformin", "Amlodipine", "Losartan", "Omeprazole", "Pantoprazole",
    "Cetirizine", "Loratadine", "Levocetirizine", "Ranitidine", "Domperidone",
    "Salbutamol", "Montelukast", "Prednisolone", "Doxycycline", "Clarithromycin",
    "Fluconazole", "Ketoconazole", "Nystatin", "Vitamin C", "Vitamin D",
    "Calcium Carbonate", "Ferrous Sulfate", "Folic Acid", "Hydrocortisone", "Triamcinolone",
    "Gabapentin", "Pregabalin", "Paroxetine", "Sertraline", "Fluoxetine",
    "Lorazepam", "Alprazolam", "Diazepam", "Amiodarone", "Digoxin",
    "Atorvastatin", "Simvastatin", "Rosuvastatin", "Clopidogrel", "Aspirin",
    "Warfarin", "Rivaroxaban", "Enoxaparin", "Metoprolol", "Propranolol",
    "Carvedilol", "Hydrochlorothiazide", "Furosemide", "Spironolactone", "Triamterene",
    "Levothyroxine", "Liothyronine", "Insulin", "Glimepiride", "Sitagliptin",
    "Ondansetron", "Domperidone", "Loperamide", "Rifaximin", "Dicyclomine",
    "Lansoprazole", "Esomeprazole", "Rabeprazole", "Sucralfate", "Magaldrate",
    "Amantadine", "Levodopa", "Carbidopa", "Donepezil", "Rivastigmine",
    "Montelukast", "Tiotropium", "Budesonide", "Fluticasone", "Mometasone",
    "Salmeterol", "Formoterol", "Hydroxychloroquine", "Methotrexate", "Azathioprine",
    "Cyclophosphamide", "Prednisone", "Dexamethasone", "Betamethasone", "Methylprednisolone",
    "Insulin Glargine", "Insulin Aspart", "Insulin Lispro", "Methimazole", "Propylthiouracil",
    "Allopurinol", "Colchicine", "Hydroxyzine", "Promethazine", "Meclizine",
    "Acetaminophen", "Tramadol", "Codeine", "Morphine", "Oxycodone"
    ]


    diagnoses = [
    "Acute bronchitis", "Chronic sinusitis", "Type 2 diabetes", "Hypertension", "Migraine headache",
    "Osteoarthritis knee", "Asthma attack", "Gastroesophageal reflux", "Acute tonsillitis", "Chronic kidney disease",
    "Iron deficiency anemia", "Acute myocardial infarction", "Chronic obstructive pulmonary", "Pneumonia infection", "Urinary tract infection",
    "Hypothyroidism disorder", "Hyperthyroidism condition", "Rheumatoid arthritis", "Psoriasis vulgaris", "Atopic dermatitis",
    "Acute pancreatitis", "Gallstone disease", "Hepatitis B", "Hepatitis C", "Liver cirrhosis",
    "Peptic ulcer disease", "Irritable bowel syndrome", "Crohn's disease", "Ulcerative colitis", "Diverticular disease",
    "Epilepsy disorder", "Parkinson's disease", "Alzheimer's disease", "Peripheral neuropathy", "Multiple sclerosis",
    "Anxiety disorder", "Major depression", "Bipolar disorder", "Schizophrenia spectrum", "Obsessive compulsive disorder",
    "Acute appendicitis", "Hernia inguinal", "Cholelithiasis gallstones", "Varicose veins", "Deep vein thrombosis",
    "Pulmonary embolism", "Bronchial asthma", "Chronic bronchitis", "Sleep apnea", "Obstructive sleep apnea",
    "Acute otitis media", "Chronic otitis media", "Sinus infection", "Seasonal allergies", "Allergic rhinitis",
    "Acute cystitis", "Chronic prostatitis", "Benign prostatic hyperplasia", "Endometriosis condition", "Polycystic ovary",
    "Menstrual disorder", "Gestational diabetes", "Pregnancy hypertension", "Pre-eclampsia syndrome", "Ectopic pregnancy",
    "Skin abscess", "Contact dermatitis", "Fungal infection", "Bacterial infection", "Viral infection",
    "Conjunctivitis bacterial", "Conjunctivitis viral", "Glaucoma primary", "Cataract senile", "Macular degeneration",
    "Otitis externa", "Tonsil hypertrophy", "Laryngitis acute", "Pharyngitis bacterial", "Pharyngitis viral",
    "Acne vulgaris", "Seborrheic dermatitis", "Psoriatic arthritis", "Fibromyalgia syndrome", "Chronic fatigue",
    "Back strain", "Neck sprain", "Shoulder impingement", "Carpal tunnel", "Rotator cuff injury",
    "Knee ligament tear", "Ankle sprain", "Hip bursitis", "Frozen shoulder", "Plantar fasciitis",
    "Vitamin D deficiency", "Vitamin B12 deficiency", "Calcium deficiency", "Magnesium deficiency", "Protein malnutrition",
    "Hypoglycemia episode", "Hyperglycemia episode", "Cardiomyopathy dilated", "Heart failure", "Angina pectoris",
    "Myocardial ischemia", "Atrial fibrillation", "Ventricular tachycardia", "Congenital heart disease", "Peripheral artery disease"
    ]

    female_specific_diagnoses = [
    "Endometriosis condition",
    "Polycystic ovary",
    "Menstrual disorder",
    "Gestational diabetes",
    "Pregnancy hypertension",
    "Pre-eclampsia syndrome",
    "Ectopic pregnancy",
    "Benign prostatic hyperplasia"  #   actually male-specific, can include if needed for males
    ]

    male_diagnoses = [d for d in diagnoses if d not in female_specific_diagnoses]
    female_diagnoses = diagnoses.copy()  # all diagnoses are allowed

    # Male-appropriate complaints (everyone else)
    male_complaints = [c for c in complaints if c not in female_specific]

    # Female-appropriate complaints (all including female-specific)
    female_complaints = complaints.copy()  # all complaints are allowed for females
    visit_types = [
    "Consultation", "Follow-up", "Emergency", "Specialist Consultation", "Second Opinion",
    "In-person", "Telemedicine", "Home Visit",
    "Short Consultation", "Extended Consultation", "Procedural Visit",
    "One-time", "Routine", "Preventive Screening", "Diagnostic Visit",
    "Therapy/Treatment", "Pre-Op", "Post-Op", "Vaccination"
    ]
    frequencies = ["OD", "BD", "TDS", "QID", "HS", "PRN"]
    # Quantity per dose
    quantities = ["1 tablet", "2 tablets", "5 mL", "10 mL", "1 capsule", "2 capsules", "3 drops"]
    # Duration options
    durations = ["3 days", "5 days", "7 days", "10 days", "14 days", "Until recovery"]

    # Function to generate a single medicine prescription
    def random_medicine():
        return {
            "medicine": random.choice(medicines),
            "quantity_per_dose": random.choice(quantities),
            "frequency": random.choice(frequencies),
            "duration": random.choice(durations),
            "instructions": random.choice(["After meals", "Before meals", "With water", "Avoid alcohol"])
        }

    # Example: add medicines to a patient prescription
    def generate_prescription_medicines(num_meds=3):
        meds = [random_medicine() for _ in range(num_meds)]
        return "; ".join([f"{m['medicine']} {m['quantity_per_dose']} {m['frequency']} for {m['duration']}" 
                        for m in meds])


    departments = {
    "Cardiology": "Deals with disorders of the heart and circulatory system, including diagnosis and treatment of heart diseases.",
    "Pediatrics": "Focuses on medical care for infants, children, and adolescents, covering growth, development, and vaccinations.",
    "Orthopedics": "Specializes in bones, joints, ligaments, and muscles, including treatment of fractures and sports injuries.",
    "Dermatology": "Cares for skin, hair, and nail conditions, as well as cosmetic treatments like laser therapy.",
    "Neurology": "Concerned with the nervous system, diagnosing and treating disorders of the brain, spine, and nerves.",
    "Gynecology": "Dedicated to women’s reproductive health, pregnancy care, and treatment of related conditions.",
    "Ophthalmology": "Provides medical and surgical care for eye conditions, including vision correction and cataract treatment.",
    "Psychiatry": "Focuses on diagnosis, treatment, and prevention of mental health conditions and emotional disorders.",
    "Gastroenterology": "Specializes in digestive system health, including the stomach, liver, pancreas, and intestines.",
    "General Medicine": "Provides primary healthcare, preventive medicine, and management of chronic conditions."
    }

    def random_dob(start="1950-01-01", end="2015-12-31"):
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return (start_date + timedelta(days=random_days)).date()

    
    for name, desc in departments.items():
        d = Department(name=name, description=desc)
        db.session.add(d)
    db.session.commit()
    print("  Departments created")

    # -----------------
    # 40 Patients
    # -----------------
    patients = []
    used_patient_names = set()
    for i in range(NO_OF_PATIENTS):
        name = random.choice(names)
        last_name = random.choice(surnames)
        # Ensure unique name+last_name combination
        while (name + last_name) in used_patient_names:
            name = random.choice(names)
            last_name = random.choice(surnames)
        used_patient_names.add(name + last_name)
        p = Patient(
            name=name,
            last_name=last_name,
            dob=random_dob(),
            phone=str(fake.random_number(digits=10, fix_len=True)),
            address=f"{random.choice(streets)}, {random.choice(locations)}, {random.choice(cities)}",
            email=f"patient{i}@example.com",
            password="123",
            role="patient",
        )
        db.session.add(p)
        patients.append(p)
    db.session.commit()
    print(f"  Created {len(patients)} patients")

    # -----------------
    # 10 Doctors
    # -----------------
    doctors_created = []
    used_doctor_names = set()
    for i in range(NO_OF_DOCTORS):
        doc_info = random.choice(doctors)
        name = doc_info["name"]
        last_name = doc_info["surn"]
        # Ensure unique name+last_name combination
        while (name + last_name) in used_doctor_names:
            doc_info = random.choice(doctors)
            name = doc_info["name"]
            last_name = doc_info["surn"]
        used_doctor_names.add(name + last_name)
        k = random.randint(0, len(doctors) - 1)
        department = doctors[k]["dep"]
        speciality = doctors[k]["desc"]
        dob = random_dob(start="1960-01-01", end="1995-12-31")
        experience = int(date.today().year - dob.year - ((date.today().month, date.today().day) < (dob.month, dob.day)) - 25)
        dep = Department.query.filter_by(name=department).first()
        doc = Doctor(
            name="Dr. "+name,
            last_name=last_name,
            dob=dob,
            department=dep,
            speciality=speciality,
            experience=experience if experience > 0 else 1,
            phone=str(fake.random_number(digits=10, fix_len=True)),
            address=f"{random.choice(streets)}, {random.choice(locations)}, {random.choice(cities)}",
            email=f"doctor{i}@example.com",
            password="123",
            role="doctor"
        )
        db.session.add(doc)
        doctors_created.append(doc)
    db.session.commit()
    print(f"  Created {len(doctors_created)} doctors")

    sessions = [s.value for s in Sessions]
    start_date = START_DATE
    no_of_days=NO_OF_PAST_DAYS+NO_OF_FUTURE_DAYS
    slots_by_doctor = {}
    doctors = Doctor.query.all()
    for doc in doctors:
        slots_by_doctor[doc.id] = []
        for offset in range(no_of_days):
            d = start_date + timedelta(days=offset)
            for sess in sessions:
                slot = Slot(doctor=doc, date=d, session=sess, available=True)
                db.session.add(slot)
                slots_by_doctor[doc.id].append(slot)
    db.session.commit()
    print("  Created availability slots")

    # ---------- New logic: patient <-> doctors mapping ----------
# For reproducibility tune values here:
    MIN_DOCTORS_PER_PATIENT = 3
    MAX_DOCTORS_PER_PATIENT = 5

    patients = Patient.query.filter(Patient.status != "deleted").all()
    doctors = Doctor.query.all()
    doctor_ids = [d.id for d in doctors]

    # Map each patient to a small random subset of doctors
    patient_doctors_map = {}
    for p in patients:
        k = random.randint(MIN_DOCTORS_PER_PATIENT, min(MAX_DOCTORS_PER_PATIENT, len(doctors)))
        assigned = random.sample(doctor_ids, k)
        patient_doctors_map[p.id] = assigned

    # -----------------
    # Slot creation already exists above (slots_by_doctor)
    # Ensure slots_by_doctor is available here (created earlier)
    # -----------------
    today = date.today()

    # ---------- Appointment clustering parameters ----------
    # Each patient will have 1..3 clusters of visits per doctor they are connected to.
    MIN_CLUSTERS = 1
    MAX_CLUSTERS = 3
    MIN_CLUSTER_SIZE = 1      # consecutive visits in the cluster
    MAX_CLUSTER_SIZE = 6
    MAX_GAP_BETWEEN_CLUSTERS_DAYS = 30  # gap between clusters

    # helper to compute estimated charges for tests/meds
    def estimate_tests_and_meds_charge(tests, medicines):
        tests_cost = random.randint(0, 3) * 200  # rough random component
        meds_cost = 0
        if isinstance(medicines, list):
            meds_cost = len(medicines) * random.randint(50, 300)
        elif isinstance(medicines, str) and medicines:
            meds_cost = random.randint(50, 500)
        return tests_cost + meds_cost

    # ---------- Create clustered appointments ----------
    for pid, assigned_doctor_ids in patient_doctors_map.items():
        patient = db.session.get(Patient, pid)
        if not patient:
            continue

        # For each doctor assigned to this patient, create 0..N clusters of appointments
        for doc_id in assigned_doctor_ids:
            # available slots for this doctor
            free_slots = [s for s in slots_by_doctor[doc_id] if getattr(s, "available", True) and getattr(s, "is_free", True)]
            if not free_slots:
                continue

            # create clusters
            n_clusters = random.randint(MIN_CLUSTERS, MAX_CLUSTERS)
            # pick random start indices (so clusters are spread across timeframe)
            # We'll build clusters by picking a random date then taking consecutive dates/sessions
            for c in range(n_clusters):
                # choose a cluster central index in the free_slots list
                if not free_slots:
                    break

                cluster_size = random.randint(MIN_CLUSTER_SIZE, MAX_CLUSTER_SIZE)
                # choose a seed slot (pop it so we do not reuse same slot too often)
                seed_idx = random.randint(0, len(free_slots) - 1)
                seed_slot = free_slots.pop(seed_idx)

                # collect cluster slots: try to pick adjacent days/sessions near seed
                cluster_slots = [seed_slot]
                # attempt to pick preceding and succeeding slots close to seed (by date)
                attempts = 0
                i = 0
                while len(cluster_slots) < cluster_size and free_slots and attempts < cluster_size * 5:
                    # pick candidate and accept if date within a small window of the seed
                    candidate_idx = random.randint(0, len(free_slots) - 1)
                    candidate = free_slots[candidate_idx]
                    day_diff = abs((candidate.date - seed_slot.date).days)
                    # allow same-day or within small neighbourhood to create "cluster"
                    if day_diff <= 3:
                        cluster_slots.append(candidate)
                        free_slots.pop(candidate_idx)
                    else:
                        # sometimes accept a slightly farther slot to increase variety
                        if random.random() < 0.15:
                            cluster_slots.append(candidate)
                            free_slots.pop(candidate_idx)
                        else:
                            attempts += 1

                # Book each slot in the cluster (if still free)
                # Book each slot in the cluster (if still free)
                for slot in cluster_slots:
                    try:
                        # create reason using your complaint lists
                        if patient.name in male_names:
                            comp = male_complaints
                        else:
                            comp = female_complaints
                        reason = random.choice(comp) + " " + random.choice(comp)

                        # Try to book the slot (this may raise ValueError for double-book)
                        slot.book(patient_id=patient.id, reason=reason)

                        # Immediately flush so the new appointment is visible for subsequent checks/queries
                        db.session.flush()

                    except ValueError as e:
                        # Don't rollback here — ValueError in our case is a business rule raised before DB change.
                        msg = str(e)
                        if "Patient already has an appointment in this slot" in msg:
                            # Find alternate slot among pre-built in-memory slots_by_doctor (fast and aware of in-session changes)
                            key = (slot.date, slot.session)
                            possible = []
                            # gather all slots for this date/session from slots_by_doctor
                            for doc_id, slist in slots_by_doctor.items():
                                # skip the original doctor to prefer other doctors
                                if doc_id == slot.doctor_id:
                                    continue
                                for s in slist:
                                    if s.date == slot.date and s.session == slot.session:
                                        # check basic availability flags and ensure not the original slot
                                        if getattr(s, "available", True) and getattr(s, "is_free", True):
                                            possible.append(s)

                            # remove any candidate that would violate patient's in-memory appointments
                            def conflicts_with_patient(s):
                                for appt in patient.appointments:
                                    if appt.slot.date == s.date and appt.slot.session == s.session and appt.status != AppointmentStatus.CANCELLED:
                                        return True
                                return False

                            candidates = [s for s in possible if not conflicts_with_patient(s)]
                            if not candidates:
                                # no alternate available, skip
                                continue

                            alt_slot = random.choice(candidates)

                            try:
                                alt_slot.book(patient_id=patient.id, reason=reason)
                                db.session.flush()   # flush the successful alternate booking
                            except ValueError:
                                # unlikely: another double-book detected by model; skip
                                db.session.rollback()
                                continue
                            except Exception:
                                # DB or unexpected failure trying to book the alternate slot
                                db.session.rollback()
                                continue

                        else:
                            # Some other business-rule error: skip and continue
                            continue

                    except Exception:
                        # database-level error during flush/insert etc.
                        db.session.rollback()
                        continue

                        
    # ---------- Post-process: Ensure all past appointments are closed (completed or cancelled) ----------
    # Iterate all appointments up to today and ensure none are left in BOOKED state in the past.
    all_appointments = Appointment.query.all()
    for appt in all_appointments:
        # safeguard: use status attribute names consistent with your model
        appt_date = getattr(appt, "slot").date if getattr(appt, "slot", None) else None
        status = getattr(appt, "status", None)

        if appt_date and appt_date < today:
            # If booked in past, either complete with treatment or cancel
            if status == AppointmentStatus.BOOKED:
                # decide completed vs cancelled (weighted towards completed)
                if random.random() < 0.80:
                    # complete the appointment and create Treatment
                    if appt.patient.name in female_names:
                        diag = female_diagnoses
                    else:
                        diag = male_diagnoses
                    prescription = generate_prescription_medicines(num_meds=random.randint(1, 5))
                    consultation_fee = random.randint(1, 5) * 500  # mandatory charge
                    treatment = Treatment(
                        appointment_id=appt.id,
                        diagnosis=random.choice(diag),
                        prescription=prescription,
                        notes=fake.paragraph(nb_sentences=2),
                        visit_type=random.choice(visit_types),
                        tests=random.choice(tests),
                        medicines=prescription,
                        consultation_fee=consultation_fee
                    )
                    # compute extra charges for tests & meds and attach as total_charge if model has it
                    extra = estimate_tests_and_meds_charge(treatment.tests, treatment.medicines)
                    total = consultation_fee + extra
                    # if model supports a total/amount field, set it; otherwise record in notes
                    if hasattr(treatment, "total_charge"):
                        setattr(treatment, "total_charge", total)
                    elif hasattr(treatment, "bill_amount"):
                        setattr(treatment, "bill_amount", total)
                    else:
                        # append billing info to notes
                        treatment.notes = (treatment.notes or "") + f"\n\nEstimated total charge: {total}"

                    db.session.add(treatment)
                    db.session.flush()
                    # use your model's API to mark appointment complete
                    try:
                        appt.complete(treatment)
                    except Exception:
                        # fallback: set status and link treatment
                        appt.status = AppointmentStatus.COMPLETED
                        # if your appt has treatment_id field:
                        if hasattr(appt, "treatment_id"):
                            appt.treatment_id = treatment.id
                else:
                    # cancel the appointment
                    try:
                        appt.cancel()
                    except Exception:
                        appt.status = AppointmentStatus.CANCELLED
                        # free the slot if necessary
                        if hasattr(appt.slot, "available"):
                            appt.slot.available = True

    # Commit final changes
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error during final commit:", e)

    print("  Appointments & treatments created (clusters, past closed, charges added)")


if __name__ == "__main__":
    with app.app_context():
        seed_database()
