from dictdiffer import diff


old = {
    'foo': {
        "status": "todo",
        "title": "test",
        "url": "before_change"
    },
    'bar': {
        "status": "in_progress",
        "title": "test2",
        "url": "someurl"
    }
}

new = {
    'foo': {
        "status": "done",
        "title": "test",
        "url": "after_change"
    },
    'bar': {
        "status": "in_progress",
        "title": "test2",
        "url": "someurl"
    }
}


delta_list = diff(old, new)

print([x for x in delta_list])
