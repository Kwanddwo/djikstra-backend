from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.db import get_db
from models.models import Course, Unit, Lesson, PracticeProblem, Skill, User, user_skills, lesson_skills, problem_skills, UserCourseOrderProgress, UserLessonCompletion, UserProblemCompletion
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

@router.post("/courses", response_model=schemas.CourseOut)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    new_course = Course(**course.dict())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course

@router.put("/courses/{course_id}", response_model=schemas.CourseOut)
def update_course(course_id: str, course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(404, "course not found")
    for k, v in course.dict().items():
        setattr(db_course, k, v)
    db.commit()
    db.refresh(db_course)
    return db_course

# @router.delete("/courses/{course_id}")
# def delete_course(course_id: str, db: Session = Depends(get_db)):
#     db_course = db.query(Course).filter(Course.id == course_id).first()
#     if not db_course:
#         raise HTTPException(404, "course not found")
#     db.delete(db_course)
#     db.commit()
#     return {"detail": "Lesson deleted"}

@router.get("/units/{unit_id}", response_model=schemas.UnitOut)
def get_unit(unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(404, "Unit not found")
    return unit

@router.post("/units", response_model=schemas.UnitOut)
def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    new_unit = Unit(**unit.dict())
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

@router.put("/units/{unit_id}", response_model=schemas.UnitUpdate)
def update_unit(unit_id: str, unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    db_unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not db_unit:
        raise HTTPException(404, "unit not found")
    for k, v in unit.dict().items():
        setattr(db_unit, k, v)
    db.commit()
    db.refresh(db_unit)
    return db_unit

# @router.delete("/units/{unit_id}")
# def delete_unit(unit_id: str, db: Session = Depends(get_db)):
#     db_unit = db.query(Unit).filter(Unit.id == unit_id).first()
#     if not db_unit:
#         raise HTTPException(404, "unit not found")
#     db.delete(db_unit)
#     db.commit()
#     return {"detail": "unit deleted"}

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
    # You may need to join with the user_skills table to get the learning levels
    skills_user = db.query(user_skills).filter(user_skills.c.user_id == user_id).all()
    skills = []
    for user_skill in skills_user:
        skill = db.query(Skill).filter(Skill.id == user_skill.skill_id).first()
        if skill:
            skills.append({
                "id": skill.id,
                "name": skill.name,
                "description": skill.description,
                "learning_level": user_skill.learning_level
            })
    return skills

def get_progress_percentage(
        unit: Unit, 
        lesson_completions: List[UserLessonCompletion], 
        problem_completions: List[UserProblemCompletion]
    ):
    # Units always have only one lesson
    total_parts = 1 + len(unit.practice_problems)

    if total_parts == 0:
        return 0  # Avoid division by zero if there are no parts in the unit

    completed_lessons = 1 if unit.lesson.id in [lc.lesson_id for lc in lesson_completions] else 0
    completed_problems = sum(1 for problem in unit.practice_problems if problem.id in [pc.problem_id for pc in problem_completions])
    completed_parts = completed_lessons + completed_problems
    return int((completed_parts / total_parts) * 100)


@router.get("/users/{user_id}/units", response_model=List[schemas.UserUnitProgressOut])
def get_user_units(user_id: str, db: Session = Depends(get_db)):
    lesson_completions = db.query(UserLessonCompletion).filter(UserLessonCompletion.user_id == user_id).all()
    problem_completions = db.query(UserProblemCompletion).filter(UserProblemCompletion.user_id == user_id).all()
    # Extract unit_ids from completions
    lesson_unit_ids = [completion.lesson.unit_id for completion in lesson_completions]
    problem_unit_ids = [completion.problem.unit_id for completion in problem_completions]
    
    # Get unique unit_ids
    all_unit_ids = set(lesson_unit_ids + problem_unit_ids)
    units = db.query(Unit).filter(Unit.id.in_(all_unit_ids)).all()

    user_units = []
    for unit in units:
        progress_percentage = get_progress_percentage(unit, lesson_completions, problem_completions)
        user_units.append({
            "user_id": user_id,
            "unit_id": unit.id,
            "completion_percentage": progress_percentage,
            "last_updated": datetime.now(timezone.utc)
        })

    return user_units

@router.get("/users/{user_id}/units/{unit_id}/progress", response_model=schemas.UserUnitProgressOut)
def get_user_unit_progress(user_id: str, unit_id: str, db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()    
    if not unit:
        raise HTTPException(404, "Unit not found")
    
    lesson_completions = db.query(UserLessonCompletion).filter(
        UserLessonCompletion.user_id == user_id,
        UserLessonCompletion.lesson.has(unit_id=unit_id)
    ).all()
    problem_completions = db.query(UserProblemCompletion).filter(
        UserProblemCompletion.user_id == user_id,
        UserProblemCompletion.problem.has(unit_id=unit_id)
    ).all()
    completion_percentage = get_progress_percentage(unit, lesson_completions, problem_completions)
    progress = {
        "user_id": user_id,
        "unit_id": unit_id,
        "completion_percentage": completion_percentage,
        "last_updated": datetime.now(timezone.utc)
    }
    return progress

# --- Lesson and Problem Completion ---
@router.get("/users/{user_id}/complete", response_model=schemas.UserCompletions)
def get_user_completions(user_id: str, db: Session = Depends(get_db)):
    completions = {
        "user_id": user_id,
        "lessons": db.query(UserLessonCompletion).filter(UserLessonCompletion.user_id == user_id).all(),
        "practice_problems": db.query(UserProblemCompletion).filter(UserProblemCompletion.user_id == user_id).all()
    }
    return completions

def addLessonSkillsToUser(user: User, skills: List[Skill], lesson_id: str, db: Session):
    for skill in skills:
        # Check if user already has this skill
        existing_user_skill = db.query(user_skills).filter(
            user_skills.c.user_id == user.id,
            user_skills.c.skill_id == skill.id
        ).first()
        
        if existing_user_skill:
            # Update existing learning level by adding the gain
            # Get the gain from lesson_skills association table
            lesson_skill_gain = db.query(lesson_skills.c.gain).filter(
                lesson_skills.c.skill_id == skill.id,
                lesson_skills.c.lesson_id == lesson_id
            ).first()
            
            gain_value = lesson_skill_gain[0] if lesson_skill_gain else 0.1  # Default gain
            
            # Update the learning level
            db.execute(
                user_skills.update()
                .where(user_skills.c.user_id == user.id)
                .where(user_skills.c.skill_id == skill.id)
                .values(learning_level=user_skills.c.learning_level + gain_value)
            )
        else:
            # Create new user_skills entry
            lesson_skill_gain = db.query(lesson_skills.c.gain).filter(
                lesson_skills.c.skill_id == skill.id
            ).first()
            
            initial_level = lesson_skill_gain[0] if lesson_skill_gain else 0.1  # Default gain
            
            # Insert new user_skills entry
            db.execute(
                user_skills.insert().values(
                    user_id=user.id,
                    skill_id=skill.id,
                    learning_level=initial_level
                )
            )

def addProblemSkillsToUser(user: User, skills: List[Skill], problem_id: str, db: Session):
    for skill in skills:
        # Check if user already has this skill
        existing_user_skill = db.query(user_skills).filter(
            user_skills.c.user_id == user.id,
            user_skills.c.skill_id == skill.id
        ).first()
        
        if existing_user_skill:
            # Update existing learning level by adding the gain
            # Get the gain from problem_skills association table
            problem_skill_gain = db.query(problem_skills.c.gain).filter(
                problem_skills.c.skill_id == skill.id,
                problem_skills.c.problem_id == problem_id
            ).first()
            
            gain_value = problem_skill_gain[0] if problem_skill_gain else 0.1  # Default gain
            
            # Update the learning level
            db.execute(
                user_skills.update()
                .where(user_skills.c.user_id == user.id)
                .where(user_skills.c.skill_id == skill.id)
                .values(learning_level=user_skills.c.learning_level + gain_value)
            )
        else:
            # Create new user_skills entry
            problem_skill_gain = db.query(problem_skills.c.gain).filter(
                problem_skills.c.skill_id == skill.id
            ).first()
            
            initial_level = problem_skill_gain[0] if problem_skill_gain else 0.1  # Default gain
            
            # Insert new user_skills entry
            db.execute(
                user_skills.insert().values(
                    user_id=user.id,
                    skill_id=skill.id,
                    learning_level=initial_level
                )
            )

@router.post("/users/{user_id}/lessons/{lesson_id}/complete", response_model=schemas.UserLessonCompletion)
def complete_lesson(user_id: str, lesson_id: str, db: Session = Depends(get_db)):
    # Check if this completion already exists
    existing_completion = db.query(UserLessonCompletion).filter(
        UserLessonCompletion.user_id == user_id,
        UserLessonCompletion.lesson_id == lesson_id
    ).first()
    if existing_completion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lesson already completed")
    
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    
    unit = db.query(Unit).filter(Unit.id == lesson.unit_id).first()
    
    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson's unit not found")
    
    order_progress = db.query(UserCourseOrderProgress).filter(
            UserCourseOrderProgress.user_id == user_id,
            UserCourseOrderProgress.course_id == unit.course_id
        ).first()
    
    # Check order constraints
    unit_order = unit.order
    current_order = order_progress.current_order if order_progress else None
    
    if (order_progress is None and unit_order != 1) or (order_progress is not None and current_order != unit_order):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This unit is either finished or not unlocked yet")
    
    
    db_lesson_completion = UserLessonCompletion(user_id=user_id, lesson_id=lesson_id)
    db.add(db_lesson_completion)
    addLessonSkillsToUser(db.query(User).filter(User.id == user_id).first(), lesson.skills, str(lesson.id), db)
    db.commit()
    db.refresh(db_lesson_completion)
    return db_lesson_completion

@router.post("/users/{user_id}/practice_problems/{problem_id}/complete", response_model=schemas.UserProblemCompletion)
def complete_problem(user_id: str, problem_id: str, db: Session = Depends(get_db)):
    existing_completion = db.query(UserProblemCompletion).filter(
        UserProblemCompletion.user_id == user_id,
        UserProblemCompletion.problem_id == problem_id
    ).first()
    if existing_completion:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lesson already completed")
    
    problem = db.query(PracticeProblem).filter(PracticeProblem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")
    
    unit = db.query(Unit).filter(Unit.id == problem.unit_id).first()
    
    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem's unit not found")

    order_progress = db.query(UserCourseOrderProgress).filter(
            UserCourseOrderProgress.user_id == user_id,
            UserCourseOrderProgress.course_id == unit.course_id
        ).first()
    
    print("order_progress: " + str(order_progress.current_order) if order_progress is not None else "1")
    
    if (order_progress is None and unit.order != 1) or (order_progress is not None and order_progress.current_order != unit.order):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This unit is either finished or not unlocked yet")
    
    db_problem_completion = UserProblemCompletion(user_id=user_id, problem_id=problem_id)
    db.add(db_problem_completion)
    addProblemSkillsToUser(db.query(User).filter(User.id == user_id).first(), problem.skills, str(problem.id), db)
    db.commit()
    db.refresh(db_problem_completion)

    print(f"unit_progress: {get_user_unit_progress(user_id, str(unit.id), db)}")

    # Check if the user has completed all problems in the unit
    if get_user_unit_progress(user_id, str(unit.id), db)["completion_percentage"] == 100:
        # If this is the last problem, mark the unit as complete
        
        if order_progress is None and unit.order != 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot complete last problem without completing previous units")
        
        if order_progress is not None:
            # Update existing progress
            setattr(order_progress, 'current_order', order_progress.current_order + 1)
            setattr(order_progress, 'last_updated', datetime.now(timezone.utc))
            db.commit()
        else:
            order_progress = UserCourseOrderProgress(
                user_id=user_id,
                course_id=unit.course_id,
                current_order=2,  # Fix: Set to 2 since we're moving to next unit
                last_updated=datetime.now(timezone.utc)
            )
            db.add(order_progress)
            db.commit()

    return db_problem_completion
