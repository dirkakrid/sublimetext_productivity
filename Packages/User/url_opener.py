'''
url_opener.py

author: Dealga McArdle, 2013
functionality: point webbrowser at selected url
sublime API docs: sublimetext.com/docs/2/api_reference.html

'''
import sublime, sublime_plugin

# def nothing_selected():
#    sublime.status_message('nothing selected, fool')


class UrlOpener(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.enabled():
            print('from URL opener, you must select a word or url')
            return

        view = self.view
        sel = view.sel()[0]
        url_search_term = view.substr(sel)

        url_prefix = 'http://'
        if not url_search_term.startswith(url_prefix):
            url_search_term = url_prefix + url_search_term

        import webbrowser
        webbrowser.open(url_search_term)

        # if chrome doesn't find the url, 
        # - hit tab to focus search button
        # - hit enter to search that way instead


    def enabled(self):
        '''only allow 1 selection for version 0.1''' 

        sels   = self.view.sel()    # lists regions, 
        nsels  = len(sels)          # dir(sels[0]) for methods
        fsel   = sels[0]            # first selection

        if nsels == 1 and not fsel.empty():
            return True

