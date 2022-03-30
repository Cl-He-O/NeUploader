#!/usr/bin/env python3

import os, shutil
import chardet

###########################################################
#####  you shouldn't try to read these garbage codes  #####
###########################################################

RLO_char = "\u202E"

brackets = "[]「」【】〔〕［］〚〛〘〙（）()『』〖〗｛｝《》〈〉«»‹›⟨⟩"
brackets_to = ""

for i in range(len(brackets)):
    brackets_to += brackets[i ^ 1]

brackets_map = str.maketrans(brackets, brackets_to)


def txt2lrc(
    file: str,
    split_lines=800,
    to_files=False,
    dstpath: str = "",
) -> list[str]:

    content = open(file, "rb").read()

    content = content.decode(chardet.detect(content)["encoding"])
    content = content.translate(brackets_map)

    lrc = []

    cnt = 0
    for line in content.splitlines():
        if line.strip() == "":
            # ignore empty lines
            continue

        if cnt % split_lines == 0:
            lrc.append("")

        lrc[-1] += "[00:01.00]" + RLO_char + line.strip()[::-1] + RLO_char + "\n"
        # "[00:{:0>2d}.00]".format(cnt)
        cnt += 1

    if to_files:
        if dstpath == "":
            dstpath = file + ".lrc"

        try:
            os.mkdir(dstpath)
        except:
            shutil.rmtree(dstpath)
            os.mkdir(dstpath)

        for i in range(len(lrc)):
            open(dstpath + "/" + str(i) + ".lrc", "w", encoding="utf-8").write(lrc[i])

    return lrc
