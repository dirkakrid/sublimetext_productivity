'''


'''
import sublime, sublime_plugin


def nothing_selected():
    sublime.status_message('nothing selected, fool')

class Evalifier(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.enabled():
            nothing_selected()
            return

        def get_whitespace(selection):
            dstr = ''
            for s in selection:
                if s.isspace():
                    dstr += ' '
                else:
                    break
            return dstr

        view = self.view
        selections = view.sel()
        sel = view.line(selections[0])

        # find begin and end points of line, make new Region reference
        full_line_region = sublime.Region(sel.a, sel.b) 

        # get all characters from line
        selection = view.substr(sel)
        whitespace = get_whitespace(selection)
        final = str(eval(selection))

        if not final: 
            return

        view.replace(edit, full_line_region, whitespace + final)

    
    def enabled(self):
        '''only allow 1 selection for version 0.1''' 

        sels = self.view.sel()    # lists regions, 
        nsels = len(sels)          # dir(sels[0]) for methods
        fsel = sels[0]            # first selection

        if nsels == 1 and not fsel.empty():
            return True
