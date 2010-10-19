import pymongo
from quantumlounge.content.base import ContentManager

def pytest_funcarg__cstore(request):
    """initialize a content store and return it"""
    db = pymongo.Connection().ql_test
    db.drop_collection("contents")
    return ContentManager(db, "contents")

