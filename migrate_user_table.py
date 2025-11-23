"""
Migration script to add email verification fields to User table
Run this once to update the database schema
"""
import streamlit as st
from sqlalchemy import text, create_engine

def migrate_user_table():
    db_url = st.secrets.get("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found in secrets")
        return
    
    engine = create_engine(db_url, connect_args={"sslmode": "require"})
    
    # SQL to add new columns if they don't exist
    migration_sql = """
    ALTER TABLE "user" 
    ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS verification_otp VARCHAR,
    ADD COLUMN IF NOT EXISTS otp_expires_at TIMESTAMP;
    """
    
    try:
        with engine.connect() as conn:
            conn.execute(text(migration_sql))
            conn.commit()
            print("✅ Migration successful! Added email verification columns.")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    st.write("🔄 Running database migration...")
    migrate_user_table()
    st.success("Migration complete! Please reboot the app.")
