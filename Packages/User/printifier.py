'''
author: Dealga McArdle, 2013. 

http://www.sublimetext.com/docs/2/api_reference.html

Installation
- place printifier.py in Data/Packages/User
- place dictionary entry in Keybindings, User
{ "keys": ["ctrl+alt+P"], "command": "printifier" }

Usage

some_variable = [1,2,3,4]
some_variable

duplicate the variable name to a new line 
then select the it and hit ctrl+alt+p and it will 
replace it with:

print('some_variable', some_variable)

'''
import sublime, sublime_plugin


def nothing_selected():
    sublime.status_message('nothing selected, fool')

def print_variable_and_repr(var_in):
    return 'print(\'{0}\', {0})'.format(var_in)

class Printifier(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.enabled():
            nothing_selected()
            return

        view = self.view
        sel = view.sel()[0]

        # get selection and trn it into it's printable form
        selection = view.substr(sel)
        new_text = print_variable_and_repr(selection)
        
        edit = view.begin_edit()    # stick onto undo stack
        view.replace(edit, sel, new_text)

        # finalize this edit, use as one undo level
        view.end_edit(edit)
    
    def enabled(self):
        '''only allow 1 selection for version 0.1''' 

        sels   = self.view.sel()    # lists regions, 
        nsels  = len(sels)          # dir(sels[0]) for methods
        fsel   = sels[0]            # first selection

        if nsels == 1 and not fsel.empty():
            return True

