"""
Migration script to add role column to users table
"""
from sqlalchemy import text
from database import engine

def add_role_column():
    with engine.connect() as connection:
        # Check if column exists
        result = connection.execute(
            text("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_name='users' AND column_name='role'
            )
            """)
        )
        column_exists = result.scalar()
        
        if not column_exists:
            # Add role column
            connection.execute(
                text("""
                ALTER TABLE users 
                ADD COLUMN role VARCHAR(45) DEFAULT NULL
                """)
            )
            connection.commit()
            print("✓ Role column added successfully to users table")
        else:
            # Modify existing column
            connection.execute(
                text("""
                ALTER TABLE users 
                ALTER COLUMN role TYPE VARCHAR(45),
                ALTER COLUMN role SET DEFAULT NULL
                """)
            )
            connection.commit()
            print("✓ Role column updated successfully")

if __name__ == "__main__":
    try:
        add_role_column()
    except Exception as e:
        print(f"✗ Error: {e}")
