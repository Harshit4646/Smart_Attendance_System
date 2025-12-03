"""
Handles Attendance model for attendance system. Manages marking, fetching by
student/class/date/subject, and updating/deleting attendance using Supabase.
"""
from ..supabase_client import supabase
from typing import Optional, List

def mark_attendance(data: dict) -> dict:
    """Insert new attendance record for a student."""
    res = supabase.table("attendance").insert([data]).execute()
    return res.data[0] if res.data else None

def get_attendance_by_student(student_id: str) -> List[dict]:
    """Fetch attendance records for a student."""
    res = supabase.table("attendance").select("*").eq("student_id", student_id).execute()
    return res.data or []

def get_attendance_by_class(class_id: str) -> List[dict]:
    """Fetch attendance for all students in a class (via join, simulated by multiple queries or view)."""
    # Direct query not possible without join, simulate by getting student ids elsewhere
    return []  # To implement in context

def get_attendance_by_date(date: str) -> List[dict]:
    """Fetch all attendance on a given date (YYYY-MM-DD)."""
    res = supabase.table("attendance").select("*").eq("attendance_date", date).execute()
    return res.data or []

def update_attendance(attendance_id: str, updates: dict) -> Optional[dict]:
    """Update an attendance record by id."""
    res = supabase.table("attendance").update(updates).eq("id", attendance_id).execute()
    return res.data[0] if res.data else None

def delete_attendance(attendance_id: str) -> bool:
    """Delete an attendance record by id."""
    res = supabase.table("attendance").delete().eq("id", attendance_id).execute()
    return bool(res.data)
