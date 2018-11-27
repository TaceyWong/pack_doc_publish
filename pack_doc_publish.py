#! /ust/bin/env python3

"""
:pack in local & run in remote
author:by Tacey Wong
date:2018.11.23
"""
import os
import sys
import shutil
import atexit
from contextlib import contextmanager
from fabric import Connection

MKDOCS_PATH = ""
HTML_SRC_DIR = ""
REMOTE_HOST = ''
REMOTE_USER = ''
REMOTE_PWD = ""
EXE_NAME = ""
EXE_PORT = ''


GO_SRC = """
package main
import (
  "log"
  "net/http"
  "github.com/GeertJohan/go.rice"
)
func main() {
  http.Handle("/", http.FileServer(rice.MustFindBox("%s").HTTPBox()))
  log.Println("Listening :%s...")
  log.Fatal(http.ListenAndServe(":%s", nil))
}
"""%(HTML_SRC_DIR, EXE_PORT,EXE_PORT)


def put_and_restart():
    """put exe to remote server and start/restart it"""
    print('INFO    -  Put exe to remote server[{}]'.format(REMOTE_HOST))
    with Connection(host=REMOTE_HOST,user=REMOTE_USER,connect_kwargs={'password':REMOTE_PWD}) as conn:
        try:
            cmd = "ps ax |grep %s | awk '{print $1}' | xargs -i kill {}"%EXE_NAME
            conn.run(cmd)
        except Exception:
            pass
        conn.put(EXE_NAME)        
        conn.run("nohup ./{} &> /dev/null &".format(EXE_NAME),pty=False)
        
    print('INFO    -  Running on [{}]:[{}]'.format(REMOTE_HOST,EXE_PORT))

def build_site():
    """make html doc from markdown using mkdocs""" 
    print('INFO    -  Build doc-site:transe markdown -> html...')
    with cd(os.sep.join(HTML_SRC_DIR.split(os.sep)[:-1])):
        os.system("{} build".format( MKDOCS_PATH))
    
def pack_into_one():
    """pack html_src into one [exe]"""
    print('INFO    -  Pack doc-site into one exe...')
    with open('go_src.go', 'w') as go_src:
        go_src.write(GO_SRC)
    os.system("rice embed-go && go build -o {}".format(EXE_NAME))
    print('INFO    -  Clean go-src')
    os.remove('go_src.go')
    os.remove('rice-box.go')

def remove_static():
    """remove static html src"""
    try:
        shutil.rmtree(HTML_SRC_DIR)
    except OSError:
        pass
    except Exception:
        pass

@contextmanager
def cd(path_to_cd):
    """cd one dir"""
    try:
        pwd = os.getcwd()
        os.chdir(os.path.abspath(path_to_cd))
        yield
    finally:
        os.chdir(pwd)

if __name__ == "__main__":
    atexit.register(lambda: print('pack_publish script exited'))
    PUT = False
    if len(sys.argv) == 2 and sys.argv[1]:
        PUT = True
    elif len(sys.argv) > 2:
        sys.exit(1)
    build_site()
    pack_into_one()
    if PUT:
        put_and_restart()
    remove_static()
