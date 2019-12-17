# coding=utf-8

src_list = [1, 2, 3, 4]
n = 2


def allot_list(src_list: list, n: int) -> list:
	"""
	    根据给定的组数,分配list给每一组-顺序分组
	    :param src_list: [1]->站内页数编码
	    :param n: 2/ 每n个分一组
	    :return:
    """
	print([src_list[i:i + n] for i in range(0, len(src_list), n)])

	return [src_list[i:i + n] for i in range(0, len(src_list), n)]


if __name__ == '__main__':
	allot_list(src_list, n)  # res=[[1, 2], [3, 4]]
