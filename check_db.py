from sqlmodel import Session, create_engine, select
from models import Room

engine = create_engine("sqlite:///hotel_inr.db")

with Session(engine) as session:
    rooms = session.exec(select(Room)).all()
    if not rooms:
        print("No rooms found.")
    else:
        print(f"Found {len(rooms)} rooms.")
        # Check unique prices
        prices = set((r.type, r.price_per_night) for r in rooms)
        for r_type, price in prices:
            print(f"Type: {r_type}, Price: {price}")
