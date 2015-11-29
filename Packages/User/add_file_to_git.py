import sublime
import sublime_plugin
import os
import subprocess
import threading


class AddFileToGit(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        filepath = view.file_name()
        dirname = os.path.dirname(filepath)

        print('git add', filepath)
        # th = GnomeTerminalThread(dirname)
        # th.start()
        subprocess.Popen(['git', 'add', filepath, '-f'], cwd=dirname)

    def enabled(self):
        return True if self.view.file_name() else False


# class GnomeTerminalThread(threading.Thread):
#     def __init__(self, dirname):
#         self.dirname = dirname
#         threading.Thread.__init__(self)

#     def run(self):
#         if self.dirname:
#             fpc = "--working-directory={0}".format(self.dirname)
#             subprocess.call(['gnome-terminal', fpc])
