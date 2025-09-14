# Kanban-fastapi

Backend ระบบ Kanban Board เขียนด้วย **FastAPI + SQLAlchemy + MySQL**  
มีระบบผู้ใช้ บอร์ด คอลัมน์ งาน และสมาชิก พร้อม Docker สำหรับการรันสะดวก  

---

## Features
- สมัครสมาชิก / ล็อกอิน ด้วย JWT
- จัดการบอร์ด (สร้าง, แก้ไข, ลบ, ดึงข้อมูล)
- จัดการสมาชิกในบอร์ด
- จัดการงาน (Task) ภายในบอร์ด
- จัดการคอลัมน์ (Column) ภายในบอร์ด
- รองรับ Docker Compose

---

## 🛠️ Installation

### 1. Clone Project
```bash
git clone https://github.com/JiratikarnDo/Kanban-fastapi.git
cd Kanban-fastapi
```
### 2. .Env
``` bash
DB_USER=root
DB_PASS=yourpassword
DB_HOST=db
DB_PORT=3306
DB_NAME=kanban

SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3 Run with Docker
``` bash
docker-compose up --build
```

📚 API Documentation

### Auth
POST /auth/register → สมัครสมาชิกใหม่
POST /auth/login → เข้าสู่ระบบ
GET /auth/me → ดูข้อมูลผู้ใช้ปัจจุบัน

### Boards
- POST /boards/ → สร้างบอร์ดใหม่
- PUT /boards/{board_id} → อัพเดทบอร์ด
- DELETE /boards/{board_id} → ลบบอร์ด
- GET /boards/{board_id} → ดูรายละเอียดบอร์ด
- POST /boards/{board_id}/invite → เชิญสมาชิกเข้าบอร์ด
- GET /boards/me → ดูบอร์ดทั้งหมดของฉัน

### Tasks
- POST /tasks/ → สร้างงาน (Task)
- PUT /tasks/{task_id} → อัพเดทงาน
- DELETE /tasks/{task_id} → ลบงาน
- POST /tasks/{task_id}/assign → มอบหมายงานให้สมาชิก
- GET /tasks/me/assignees → ดูงานที่ฉันรับผิดชอบ
- GET /tasks/{task_id}/assignees → ดูสมาชิกที่รับผิดชอบงานนี้

### Columns
- POST /columns/{board_id} → สร้างคอลัมน์ในบอร์ด
- PUT /columns/{column_id} → อัพเดทคอลัมน์
- DELETE /columns/{column_id} → ลบคอลัมน์
- GET /columns/{column_id} → ดูงานทั้งหมดในคอลัมน์

- Testing -
ใช้ Swagger UI ที่ http://localhost:8000/docs
หรือ Postman

- Tech Stack in Project -
- FastAPI – Web Framework
- SQLAlchemy – ORM
- MySQL – Database
- Docker Compose – Container Orchestration
- JWT – Authentication
