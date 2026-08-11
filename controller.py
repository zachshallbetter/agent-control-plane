"""Provider-neutral merge/status controller; all mutations are injected."""
class Controller:
    def __init__(self,read,merge,set_status): self.read=read; self.merge=merge; self.set_status=set_status
    def qualify(self,repository,pr,project_item,evidence):
        state=self.read(repository,pr)
        if state.get('mergeable') != 'MERGEABLE': return {'decision':'BLOCKED','reason':'pull request is not mergeable'}
        if not evidence.get('human_acknowledged'): return {'decision':'BLOCKED','reason':'human acknowledgement is missing'}
        result=self.merge(repository,pr)
        self.set_status(project_item,'Done')
        return {'decision':'QUALIFIED','merge':result,'status':'Done'}
