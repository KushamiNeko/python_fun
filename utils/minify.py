import re
from typing import IO


def minifyWeb(content: bytes) -> bytes:
    jsLineComment = re.compile(bytes(r"(\s|\n)//.*\n", "utf-8"))
    htmlLineComment = re.compile(bytes(r"(\s|\n)*<!--[^\r]*?-->", "utf-8"))
    cssLineComment = re.compile(bytes(r"(?m)^(\s|\n)*/\*[^\r]*?\*/", "utf-8"))
    emptyLine = re.compile(bytes(r"(?m)\s*\n+", "utf-8"))
    startingSpace = re.compile(bytes(r"(?m)^\s+", "utf-8"))

    content = jsLineComment.sub(b"", content)
    content = htmlLineComment.sub(b"", content)
    content = cssLineComment.sub(b"", content)
    content = emptyLine.sub(b"", content)
    content = startingSpace.sub(b"", content)
    return content


def minifyWebString(content: str) -> str:
    jsLineComment = re.compile(r"(\s|\n)//.*\n")
    htmlLineComment = re.compile(r"(\s|\n)*<!--[^\r]*?-->")
    cssLineComment = re.compile(r"(?m)^(\s|\n)*/\*[^\r]*?\*/")
    emptyLine = re.compile(r"(?m)\s*\n+")
    startingSpace = re.compile(r"(?m)^\s+")

    content = jsLineComment.sub("", content)
    content = htmlLineComment.sub("", content)
    content = cssLineComment.sub("", content)
    content = emptyLine.sub("", content)
    content = startingSpace.sub("", content)
    return content


def minifyWebIO(src: IO) -> IO:
    src.seek(0)
    content = src.read()

    if type(content) == str:
        content = minifyWebString(content)
    elif type(content) == bytes:
        content = minifyWeb(content)

    src.seek(0)
    src.write(content)
    src.seek(0)

    return src
