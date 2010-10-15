import pymongo
from quantumlounge.content.folders import FolderManager

def pytest_funcarg__fstore(request):
    """initialize a folder store and return it"""
    db = pymongo.Connection().ql_test
    db.drop_collection("folders")
    f = FolderManager(db,"folders")
    return f

