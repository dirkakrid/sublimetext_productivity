'''
sublime_to_gist.py

author: Dealga McArdle, 2013
functionality: upload anonymous gist from current tab
sublime API docs: sublimetext.com/docs/2/api_reference.html

milestones

[x] print current tab name
[-] print current tab content, if nothing selected
[x] print current selected text
[x] upload anonymously + spawn browser
[x] trim any leading whitespace, if selection indented.
[ ] deal with tabs where there should be spaces


'''
import json
import sys
import sublime, sublime_plugin
import os.path
from urllib.request import urlopen

def nothing_selected():
    sublime.status_message('nothing selected, fool')

def get_file_name(view):
    file_path = view.file_name()
    return os.path.basename(file_path)

def detect_newline_char(selection):
    ''''\n (newline) and \r (carriage return). '''
    newline = '\n'
    # carriage = '\r\n'
    # -- find the sublime setting for this.
    # os.linesep  ?
    # supposedly \n is now universal for python..
    return newline

def find_minimal_indent(lines):
    """for larger files this can be done more efficiently"""
    white_space_set = set([])
    
    for line in lines:
        lstripped = line.lstrip()
        num_whitespaces = len(line) - len(lstripped)

        if len(line) > 0:
            if num_whitespaces == 0:
                return 0
            white_space_set.update([num_whitespaces])

    # can safely indent by this amount, if zero do nothing.
    return min(white_space_set)

def undent(view, selection):
    '''remove excess whitespace but preserve relative indentation
    --- assumes tabs are not used for space.'''

    # print(repr(view.line_endings()))
    newline_char = detect_newline_char(selection)
    lines = selection.split(newline_char)

    amount_to_indent = find_minimal_indent(lines)

    # no indent required
    if amount_to_indent == 0:
        return selection

    # carve it up! 
    undented_lines = []
    for line in lines:
        this_line = ''
        if not line.isspace():
            this_line = line[amount_to_indent:]
        
        undented_lines.append(this_line)

    # notification to user
    indent_message = 'undented by ' + str(amount_to_indent)
    sublime.status_message(indent_message)

    return newline_char.join(undented_lines)


def main_upload_function(gist_filename, gist_description, gist_body):

    gist_post_data = {  'description': gist_description, 
                        'public': True,
                        'files': {gist_filename: {'content': gist_body}}}

    json_post_data = json.dumps(gist_post_data).encode('utf-8')

    def get_gist_url(found_json):
        wfile = json.JSONDecoder()
        wjson = wfile.decode(found_json)
        gist_url = 'https://gist.github.com/' + wjson['id']

        import webbrowser
        print(gist_url)
        webbrowser.open(gist_url)
        # or just copy url to clipboard?

    def upload_gist():
        print('sending')
        url = 'https://api.github.com/gists'
        json_to_parse = urlopen(url, data=json_post_data)
        
        print('received response from server')
        # found_json = json_to_parse.readall().decode()   py3
        found_json = json_to_parse.read().decode()
        get_gist_url(found_json)

    upload_gist()


class SublimeToGist(sublime_plugin.TextCommand):
    def run(self, edit):
        if not self.enabled():
            nothing_selected()
            return

        view = self.view
        sel = view.sel()[0]

        file_name = get_file_name(view)
        print(file_name)

        # adjust the sel.begin to be at line start
        sel = view.line(sel) 

        # get the content of the selected region
        selection = view.substr(sel)

        # if region is indented, this undents, else returns original
        undented = undent(view, selection)

        main_upload_function(file_name, 'test', undented)
        # sublime.status_message('magnets, bitches')
        
    
    def enabled(self):
        '''only allow 1 selection for version 0.1''' 

        sels   = self.view.sel()    # lists regions, 
        nsels  = len(sels)          # dir(sels[0]) for methods
        fsel   = sels[0]            # first selection

        if nsels == 1 and not fsel.empty():
            return True

