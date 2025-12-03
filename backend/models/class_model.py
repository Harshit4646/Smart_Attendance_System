"""
Handles Classes model for attendance system. Provides CRUD operations and lookups
for class records using Supabase.
"""
from supabase_client import supabase
from typing import Optional

def create_class(data: dict) -> dict:
    """Insert new class record."""
    res = supabase.table("classes").insert([data]).execute()
    return res.data[0] if res.data else None

def get_class_by_id(class_id: str) -> Optional[dict]:
    """Fetch class by UUID."""
    res = supabase.table("classes").select("*").eq("id", class_id).single().execute()
    return res.data if res.data else None

def get_all_classes() -> list:
    """Get all classes."""
    res = supabase.table("classes").select("*").execute()
    return res.data or []

def update_class(class_id: str, updates: dict) -> Optional[dict]:
    """Update class record."""
    res = supabase.table("classes").update(updates).eq("id", class_id).execute()
    return res.data[0] if res.data else None

def delete_class(class_id: str) -> bool:
    """Delete class by id."""
    res = supabase.table("classes").delete().eq("id", class_id).execute()
    return bool(res.data)

