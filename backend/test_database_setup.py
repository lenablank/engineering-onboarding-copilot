"""
Test database setup and schema for Documentation Gap Radar.

This script verifies:
1. Database connection works
2. Tables can be created
3. CRUD operations work
4. Schema is correct
"""
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

load_dotenv()

from app.models import Base, engine, get_db, DocumentationGap
from app.models.gap import GapStatus
from sqlalchemy import text


def test_database_setup():
    """Test database setup and basic operations."""
    
    print("=" * 70)
    print("DATABASE SETUP TEST")
    print("=" * 70)
    print()
    
    # Step 1: Create all tables
    print("Step 1: Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ Tables created successfully")
    except Exception as e:
        print(f"✗ Failed to create tables: {e}")
        return False
    
    # Step 2: Test database connection
    print("\nStep 2: Testing database connection...")
    db = next(get_db())
    try:
        # Test query
        db.execute(text("SELECT 1"))
        print("✓ Database connection successful")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False
    finally:
        db.close()
    
    # Step 3: Insert test data
    print("\nStep 3: Inserting test documentation gap...")
    db = next(get_db())
    try:
        test_gap = DocumentationGap(
            question="How do I configure SSL certificates?",
            confidence_score=0.45,
            frequency=1,
            status=GapStatus.NEW,
            retrieval_context=[
                {
                    "chunk_id": 1,
                    "content": "Basic security setup...",
                    "score": 0.4
                }
            ]
        )
        db.add(test_gap)
        db.commit()
        db.refresh(test_gap)
        
        print(f"✓ Inserted gap with ID: {test_gap.id}")
        print(f"  Question: {test_gap.question}")
        print(f"  Confidence: {test_gap.confidence_score}")
        print(f"  Status: {test_gap.status.value}")
        print(f"  Created: {test_gap.created_at}")
        
        gap_id = test_gap.id
        
    except Exception as e:
        print(f"✗ Failed to insert test data: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    # Step 4: Query test data
    print("\nStep 4: Querying documentation gaps...")
    db = next(get_db())
    try:
        # Query by ID
        gap = db.query(DocumentationGap).filter(DocumentationGap.id == gap_id).first()
        if gap:
            print(f"✓ Found gap by ID: {gap.question}")
        else:
            print("✗ Could not find gap by ID")
            return False
        
        # Query all gaps
        all_gaps = db.query(DocumentationGap).all()
        print(f"✓ Total gaps in database: {len(all_gaps)}")
        
        # Query by status
        new_gaps = db.query(DocumentationGap).filter(
            DocumentationGap.status == GapStatus.NEW
        ).all()
        print(f"✓ Gaps with status 'NEW': {len(new_gaps)}")
        
    except Exception as e:
        print(f"✗ Query failed: {e}")
        return False
    finally:
        db.close()
    
    # Step 5: Update test data
    print("\nStep 5: Updating gap frequency...")
    db = next(get_db())
    try:
        gap = db.query(DocumentationGap).filter(DocumentationGap.id == gap_id).first()
        if gap:
            gap.frequency += 1
            gap.status = GapStatus.REVIEWED
            db.commit()
            print(f"✓ Updated gap frequency to: {gap.frequency}")
            print(f"✓ Updated status to: {gap.status.value}")
        else:
            print("✗ Gap not found for update")
            return False
    except Exception as e:
        print(f"✗ Update failed: {e}")
        db.rollback()
        return False
    finally:
        db.close()
    
    # Step 6: Test to_dict() method
    print("\nStep 6: Testing to_dict() serialization...")
    db = next(get_db())
    try:
        gap = db.query(DocumentationGap).filter(DocumentationGap.id == gap_id).first()
        if gap:
            gap_dict = gap.to_dict()
            print(f"✓ Serialized to dict:")
            print(f"  ID: {gap_dict['id']}")
            print(f"  Question: {gap_dict['question']}")
            print(f"  Frequency: {gap_dict['frequency']}")
            print(f"  Status: {gap_dict['status']}")
        else:
            print("✗ Gap not found for serialization")
            return False
    except Exception as e:
        print(f"✗ Serialization failed: {e}")
        return False
    finally:
        db.close()
    
    # Step 7: Verify schema
    print("\nStep 7: Verifying table schema...")
    try:
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        # Check table exists
        tables = inspector.get_table_names()
        if "documentation_gaps" in tables:
            print("✓ Table 'documentation_gaps' exists")
        else:
            print("✗ Table 'documentation_gaps' not found")
            return False
        
        # Check columns
        columns = inspector.get_columns("documentation_gaps")
        column_names = [col['name'] for col in columns]
        
        required_columns = [
            'id', 'question', 'confidence_score', 'frequency',
            'status', 'retrieval_context', 'created_at', 'updated_at'
        ]
        
        for col_name in required_columns:
            if col_name in column_names:
                print(f"  ✓ Column '{col_name}' exists")
            else:
                print(f"  ✗ Column '{col_name}' missing")
                return False
        
        # Check indexes
        indexes = inspector.get_indexes("documentation_gaps")
        print(f"✓ Found {len(indexes)} indexes")
        for idx in indexes:
            print(f"  - Index on: {idx['column_names']}")
        
    except Exception as e:
        print(f"✗ Schema verification failed: {e}")
        return False
    
    # Cleanup
    print("\nStep 8: Cleanup test data...")
    db = next(get_db())
    try:
        db.query(DocumentationGap).filter(DocumentationGap.id == gap_id).delete()
        db.commit()
        print("✓ Test data cleaned up")
    except Exception as e:
        print(f"⚠ Cleanup warning: {e}")
    finally:
        db.close()
    
    print()
    print("=" * 70)
    print("✓ ALL TESTS PASSED - DATABASE SETUP COMPLETE")
    print("=" * 70)
    print()
    print("Database file: gaps.db")
    print("Table: documentation_gaps")
    print("Ready for Gap Radar implementation!")
    
    return True


if __name__ == "__main__":
    success = test_database_setup()
    sys.exit(0 if success else 1)
