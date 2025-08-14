# db/seed.py
import json
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models import Atom

# Path to the atoms data directory
ATOMS_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'atoms')

def seed_atoms(db: Session):
    """Seeds the database with CPL atoms from JSON files."""
    print("Seeding CPL atoms...")
    # Get a list of all JSON files in the atoms directory
    json_files = [f for f in os.listdir(ATOMS_DIR) if f.endswith('.json')]

    for file_name in json_files:
        file_path = os.path.join(ATOMS_DIR, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            atom_id = data.get("atom_id")

            # Check if an atom with this ID already exists
            exists = db.query(Atom).filter(Atom.atom_id == atom_id).first()
            if not exists:
                # Create a new Atom object and add it to the database
                new_atom = Atom(
                    atom_id=atom_id,
                    intent=data.get("intent"),
                    pattern_data=data.get("pattern_data")
                )
                db.add(new_atom)
                print(f"  - Added atom: {atom_id}")
            else:
                print(f"  - Atom already exists, skipping: {atom_id}")

    db.commit()
    print("Atom seeding complete.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_atoms(db)
    finally:
        db.close()