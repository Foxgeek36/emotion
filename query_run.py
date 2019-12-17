# coding:utf8
import os, sys
import jieba

'''
[state]结果搜索功能
#查询指定关键词的图片
-使用命令:python query_run.py 蘑菇头 科普
'''

ROOT_DIR = './out'  # 下载保存图片的目录


def search_level_first(path: str, w: str) -> list:
    """
	    遍历第一层文件夹,获取一级分类
	    :param path: 存放目录
	    :param w: 一级关键词
	    :return: 返回符合匹配条按键的一级分类目录
    """
    return [os.path.join(path, i) for i in os.listdir(path) if w in i]


def search_level_all(path: str, w: str) -> list:
    """
	    遍历path下所有子文件
	    @param: path    磁盘路径地址/ 一级分类地址
	    @param: w       关键词检索.子文件名包含w的会return
    """
    rs = []
    # 固定格式: root->当前目录/ files->目录下文件
    for root, dirs, files in os.walk(path):
        for file in files:
            if w in file:
                rs.append(os.path.join(root, file))  # 存储文件路径
    return rs


def main(w1, w2, limit):
    """
	    主入口,搜索特定关键词的表情包
	    :param w1: 一级分类/ '蘑菇头'
	    :param w2: 关键词/ '科普'
	    :param limit: 回显条数
	    :return:
    """
    rs = []
    f1 = search_level_first(ROOT_DIR, w1)  # 在下载地址中查找一级目录 +--
    for r in f1:
        # 先从一级分类里找到符合条件的关键词
        for rr in search_level_all(r, w2):
            if len(rs) >= limit:
                # 达到limit条数限制,break
                break
            rs.append(rr)
    if len(rs) < limit:
        # 当通过w1查询不到的话,再延伸到保存图片的所有目录下
        # 结巴分词的使用
        for w in jieba.cut(w2, cut_all=False):
            for rr in search_level_all(ROOT_DIR, w):
                if len(rs) >= limit:
                    # 达到limit条数限制,break
                    break
                rs.append(rr)
    return rs


# 显示条数
LIMIT = 5
# 返回值
r = []
# 关键词数量计算的是python后面以' '做分隔的内容
# 执行命令格式为: python query_run.py 蘑菇头 科普/ 必须固定参数数量 +--
if len(sys.argv) == 3:
    r = main(sys.argv[1], sys.argv[2], LIMIT)
else:
    r = main('蘑菇头', '科普', LIMIT)

print('\n'.join(r))  # attention:将list中元素依次做隔行显示
