# add_category_column.py
from app import create_app, db
from sqlalchemy import text

def add_category_column():
    app = create_app()
    with app.app_context():
        try:
            # Check if column exists
            result = db.session.execute(text("PRAGMA table_info(services)"))
            columns = [row[1] for row in result]
            
            if 'category' in columns:
                print("✓ Category column already exists!")
                return
            
            # Add category column
            print("Adding category column to services table...")
            db.session.execute(text('ALTER TABLE services ADD COLUMN category VARCHAR(50)'))
            db.session.commit()
            print("✓ Category column added successfully!")
            
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error: {e}")

if __name__ == '__main__':
    add_category_column()