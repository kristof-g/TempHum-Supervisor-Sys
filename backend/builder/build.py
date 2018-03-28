import os, shutil, subprocess, sys
from termcolor import colored
from pyspin.spin import make_spin, Default

FNULL = open(os.devnull, 'w')
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
npm_path = os.path.join(base_path,"front")
front_folder = os.path.join(base_path, "server/front")

def res(path1, path2):
    return os.path.join(path1, path2)

def logger(src, color, msg):
    print("\n[{}]: {}".format(colored(src, 'cyan'), colored(msg, color)))

def cleanFolder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) and not file_path.endswith('.py'):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    logger('CLEAN-FOLDER', 'yellow', "deleted folder: {}".format(folder))
        
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

@make_spin(Default, "DIST COPY...")
def copyDist():
    try:
        cleanFolder(front_folder)
        copytree(res(npm_path, 'dist'), front_folder)
    except Exception as error:
        print("[Something went wrong in CopyGui]: {}".format(error))
        return
    logger('COPY', 'green', "copy done!")

@make_spin(Default, "NPM RUN DIST RUNNING...")
def npmRunDist():
    os.chdir(npm_path)
    try:
        subprocess.check_call('npm run build', shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    except Exception as error:
        logger('NODE', 'red', 'Something went wrong during build proc... \n{}'.format(error))
    logger('NODE-DIST', 'green', 'BUILD SUCCESSFULL')
    os.chdir(base_path)


def npmRunDev():
    os.chdir(npm_path)
    try:
        subprocess.check_call('npm run dev', shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
    except Exception as error:
        logger('NODE', 'red', 'Something went wrong during build proc... \n{}'.format(error))
    logger('NODE-DEV', 'green', 'DEV STARTED')
    os.chdir(base_path)

def pyRunServer():
    try:
        cmd = ['python3', base_path+'/run.py']
        subprocess.Popen(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
        logger('PY-DEV', 'green', 'DEV STARTED')
    except Exception as error:
        logger('NODE', 'red', 'Something went wrong during build proc... \n{}'.format(error))
    logger('NODE-DEV', 'green', 'DEV STARTED')
    os.chdir(base_path)


header = "[=============================================]\n"\
         "|             VUE JS FLASK TOOL               |\n"\
         "[=============================================]"


if __name__ == '__main__':
    print(colored(header,'blue'))
    try:
        if sys.argv[1] == 'PROD':
            logger('NODE-DIST', 'white', 'VUEJS BUILD PROC STARTING NOW...')
            npmRunDist()
            copyDist()
        elif sys.argv[1] == 'DEV':
            pyRunServer()
            npmRunDev()
    except IndexError:
        logger('ARG','red', 'No args, add PROD or DEV')

