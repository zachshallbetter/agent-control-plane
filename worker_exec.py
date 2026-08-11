"""Supervised external worker execution with bounded output and timeout."""
import subprocess

def run(command, cwd, timeout=1800, env=None):
    result=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True,timeout=timeout)
    return {'decision':'APPROVED' if result.returncode==0 else 'BLOCKED','exit_code':result.returncode,'stdout':result.stdout[-12000:],'stderr':result.stderr[-12000:]}
