from django.template import Template

### Utils ###
#file loader
def loader(fname):
    fp = open(fname + '.html')
    t = Template(fp.read())
    fp.close()
    return t


def http_response(html, cookie=""):
    if cookie:
        return "Content-Type: text/html\r\n" + "Set-Cookie: " + cookie + "\r\n\r\n" + html
    else:
        return "Content-Type: text/html\r\n" + "\r\n\r\n" + html

#############
