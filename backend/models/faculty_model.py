"""
Handles Faculty model for the attendance system. Provides CRUD operations and
lookup helpers for faculty records using Supabase.
"""
from ..supabase_client import supabase
from typing import Optional

def create_faculty(data: dict) -> dict:
    """Insert new faculty record."""
    res = supabase.table("faculty").insert([data]).execute()
    return res.data[0] if res.data else None

def get_faculty_by_id(faculty_id: str) -> Optional[dict]:
    """Fetch faculty member by UUID."""
    res = supabase.table("faculty").select("*").eq("id", faculty_id).single().execute()
    return res.data if res.data else None

def get_all_faculty() -> list:
    """Get all faculty members."""
    res = supabase.table("faculty").select("*").execute()
    return res.data or []

def update_faculty(faculty_id: str, updates: dict) -> Optional[dict]:
    """Update faculty record."""
    res = supabase.table("faculty").update(updates).eq("id", faculty_id).execute()
    return res.data[0] if res.data else None

def delete_faculty(faculty_id: str) -> bool:
    """Delete faculty by id."""
    res = supabase.table("faculty").delete().eq("id", faculty_id).execute()
    return bool(res.data)

def get_faculty_by_email(email: str) -> Optional[dict]:
    """Fetch faculty by email."""
    res = supabase.table("faculty").select("*").eq("email", email).single().execute()
    return res.data if res.data else None
