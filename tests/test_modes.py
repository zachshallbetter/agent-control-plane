import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from operating_mode import evaluate
assert evaluate(project_access="available").name == "normal"
assert evaluate(project_access="rate_limited").name == "degraded"
assert "implement" in evaluate(project_access="rate_limited").blocked
assert evaluate(project_access="rate_limited", existing_lease=True, lease_valid=True).name == "continuation"
assert evaluate(project_access="unauthorized").name == "paused"
print("operating mode tests passed")
