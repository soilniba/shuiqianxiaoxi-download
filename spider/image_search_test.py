import requests
from PIL import Image
from io import BytesIO
from config import azure_api_key

# Bing Image Search API认证信息

headers = {"Ocp-Apim-Subscription-Key": azure_api_key}

# 要搜索的关键字
query = "双重曝光（Double Exposure）"
number = 2

# 发送搜索请求
url = f"https://api.bing.microsoft.com/v7.0/images/search?q={query}&count={number}"

response = requests.get(url, headers=headers)

# 解析返回的JSON数据
data = response.json()
if "value" in data:
    # 获取所有图片链接
    image_urls = [item["contentUrl"] for item in data["value"]]
    
    # 加载和显示所有图片
    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.show()
else:
    print("No image found.")
