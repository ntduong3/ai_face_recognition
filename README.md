# ai_face_recognition

Base facial attendance system based on the following architecture:

Mobile App (200 devices)
        │
        │ capture face
        ▼
API Gateway / Load Balancer
        ▼
Face Recognition Service (Python)
        │
        ├─ Face Detection
        ├─ Face Embedding
        ▼
Vector Search Engine (FAISS)
        ▼
Identity Match
        ▼
Attendance Service

## Technologies
- FastAPI – API server
- OpenCV – image processing
- ArcFace – create embeddings (stub, need to replace with real model)
- FAISS – fast vector search
- Redis – cache (optional)
- JSON – temporary data storage
- Bootstrap 5 + Bootstrap Icons + Google Fonts (UI dashboard)

## Running the Server
### 1) Using Virtual Environment (recommended)
```bash
# Create venv
python -m venv .venv

# Activate (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (CMD)
.\.venv\Scripts\activate.bat

# Activate (Git Bash)
source .venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

### 2) Start the API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3) Open Dashboard
- `http://localhost:8000/dashboard`

### 4) Check Health
- `http://localhost:8000/health`

## Adding Images for Recognition
### 1) Register Face (enroll)
Send image to API to save embedding:

```bash
curl -X POST "http://localhost:8000/v1/enroll" \
  -F "identity_id=EMP001" \
  -F "name=Nguyen Anh Tuan" \
  -F "department=Engineering" \
  -F "email=tuan.nguyen@example.com" \
  -F "active=true" \
  -F "image=@D:\\path\\to\\face.jpg"
```
### 2) Identify (identify)
```bash
curl -X POST "http://localhost:8000/v1/identify" \
  -F "image=@D:\\path\\to\\face.jpg"
```

### 3) Attendance (attendance)
```bash
curl -X POST "http://localhost:8000/v1/attendance" \
  -F "device_id=device-01" \
  -F "image=@D:\\path\\to\\face.jpg"
```

## Image Guidelines for Better Recognition
- Face looking straight, from forehead to chin, eyes not covered.
- Two eyes, nose, mouth are clear; no sunglasses or masks.
- Uniform lighting, no backlighting, minimize strong shadows.
- Face occupies about 60-70% of the frame; image should not be blurry.
- Simple background with minimal interference; minimum resolution 200x200.

## UI CRUD
- `POST /ui/users/` (form): create user
- `PUT /ui/users/{identity_id}` (json): update user
- `DELETE /ui/users/{identity_id}`: delete user

## Main APIs
- `POST /v1/enroll` (multipart): `identity_id`, `name`, `department`, `email`, `active`, `image`
- `POST /v1/identify` (multipart): `image`
- `POST /v1/attendance` (multipart): `device_id`, `image`
- `GET /health`
- `GET /dashboard`

## Data
- `data/identities.json`: identity -> metadata mapping
- `data/faiss.index`: FAISS index
- `data/faiss_ids.json`: vector_id -> identity_id mapping
- `data/attendance.jsonl`: attendance log

## Server Logs
- Log file: `logs/server.log`
- If you encounter errors, send this log file for debugging.

## Notes
- Current embedding is a stub (deterministic) for demo purposes, needs to be replaced with real ArcFace model.
- When deploying to production, separate the recognition service, use a model inference server, and store vectors persistently.