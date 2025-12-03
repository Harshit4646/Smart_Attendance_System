"""
Handles the Students model using Supabase. Provides CRUD operations and lookups
for student info, for use in API and admin modules. Uses supabase_client.
"""
from supabase_client import supabase
from typing import Optional

def create_student(data: dict) -> dict:
    """Insert a new student record."""
    res = supabase.table("students").insert([data]).execute()
    return res.data[0] if res.data else None

def get_student_by_id(student_id: str) -> Optional[dict]:
    """Fetch student by their UUID."""
    res = supabase.table("students").select("*").eq("id", student_id).single().execute()
    return res.data if res.data else None

def get_all_students() -> list:
    """Get all students."""
    res = supabase.table("students").select("*").execute()
    return res.data or []

def update_student(student_id: str, updates: dict) -> Optional[dict]:
    """Update a student's data."""
    res = supabase.table("students").update(updates).eq("id", student_id).execute()
    return res.data[0] if res.data else None

def delete_student(student_id: str) -> bool:
    """Delete a student by id."""
    res = supabase.table("students").delete().eq("id", student_id).execute()
    return bool(res.data)

def get_student_by_email(email: str) -> Optional[dict]:
    """Fetch student by email address."""
    res = supabase.table("students").select("*").eq("email", email).single().execute()
    return res.data if res.data else None

