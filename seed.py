from models.models import Course, Unit, Lesson, PracticeProblem, Skill, User
from sqlalchemy.orm import Session
from sqlalchemy import text
from helpers.authHelpers import get_password_hash
from pathlib import Path


def reset_and_seed_database(db: Session):
    # Clear existing data
    db.execute(text("DELETE FROM lesson_skills"))
    db.execute(text("DELETE FROM problem_skills"))
    db.execute(text("DELETE FROM user_skills"))
    
    # Then delete from main tables
    db.query(Skill).delete()
    db.query(PracticeProblem).delete()
    db.query(Lesson).delete()
    db.query(Unit).delete()
    db.query(Course).delete()
    db.query(User).delete()
    db.commit()

    user = User(
        firstname="user1",
        lastname="lastName1",
        email="user1@user1.com",
        hashed_password=get_password_hash("password123")
    )
    
    db.add(user)
    db.commit()

    skills = [
        Skill(name="Graph Representation", description="Understanding graphs and their representations."),
        Skill(name="Priority Queue Usage", description="Using priority queues in algorithms."),
        Skill(name="Shortest Path Reasoning", description="Reasoning about shortest paths in graphs."),
        Skill(name="Algorithm Implementation", description="Implementing algorithms in code."),
        Skill(name="Problem Decomposition", description="Breaking down complex problems into manageable parts."),
        Skill(name="Pseudocode Writing", description="Writing clear and effective pseudocode for algorithms."),
        Skill(name="Time Complexity Analysis", description="Analyzing the time efficiency of algorithms."),
        Skill(name="Space Complexity Analysis", description="Analyzing the space efficiency of algorithms."),
        Skill(name="Recursion Mastery", description="Understanding and applying recursion in algorithms."),
        Skill(name="Greedy Algorithms", description="Designing and analyzing greedy algorithm strategies."),
        Skill(name="Dynamic Programming", description="Solving problems using dynamic programming techniques."),
        Skill(name="Divide and Conquer", description="Applying divide and conquer strategies to problem solving."),
        Skill(name="Graph Traversal (BFS/DFS)", description="Traversing graphs using BFS and DFS."),
        Skill(name="Shortest Path Algorithms", description="Understanding and implementing shortest path algorithms."),
        Skill(name="Sorting Algorithms", description="Implementing and analyzing sorting algorithms."),
        Skill(name="Searching Algorithms", description="Implementing and analyzing searching algorithms."),
        Skill(name="Hashing Techniques", description="Using hashing for efficient data retrieval."),
        Skill(name="Tree Manipulation", description="Working with tree data structures."),
        Skill(name="Backtracking", description="Solving problems using backtracking techniques."),
        Skill(name="Bit Manipulation", description="Using bitwise operations in algorithms."),
        Skill(name="Pattern Recognition", description="Identifying patterns to simplify problem solving."),
        Skill(name="Mathematical Reasoning", description="Applying mathematical logic to algorithms."),
        Skill(name="Data Structure Selection", description="Choosing appropriate data structures for problems."),
        Skill(name="Algorithm Optimization", description="Improving the efficiency of algorithms."),
    ]
    for skill in skills:
        db.add(skill)
    db.commit()

    # Helper: Find skill by name
    def skill_by_name(name):
        return next((s for s in skills if s.name == name), None)

    # List of lessons (filename, title, skills)
    lesson_infos = [
        ("01.md", "What is a Graph?", [
            "Graph Representation", "Pattern Recognition", "Mathematical Reasoning"
        ]),
        ("02.md", "Weighted Graphs", [
            "Graph Representation", "Mathematical Reasoning"
        ]),
        ("03.md", "Paths and Shortest Path", [
            "Shortest Path Reasoning", "Graph Representation"
        ]),
        ("04.md", "Shortest Path Algorithms Overview", [
            "Shortest Path Algorithms", "Algorithm Optimization", "Pattern Recognition"
        ]),
        ("05.md", "Dijkstra's Algorithm", [
            "Shortest Path Algorithms", "Priority Queue Usage", "Algorithm Implementation", "Time Complexity Analysis"
        ]),
    ]

    # Create course
    course = Course(
        name="Dijkstra's Algorithm",
        description="Learn how Dijkstra's algorithm finds the shortest path in a graph using a priority queue and a greedy approach."
    )
    db.add(course)
    db.commit()

    for idx, (filename, title, skill_names) in enumerate(lesson_infos, start=1):
        # Create unit
        unit = Unit(
            name=title,
            course_id=course.id,
            order=idx 
        )
        db.add(unit)
        db.commit()

        # Read lesson content from markdown file
        lesson_path = Path(__file__).parent /  "lessons" / filename
        with open(lesson_path, encoding="utf-8") as f:
            content = f.read()

        # Create lesson
        lesson = Lesson(
            title=title,
            content=content,
            unit_id=unit.id,
            skills=[skill_by_name(name) for name in skill_names if skill_by_name(name)]
        )
        db.add(lesson)
        db.commit()

        # Add practice problems for each unit
        problems = []
        if idx == 1:
            problems = [
                PracticeProblem(
                    type="multiple_choice",
                    question="Which of the following best describes a graph?",
                    data='{"choices": ["A collection of numbers", "A set of nodes and edges", "A sorted list", "A type of tree"], "answer": 1}',
                    unit_id=unit.id,
                    skills=[skill_by_name("Graph Representation")]
                ),
                PracticeProblem(
                    type="multiple_choice",
                    question="What is an example of an undirected graph?",
                    data='{"choices": ["Road map", "Task list", "Family tree", "Recipe steps"], "answer": 0}',
                    unit_id=unit.id,
                    skills=[skill_by_name("Pattern Recognition")]
                ),
            ]
        elif idx == 2:
            problems = [
                PracticeProblem(
                    type="multiple_choice",
                    question="What does a weight on a graph edge usually represent?",
                    data='{"choices": ["A node label", "A cost or distance", "A color", "A direction"], "answer": 1}',
                    unit_id=unit.id,
                    skills=[skill_by_name("Graph Representation")]
                ),
            ]
        elif idx == 3:
            problems = [
                PracticeProblem(
                    type="multiple_choice",
                    question="What is a simple path in a graph?",
                    data='{"choices": ["A path with no repeated nodes", "A path with the fewest edges", "A path with the largest weight", "A path that forms a cycle"], "answer": 0}',
                    unit_id=unit.id,
                    skills=[skill_by_name("Shortest Path Reasoning")]
                ),
            ]
        elif idx == 4:
            problems = [
                PracticeProblem(
                    type="multiple_choice",
                    question="Which algorithm can handle negative edge weights?",
                    data='{"choices": ["Dijkstra", "Bellman-Ford", "A*", "BFS"], "answer": 1}',
                    unit_id=unit.id,
                    skills=[skill_by_name("Shortest Path Algorithms")]
                ),
            ]
        elif idx == 5:
            problems = [
                PracticeProblem(
                    type="multiple_choice",
                    question="What data structure is essential for Dijkstra's algorithm efficiency?",
                    data='{"choices": ["Stack", "Queue", "Priority Queue", "Set"], "answer": 2}',
                    unit_id=unit.id,
                    skills=[skill_by_name("Priority Queue Usage")]
                ),
                PracticeProblem(
                    type="interactive_graph",
                    question="Find the shortest path from node A to node F in the given graph.",
                    data='{"graph": {"nodes": ["A", "B", "C", "D", "E", "F"], "edges": [["A", "B", 2], ["A", "C", 5], ["B", "D", 1], ["C", "D", 2], ["D", "E", 3], ["E", "F", 1]]}}',
                    unit_id=unit.id,
                    skills=[skill_by_name("Shortest Path Algorithms"), skill_by_name("Algorithm Implementation")]
                ),
            ]
        for p in problems:
            db.add(p)
        db.commit()

    print("Dijkstra course, units, lessons, and practice problems created from markdown files.")

if __name__ == "__main__":
    from db.db import SessionLocal
    db = SessionLocal()
    try:
        reset_and_seed_database(db)
    finally:
        db.close()