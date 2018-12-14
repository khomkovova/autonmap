
import argparse
import threading
import os
import re
import subprocess
import sys
import pty

t = threading.Thread()
numberNow = 0
parser = argparse.ArgumentParser(description="Write your command, file and thread")
parser.add_argument("-c", dest="command", help="Command to be execute example \"ping ??? -c  && ls\"")
parser.add_argument("-f", dest="filename", help="File to be checked")
parser.add_argument("-d", dest="dir", help="Folder for output")
parser.add_argument("-t", dest="thread", help="Count thread")
args = parser.parse_args()

execCommand = str(args.command)
filename = str(args.filename)
thread = int(args.thread)
DIR = str(args.dir)
ip = [line.rstrip('\n') for line in open(filename)]

def getCommand():
    if numberNow < len(ip):
        command = ip[numberNow]
        return command
    else:
        return ""

def runCommand(url):
    global numberNow
    global execCommand
    r = re.search(r'([^$]+)\?\?\?(.+)', execCommand)
    firstCmd = r[1]
    secondCmd = str(r[2])

    cmd = firstCmd + url + secondCmd
    filename = re.sub(r'/', '*', cmd)
    wrCmd = "  '" + DIR + filename + ".txt'"
    cmd += wrCmd
    print(cmd)
    master, slave = pty.openpty()
    p = subprocess.run([cmd], shell=True, stdin=slave, stdout=slave, stderr=slave)

    os.close(slave)
    os.close(master)
    command = getCommand()

    if (command == ""):

        return
    else:
        numberNow +=1
        newThread(command)

def newThread(line):
    global t
    print("Line = " + line)
    t = threading.Thread(target=runCommand, kwargs={"url":line})
    t.start()

def main():
    global numberNow

    for i in range(thread):
        command = getCommand()
        if (command != ""):
            newThread(command)
            numberNow = numberNow + 1

if __name__ == "__main__":
    main()
    sys.exit(1)