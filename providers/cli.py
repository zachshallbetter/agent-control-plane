"""Bounded subprocess client for authenticated provider CLIs."""
import json,subprocess

class ProviderError(RuntimeError): pass

def run(command, timeout=30):
    try: result=subprocess.run(command,text=True,capture_output=True,timeout=timeout,check=True)
    except (subprocess.CalledProcessError,subprocess.TimeoutExpired) as exc: raise ProviderError(str(exc)) from exc
    try: return json.loads(result.stdout)
    except json.JSONDecodeError: return {"output":result.stdout.strip()}

class RailwayCLI:
    def whoami(self): return run(['railway','whoami'])
    def status(self): return run(['railway','status'])
    def logs(self,service,environment=None): return run(['railway','logs','--service',service] + (['--environment',environment] if environment else []),timeout=60)

class VercelCLI:
    def whoami(self): return run(['vercel','whoami'])
    def inspect(self,url): return run(['vercel','inspect',url])
    def logs(self,project): return run(['vercel','logs',project],timeout=60)
