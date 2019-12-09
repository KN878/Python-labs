import subprocess


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


def main():
    while True:
        try:
            cmd = input("myshell> ")
            if cmd == "exit":
                break
            run_command(cmd)
        except EOFError:
            break
    print("Goodbye!")


main()
