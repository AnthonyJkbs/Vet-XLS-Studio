from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import date, timedelta


@dataclass
class Owner:
    id: int
    name: str
    phone: str = ""
    email: str = ""
    address: str = ""


@dataclass
class Pet:
    id: int
    name: str
    species: str = ""
    breed: str = ""
    sex: str = ""
    birth_date: str = ""
    microchip: str = ""
    owner_id: int | None = None
    hospitalized: bool = False


@dataclass
class Appointment:
    id: int
    pet_id: int
    date: str = ""
    time: str = ""
    vet: str = ""
    reason: str = ""
    status: str = "Scheduled"


@dataclass
class Treatment:
    id: int
    pet_id: int
    date: str = ""
    type: str = "Treatment"
    description: str = ""
    vet: str = ""
    next_due: str = ""


class Store:
    """In-memory clinic database with JSON persistence and cascade deletes."""

    def __init__(self) -> None:
        self.owners: list[Owner] = []
        self.pets: list[Pet] = []
        self.appointments: list[Appointment] = []
        self.treatments: list[Treatment] = []
        self._next_id: int = 1
        self.hospital_capacity: int = 15
        self.night_vet_name: str = ""
        self.night_vet_phone: str = ""
        self.notes: list[dict] = []

    def _id(self) -> int:
        nid = self._next_id
        self._next_id += 1
        return nid

    def _reindex(self) -> None:
        ids = ([o.id for o in self.owners] + [p.id for p in self.pets]
               + [a.id for a in self.appointments] + [t.id for t in self.treatments])
        self._next_id = max(ids, default=0) + 1

    # ------------------------------------------------------- lookups ----
    def get_owner(self, oid):
        return next((o for o in self.owners if o.id == oid), None)

    def get_pet(self, pid):
        return next((p for p in self.pets if p.id == pid), None)

    def pets_of(self, owner_id):
        return [p for p in self.pets if p.owner_id == owner_id]

    def appointments_of(self, pet_id):
        return [a for a in self.appointments if a.pet_id == pet_id]

    def treatments_of(self, pet_id):
        return [t for t in self.treatments if t.pet_id == pet_id]

    def owner_name(self, pet) -> str:
        o = self.get_owner(pet.owner_id) if pet else None
        return o.name if o else ""

    def pet_label(self, pet_id) -> str:
        p = self.get_pet(pet_id)
        return f"{p.name} ({self.owner_name(p)})" if p else f"#{pet_id}"

    # ---------------------------------------------------------- CRUD ----
    def add_owner(self, **kw) -> Owner:
        o = Owner(id=self._id(), **kw)
        self.owners.append(o)
        return o

    def add_pet(self, **kw) -> Pet:
        p = Pet(id=self._id(), **kw)
        self.pets.append(p)
        return p

    def add_appointment(self, **kw) -> Appointment:
        a = Appointment(id=self._id(), **kw)
        self.appointments.append(a)
        return a

    def add_treatment(self, **kw) -> Treatment:
        t = Treatment(id=self._id(), **kw)
        self.treatments.append(t)
        return t

    def delete_owner(self, oid) -> tuple[int, int]:
        pet_ids = {p.id for p in self.pets if p.owner_id == oid}
        n_appts = sum(1 for a in self.appointments if a.pet_id in pet_ids)
        n_treats = sum(1 for t in self.treatments if t.pet_id in pet_ids)
        self.treatments = [t for t in self.treatments if t.pet_id not in pet_ids]
        self.appointments = [a for a in self.appointments if a.pet_id not in pet_ids]
        self.pets = [p for p in self.pets if p.owner_id != oid]
        self.owners = [o for o in self.owners if o.id != oid]
        return len(pet_ids), n_appts + n_treats

    def delete_pet(self, pid) -> int:
        before = len(self.appointments) + len(self.treatments)
        self.appointments = [a for a in self.appointments if a.pet_id != pid]
        self.treatments = [t for t in self.treatments if t.pet_id != pid]
        self.pets = [p for p in self.pets if p.id != pid]
        return before - (len(self.appointments) + len(self.treatments))

    # ------------------------------------------------------ dashboard ---
    def is_empty(self) -> bool:
        return not (self.owners or self.pets or self.appointments or self.treatments)

    def upcoming_appointments(self, limit=6):
        today = date.today().isoformat()
        rows = [a for a in self.appointments
                if a.status == "Scheduled" and a.date >= today]
        rows.sort(key=lambda a: (a.date, a.time))
        return rows[:limit]

    def vaccinations_due(self, days=30):
        start = date.today()
        end = start + timedelta(days=days)
        rows = []
        for t in self.treatments:
            if t.type != "Vaccination" or not t.next_due:
                continue
            try:
                d = date.fromisoformat(t.next_due)
            except ValueError:
                continue
            if d <= end:
                rows.append((d, t))
        rows.sort(key=lambda r: r[0])
        return rows

    def species_breakdown(self):
        counts: dict[str, int] = {}
        for p in self.pets:
            key = p.species.strip() or "Other"
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: -kv[1]))

    def add_note(self, text: str) -> dict:
        nid = max((n.get("id", 0) for n in self.notes), default=0) + 1
        note = {"id": nid, "text": text.strip(),
                "date": __import__("datetime").date.today().isoformat()}
        self.notes.append(note)
        return note

    def update_note(self, idx: int, text: str) -> None:
        if 0 <= idx < len(self.notes):
            self.notes[idx]["text"] = text.strip()
            self.notes[idx]["date"] = \
                __import__("datetime").date.today().isoformat()

    def delete_note(self, idx: int) -> None:
        if 0 <= idx < len(self.notes):
            del self.notes[idx]

    def hospitalized_count(self) -> int:
        return sum(1 for p in self.pets if p.hospitalized)

    def hospital_free(self) -> int:
        return max(self.hospital_capacity - self.hospitalized_count(), 0)

    # ---------------------------------------------------- persistence ---
    def save(self, path: str) -> None:
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)
        data = {
            "next_id": self._next_id,
            "hospital_capacity": self.hospital_capacity,
            "night_vet_name": self.night_vet_name,
            "night_vet_phone": self.night_vet_phone,
            "owners": [asdict(o) for o in self.owners],
            "pets": [asdict(p) for p in self.pets],
            "appointments": [asdict(a) for a in self.appointments],
            "treatments": [asdict(t) for t in self.treatments],
            "notes": list(self.notes),
        }
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        os.replace(tmp, path)

    @classmethod
    def load(cls, path: str) -> "Store":
        store = cls()
        if not os.path.exists(path):
            return store
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (json.JSONDecodeError, OSError):
            return store
        store.owners = [Owner(**d) for d in data.get("owners", [])]
        store.pets = [Pet(**d) for d in data.get("pets", [])]
        store.appointments = [Appointment(**d) for d in data.get("appointments", [])]
        store.treatments = [Treatment(**d) for d in data.get("treatments", [])]
        cap = data.get("hospital_capacity")
        if isinstance(cap, int) and cap > 0:
            store.hospital_capacity = cap
        store.night_vet_name = str(data.get("night_vet_name") or "")
        store.night_vet_phone = str(data.get("night_vet_phone") or "")
        store.notes = [dict(n) for n in data.get("notes", [])]
        store._reindex()
        stored = data.get("next_id")
        if isinstance(stored, int):
            store._next_id = max(store._next_id, stored)
        return store
