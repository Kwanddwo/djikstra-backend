from models.models import Skill, User
from sqlalchemy.orm import Session

def get_user_context(user_id: str, db: Session):
    # Query all skills and the user's learning level for each
    results = (
        db.execute(
            """
            SELECT s.name, us.learning_level
            FROM skills s
            LEFT JOIN user_skills us ON s.id = us.skill_id AND us.user_id = :user_id
            """,
            {"user_id": user_id}
        )
    ).fetchall()

    learning_levels = {row[0]: float(row[1]) if row[1] is not None else 0.0 for row in results}

    # Optionally, you can add more context (e.g., current page/unit)
    return {
        "Learning Levels": learning_levels,
        # "Current Page": ... # Add if you have this info
    }