from __future__ import annotations

import random
from datetime import date, timedelta

from models import Appointment, Owner, Pet, Store, Treatment

FIRST = ["Anna", "Mark", "Sofia", "James", "Elena", "Peter", "Lucy", "Omar",
         "Nina", "David", "Grace", "Tom", "Hana", "Leo", "Maya", "Igor",
         "Clara", "Sam", "Iris", "Noah", "Emma", "Paul"]
LAST = ["Smith", "Johnson", "Brown", "Garcia", "Miller", "Davis", "Wilson",
        "Moore", "Taylor", "Anderson", "Thomas", "White", "Harris",
        "Martin", "Clark", "Lewis", "Walker", "Hall", "Young", "King"]

STREETS = ["Maple St", "Oak Ave", "Cedar Ln", "Pine Rd", "Elm Dr",
           "Willow Way", "Birch Blvd", "Aspen Ct"]

SPECIES = {
    "Dog": ["Labrador", "Beagle", "Poodle", "Border Collie", "Bulldog",
            "Golden Retriever", "Dachshund", "Shiba Inu"],
    "Cat": ["Domestic Shorthair", "Siamese", "Maine Coon", "Persian",
            "Ragdoll", "Bengal"],
    "Bird": ["Parakeet", "Cockatiel", "Canary", "Lovebird"],
    "Rabbit": ["Holland Lop", "Netherland Dwarf", "Lionhead", "Rex"],
}

PET_NAMES = {
    "Dog": ["Max", "Bella", "Rocky", "Luna", "Charlie", "Daisy", "Milo",
            "Ruby", "Buddy", "Coco"],
    "Cat": ["Whiskers", "Oliver", "Misty", "Simba", "Nala", "Felix",
            "Pepper", "Mochi"],
    "Bird": ["Kiwi", "Sunny", "Rio", "Mango", "Sky"],
    "Rabbit": ["Clover", "Thumper", "Nibbles", "Snowball"],
}

VETS = ["Dr. Kim", "Dr. Alvarez", "Dr. Osei", "Dr. Novak", "Dr. Reyes"]

REASONS = ["Annual check-up", "Vaccination visit", "Skin irritation",
           "Limping", "Dental cleaning", "Ear infection", "Weight review",
           "Follow-up exam", "Spay/neuter consult", "Digestive upset"]

VACCINES = ["Rabies", "DHPP booster", "FVRCP", "Leptospirosis",
            "Bordetella", "FeLV"]


def build_sample(store: Store, seed=None) -> Store:
    rng = random.Random(seed)
    today = date.today()

    # owners ------------------------------------------------------------
    used_emails: set[str] = set()
    for i in range(20):
        first, last = rng.choice(FIRST), rng.choice(LAST)
        base = f"{first.lower()}.{last.lower()}{i}"
        email = f"{base}@example.com"
        while email in used_emails:
            base += str(rng.randint(0, 9))
            email = f"{base}@example.com"
        used_emails.add(email)
        store.add_owner(
            name=f"{first} {last}",
            phone=f"(555) {rng.randint(100, 999)}-{rng.randint(1000, 9999)}",
            email=email,
            address=f"{rng.randint(2, 480)} {rng.choice(STREETS)}",
        )

    # pets ---------------------------------------------------------------
    for i in range(30):
        species = rng.choice(list(SPECIES))
        birth = today - timedelta(days=rng.randint(120, 5000))
        store.add_pet(
            name=rng.choice(PET_NAMES[species]),
            species=species,
            breed=rng.choice(SPECIES[species]),
            sex=rng.choice(["M", "F"]),
            birth_date=birth.isoformat(),
            microchip="".join(rng.choices("0123456789", k=15)),
            owner_id=rng.choice(store.owners).id,
            hospitalized=rng.random() < 0.17,
        )

    store.hospital_capacity = 18
    store.night_vet_name = rng.choice(VETS)
    store.night_vet_phone = (f"(555) {rng.randint(100, 999)}-"
                             f"{rng.randint(1000, 9999)}")

    def rand_time():
        return f"{rng.randint(8, 17):02d}:{rng.choice(['00', '15', '30', '45'])}"

    # appointments ---------------------------------------------------------
    for pet in store.pets:
        for _ in range(rng.randint(1, 3)):
            future = rng.random() < 0.30
            if future:
                d = today + timedelta(days=rng.randint(1, 21))
                status = "Scheduled"
            else:
                d = today - timedelta(days=rng.randint(1, 365))
                status = "Completed" if rng.random() < 0.85 else "Cancelled"
            store.add_appointment(
                pet_id=pet.id, date=d.isoformat(), time=rand_time(),
                vet=rng.choice(VETS), reason=rng.choice(REASONS),
                status=status,
            )

    # treatments & vaccinations ---------------------------------------------
    for pet in store.pets:
        for _ in range(rng.randint(1, 3)):
            is_vax = rng.random() < 0.45
            given = today - timedelta(days=rng.randint(5, 400))
            entry = dict(
                pet_id=pet.id, date=given.isoformat(),
                vet=rng.choice(VETS),
                description=(rng.choice(VACCINES) if is_vax
                             else rng.choice(["Antibiotic course",
                                              "Wound treatment",
                                              "Deworming",
                                              "Allergy injection",
                                              "Nail trim + exam"])),
            )
            if is_vax:
                entry["type"] = "Vaccination"
                entry["next_due"] = (given + timedelta(days=365)).isoformat()
            store.add_treatment(**entry)

    for _ in range(8):
        pet = rng.choice(store.pets)
        store.add_treatment(
            pet_id=pet.id,
            date=(today - timedelta(days=rng.randint(30, 340))).isoformat(),
            type="Vaccination",
            description=rng.choice(VACCINES),
            vet=rng.choice(VETS),
            next_due=(today + timedelta(days=rng.randint(-4, 28))).isoformat(),
        )
    return store
