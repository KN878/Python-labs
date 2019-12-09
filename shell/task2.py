import subprocess
import os


def run_command(cmd):
    proc = subprocess.Popen(cmd,
                            shell=True,
                            universal_newlines=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            encoding="cp866")
    try:
        stdout, stderr = proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()

    print(stdout)
    print(stderr)


def change_dir(path):
    try:
        os.chdir(os.path.abspath(path))
    except Exception:
        print("myshell> cd: no such file or directory: {}".format(path))


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
    while True:
        try:
            cmd = input("myshell [{}]> ".format(screw_path()))
            if cmd == "exit":
                break
            elif cmd[:3] == "cd ":
                change_dir(cmd[3:])
            else:
                run_command(cmd)
        except EOFError:
            break
    print("Goodbye!")


main()
