"""Bounded GitHub CLI provider. One command per requested fact; no retries."""
import json,subprocess

class GitHubCLI:
    def __init__(self,owner,project): self.owner=owner; self.project=project
    def _run(self,args): return json.loads(subprocess.check_output(['gh',*args],text=True))
    def issue(self,repo,number): return self._run(['issue','view',str(number),'--repo',repo,'--json','state,title,body,comments,labels,milestone,assignees'])
    def project_items(self): return self._run(['project','item-list',str(self.project),'--owner',self.owner,'--limit','500','--format','json'])
    def pr(self,repo,number): return self._run(['pr','view',str(number),'--repo',repo,'--json','state,mergeable,reviewDecision,statusCheckRollup,body,comments'])
    def comment(self,repo,number,body): return subprocess.check_output(['gh','issue','comment',str(number),'--repo',repo,'--body',body],text=True)
