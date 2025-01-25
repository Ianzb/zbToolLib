from .file import *
from .info import *
import logging

def isUrl(url: str):
    """
    判断是否是网址
    @param url: 网址字符串
    @return: 布尔值
    """
    return url.startswith("http://") or url.startswith("https://")

def joinUrl(*urls):
    """
    拼接网址
    @param urls: 网址
    @return: 拼接结果
    """
    from urllib.parse import urljoin
    data: str = ""
    for i in urls:
        data = urljoin(data, i)
    return data

def getUrl(url: str, header=None, timeout: int | tuple = (5, 10), times: int = 5):
    """
    可重试的get请求
    @param url: 链接
    @param header: 请求头
    @param timeout: 超时
    @param times: 重试次数
    @return:
    """
    import requests
    logging.info(f"正在Get请求{url}的信息！")
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "http://" + url
    for i in range(times):
        try:
            response = requests.get(url, headers=header, stream=True, timeout=timeout)
            logging.info(f"Get请求{url}成功！")
            return response
        except Exception as ex:
            logging.warning(f"第{i + 1}次Get请求{url}失败，错误信息为{ex}，正在重试中！")
            continue
    logging.error(f"Get请求{url}失败！")

def postUrl(url: str, json: dict, header=None, timeout: int | tuple = (5, 10), times: int = 5):
    """
    可重试的post请求
    @param url: 链接
    @param json: 发送数据
    @param header: 请求头
    @param timeout: 超时
    @param times: 重试次数
    @return:
    """
    import requests
    logging.info(f"正在Post请求{url}的信息！")
    if not url.startswith("https://") and not url.startswith("http://"):
        url = "http://" + url
    for i in range(times):
        try:
            response = requests.post(url, headers=header, json=json, timeout=timeout)
            logging.info(f"Post请求{url}成功！")
            return response
        except Exception as ex:
            logging.warning(f"第{i + 1}次Post请求{url}失败，错误信息为{ex}，正在重试中！")
            continue
    logging.error(f"Post请求{url}失败！")

def getFileNameFromUrl(url: str):
    """
    从链接获取文件名
    @param url: 链接
    @return:
    """
    from urllib.parse import urlparse
    import os
    return os.path.basename(urlparse(url).path)

def singleDownload(url: str, path: str, exist: bool = True, force: bool = False, header: dict = REQUEST_HEADER):
    """
    下载文件
    @param url: 下载链接
    @param path: 下载后完整目录/文件名
    @param exist: 是否在已有文件的情况下下载（False时force无效）
    @param force: 是否强制下载（替换已有文件）
    @param header: 请求头
    @return:
    """
    import requests
    if not existPath(path):
        createDir(splitPath(path, 3))
    try:
        if isDir(path):
            path = joinPath(path, getFileNameFromUrl(url))
        if isFile(path) and not exist:
            logging.warning(f"由于文件{path}已存在，自动跳过单线程下载！")
            return False
        if exist and not force:
            path = addRepeatSuffix(path)
        logging.info(f"正在单线程下载文件{url}到{path}！")
        response = requests.get(url, headers=header, stream=True)
        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logging.info(f"已将文件{url}单线程下载到到{path}！")
        return path
    except Exception as ex:
        logging.error(f"单线程下载文件{url}到{path}失败，报错信息：{ex}！")
        return False

