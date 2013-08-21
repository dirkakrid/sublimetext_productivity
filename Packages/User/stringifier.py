'''
author: Dealga McArdle, 2013. 

http://www.sublimetext.com/docs/2/api_reference.html

Installation
- place stringifier.py in Data/Packages/User
- place dictionary entry in Keybindings, User
{ "keys": ["ctrl+shift+["], "command": "stringifier" }

Usage
select a sequence of space separated words then press the key combo

one two three four  -> ctrl+shift+[ -> ['one', 'two', 'three', 'four']

'''
import sublime, sublime_plugin


def nothing_selected():
    sublime.status_message('nothing selected, fool')

class Stringifier(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.enabled():
            nothing_selected()
            return

        view = self.view
        sel = view.sel()[0]

        # just selected region
        selection = view.substr(sel)
        split_selection = selection.split()

        # wchar = wrap character
        wrap = lambda x, wchar: wchar + x + wchar
        wrap2 = lambda x, wchars: wchars[0] + x + wchars[1]

        wrapped = [wrap(word, "'") for word in split_selection]
        wrapped_pre =', '.join(wrapped)
        wrapped_final = wrap2(wrapped_pre, "[]")

        edit = view.begin_edit()    # stick onto undo stack
        view.replace(edit, sel, wrapped_final)

        # finalize this edit, use as one undo level
        view.end_edit(edit)
        print(wrapped_final)

    
    def enabled(self):
        '''only allow 1 selection for version 0.1''' 

        sels   = self.view.sel()    # lists regions, 
        nsels  = len(sels)          # dir(sels[0]) for methods
        fsel   = sels[0]            # first selection

        if nsels == 1 and not fsel.empty():
            return True

