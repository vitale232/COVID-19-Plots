from datetime import date, datetime
import os
import subprocess
import shutil
import sys


start_time = datetime.now()
print(f'\nRunning script : {os.path.abspath(__file__)}')
print(f'Start time     : {start_time}')


PYTHON = os.path.abspath(os.path.join(
    sys.exec_prefix,
    'python.exe'
))
BASE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '..',
))
SRC_DIR = os.path.join(
    BASE_DIR,
    'source'
)

def verbose_checkcall(command, shell=False):
    cmd = ' '.join(command)
    print(f' {cmd}')
    subprocess.check_call(command, shell=shell)
    return True

# Archive current PNGs
png_dir = os.path.join(
    BASE_DIR,
    'output',
    'PNGs',
)
archive_dir = os.path.join(
    png_dir,
    'archive',
    str(date.today())
)
print(f'Archiving PNGs to:\n {archive_dir}')
if not os.path.isdir(archive_dir):
    os.makedirs(archive_dir)

for png_file in os.listdir(png_dir):
    if not png_file.endswith('.png'):
        continue
    shutil.copyfile(
        os.path.join(png_dir, png_file),
        os.path.join(archive_dir, png_file)
    )

# Check for new data from Johns Hopkins
print('Pull data from GitHub')
data_dir = os.path.abspath(os.path.join(
    BASE_DIR,
    'data',
    'COVID-19'
))
os.chdir(data_dir)

download_data_command = [
    'git',
    'pull'
]
verbose_checkcall(download_data_command)

# Run the parse_and_plot.py script
print('\nParse the data and make some plots')
os.chdir(BASE_DIR)

print('\nCalling script')
python_parse_and_plot_command = [
    PYTHON,
    os.path.join(SRC_DIR, 'parse_and_plot.py')
]
verbose_checkcall(python_parse_and_plot_command, shell=True)

# Run the new_and_total_plots.py script
print('Calling script')
new_and_total_plots_command = [
    PYTHON,
    os.path.join(SRC_DIR, 'new_and_total_plots.py')
]
verbose_checkcall(new_and_total_plots_command)

# Push the new plots to GitHub
print(f'\nRunning git commands in directory:\n {os.getcwd()}\n')
print('\nGit status:')
git_status_command = [
    'git',
    'status'
]
verbose_checkcall(git_status_command, shell=True)

print('\nAdd files to git')
git_add_command = [
    'git',
    'add',
    '.'
]
verbose_checkcall(git_add_command, shell=True)

print('\nCommit files to git')
git_commit_command = [
    'git',
    'commit',
    '-m',
    'Update figures (from script)'
]
verbose_checkcall(git_commit_command, shell=True)

print('\nPush files to git')
git_push_command = [
    'git',
    'push'
]
verbose_checkcall(git_push_command, shell=True)

print('\nGit status:')
verbose_checkcall(git_status_command, shell=True)

end_time = datetime.now()
print(f'\nScript completed : {end_time}')
print(f'Run time         : {end_time-start_time}\n')
