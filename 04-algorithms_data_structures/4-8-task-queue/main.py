class Queue:
    def __init__(self):
        self.items = []
    
    def is_empty(self) -> bool:
        return len(self.items) == 0

    def enqueue(self, item: object) -> None:
        self.items.append(item)

    def dequeue(self) -> object | None:
        if not self.is_empty():
            return self.items.pop(0)
        else:
            return None

    def size(self) -> int:
        return len(self.items)

class Task:
    name: str

    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

class TaskQueue(Queue):
    def __init__(self):
        super().__init__()

    def add_task(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("Task should be instances of Task")
        super().enqueue(task)

    def get_next_task(self) -> Task | None:
        task = super().dequeue()
        if task is None:
            return None
        if not isinstance(task, Task):
            raise TypeError("Wrong queue element type")
        return task

tq = TaskQueue()

count = 5
for i in range(count):
    tq.add_task(Task("Задача " + str(i+1)))

try:
    for i in range(tq.size() + 1):
        next_task = tq.get_next_task()
        print(f"Следующая задача: {next_task.get_name() if next_task else 'Нет задач'}")
except Exception as e:
    print('Error:', e)
    exit()
