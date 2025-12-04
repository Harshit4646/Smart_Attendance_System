import os
from supabase import create_client, Client
from dotenv import load_dotenv
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY

load_dotenv()

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in the environment.")

# Standard client (anon key)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Admin client for auth.admin operations (needs service key)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
