import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

security = HTTPBearer()

try:
    if not os.path.exists(FIREBASE_KEY_PATH):
        raise FileNotFoundError("firebase_key.json not found")

    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully")

except Exception as e:
    print(f"Firebase initialization failed: {e}")
    # Do NOT crash app — just log error

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        decoded_token = auth.verify_id_token(credentials.credentials)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")