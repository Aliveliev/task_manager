import csv

def export_tasks_to_csv(tasks, file_path):
    """ Export tasks to a CSV file """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Title", "Description", "Deadline", "Priority", "Status"])
        for task in tasks:
            writer.writerow(task)