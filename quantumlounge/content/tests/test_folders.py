from quantumlounge.content.folders import Folder

def test_create(fstore):
    f = Folder(title="test", description="a folder" )
    i = fstore.put(f)
    assert len(str(i))==24

def test_get(fstore):
    f = Folder(title="test2", description="a folder" )
    i = fstore.put(f)
    f2 = fstore[i]
    assert f.title == f2.title

def test_parent_chain(fstore):
    f1 = Folder(title="level1", description="a folder on level 1" )
    i1 = fstore.put(f1)
    f1 = fstore[i1]

    # create a subfolder
    f2 = Folder(title="level2", description="a folder on level 2" )
    f2.parent=f1
    i2 = fstore.put(f2)

    f2 = fstore[i2]
    assert f2.parent is not None
    p = f2.parent
    assert p._id == f1._id

    assert f1.parent is None
    assert f1.parent_id is None

def test_get_recursive_children_ids(fstore):
    """try to obtain the ids of the nodes in the subtree of a folder"""

    # create highest level
    main = fstore[fstore.put(Folder(title="main"))]

    # create 5 nodes on level 1 beneath
    n=0
    for i in range(1,5):
        f1 = fstore[fstore.put(Folder(_id="l-%s" %i, title="level1-%s" %i, parent_id=main.oid))]
        n=n+1
        for j in range(1,5):
            f2 = fstore[fstore.put(Folder(_id="l-%s-%s" %(i,j), title="level1-%s-%s" %(i,j), parent_id=f1.oid))]
            n=n+1

    assert len(main.all_cids) == n

    # check one inbetween
    f = fstore['l-1']
    assert len(f.all_cids)==4

def test_ancestors_delete_leaf(fstore):

    main = fstore[fstore.put(Folder(_id='root',title="main"))]
    for i in range(1,5):
        f1 = fstore[fstore.put(Folder(_id="l-%s" %i, title="level1-%s" %i, parent_id=main.oid))]
        for j in range(1,5):
            f2 = fstore[fstore.put(Folder(_id="l-%s-%s" %(i,j), title="level1-%s-%s" %(i,j), parent_id=f1.oid))]

    # delete a leaf node
    f = fstore['l-1-2']
    assert f.ancestors==['root','l-1']
    f.parent = None
    fstore.update(f)
    assert f.ancestors==[]

    # check ancestors
    f = fstore['l-1']
    assert len(f.all_cids)==3


def test_ancestors_delete_middle(fstore):

    main = fstore[fstore.put(Folder(_id='root',title="main"))]
    for i in range(1,5):
        f1 = fstore[fstore.put(Folder(_id="l-%s" %i, title="level1-%s" %i, parent_id=main.oid))]
        for j in range(1,5):
            f2 = fstore[fstore.put(Folder(_id="l-%s-%s" %(i,j), title="level1-%s-%s" %(i,j), parent_id=f1.oid))]

    # delete a node inbetween
    f = fstore['l-1']
    f.parent = None
    fstore.update(f)
    assert f.ancestors==[]

    # check ancestors
    f = fstore['l-1-2']
    assert f.ancestors==['l-1']


def test_ancestors_reroot(fstore):

    main = fstore[fstore.put(Folder(_id='root',title="main"))]
    main2 = fstore[fstore.put(Folder(_id='root2',title="main"))]
    for i in range(1,5):
        f1 = fstore[fstore.put(Folder(_id="l-%s" %i, title="level1-%s" %i, parent_id=main.oid))]
        for j in range(1,5):
            f2 = fstore[fstore.put(Folder(_id="l-%s-%s" %(i,j), title="level1-%s-%s" %(i,j), parent_id=f1.oid))]

    # delete a node inbetween
    f = fstore['l-1']
    f.parent = main2
    fstore.update(f)
    assert f.ancestors==['root2']

    # check ancestors
    f = fstore['l-1-2']
    assert f.ancestors==['root2','l-1']














