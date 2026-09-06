from database import SessionLocal, engine
import models
import uuid

# Ensure all tables are created
models.Base.metadata.create_all(bind=engine)

def seed_database():
    db = SessionLocal()
    
    try:
        # Clear existing dummy data
        db.query(models.Listing).delete()
        
        # Insert 15 Verified Produce Listings matching the current schema keys
        listings = [
            {"id": str(uuid.uuid4()), "crop_type": "Red Onion", "district": "Pimpalgaon, Nashik", "quantity_quintals": 150, "expected_price_per_quintal": 2200, "grade": "Grade A", "farmer_name": "Suresh", "phone": "9876543210", "defect_percentage": 2.1, "uniformity_score": 95},
            {"id": str(uuid.uuid4()), "crop_type": "Red Onion", "district": "Lasalgaon, Nashik", "quantity_quintals": 100, "expected_price_per_quintal": 2550, "grade": "Grade A", "farmer_name": "Ramesh", "phone": "9876543211", "defect_percentage": 1.5, "uniformity_score": 98},
            {"id": str(uuid.uuid4()), "crop_type": "Red Onion", "district": "Dindori, Nashik", "quantity_quintals": 50, "expected_price_per_quintal": 2300, "grade": "Grade B", "farmer_name": "Ganesh", "phone": "9876543212", "defect_percentage": 5.0, "uniformity_score": 85},
            {"id": str(uuid.uuid4()), "crop_type": "Red Onion", "district": "Kalwan, Nashik", "quantity_quintals": 80, "expected_price_per_quintal": 2400, "grade": "Grade A", "farmer_name": "Dinesh", "phone": "9876543213", "defect_percentage": 2.8, "uniformity_score": 92},
            {"id": str(uuid.uuid4()), "crop_type": "Red Onion", "district": "Yeola, Nashik", "quantity_quintals": 120, "expected_price_per_quintal": 2250, "grade": "Grade B", "farmer_name": "Mahesh", "phone": "9876543214", "defect_percentage": 4.5, "uniformity_score": 88},
            {"id": str(uuid.uuid4()), "crop_type": "Red Onion", "district": "Sinnar, Nashik", "quantity_quintals": 30, "expected_price_per_quintal": 2500, "grade": "Grade A", "farmer_name": "Rajesh", "phone": "9876543215", "defect_percentage": 1.2, "uniformity_score": 97},
            {"id": str(uuid.uuid4()), "crop_type": "Red Onion", "district": "Malegaon, Nashik", "quantity_quintals": 60, "expected_price_per_quintal": 2350, "grade": "Grade B", "farmer_name": "Mukesh", "phone": "9876543216", "defect_percentage": 6.1, "uniformity_score": 82},
            
            {"id": str(uuid.uuid4()), "crop_type": "Yellow Soybean", "district": "Ausa, Latur", "quantity_quintals": 200, "expected_price_per_quintal": 4200, "grade": "Grade A", "farmer_name": "Anil", "phone": "9876543217", "defect_percentage": 2.0, "uniformity_score": 94},
            {"id": str(uuid.uuid4()), "crop_type": "Yellow Soybean", "district": "Nilanga, Latur", "quantity_quintals": 150, "expected_price_per_quintal": 4500, "grade": "Grade A", "farmer_name": "Sunil", "phone": "9876543218", "defect_percentage": 1.8, "uniformity_score": 96},
            {"id": str(uuid.uuid4()), "crop_type": "Yellow Soybean", "district": "Renapur, Latur", "quantity_quintals": 50, "expected_price_per_quintal": 4300, "grade": "Grade B", "farmer_name": "Nitin", "phone": "9876543219", "defect_percentage": 4.2, "uniformity_score": 89},
            {"id": str(uuid.uuid4()), "crop_type": "Yellow Soybean", "district": "Udgir, Latur", "quantity_quintals": 100, "expected_price_per_quintal": 4400, "grade": "Grade A", "farmer_name": "Pravin", "phone": "9876543220", "defect_percentage": 2.5, "uniformity_score": 93},
            
            {"id": str(uuid.uuid4()), "crop_type": "Raw Cotton", "district": "Balapur, Akola", "quantity_quintals": 120, "expected_price_per_quintal": 6900, "grade": "Grade B", "farmer_name": "Sachin", "phone": "9876543221", "defect_percentage": 5.5, "uniformity_score": 86},
            {"id": str(uuid.uuid4()), "crop_type": "Raw Cotton", "district": "Patur, Akola", "quantity_quintals": 80, "expected_price_per_quintal": 7100, "grade": "Grade A", "farmer_name": "Kiran", "phone": "9876543222", "defect_percentage": 2.9, "uniformity_score": 91},
            {"id": str(uuid.uuid4()), "crop_type": "Raw Cotton", "district": "Barshitakli, Akola", "quantity_quintals": 40, "expected_price_per_quintal": 7300, "grade": "Grade A", "farmer_name": "Vijay", "phone": "9876543223", "defect_percentage": 1.1, "uniformity_score": 99},
            {"id": str(uuid.uuid4()), "crop_type": "Raw Cotton", "district": "Murtizapur, Akola", "quantity_quintals": 60, "expected_price_per_quintal": 7000, "grade": "Grade B", "farmer_name": "Ajay", "phone": "9876543224", "defect_percentage": 4.8, "uniformity_score": 87},
        ]
        
        # Execute the database insertion
        db.add_all([models.Listing(**l) for l in listings])
        db.commit()
        
        print("Seed Data Complete: 15 Listings and 20 Bids inserted successfully.")
    
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()