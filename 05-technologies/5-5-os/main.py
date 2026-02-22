import os
import shutil

# 1
print('Task.1')
BASE_PATH = os.getcwd()
dir = 'Управление_файлами'
os.mkdir(dir)
os.chdir(dir)

f1 = "file1.txt"
f2 = "file2.txt"
with open(f1, "w", encoding="utf-8") as f:
    f.write("Hello world")

with open(f2, "w", encoding="utf-8") as f:
    f.write("Some text")
    f.write("Another text")

print(os.listdir('.'))


# 2
print('\nTask.2')
os.remove(f1)
sub_dir = 'Поддиректория'
os.mkdir(sub_dir)
shutil.move(os.path.join(os.getcwd(), f2), os.path.join(os.getcwd(), sub_dir))
os.chdir(os.path.join(os.getcwd(), sub_dir))
print(os.listdir('.'))
os.chdir('../..')
shutil.rmtree(dir)
print(os.listdir('.'))