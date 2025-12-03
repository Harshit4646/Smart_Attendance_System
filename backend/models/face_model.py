"""
Handles Face Embeddings model for face-based attendance. Provides helpers
for storing, fetching, updating, and deleting face embeddings with Supabase.
"""
from supabase_client import supabase
from typing import Optional, List

def register_face_embedding(data: dict) -> dict:
    """Insert new face embedding for a student (expects embedding, student_id, image_url)."""
    res = supabase.table("face_embeddings").insert([data]).execute()
    return res.data[0] if res.data else None

def get_face_by_student_id(student_id: str) -> Optional[dict]:
    """Fetch latest face embedding for a student."""
    res = supabase.table("face_embeddings").select("*").eq("student_id", student_id).order("created_at", desc=True).limit(1).single().execute()
    return res.data if res.data else None

def get_all_faces() -> List[dict]:
    """Get all stored face embeddings (admin/faculty usage)."""
    res = supabase.table("face_embeddings").select("*").execute()
    return res.data or []

def update_face_embedding(face_id: str, updates: dict) -> Optional[dict]:
    """Update a face embedding's data (for admin correction or new image)."""
    res = supabase.table("face_embeddings").update(updates).eq("id", face_id).execute()
    return res.data[0] if res.data else None

def delete_face_by_id(face_id: str) -> bool:
    """Delete face embedding by ID."""
    res = supabase.table("face_embeddings").delete().eq("id", face_id).execute()
    return bool(res.data)

