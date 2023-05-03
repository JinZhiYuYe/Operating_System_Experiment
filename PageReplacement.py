# -*- coding=utf-8 -*- 
# time = '2020/11/10 17:56'
import random

random.seed(2019)


class PageReplacement(object):

    def __init__(self):
        self.order_list = []
        self.user_capacity = 29   # 4-32+1页=29页
        self.page_miss = 0
        self.order_sum = 320

    def start_status(self):
        ret = []
        count = 320
        while count > 0:
            count -= 4
            m = random.randint(0, 319)
            pre = random.randint(0, m + 1)
            next = random.randint(pre + 2, 319)
            ret.extend([m + 1, pre, pre + 1, next])
        for i in ret:


            self.order_list.append(i//10)
        print("所有指令：", self.order_list)
        print("\n")

    def OPT(self):
        """
        最佳置换算法
        :return:命中率
        """
        order_user = []         # 用户内存
        for index, page in enumerate(self.order_list):
            if order_user.__len__() == self.user_capacity:   # 用户内存容量已满，需要进行页面置换

                if page not in order_user:   # 页面不在用户内存中，发生置换操作
                    self.page_miss += 1   # 页面失效次数+1
                    max_gap = 0
                    replacement_page = None
                    for page_u in order_user:  # 查找最长时间不被访问的页面
                        for i in range(index+1, self.order_sum):

                            if page_u == self.order_list[i]:
                                # 找到第一个相同页，与最大距离比较
                                if i-index+1 > max_gap:
                                    max_gap = i-index+1
                                    replacement_page = page_u
                                break

                            if i + 1 == self.order_sum and page_u != self.order_list[i]:
                                # 当前页面以后不会再访问
                                max_gap = self.order_sum + 1
                                # print(max_gap)
                                replacement_page = page_u

                    if replacement_page:
                        print("置换前的用户内存：", order_user)
                        print("需要置换出的页面：", replacement_page)
                        print("需要置换进的页面：", page)
                        order_user.remove(replacement_page)   # 取出最长时间不被访问的页面
                        order_user.append(page)
                        print("置换后的用户内存：", order_user)
                        print("="*50)
                    else:
                        # 当前用户内存中的所有页面之后都不会再次访问，默认选择一个页面进行置换
                        order_user.pop()
                        order_user.append(page)

            elif order_user.__len__() < self.user_capacity:  # 用户内存未满
                if page not in order_user:
                    self.page_miss += 1  # 页面失效次数+1
                    order_user.append(page)

        return 1-(self.page_miss/self.order_sum)

    def FIFO(self):
        """
        先进先出置换算法
        :return:命中率
        """
        order_user = []  # 队列

        for page in self.order_list:
            if order_user.__len__() == self.user_capacity:  # 用户内存容量已满，需要进行页面置换
                if page not in order_user:  # 页面不在用户内存中，发生置换操作
                    self.page_miss += 1  # 页面失效次数+1
                    order_user.pop(0)  # 置换出最先进入用户内存的页面
                    order_user.append(page)

            elif order_user.__len__() < self.user_capacity:    # 用户内存未满
                if page not in order_user:
                    self.page_miss += 1  # 页面失效次数+1
                    order_user.append(page)
        return 1-(self.page_miss/self.order_sum)

    def LRU(self):
        """
        最近最久未使用置换算法
        :return:命中率
        """
        order_user = []  # 堆栈
        for page in self.order_list:

            if order_user.__len__() == self.user_capacity:  # 用户内存容量已满，需要进行页面置换
                if page not in order_user:
                    order_user_tmp = []
                    for i in range(len(order_user)):
                        if i == self.user_capacity-1:
                            order_user.pop()
                            for j in range(len(order_user_tmp)):
                                order_user.append(order_user_tmp.pop())
                            order_user.append(page)
                        else:
                            order_user_tmp.append(order_user.pop())

                else:
                    # 内存中已存在改页面，需要将该页面放在栈顶（表示最近访问）
                    order_user_tmp = []
                    for i in range(len(order_user)):
                        page_u = order_user.pop()
                        if page_u != page:
                            order_user_tmp.append(page_u)
                        elif page_u == page:
                            for j in range(len(order_user_tmp)):
                                order_user.append(order_user_tmp.pop())
                            order_user.append(page)
                            break

            elif order_user.__len__() < self.user_capacity:  # 用户内存未满
                if page not in order_user:
                    self.page_miss += 1  # 页面失效次数+1
                    order_user.append(page)
                else:
                    # 内存中已存在改页面，需要将该页面防止栈顶（表示最近访问）
                    order_user_tmp = []
                    for i in range(len(order_user)):
                        page_u = order_user.pop()
                        if page_u != page:
                            order_user_tmp.append(page_u)
                        elif page_u == page:
                            for j in range(len(order_user_tmp)):
                                order_user.append(order_user_tmp.pop())
                            order_user.append(page)
                            break
        return 1 - (self.page_miss / self.order_sum)


if __name__ == '__main__':
    pr = PageReplacement()
    pr.start_status()

    print("最佳置换算法（OPT）：", pr.OPT())
    print("先进先出算法（FIFO）：", pr.FIFO())
    print("最近最少使用（LRU）：", pr.LRU())
