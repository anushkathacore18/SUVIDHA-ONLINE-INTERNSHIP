from app import app, db
from sqlalchemy import text

def migrate():
    with app.app_context():
        try:
            # Drop existing tables in correct order
            db.session.execute(text('SET FOREIGN_KEY_CHECKS=0'))
            db.session.execute(text('DROP TABLE IF EXISTS application'))
            db.session.execute(text('DROP TABLE IF EXISTS internship'))
            db.session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
            db.session.commit()
            
            # Recreate all tables
            db.create_all()
            print("Migration completed successfully! Database tables have been recreated.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error during migration: {str(e)}")
            raise

if __name__ == '__main__':
    migrate() 