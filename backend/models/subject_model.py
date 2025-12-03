"""
Handles Subjects model for attendance system. Provides CRUD operations and lookups
for subject records using Supabase.
"""
from supabase_client import supabase
from typing import Optional

def create_subject(data: dict) -> dict:
    """Insert new subject record."""
    res = supabase.table("subjects").insert([data]).execute()
    return res.data[0] if res.data else None

def get_subject_by_id(subject_id: str) -> Optional[dict]:
    """Fetch subject by UUID."""
    res = supabase.table("subjects").select("*").eq("id", subject_id).single().execute()
    return res.data if res.data else None

def get_all_subjects() -> list:
    """Get all subjects."""
    res = supabase.table("subjects").select("*").execute()
    return res.data or []

def update_subject(subject_id: str, updates: dict) -> Optional[dict]:
    """Update subject record."""
    res = supabase.table("subjects").update(updates).eq("id", subject_id).execute()
    return res.data[0] if res.data else None

def delete_subject(subject_id: str) -> bool:
    """Delete subject by id."""
    res = supabase.table("subjects").delete().eq("id", subject_id).execute()
    return bool(res.data)

