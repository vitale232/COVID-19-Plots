import os
import subprocess
import sys


PYTHON = os.path.abspath(os.path.join(
    sys.exec_prefix,
    'python.exe'
))
BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

def verbose_checkcall(command, shell=False):
    cmd = ' '.join(command)
    print(f' {cmd}')
    subprocess.check_call(command, shell=shell)
    return True

# Check for new data from Johns Hopkins
print('Pull data from GitHub')
data_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
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
os.chdir(os.path.abspath(os.path.join(
    os.path.dirname(__file__)
)))

python_parse_and_plot_command = [
    PYTHON,
    os.path.join(BASE_DIR, 'parse_and_plot.py')
]
verbose_checkcall(python_parse_and_plot_command, shell=True)

# Run the new_and_total_plots.py script
new_and_total_plots_command = [
    PYTHON,
    os.path.join(BASE_DIR, 'new_and_total_plots.py')
]
verbose_checkcall(new_and_total_plots_command)

# Push the new plots to GitHub
print(f'\nRunning git commands in directory:\n {os.getcwd()}\n')
print('\nGit status:')
git_status_command = [
    'git',
    'status'
]
verbose_checkcall(git_status_command)

print('\nAdd files to git')
git_add_command = [
    'git',
    'add',
    '.'
]
verbose_checkcall(git_add_command)

print('\nCommit files to git')
git_commit_command = [
    'git',
    'commit',
    '-m',
    'Update figures (from script)'
]
verbose_checkcall(git_commit_command)

print('\nPush files to git')
git_push_command = [
    'git',
    'push'
]
verbose_checkcall(git_push_command)

print('\nGit status:')
verbose_checkcall(git_status_command)