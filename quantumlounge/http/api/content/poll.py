from common import MethodAdapter
from quantumlounge.framework import json

class Vote(MethodAdapter):
    """a voting adapter for polls"""

    @json(content_type="application/json")
    def post(self, **kw):
        """post a new vote to this poll"""
        answer_no = self.request.form.get("answer_no",None)
        if answer_no is None:
            return {'error' : 'Answer number not given'}
        self.item.vote(answer_no)
        self.item._store.update(self.item)
        return {'status':'ok'}

class Results(MethodAdapter):
    """a results adapter for polls"""

    @json(content_type="application/json")
    def get(self, answer_no=None, **kw):
        """post a new vote to this poll"""
        return self.item.results

