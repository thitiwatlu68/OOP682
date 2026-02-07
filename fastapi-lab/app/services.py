from fastapi import HTTPException
from .repositories import ITaskRepository
from .models import TaskCreate

class TaskService:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def get_tasks(self):
        return self.repo.get_all()

    def create_task(self, task_in: TaskCreate):
        existing_task = self.repo.get_by_title(task_in.title)
        
        if existing_task:
            raise HTTPException(
                status_code=400, 
                detail=f"Task ที่ชื่อ '{task_in.title}' มีอยู่แล้วครับนายนัธทวัฒน์!"
            )
            
        return self.repo.create(task_in)
    
    def mark_as_complete(self, task_id: int):
        return self.repo.update(task_id, {"completed": True})