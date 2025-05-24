from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db import get_db
from models.models import Course, Unit, Lesson, PracticeProblem, Skill, User, PromptLog, UserUnitProgress
from schemas import schemas
from typing import List

router = APIRouter()

# --- Courses & Units ---
@router.get("/courses", response_model=List[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()

@router.get("/courses/{course_id}", response_model=schemas.CourseOut)
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course not found")
    return course

@router.get("/units/{unit_id}", response_model=schemas.UnitOut)
def get_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(404, "Unit not found")
    return unit

# --- Lessons ---
@router.get("/lessons/{lesson_id}", response_model=schemas.LessonOut)
def get_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return lesson

@router.post("/lessons", response_model=schemas.LessonOut)
def create_lesson(lesson: schemas.LessonCreate, db: Session = Depends(get_db)):
    new_lesson = Lesson(**lesson.dict())
    db.add(new_lesson)
    db.commit()
    db.refresh(new_lesson)
    return new_lesson

@router.put("/lessons/{lesson_id}", response_model=schemas.LessonOut)
def update_lesson(lesson_id: str, lesson: schemas.LessonCreate, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(404, "Lesson not found")
    for k, v in lesson.dict().items():
        setattr(db_lesson, k, v)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

@router.delete("/lessons/{lesson_id}")
def delete_lesson(lesson_id: str, db: Session = Depends(get_db)):
    db_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not db_lesson:
        raise HTTPException(404, "Lesson not found")
    db.delete(db_lesson)
    db.commit()
    return {"detail": "Lesson deleted"}

# --- Practice Problems ---
@router.get("/practice_problems/{problem_id}", response_model=schemas.PracticeProblemOut)
def get_problem(problem_id: str, db: Session = Depends(get_db)):
    problem = db.query(PracticeProblem).filter(PracticeProblem.id == problem_id).first()
    if not problem:
        raise HTTPException(404, "Practice problem not found")
    return problem

@router.post("/practice_problems", response_model=schemas.PracticeProblemOut)
def create_problem(problem: schemas.PracticeProblemCreate, db: Session = Depends(get_db)):
    new_problem = PracticeProblem(**problem.dict())
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return new_problem

@router.put("/practice_problems/{problem_id}", response_model=schemas.PracticeProblemOut)
def update_problem(problem_id: str, problem: schemas.PracticeProblemCreate, db: Session = Depends(get_db)):
    db_problem = db.query(PracticeProblem).filter(PracticeProblem.id == problem_id).first()
    if not db_problem:
        raise HTTPException(404, "Practice problem not found")
    for k, v in problem.dict().items():
        setattr(db_problem, k, v)
    db.commit()
    db.refresh(db_problem)
    return db_problem

@router.delete("/practice_problems/{problem_id}")
def delete_problem(problem_id: str, db: Session = Depends(get_db)):
    db_problem = db.query(PracticeProblem).filter(PracticeProblem.id == problem_id).first()
    if not db_problem:
        raise HTTPException(404, "Practice problem not found")
    db.delete(db_problem)
    db.commit()
    return {"detail": "Practice problem deleted"}

# --- Skills ---
@router.get("/skills", response_model=List[schemas.SkillOut])
def list_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()

@router.get("/skills/{skill_id}", response_model=schemas.SkillOut)
def get_skill(skill_id: str, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(404, "Skill not found")
    return skill

# --- User Progress & Skills ---
@router.get("/users/{user_id}/skills", response_model=List[schemas.UserSkillOut])
def get_user_skills(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    # You may need to join user_skills for progress
    return user.skills

@router.get("/users/{user_id}/units", response_model=List[schemas.UserUnitProgressOut])
def get_user_units(user_id: str, db: Session = Depends(get_db)):
    return db.query(UserUnitProgress).filter(UserUnitProgress.user_id == user_id).all()

@router.get("/users/{user_id}/units/{unit_id}/progress", response_model=schemas.UserUnitProgressOut)
def get_user_unit_progress(user_id: str, unit_id: str, db: Session = Depends(get_db)):
    progress = db.query(UserUnitProgress).filter(UserUnitProgress.user_id == user_id, UserUnitProgress.unit_id == unit_id).first()
    if not progress:
        raise HTTPException(404, "Progress not found")
    return progress

@router.post("/users/{user_id}/units/{unit_id}/progress", response_model=schemas.UserUnitProgressOut)
def update_user_unit_progress(user_id: str, unit_id: str, progress: schemas.UserUnitProgressUpdate, db: Session = Depends(get_db)):
    db_progress = db.query(UserUnitProgress).filter(UserUnitProgress.user_id == user_id, UserUnitProgress.unit_id == unit_id).first()
    if not db_progress:
        db_progress = UserUnitProgress(user_id=user_id, unit_id=unit_id, **progress.dict())
        db.add(db_progress)
    else:
        for k, v in progress.dict().items():
            setattr(db_progress, k, v)
    db.commit()
    db.refresh(db_progress)
    return db_progress

# --- Logging ---
@router.get("/users/{user_id}/prompt_logs", response_model=List[schemas.PromptLogOut])
def get_prompt_logs(user_id: str, db: Session = Depends(get_db)):
    return db.query(PromptLog).filter(PromptLog.user_id == user_id).all()
