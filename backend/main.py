from fastapi import FastAPI
from backend.database import engine
from backend import models
from backend.routers import auth, boards, columns, tasks


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Kanban API")

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(boards.router, prefix="/boards", tags=["Boards"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(columns.router, prefix="/columns", tags=["Columns"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
