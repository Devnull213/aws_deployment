#!/usr/bin/env python3
import os
import subprocess

def repo_config(repo_name, repo_url):

    #////Update system and install basic programs and bd////

    subprocess.run(['sudo', 'apt', 'update'])
    subprocess.run(['sudo', 'apt', 'install', 'postgresql', 'postgresql-contrib'])
    subprocess.run(['sudo', 'apt', 'install', 'nginx'])
    subprocess.run(['git', 'clone', repo_url])
    subprocess.run(['sudo', 'apt', 'install', 'python3-venv'])
    os.chdir(repo_name)
    subprocess.run(['python3', '-m', 'venv', 'venv'])
    subprocess.run(['source', 'venv/bin/activate'])

    #////install framework, and specific use programs////

    subprocess.run(['pip', 'install', 'django==2.2.4'])
    subprocess.run(['pip', 'install', 'bcrypt'])
    subprocess.run(['pip', 'install', 'gunicorn'])


def project_settings_mods(project_name, server_ip):
    ip_for_settings_mods = 'ALLOWED_HOSTS = [\'' + str(server_ip) +'\']'

    os.chdir(project_name)
    with open ('settings.py', 'r') as settings:
        mods = settings.read()

    mods = mods.replace('DEBUG = True', 'DEBUG = False')
    mods = mods.replace('ALLOWED_HOSTS = []', ip_for_settings_mods)

    with open ('settings.py', 'w') as settings:
        settings.write(mods)

    with open ('settings.py', 'a') as settings:
        settings.write('\nSTATIC_ROOT = os.path.join(BASE_DIR, "static/")')

    os.chdir('..')

    subprocess.run(['python', 'manage.py', 'collectstatic'])
    subprocess.run(['python', 'manage.py', 'makemigrations'])
    subprocess.run(['python', 'manage.py', 'migrate'])


if __name__ == "__main__":

    repo_name = input('Enter repository name: ')
    repo_url = input('Enter repository url: ')

    repo_config(repo_name, repo_url)

    project_name = input('Enter the name of the project (NOT THE REPO):')
    server_ip = input('Enter the server ip address: ')

    project_settings_mods(project_name, server_ip)

