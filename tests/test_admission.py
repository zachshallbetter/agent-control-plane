import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1]))
from admission import decide
packet={"issue":286,"project_item":"PVTI_test","repository":"org/services","authorized_paths":["src"],"exclusions":[],"dependencies":[],"acceptance_criteria":["x"],"evidence_requirements":["y"],"definition_of_done":["z"],"status":"Ready"}
assert decide(packet)[0] == "APPROVED"
assert decide(packet, topology_ok=False)[0] == "BLOCKED"
assert decide(packet, provider_available=False)[0] == "BLOCKED"
assert decide(packet, corpus_fresh=False)[0] == "BLOCKED"
print("admission tests passed")
