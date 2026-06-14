from app.services.planner import create_plan


plan = create_plan(
    "Add JWT authentication to this FastAPI app"
)

print(plan)