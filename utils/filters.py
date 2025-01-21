def filter_tasks(tasks, status=None, priority=None):
    """ Filter tasks based on status and priority """
    filtered_tasks = tasks
    if status is not None:
        filtered_tasks = [task for task in filtered_tasks if task[5] == status]
    if priority is not None:
        filtered_tasks = [task for task in filtered_tasks if task[4] == priority]
    return filtered_tasks

def sort_tasks(tasks, sort_by="deadline", ascending=True):
    """ Sort tasks based on a given column """
    column_index = {
        "id": 0,
        "title": 1,
        "description": 2,
        "deadline": 3,
        "priority": 4,
        "status": 5
    }.get(sort_by, 3)  # Default to sorting by deadline

    sorted_tasks = sorted(tasks, key=lambda x: x[column_index], reverse=not ascending)
    return sorted_tasks