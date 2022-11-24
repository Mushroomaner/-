import requests #爬取模块
import re       #正则匹配模块
import json     #json解析模块
import pprint   #格式化输出模块



def get_response(html_url):
    """发送请求,获取响应体"""
    headers = {
        'referer': 'https://www.bilibili.com/',
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
    }
    response = requests.get(url=html_url,headers=headers)
    print("视频解析中......")
    return response

def get_video_info(html_url):
    """get到video的内容"""
    response = get_response(html_url)
    title = re.findall('<title data-vue-meta="true">(.*?)_哔哩哔哩bilibili',response.text)[0]
    html_data = re.findall('<script>window.__playinfo__=(.*?)</script>',response.text)[0]
    #   正则表达式匹配出来的数据 是列表 [0]是索引取0 取出列表里面的内容 字符串
    #   像json数据 把字符串转成json字典数据
    json_data = json.loads(html_data)
    #   防盗链的作用： 告诉服务器   我们发送的请求的url地址是从哪里过来的
    #   数据解析    json解析  键值对取值
    audio_url = json_data['data']['dash']['audio'][0]['base_url']
    video_url = json_data['data']['dash']['video'][0]['base_url']
    video_info = [title,audio_url,video_url]
    return video_info

def save(title,audio_url,video_url):
    """保存数据到本地"""
    # 音频的二进制数据  response.content 获取响应体的二进制内容
    audio_content = get_response(audio_url).content
    # 视频的二进制
    video_content = get_response(video_url).content
    with open(title + '.mp3', mode='wb') as f:
        f.write(audio_content)
    with open(title + '.mp4', mode='wb') as f:
        f.write(video_content)

url = input("请输入视频的url地址：")
video_info = get_video_info(url)
save(video_info[0],video_info[1],video_info[2])
print("保存完毕")