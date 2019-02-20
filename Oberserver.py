'''
观察者模式描述单个对象（发布者，又称为主持者或可观察者）与一个或多个对象（订阅者，又称为观察者）之间的发布—订阅关系。
当我们希望在一个对象（主持者/发布者/可观察者）发生变化时通知/更新另一个或多个对象的时候，通常会使用观察者模式。
例子：
1：社交网络 ： 如果你使用社交网络服务关联了另一个人，在关联的人更新某些内容时，你能收到相关通知
2：js事件驱动：比如onclick事件可以绑定鼠标点击，触发某个函数

代码示例

_data 值变动会调用基类notify方法，从而导致所有的观察者调用notify方法
'''


class Publisher:
    def __init__(self):
        #收集观察者/订阅者的列表
        self.observers = []

    def add(self, observer):

        if observer not in self.observers:
            self.observers.append(observer)

        else:
            print('Failed to add: {}'.format(observer))

    def remove(self, observer):

        try:
            self.observers.remove(observer)

        except ValueError:
            print('Failed to remove: {}'.format(observer))

    def notify(self):
        # 本函数作用是 使迭代器中的每一个观察者调用自身的notify方法，来做到更新观察者自身
        [o.notify(self) for o in self.observers]


class DefaultFormatter(Publisher):
    def __init__(self, name):
        # Publisher.__init__(self) 同下super函数同样效果
        super(DefaultFormatter, self).__init__()
        self.name = name
        # 初始变量
        self._data = 0

    def __str__(self):
        #实例打印时调用
        return "{}: '{}' has data = {}".format(type(self).__name__, self.name,
                                               self._data)

    @property
    def data(self):
        #装饰器使方法操作起来像一个变量一样获取值
        return self._data

    @data.setter
    def data(self, new_value):
        # 装饰器使方法操作起来像一个变量一样赋值
        try:
            self._data = int(new_value)
        except ValueError as e:
            print('Error: {}'.format(e))
        else:
            #没有报错情况下走这个分支
            self.notify()


class HexFormatter:
    def notify(self, publisher):
        print("{}: '{}' has now hex data = {}".format(type(self).__name__, publisher.name, hex(publisher.data)))


class BinaryFormatter:
    def notify(self, publisher):
        print("{}: '{}' has now bin data = {}".format(type(self).__name__,publisher.name, bin(publisher.data)))


def main():
    # 实例化一个具备有名字，有驱动的发布者 df
    df = DefaultFormatter('test1')
    print(df) # DefaultFormatter: 'test1' has data = 0
    print()
    # 实例化一个 订阅者hf
    hf = HexFormatter()
    # 将订阅者hf添加到df的影响范围列表中，从此时起， 如果df的data属性改变，那么hf对象就会调用notify方法
    df.add(hf)
    df.data = 3
    print(df) # HexFormatter: 'test1' has now hex data = 0x3 ，DefaultFormatter: 'test1' has data = 3
    print()
    # # 实例化一个 订阅者bf
    bf = BinaryFormatter()
    df.add(bf)
    # # 此时df已经有两个订阅者了
    df.data = 21 # HexFormatter: 'test1' has now hex data = 0x15 ，BinaryFormatter: 'test1' has now bin data = 0b10101
    print(df) #DefaultFormatter: 'test1' has data = 21
    print()
    df.remove(hf)
    df.data = 40 #BinaryFormatter: 'test1' has now bin data = 0b101000
    print(df)# DefaultFormatter: 'test1' has data = 40
    print()
    df.remove(hf) #Failed to remove: <__main__.HexFormatter object at 0x00000000027C79B0>
    df.add(bf) #Failed to add: <__main__.BinaryFormatter object at 0x00000000027C79E8>
    df.data = 'hello'  #Error: invalid literal for int() with base 10: 'hello'
    print(df) #DefaultFormatter: 'test1' has data = 40
    print()
    df.data = 15.8 #BinaryFormatter: 'test1' has now bin data = 0b1111
    print(df) #DefaultFormatter: 'test1' has data = 15
if __name__ == '__main__':
    main()