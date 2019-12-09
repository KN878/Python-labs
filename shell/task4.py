import subprocess
import os
import logging


def log(cmd, proc, stdout):
    cmd = cmd.split()
    logging.debug('%s, args: %s, stdout: %d, pid: %d, exit: %d', cmd[0], cmd[1:], stdout.count("\n"), proc.pid, proc.returncode)


def log_cd(cmd, exit_code):
    cmd = cmd.split()
    logging.debug('%s, args: %s, stdout: %d, exit: %d', cmd[0], cmd[1:], 0, exit_code)


def run_command(cmd, err_file):
    proc = subprocess.Popen(cmd,
                            shell=True,
                            universal_newlines=True,
                            stdout=subprocess.PIPE,
                            stderr=err_file,
                            encoding="cp866")
    try:
        stdout, stderr = proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
    print(stdout)
    log(cmd, proc, stdout)


def change_dir(cmd, err_file):
    try:
        os.chdir(os.path.abspath(cmd[3:]))
        log_cd(cmd, 0)
    except Exception:
        err_file.write("cd: no such file or directory: {}".format(cmd[3:]))


def screw_path():
    path = os.getcwd()
    screwed_path = ""
    if os.name == 'nt':
        path = path.split('\\')
        screwed_path += path[0]
        if len(path) != 1:
            for i in range(1, len(path)):
                screwed_path += '\\' + path[i][0]
    else:
        path = path.split('/')
        for i in range(0, len(path)):
            screwed_path += '/' + path[i][0]
    return screwed_path


def main():
    err_file = open("myshell.stderr", "a+")
    while True:
        try:
            cmd = input("myshell [{}]> ".format(screw_path()))
            if cmd == "exit":
                break
            elif cmd[:3] == "cd ":
                change_dir(cmd, err_file)
            else:
                run_command(cmd, err_file)
        except EOFError:
            break
        err_file.close()
    print("Goodbye!")


LOG_FILE = "myshell.log"
logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, format='[%(asctime)s] cmd:%(message)s')
main()
