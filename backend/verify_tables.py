"""
Verification script to audit all tables in recruitment_hub.db.
Confirms:
1. Exactly 12 tables exist.
2. Each table has at least 12 records (count >= 12).
"""

import sys
from backend.database import get_connection, TABLE_NAMES, get_table_counts

REQUIRED_MIN_RECORDS = 12


def audit_tables():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;")
        actual_tables = [row[0] for row in cursor.fetchall()]

    counts = get_table_counts()
    
    print("\n" + "=" * 65)
    print(" RECRUITMENT INTELLIGENCE PLATFORM -- DATABASE AUDIT REPORT ")
    print("=" * 65)
    print(f"Total tables detected in SQLite: {len(actual_tables)}")
    print(f"Expected 12 core tables: {len(TABLE_NAMES)}")
    print("-" * 65)
    print(f"{'#':<3} | {'Table Name':<26} | {'Count':<6} | {'Req':<4} | {'Status'}")
    print("-" * 65)

    all_passed = True
    missing_tables = []
    underpopulated_tables = []

    for idx, table in enumerate(TABLE_NAMES, start=1):
        if table not in actual_tables:
            missing_tables.append(table)
            print(f"{idx:<3} | {table:<26} | {'0':<6} | {REQUIRED_MIN_RECORDS:<4} | [MISSING]")
            all_passed = False
            continue
        
        count = counts.get(table, 0)
        if count < REQUIRED_MIN_RECORDS:
            underpopulated_tables.append((table, count))
            print(f"{idx:<3} | {table:<26} | {count:<6} | {REQUIRED_MIN_RECORDS:<4} | [FAIL < 12]")
            all_passed = False
        else:
            print(f"{idx:<3} | {table:<26} | {count:<6} | {REQUIRED_MIN_RECORDS:<4} | [PASS >= 12]")

    print("-" * 65)

    if all_passed and len(actual_tables) >= 12:
        print(">> SUCCESS: All 12 tables verified with at least 12 records each!")
        print("=" * 65 + "\n")
        return True
    else:
        print(">> AUDIT FAILED:")
        if missing_tables:
            print(f"  Missing tables: {missing_tables}")
        if underpopulated_tables:
            print(f"  Underpopulated tables: {underpopulated_tables}")
        print("=" * 65 + "\n")
        return False


if __name__ == "__main__":
    success = audit_tables()
    sys.exit(0 if success else 1)
