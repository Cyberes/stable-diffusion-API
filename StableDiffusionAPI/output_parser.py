from bs4 import BeautifulSoup


def markup_resembles_filename(markup):
    """Error-handling method to raise a warning if incoming markup
    resembles a filename.

    :param markup: A bytestring or string.
    :return: Whether or not the markup resembles a filename
        closely enough to justify a warning.

    stolen from bs4
    """
    path_characters = '/\\'
    extensions = ['.html', '.htm', '.xml', '.xhtml', '.txt']
    if isinstance(markup, bytes):
        path_characters = path_characters.encode("utf8")
        extensions = [x.encode('utf8') for x in extensions]
    filelike = False
    if any(x in markup for x in path_characters):
        filelike = True
    else:
        lower = markup.lower()
        if any(lower.endswith(ext) for ext in extensions):
            filelike = True
    if filelike:
        return True
    return False


class OutputParser:
    def __init__(self, html):
        if not markup_resembles_filename(html):
            self.__soup = BeautifulSoup(html, 'html.parser')
            self.__skip = False
        else:
            self.__soup = html
            self.__skip = True

    def check_for_error(self):
        if not self.__skip:
            elm = self.__soup.find('div', {'class': 'error'})
            if elm is not None and len(elm) > 0:
                return [True, elm.findChild('p').string]
            return [False, None]
        else:
            return [False, self.__soup]
