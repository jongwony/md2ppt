import base64
import binascii
import os
from io import BufferedIOBase

is_screen = os.environ.get('TERM').startswith('screen')
osc = b'\033Ptmux;\033\033]' if is_screen else b'\033]'
st = b'\a\033\\' if is_screen else b'\a'


def get_content(content) -> bytes:
    # bytes
    if isinstance(content, bytes):
        return content

    # file-like object
    if isinstance(content, BufferedIOBase):
        return content.read()

    # str
    try:
        # base64 string
        return base64.b64decode(content, validate=True)
    except binascii.Error:
        # filename
        with open(content, 'rb') as f:
            raw_content = f.read()
        return raw_content


def iterm2_img_format(content, inline=1, preserve=1,
                      width=None, height=None) -> str:
    raw_content = get_content(content)
    size = len(raw_content)
    b64content = base64.b64encode(raw_content)

    result = osc
    result += b'1337;File='
    result += b'size=%s;' % bytes(str(size).encode())
    result += b'inline=%s;' % bytes(str(inline).encode())
    if width is not None:
        result += b'width=%s;' % bytes(str(width).encode())
    if height is not None:
        result += b'height=%s;' % bytes(str(height).encode())
    result += b'preserveAspectRatio=%s;' % bytes(str(preserve).encode())
    result += b':'
    result += b'%s' % b64content
    result += st
    result += b'\n'

    return result.decode()
