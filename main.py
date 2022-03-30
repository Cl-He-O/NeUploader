#!/usr/bin/env python3

import os
import neuploader as nu
from tkinter import filedialog
from txt2lrc import txt2lrc

files = filedialog.askopenfilenames(
    title="choose files you want to upload.", initialdir="~/"
)

aurl = nu.UploadFile((".mp3", open("1.mp3", "rb").read())).url

print(aurl)

for file in files:
    lrcs = txt2lrc(file)
    nc = nu.NewColumn(os.path.split(file)[1], "=_=", "")
    print(nc.column)
    for (i, lrc) in enumerate(lrcs):
        res = nu.NewArticle(aurl, 5, str(i), nc.column)
        if not res.successed:
            input(res.message)

        articleId = res.articleId
        res = nu.UpdateSubtitle(lrc.encode(), articleId)
        if not res.successed:
            input(res.message)

        res = nu.PublishArticle(articleId)
        print(res.res)
