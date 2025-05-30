from models.models import Skill, User, user_skills
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

def get_user_learning_levels(user_id: str, db: Session, skills_whitelist: List[Skill] = None):
    # Query all skills and the user's learning level for each
    if skills_whitelist is None:
        skills_whitelist = db.query(Skill).all()
          # Fetch all skills if no whitelist provided
    whitelist_skill_ids = [skill.id for skill in skills_whitelist]
    
    results = (
        db.query(Skill.name, user_skills.c.learning_level)
        .join(user_skills, Skill.id == user_skills.c.skill_id)
        .filter(user_skills.c.user_id == user_id)
        .filter(Skill.id.in_(whitelist_skill_ids))
        .all()
    )

    learning_levels = {row[0]: float(row[1]) if row[1] is not None else 0.0 for row in results}

    return {
        "Learning Levels": learning_levels,
    }