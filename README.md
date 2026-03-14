# ai_face_recognition

Base hệ thống điểm danh khuôn mặt theo kiến trúc:

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

## Công nghệ
- FastAPI – API server
- OpenCV – xử lý ảnh
- ArcFace – tạo embedding (stub, cần thay bằng model thật)
- FAISS – tìm vector nhanh
- Redis – cache (optional)
- JSON – lưu dữ liệu tạm
- Bootstrap 5 + Bootstrap Icons + Google Fonts (UI dashboard)

## Chạy server
### 1) Dùng môi trường ảo (khuyến nghị)
```bash
# Tạo venv
python -m venv .venv

# Kích hoạt (PowerShell)
.\.venv\Scripts\Activate.ps1

# Kích hoạt (CMD)
.\.venv\Scripts\activate.bat

# Kích hoạt (Git Bash)
source .venv/Scripts/activate

# Cài dependencies
pip install -r requirements.txt
```

### 2) Khởi động API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3) Mở dashboard
- `http://localhost:8000/dashboard`

### 4) Kiểm tra health
- `http://localhost:8000/health`

## Thêm ảnh để nhận diện
### 1) Đăng ký khuôn mặt (enroll)
Gửi ảnh lên API để lưu embedding:

```bash
curl -X POST "http://localhost:8000/v1/enroll" \
  -F "identity_id=EMP001" \
  -F "name=Nguyen Anh Tuan" \
  -F "department=Engineering" \
  -F "email=tuan.nguyen@example.com" \
  -F "active=true" \
  -F "image=@D:\\path\\to\\face.jpg"
```
### 2) Nhận diện (identify)
```bash
curl -X POST "http://localhost:8000/v1/identify" \
  -F "image=@D:\\path\\to\\face.jpg"
```

### 3) Điểm danh (attendance)
```bash
curl -X POST "http://localhost:8000/v1/attendance" \
  -F "device_id=device-01" \
  -F "image=@D:\\path\\to\\face.jpg"
```

## Hướng dẫn ảnh chuẩn để nhận diện tốt
- Mặt nhìn thẳng, đủ trán đến cằm, không che mắt.
- Hai mắt, mũi, miệng rõ nét; không đeo kính râm hoặc khẩu trang.
- Ánh sáng đều, không ngược sáng, hạn chế bóng đổ mạnh.
- Khuôn mặt chiếm khoảng 60-70% khung hình; ảnh không mờ/nhòe.
- Nền đơn giản, ít vật thể gây nhiễu; độ phân giải tối thiểu 200x200.

## UI CRUD
- `POST /ui/users/` (form): tạo user
- `PUT /ui/users/{identity_id}` (json): sửa user
- `DELETE /ui/users/{identity_id}`: xóa user

## API chính
- `POST /v1/enroll` (multipart): `identity_id`, `name`, `department`, `email`, `active`, `image`
- `POST /v1/identify` (multipart): `image`
- `POST /v1/attendance` (multipart): `device_id`, `image`
- `GET /health`
- `GET /dashboard`

## Dữ liệu
- `data/identities.json`: map identity -> metadata
- `data/faiss.index`: FAISS index
- `data/faiss_ids.json`: map vector_id -> identity_id
- `data/attendance.jsonl`: log điểm danh

## Log server
- Log file: `logs/server.log`
- Nếu gặp lỗi, gửi log này để debug.

## Ghi chú
- Embedding hiện tại là stub (deterministic) để chạy demo, cần thay bằng ArcFace thật.
- Khi đưa lên production, tách riêng service nhận diện, dùng model inference server và lưu vector bền vững.