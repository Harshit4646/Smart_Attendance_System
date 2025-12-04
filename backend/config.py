import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Public anon key (for normal client calls)
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
# Service role key (for admin.create_user, etc.). Must be kept secret.
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", SUPABASE_KEY)

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "super_secret")
SUPABASE_STORAGE_URL = os.getenv("SUPABASE_STORAGE_URL")
