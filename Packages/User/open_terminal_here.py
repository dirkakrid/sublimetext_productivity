  import sublime, sublime_plugin
import os
import subprocess
import threading


class OpenTerminalHere(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        file_path = view.file_name()
        dirname = os.path.dirname(file_path)

        th = GnomeTerminalThread(dirname)
        th.start()

    def enabled(self):
        return True if self.view.file_name() else False

class GnomeTerminalThread(threading.Thread):
    def __init__(self, dirname):
        self.dirname = dirname
        threading.Thread.__init__(self)

    def run(self):
        if self.dirname:
            fpc = "--working-directory={0}".format(self.dirname)
            subprocess.call(['gnome-terminal', fpc])
