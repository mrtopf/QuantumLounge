import common
import poll

r_common = {
        'subtree' : common.SubTree,
        'jsview' : common.JSView,
        'parents' : common.Parents,
        'children' : common.Children,
        'default' : common.Default,
}

r_poll = {
        'vote' : poll.Vote,
        'results' : poll.Results,
}
r_poll.update(r_common)

type_registry = {
    'status' : r_common,
    'link' : r_common,
    'folder' : r_common,
    'poll' : r_poll,
     
}
__all__ = ['type_registry']
