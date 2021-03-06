import requests
from lxml import html
import os
import time
from socket import timeout as socket_timeout


if not os.path.exists('F:ile'):
    os.mkdir('F:/ile')

def sleep_time():
    time.sleep(0.1)

def get_page_number(num):
    #构建函数，用来查找该页内所有图片集的详细地址。目前一页包含15组套图，所以应该返回包含15个链接的序列。
    url = 'http://www.mmjpg.com/home/' + num
    #构造每个分页的网址
    response = requests.get(url).content
    #调用requests库，获取二进制的相应内容。注意，这里使用.text方法的话，下面的html解析会报错，大家可以试一下。这里涉及到.content和.text的区别了。简单说，如果是处理文字、链接等内容，建议使用.text，处理视频、音频、图片等二进制内容，建议使用.content。
    selector = html.fromstring(response)
    #使用lxml.html模块构建选择器，主要功能是将二进制的服务器相应内容response转化为可读取的元素树（element tree）。lxml中就有etree模块，是构建元素树用的。如果是将html字符串转化为可读取的元素树，就建议使用lxml.html.fromstring，毕竟这几个名字应该能大致说明功能了吧。
    urls = []
    #准备容器
    for i in selector.xpath("//ul/li/a/@href"):
    #利用xpath定位到所有的套图的详细地址
        urls.append(i)
        #遍历所有地址，添加到容器中
    return urls
    #将序列作为函数结果返回

def get_image_title(url):
	#现在进入套图详细页面，把套图标题和图片总数提取出来
	response = requests.get(url).content
	selector = html.fromstring(response)
	image_title = selector.xpath("//h2/text()")[0]
	#xpath返回结果都是序列，所以要使用[0]进行定位
	return image_title

def get_image_amount(url):
    #这里就相当于重复造轮子了，因为基本的代码逻辑跟上一个函数一模一样。想要简单的话就是定义一个元组，然后把获取标题、获取链接、获取图片总数的3组函数的逻辑揉在一起，最后将结果作为元组输出。不过作为新手教程，还是以简单易懂为好吧。想挑战的同学可以试试写元组模式
    response = requests.get(url).content
    selector = html.fromstring(response)
    image_amount = selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
    # a标签的倒数第二个区块就是图片集的最后一页，也是图片总数，所以直接取值就可以
    return image_amount

def get_image_detail_website(url):
    #这里还是重复造轮子。
    response = requests.get(url).content
    selector = html.fromstring(response)
    image_detail_websites = []
    image_amount = selector.xpath("//div[@class='page']/a[last()-1]/text()")[0]
    #这里重复构造变量，主要是为了获取图片总数。更高级的方法是使用函数间的传值，但是我忘了怎么写了，所以用了个笨办法。欢迎大家修改
    #构建图片具体地址的容器
    for i in range(int(image_amount)):
        image_detail_link = '{}/{}'.format(url, i+1)
        response = requests.get(image_detail_link,timeout = 500).content
        sel = html.fromstring(response)
        image_download_link = sel.xpath("//div[@class='content']/a/img/@src")[0]
        #这里是单张图片的最终下载地址
        image_detail_websites.append(image_download_link)
    return image_detail_websites

def download_image(image_title,image_detail_websites):
    	#将图片保存在本地
    num = 1
    amount = len(image_detail_websites)
    	#获取图片总数
    for i in image_detail_websites:
    	filename = '%s%s.jpg'%(image_title,num)
    	print('正在下载图片:%s第%s%s张,'%(image_title,num,amount))

        #文件保存在工作目录
        #if os.path.exist('F:/ile/'):


    	with open('F:/ile/'+filename,'wb') as f:
    		f.write(requests.get(i).content)

    	num+=1

if __name__ == '__main__':
    page_number = input('请输入需要爬起的页码:')

    try:
        for link in get_page_number(page_number):
            download_image(get_image_title(link),get_image_detail_website(link))
            #time.sleep(1)
    except Exception as e:#异常处理
        print(e)
    except socket_timeout:
            print("连接超时了，休息一下...")
            time.sleep(random.randint(15,25))

print('下载完毕')

#任务抓取失败，尝试多几次
#自定义写入日志
#不断新建文件夹自动爬取