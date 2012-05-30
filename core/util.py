from django.contrib.staticfiles.finders import find
from django.http import Http404
from markdown import markdown
from seminar import settings
import os.path

def load_markdown(markdown_filename, directory_name="mdown"):
    path = os.path.join(settings.STATIC_ROOT, directory_name, markdown_filename)
    
    try:
        mdfile = open(path, 'r+')
    except IOError:
        # We must be in development! Search for the static file using staticfiles finder
        match = find(directory_name + markdown_filename)
        if (match != None):
            mdfile = open(str(match), 'r+')
        else:
            raise Http404
        
    text = mdfile.read()
    html = markdown(text)
    mdfile.close()

    return html
