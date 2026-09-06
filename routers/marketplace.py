from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, SessionLocal
from models import ProduceListingTable, BidTable
from schemas import ProduceListing, Bid


router = APIRouter(
    prefix="/api/marketplace",
    tags=["Marketplace"]
)


# ==========================================
# SEED PRODUCE LISTINGS
# ==========================================

def seed_initial_listings():

    db = SessionLocal()

    try:

        existing_count = db.query(
            ProduceListingTable
        ).count()

        if existing_count == 0:

            seed_data = [

                ProduceListingTable(
                    farmer_name="Ramesh Patil",
                    phone="+919822112233",
                    district="Nashik",
                    crop_type="Onion",
                    quantity_quintals=50.0,
                    expected_price_per_quintal=2400.0,
                    grade="Grade A",
                    uniformity_score=94.0,
                    defect_percentage=3.2
                ),

                ProduceListingTable(
                    farmer_name="Sunil Jadhav",
                    phone="+919822112244",
                    district="Nashik",
                    crop_type="Onion",
                    quantity_quintals=35.0,
                    expected_price_per_quintal=2350.0,
                    grade="Grade A",
                    uniformity_score=92.0,
                    defect_percentage=4.1
                ),

                ProduceListingTable(
                    farmer_name="Mahesh Shinde",
                    phone="+919822112255",
                    district="Latur",
                    crop_type="Soybean",
                    quantity_quintals=40.0,
                    expected_price_per_quintal=4700.0,
                    grade="Grade A",
                    uniformity_score=95.0,
                    defect_percentage=2.8
                ),

                ProduceListingTable(
                    farmer_name="Vijay Pawar",
                    phone="+919822112266",
                    district="Latur",
                    crop_type="Soybean",
                    quantity_quintals=60.0,
                    expected_price_per_quintal=4650.0,
                    grade="Grade A",
                    uniformity_score=93.0,
                    defect_percentage=3.5
                ),

                ProduceListingTable(
                    farmer_name="Santosh Deshmukh",
                    phone="+919822112277",
                    district="Akola",
                    crop_type="Cotton",
                    quantity_quintals=25.0,
                    expected_price_per_quintal=7200.0,
                    grade="Grade A",
                    uniformity_score=96.0,
                    defect_percentage=2.4
                ),

                ProduceListingTable(
                    farmer_name="Anil Wankhede",
                    phone="+919822112288",
                    district="Akola",
                    crop_type="Cotton",
                    quantity_quintals=30.0,
                    expected_price_per_quintal=7100.0,
                    grade="Grade A",
                    uniformity_score=94.0,
                    defect_percentage=3.0
                )
            ]

            db.add_all(seed_data)
            db.commit()

            print("6 marketplace listings seeded successfully.")

        else:

            print(
                f"Marketplace already contains "
                f"{existing_count} listing(s)."
            )

    finally:

        db.close()


# ==========================================
# SEED SAMPLE BIDS
# ==========================================

def seed_sample_bids():

    db = SessionLocal()

    try:

        existing_bids = db.query(
            BidTable
        ).count()

        if existing_bids > 0:

            print(
                f"Marketplace already contains "
                f"{existing_bids} bid(s)."
            )

            return

        nashik_onion_listing = (
            db.query(ProduceListingTable)
            .filter(
                ProduceListingTable.district == "Nashik",
                ProduceListingTable.crop_type == "Onion"
            )
            .first()
        )

        if not nashik_onion_listing:

            print("Nashik Onion listing not found.")
            return

        sample_bids = [

            BidTable(
                listing_id=nashik_onion_listing.id,
                buyer_company="Sahyadri Agro",
                bid_price_per_quintal=2420.0,
                delivery_terms="Pickup from farm within 2 days",
                status="pending"
            ),

            BidTable(
                listing_id=nashik_onion_listing.id,
                buyer_company="MahaExports Ltd",
                bid_price_per_quintal=2450.0,
                delivery_terms="Buyer arranges transport",
                status="pending"
            )
        ]

        db.add_all(sample_bids)
        db.commit()

        print("2 sample bids seeded successfully.")

    finally:

        db.close()


# ==========================================
# GET ALL LISTINGS + FILTERS
# ==========================================

@router.get("/listings")
def get_listings(

    crop_type: Optional[str] = Query(
        None,
        description="Filter by crop (case-insensitive)"
    ),

    district: Optional[str] = Query(
        None,
        description="Filter by district (case-insensitive)"
    ),

    min_grade: Optional[str] = Query(
        None,
        description="e.g. 'Grade A' only"
    ),

    db: Session = Depends(get_db)
):

    query = db.query(
        ProduceListingTable
    )

    if crop_type:

        query = query.filter(
            ProduceListingTable.crop_type.ilike(
                f"%{crop_type}%"
            )
        )

    if district:

        query = query.filter(
            ProduceListingTable.district.ilike(
                f"%{district}%"
            )
        )

    if min_grade:

        query = query.filter(
            ProduceListingTable.grade.ilike(
                f"%{min_grade}%"
            )
        )

    return query.all()


# ==========================================
# CREATE PRODUCE LISTING
# ==========================================

@router.post("/listings")
def create_listing(
    listing: ProduceListing,
    db: Session = Depends(get_db)
):

    new_listing = ProduceListingTable(
        farmer_name=listing.farmer_name,
        phone=listing.phone,
        district=listing.district,
        crop_type=listing.crop_type,
        quantity_quintals=listing.quantity_quintals,
        expected_price_per_quintal=(
            listing.expected_price_per_quintal
        ),
        grade=listing.grade,
        uniformity_score=listing.uniformity_score,
        defect_percentage=listing.defect_percentage
    )

    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)

    return new_listing


# ==========================================
# CREATE BID
# ==========================================

@router.post("/bids")
def create_bid(
    bid: Bid,
    db: Session = Depends(get_db)
):

    listing = (
        db.query(ProduceListingTable)
        .filter(
            ProduceListingTable.id == bid.listing_id
        )
        .first()
    )

    if not listing:

        raise HTTPException(
            status_code=404,
            detail=f"Listing ID {bid.listing_id} not found"
        )

    new_bid = BidTable(
        listing_id=bid.listing_id,
        buyer_company=bid.buyer_company,
        bid_price_per_quintal=bid.bid_price_per_quintal,
        delivery_terms=bid.delivery_terms,
        status="pending"
    )

    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)

    return new_bid


# ==========================================
# GET BIDS FOR LISTING
# ==========================================

@router.get("/listings/{listing_id}/bids")
def get_listing_bids(
    listing_id: str,
    db: Session = Depends(get_db)
):

    listing = (
        db.query(ProduceListingTable)
        .filter(
            ProduceListingTable.id == listing_id
        )
        .first()
    )

    if not listing:

        raise HTTPException(
            status_code=404,
            detail=f"Listing ID {listing_id} not found"
        )

    bids = (
        db.query(BidTable)
        .filter(
            BidTable.listing_id == listing_id
        )
        .order_by(
            BidTable.bid_price_per_quintal.desc()
        )
        .all()
    )

    return bids


# ==========================================
# UPDATE BID STATUS
# ==========================================

@router.patch("/bids/{bid_id}/status")
def update_bid_status(
    bid_id: str,
    new_status: str,
    db: Session = Depends(get_db)
):

    if new_status not in [
        "accepted",
        "rejected"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Status must be 'accepted' or 'rejected'"
        )

    bid = (
        db.query(BidTable)
        .filter(
            BidTable.id == bid_id
        )
        .first()
    )

    if not bid:

        raise HTTPException(
            status_code=404,
            detail=f"Bid ID {bid_id} not found"
        )

    bid.status = new_status

    if new_status == "accepted":

        competing_bids = (
            db.query(BidTable)
            .filter(
                BidTable.listing_id == bid.listing_id,
                BidTable.id != bid.id
            )
            .all()
        )

        for competing_bid in competing_bids:

            competing_bid.status = "rejected"

    db.commit()
    db.refresh(bid)

    return bid