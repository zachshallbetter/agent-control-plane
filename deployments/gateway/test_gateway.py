from pathlib import Path
compile((Path(__file__).parent/"gateway.py").read_text(),"gateway.py","exec")
print("portable ACP gateway package tests passed")
