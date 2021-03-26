
import subprocess
import os

def project_settings_mods(project_name, server_ip):
    subprocess.run(['pip', 'install', 'django==2.2.4'])
    subprocess.run(['pip', 'install', 'bcrypt'])
    subprocess.run(['pip', 'install', 'gunicorn'])

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

if __name__ == '__main__':

    project_name = input('Enter the name of the project (NOT THE REPO):')
    server_ip = input('Enter the server ip address: ')
    project_settings_mods(project_name, server_ip)

