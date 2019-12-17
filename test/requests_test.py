# coding=utf-8
import requests
from lxml import etree

par1 = 'https://fabiaoqing.com/tag/detail/id/2/page/1.html'
HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
	              'Chrome/77.0.3865.120 Safari/537.36 '
}

try:
	resp = requests.get(par1, headers=HEADERS, timeout=(5, 10))
	# html = etree.HTML(resp.content.decode('utf-8'))  # Element对象: <Element html at 0x1b091e96788>
	# html = etree.HTML(resp.text)  # <Element html at 0x293a128e788>
	# ---------
	html = resp.text  # 输出页面解析的html文本内容
	# html = resp.content.decode('utf-8')  # 上下两种方式所得结果一致/ 该方式包含对图片、音频、视频内容的处理
	print('html->', html)

	# h = html.xpath('//div[@class="tagbqppdiv"]/a/img')[0]  # <Element img at 0x2c7fa51e748>
	# print('h->', h)

except Exception as e:
	print('Exception->', e)
