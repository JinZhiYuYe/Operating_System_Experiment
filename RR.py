# -*- coding=utf-8 -*- 
# time = '2020/10/20 19:56'


class PCB_type:
    name = None  # 进程名
    state = None  # 进程状态  2：执行  1：就绪  0：阻塞
    cpu_time = None  # 运行需要的CPU时间（需要运行的时间片个数）


class Queue(object):
    """队列"""

    def __init__(self):
        self.__items = []

    def enqueue(self, pcb):
        self.__items.append(pcb)

    def dequeue(self):
        return self.__items.pop(0)

    def isEmpty(self):
        return not len(self.__items)

    def travle(self):
        for i in self.__items:
            print("           ", i.name, "    ", i.state, "      ", i.cpu_time)


class RR(object):

    def __init__(self):
        self.ready_queue = Queue()
        self.blocked_queue = Queue()
        self.use_cpu = 0
        self.unuse_cpu = 0

    def start_state(self):
        """读入假设数据，设置系统初始状态"""
        n = eval(input("输入就绪状态进程个数n:"))
        m = eval(input("输入阻塞状态进程个数m:"))

        # 生成就绪状态队列
        for i in range(n):
            p = PCB_type()
            ls = input("输入就绪进程名称和运行所需时间片：").split()
            p.name = ls[0]
            p.cpu_time = int(ls[1])
            p.state = 1
            self.ready_queue.enqueue(p)

        # 生成阻塞状态队列
        for i in range(m):
            p = PCB_type()
            ls = input("输入阻塞进程名称和运行所需时间片：").split()
            p.name = ls[0]
            p.cpu_time = int(ls[1])
            p.state = 0
            self.blocked_queue.enqueue(p)
        print("====================================")
        print("就绪进程   name  state  cpu_time")
        self.ready_queue.travle()
        self.dispath()

    def dispath(self):
        t = eval(input("输入t:"))
        """模拟调度"""
        print("===============")
        print("开始调度。。")
        i = 1
        while not self.ready_queue.isEmpty() or not self.blocked_queue.isEmpty():
            # 只要就绪队列和阻塞队列不空CPU就需要运转
            if not self.ready_queue.isEmpty():  # 就绪队列不空进行调度
                p = self.ready_queue.dequeue()
                p.state = 2
                print(f"时间片{i}  进程{p.name}调度")
                if i % t == 0 and not self.blocked_queue.isEmpty():  # 阻塞队列不空，每过t个时间片唤醒阻塞队列的队首进程
                    self.ready_queue.enqueue(self.blocked_queue.dequeue())
                self.use_cpu += 1   # CPU使用+1
                p.cpu_time -= 1    # 进程时间片-1
                if p.cpu_time == 0:
                    print(f"进程{p.name}完成")
                else:
                    self.ready_queue.enqueue(p)

            else:
                if i % t == 0 and not self.blocked_queue.isEmpty():
                    self.ready_queue.enqueue(self.blocked_queue.dequeue())
                self.unuse_cpu += 1  # 就绪队列已空，CPU空转+1
                print(f"时间片{i} cpu空转")
            i += 1
        self.calculate()

    def calculate(self):
        """计算CPU利用率"""
        print("CPU利用率: %f" % (self.use_cpu/(self.use_cpu+self.unuse_cpu)))


rr = RR()
rr.start_state()
