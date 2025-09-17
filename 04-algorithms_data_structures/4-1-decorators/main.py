from datetime import datetime
import requests

print('Task.1')
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        t_start = datetime.now()
        result = func(*args, **kwargs)
        t_finish = datetime.now()
        execution_time = t_finish - t_start
        milliseconds = round(execution_time.microseconds / 1000)
        print(f"Function completed in "
              f"{execution_time.seconds}s {milliseconds}ms")
        return result
    return wrapper

def is_prime(number: int):
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True

@measure_execution_time
def request_google(url):
    return requests.get(url)

print(request_google('https://google.com'))


print('\nTask.2')
def requires_admin(func):
    def wrapper(*args, **kwargs):
        if args[0]['role'] != 'admin':
            raise PermissionError(f"Only admin can do this action, found role is {args[0]['role']}")
        else:
            return func(*args, **kwargs)
    return wrapper

@requires_admin
def delete_user(user, username_to_delete):
    return f"User {username_to_delete} has been deleted by {user['username']}."


# Пример юзеров
admin_user = {'username': 'Alice', 'role': 'admin'}
regular_user = {'username': 'Bob', 'role': 'user'}

try:
    print(delete_user(admin_user, 'Charlie')) # Должно отработать
    print(delete_user(regular_user, 'Charlie')) # Должно рейзить PermissionError
except PermissionError as e:
    print('PermissionError:', e)
    exit()
except Exception as e:
    print('Error:', e)
    exit()