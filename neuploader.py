#!/usr/bin/env python3

from typing import Tuple
import httpx
import json

config = json.loads(s=open("./config.json", "rb").read())


class UploadFile:
    def __init__(
        self, file: Tuple[str, bytes], cookie: str = config["cookie"]
    ) -> Tuple[str, str, int | str]:
        """file: (file name, content)
        extension part of file name will be used to determine the type of file!"""

        res = httpx.post(
            url=config["uploadFile"],
            files={"nosFile": file},
            headers={"cookie": cookie},
        )

        content = res.json()

        if res.status_code != 200:
            self.successed = False
            self.message = content["msg"]
        else:
            self.successed = True
            self.url = json.loads(res.text)["data"]


class NewColumn:
    def __init__(
        self,
        title: str,
        intro: str,
        image: str,
        topCategory: str = "",
        secondCategory: str = "",
        private: str = "true",
        scanning: str = "false",
        cookie: str = config["cookie"],
    ) -> Tuple[int, str, any]:
        """=_="""

        res = httpx.post(
            url=config["columnSave"],
            data={
                "title": title,
                "intro": intro,
                "image": image,
                "topCat": topCategory,
                "secondCat": secondCategory,
                "private": private,
                "scanning": scanning,
            },
            headers={"cookie": cookie},
        )

        content = res.json()

        if res.status_code != 200:
            self.successed = False
            self.message = content["msg"]
        else:
            self.successed = True
            self.column = content["data"]["name"]


class NewArticle:
    def __init__(
        self,
        audioUrl: str,
        audioDuration: int,
        title: str,
        column: str,
        audioLang: str = "en",
        audioFileName: str = "",
        cookie: str = config["cookie"],
    ):
        """=_="""
        res = httpx.get(
            config["articleSave"],
            params={
                "audioUrl": audioUrl,
                "audioDuration": audioDuration,
                "title": title,
                "column": column,
                "audioLang": audioLang,
                "audioFileName": audioFileName,
            },
            headers={"cookie": cookie},
        )

        content = res.json()

        if res.status_code != 200:
            self.successed = False
            self.message = content["msg"]
        else:
            self.successed = True
            self.articleId = content["data"]["articleId"]


class UpdateSubtitle:
    def __init__(self, file: bytes, articleId: int, cookie: str = config["cookie"]):
        """=_="""
        res = httpx.post(
            url=config["subtitleUpdate"],
            files={
                "textFile": (".lrc", file),
                "articleId": ("", str(articleId).encode()),
            },
            headers={"cookie": cookie},
            timeout=60,
        )

        content = res.json()

        if res.status_code != 200:
            self.successed = False
            self.message = content["msg"]
        else:
            self.successed = True


def sync_subtitle(
    file: Tuple[str, bytes], articleId: int, cookie: str = config["cookie"]
):
    """=_="""
    now = httpx.get(
        url=config["articleGet"],
        params={"id": articleId},
        headers={"cookie": config["cookie"]},
    )


class PublishArticle:
    def __init__(self, articleId: int, cookie: str = config["cookie"]):
        """"""
        res = httpx.get(
            url=config["articleGet"],
            params={"id": articleId},
            headers={"cookie": config["cookie"]},
        )

        res = httpx.post(
            url=config["articleFullSave"],
            data=res.json()["data"],
            headers={"cookie": cookie},
        )

        res = httpx.get(
            url=config["articleUpdateStatus"],
            params={"articleId": articleId, "status": "PUBLISH"},
            headers={"cookie": cookie},
        )

        content = res.json()

        if res.status_code != 200:
            self.successed = False
            self.message = content["msg"]
        else:
            self.successed = True
            self.content = content["data"]


class Column:
    def __init__(
        self,
        id: int,  # identifier
        name: str,  # 'C' + 6 numbers
        title: str,  # title
        intro: str,  # introduction
        image: str,  # url to the cover
        allowSubscribe: bool,
        publishTime: int,  # UNIX timestamp in millisecond
        vip: bool,
        allowClients: list,
        ugc: bool,
        nickname: str,  # phone number with asterisks
        topCat,
        secondCat,
        thirdCat,
        totalElements: int,
        latestArticleTime: int,
        latestArticleId: int,
        visitNum: int,
        scanning: bool,
        hardwareCode: str,  # same with name argument
        deeplinkUrl: str,
        privacy: bool,
    ):
        """Use **kwargs to initialize."""
        self.id = id
        self.name = name
        self.title = title
        self.intro = intro
        self.image = image
        self.allowSubscribe = allowSubscribe
        self.publishTime = publishTime
        self.vip = vip
        self.allowClients = allowClients
        self.ugc = ugc
        self.nickname = nickname
        self.topCat = topCat
        self.secondCat = secondCat
        self.thirdCat = thirdCat
        self.totalElements = totalElements
        self.latestArticleTime = latestArticleTime
        self.latestArticleId = latestArticleId
        self.visitNum = visitNum
        self.scanning = scanning
        self.hardwareCode = hardwareCode
        self.deeplinkUrl = deeplinkUrl
        self.privacy = privacy


def get_column_list(cookie: str) -> Tuple[int, str, list[Column] | str]:
    """-> (status code, error message, list of Column elements | error detail)"""

    res = httpx.get(
        url=config["columnList"],
        headers={"cookie": cookie},
    )

    content = res.json()

    if res.status_code != 200:
        return (res.status_code, content["msg"], content["data"])

    return (
        200,
        content["msg"],
        [Column(**column) for column in content["data"]],
    )


class Article:
    def __init__(
        self,
        id: int,  # identifier
        title: str,  # title
        column: str,  # column which it's in
        status: str,  # HIDDEN or PUBLIC
        deepLinkUrl: str,
        hardwareCode: str,  # 'A' + numbers
        rank: int,
        createTime: str,  # create time, in form of: year-month-day hour:minute:second
        publishTime: str,  # publish time, same form as create time
        audioUrl: str,  # url to audio file
        audioLang: str,
        audioFileName: str,  # audio file name
        audioDuration: str,  # duration of audio file in seconds
    ):
        self.id = id
        self.title = title
        self.column = column
        self.status = status
        self.deepLinkUrl = deepLinkUrl
        self.hardwareCode = hardwareCode
        self.rank = rank
        self.createTime = createTime
        self.publishTime = publishTime
        self.audioUrl = audioUrl
        self.audioLang = audioLang
        self.audioFileName = audioFileName
        self.audioDuration = audioDuration


def get_article_list(
    column: str, cookie: str = config["cookie"]
) -> Tuple[int, str, list[Article] | str]:
    """column: column name, 'C' + 6 numbers

    -> (status code, error messsage, list of articles of column | error detail"""

    res = httpx.get(
        url=config["articleList"],
        params={"column": column},
        headers={"cookie": cookie},
    )

    content = res.json()

    if res.status_code != 200:
        return (res.status_code, content["msg"], content["data"])

    return (
        200,
        "SUCCESS",
        [Article(**article) for article in content["data"]["list"]],
    )
