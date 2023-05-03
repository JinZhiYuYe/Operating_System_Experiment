# -*- coding=utf-8 -*- 
# time = '2020/11/3 20:53'


class FreeNode:
    """空闲内存"""
    length = None    # 分区长度
    address = None   # 分区起始地址


class BusyNode:
    """占用内存"""
    name = None
    length = None    # 分区长度
    address = None   # 分区起始地址


class WorstFit(object):
    """最坏适应"""
    def __init__(self):
        self.__free_link = []
        self.__busy_link = []

    def start(self):
        """设置初始状态"""

        # 自由链表
        p = FreeNode()
        p.address = 64
        p.length = 640 - 64
        self.__free_link.append(p)

        # 占用链表
        q = BusyNode()
        q.address = 0
        q.name = "S"
        q.length = 64    # OS系统本身占用64k
        self.__busy_link.append(q)

        print("初始状态：")
        for i in self.__free_link:
            print(f"    空闲区的地址：{i.address}    空闲容量：{i.length}")

        for i in self.__busy_link:
            print(f"    作业名称：{i.name}    占用首址：{i.address}   占用地址：{i.length}\n")

    def require_memo(self, name, require):
        """
        模拟内存分配
        :param name: 作业名称
        :param require: 所需内存
        :return:
        """
        free_node_max = self.__free_link.pop(0)  # 取出最大空闲区
        busy_node = BusyNode()
        busy_node.length = require
        busy_node.name = name
        busy_node.address = free_node_max.address
        self.__busy_link.append(busy_node)

        free_node_max.address = free_node_max.address + require
        free_node_max.length = free_node_max.length - require
        if free_node_max.length > 0:
            self.__free_link.append(free_node_max)
            # 自有链表排序
            self.__free_link.sort(key=lambda x: x.length, reverse=True)

    def free_memo(self, name):
        """
        模拟内存回收
        :param name: 作业名称
        :return:
        """
        for index, i in enumerate(self.__busy_link):
            if name == i.name:
                free_node = FreeNode()
                p = self.__busy_link.pop(index)
                free_node.length = p.length
                free_node.address = p.address
                self.__free_link.append(free_node)
                # 自有链表排序
                self.__free_link.sort(key=lambda x: x.length, reverse=True)

    def past(self, time):
        """
        模拟系统过了time时间
        :param time:
        :return:
        """
        print(f"t{time}时刻后：")
        pass

    def print_link(self):
        # """输出内存空闲情况"""
        # while self.__busy_link:
        for i in self.__free_link:
            print(f"    空闲区的地址：{i.address}    空闲容量：{i.length}")
        for i in self.__busy_link:
            print(f"    作业名称：{i.name}    占用首址：{i.address}   占用地址：{i.length}")
        print("\n")


if __name__ == '__main__':
    wf = WorstFit()
    wf.start()
    wf.past(1)
    wf.require_memo("A", 8)
    wf.require_memo("B", 16)
    wf.require_memo("C", 64)
    wf.require_memo("D", 124)
    wf.print_link()
    wf.past(2)
    wf.free_memo("C")
    wf.print_link()
    wf.past(3)
    wf.require_memo("E", 50)
    wf.print_link()
    wf.past(4)
    wf.free_memo("D")
    wf.print_link()

    # wf.past(5)
    # wf.require_memo("F", 124)
    # wf.print_link()
