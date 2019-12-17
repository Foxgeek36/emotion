# coding:utf-8
import time, datetime, os, traceback
from threading import Thread
from multiprocessing.pool import Pool
import requests
from lxml import etree  # 注意该模块的版本号及不同的使用方式
from ez_utils import fls_log, allot_list, err_check, Error

'''
[state]爬取指定类别图片
#进程中添加线程综合爬取
'''

flog = fls_log(log_name="emotion")
# Error = fls_log(log_name="error")  # 最好从一个独立的文件中做获取/ 可以在整个项目中的其他文件中做放置及记录 +--

# ----数量只是用来做测试/ 实际数量根据任务需求再做更改
# 进程数
PCNT = 1
# 线程数
TCNT = 2

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/77.0.3865.120 Safari/537.36 '
}

# 标签为'蘑菇头'的表情包存放目录
# SAVE_PATH = './download/mogutou'  # 做下载测试
SAVE_PATH = './out/蘑菇头'  # 实际下载保存及目标查询目录
# '蘑菇头'表情包链接地址
url_base = 'https://fabiaoqing.com/tag/detail/id/2/page/%s.html'
# 爬取页数的设置
URL_LIST = [url_base % i for i in range(1, 3)]  # 1 page/ 可以加多页数


def save_img(img_url, path, name):
    """
        下载并保存图片
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(os.path.join(path, name)):  # 对所下载图片做去重判断 +--
            with open(os.path.join(path, name), 'wb') as f:
                f.write(requests.get(img_url, headers=HEADERS, timeout=10).content)  # 写入二进制
    except Exception as e:
        print('Exception->', e)
        Error.log_error(traceback.print_exc())
        # 完善error日志记录
        # flog.log_info(">>>save-error:" + img_url)


def doWork(par1: str, par2: str = 'par2', par3: str = 'par3'):
    """
        爬取操作主函数
        :param par1: 待爬url
        :param par2: 备用参数
        :param par3: 备用参数
        :return:
    """

    flog.log_info("work>>>\t" + par1)
    # print('par1->', par1)
    try:
        # print('---1---')
        # https://fabiaoqing.com/tag/detail/id/2/page/1.html
        resp = requests.get(url=par1, headers=HEADERS, timeout=10)
        # print('text->', resp.text)

        # print('---2---')
        # 注意该模块版本号及其使用方式
        # html = etree.HTML(resp.content.decode('utf-8'))
        html = etree.HTML(resp.text)
        imgs = html.xpath('//div[@class="tagbqppdiv"]/a/img')  # list
        # imgs = html.xpath('//*[@id="bqb"]/div[2]/div[1]/a/img')  # list/ 直接从浏览器中copy出xpath路径/只选中了一个
        print('imgs->', len(imgs))  # 元素为<Element img at 0x1c280777e88>
        for r in imgs:
            img_url = r.xpath('@data-original')[0]  # pic url
            img_title = r.xpath('@title')[0].strip()  # pic desc
            file_name = img_title.split(' ')[0]  # 若无匹配则返回原内容
            if '-' in img_title:
                file_name = img_title.split('-')[0]
            if '_' in img_title:
                file_name = img_title.split('_')[0]
            save_img(img_url, SAVE_PATH, file_name + '.' + img_url.split('.')[-1])

    except Exception as e:
        print('Exception->', e)
        Error.log_error(traceback.print_exc())  # 注意此处与函数装饰器@err_check功能的差别 +--
        # 完善error日志记录
        # flog.log_info(">>>error:" + par1)


def run_multithread(id: str, workPars: list, threadsCnt: int):
    """
        进线程综合执行函数: 进程函数中添加线程
        :param id: 1 ->for count
        :param workPars: [1]
        :param threadsCnt: 6
    """
    # flog.log_info('当前进程任务:' + id + (" ".join(str(i) for i in workPars)))
    begin = 0
    # start = time.time()
    while True:
        _threads = []  # 子线程列表
        # 此处对接将urls做分组/ 意义在于使用线程做均匀匹配资源 +--
        urls = workPars[begin: begin + threadsCnt]  # [0:6] ->needless ->urls=workPars
        if not urls:
            break
        for i in urls:  # 单个进程中创建多个线程 +--
            t = Thread(target=doWork, args=(i,))
            _threads.append(t)

        # ----以下两处操作结合使用以达到多线程的目的/ 两处操作并不冲突 +++
        for t in _threads:
            t.setDaemon(True)  # 设置为守护线程/ 主程序执行完成子程序随即退出
            t.start()
        for t in _threads:
            # 与t.setDaemon(True)是否冲突? / 两处设置作用相反 +--
            t.join()
        # -------------------
        begin += threadsCnt
        # end = time.time()
        # flog.log_info(id + '当前进程耗时:%.2fs' % (end-start))


@err_check  # 装饰器
def mixed_process_thread_crawler(processorsCnt: int, threadsCnt: int):  # java式的变量类型设置
    """
        :param processorsCnt: 进程数=2
        :param threadsCnt: 线程数=6
        :return:
    """
    pool = Pool(processorsCnt)  # 进程池
    workPars = URL_LIST  # [1]/ 待爬url列表,此处为链接最后的页码/ 缩减形式
    url_groups = allot_list(workPars, processorsCnt)  # [[1]]->处理之后的图片url list
    flog.log_info("总任务组数:" + str(len(url_groups)))
    cnt = 0  # 用于计数
    for per in url_groups:
        cnt += 1
        pool.apply_async(run_multithread, args=(str(cnt), per, threadsCnt))  # 异步非阻塞
    pool.close()
    pool.join()


if __name__ == '__main__':
    # 01-带时间戳的日志记录
    # flog.log_info("START>>>" + datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S'))
    # 02-直接显示在终端的运行耗时
    start = time.time()
    mixed_process_thread_crawler(PCNT, TCNT)  # 2/ 6
    # flog.log_info("END>>>" + datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S'))
    end = time.time()
    print('>>>程序运行总耗时:%.2fs' % (end - start))
