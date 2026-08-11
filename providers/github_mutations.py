"""Explicit GitHub lifecycle mutations. Callers must provide qualification evidence."""
import subprocess
from .cli import ProviderError

def merge(repository, pr, method='squash'):
    if method not in ('merge','squash','rebase'): raise ValueError('unsupported merge method')
    try: return subprocess.check_output(['gh','pr','merge',str(pr),'--repo',repository,f'--{method}'],text=True).strip()
    except subprocess.CalledProcessError as exc: raise ProviderError(str(exc)) from exc

def comment(repository, issue, body):
    return subprocess.check_output(['gh','issue','comment',str(issue),'--repo',repository,'--body',body],text=True).strip()
