import sublime, sublime_plugin
import os
import subprocess
import threading


class OpenGitbashHere(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        file_path = view.file_name()
        dirname = os.path.dirname(file_path)

        th = BashTerminalThread(dirname)
        th.start()

    def enabled(self):
        return True if self.view.file_name() else False

class BashTerminalThread(threading.Thread):
    def __init__(self, dirname):
        self.dirname = dirname
        threading.Thread.__init__(self)

    def run(self):
        if self.dirname:
            fpc = "--cd={0}".format(self.dirname)
            subprocess.call([r"C:\Program Files\Git\git-bash.exe", fpc])
