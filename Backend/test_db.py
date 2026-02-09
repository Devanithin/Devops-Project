from database import engine, Base
import models
# This command tells Postgres to create the tables if they don't exist
try:
   Base.metadata.create_all(bind=engine)
   print("✅ Success! Connection established and tables created.")
except Exception as e:
   print(f"❌ Error: {e}")
