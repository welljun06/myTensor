#coding=utf-8
import random as ran
import re
class Tensor(object):
    def __init__(self, ndim, shape, data):
        self.ndim = ndim #维数
        self.shape = shape #形状
        self.data = data #数据
#随机生成
def random(x, index):
    if index >= len(x):
        return ran.randint(0,9)
    else:
        temp = []
        for i in range(0, x[index]):
            temp.append(random(x, index+1))
        return temp
#随机生成1
def one(x, index):
    if index >= len(x):
        return 1
    else:
        temp = []
        for i in range(0, x[index]):
            temp.append(one(x, index+1))
        return temp
#随机生成0
def zero(x, index):
    if index >= len(x):
        return 0
    else:
        temp = []
        for i in range(0, x[index]):
            temp.append(zero(x, index+1))
        return temp

# 生成特定格式tensor
def create_tensor_by_structure(x, data, index):
    if index >= len(x):
        c = int(data[0])
        data.pop(0)
        return c
    else:
        temp = []
        for i in range(0, x[index]):
            temp.append(create_tensor_by_structure(x, data, index+1))
        return temp

# 分析指定结构字符串shape
def analyze_structure(str):
    str = "".join(str.split(" "))
    shape = []
    count = 1
    # 计算维度数和最后一维个数
    for c in str:
        if c == '[':
            shape.append(0)
        elif c == ',':
            count += 1
        elif c == ']':
            shape[len(shape) - 1] = count
            break
    print(shape)
    print(str)
    stack = []
    i = 0
    for c in str:
        if c == '[':
            stack.append(c)
        elif c == ']':
            stack.pop()
            if len(stack) > 0:
                shape[len(stack)-1] += 1
    print(shape)
    return shape

#解析成tensor
def analyze_tensor(tensor, temp_list):
    if isinstance(tensor, list):
        # print('yes')
        temp_list.append(len(tensor))
        analyze_tensor(tensor[0], temp_list) 
    return temp_list

# 解析输入生成语句
def analyse_statement(str):
    str_split = str.split('=') # 将输入语句按照等号划分两半
    i = 0
    # 去除分割后数组前后多余空格
    for i in range(len(str_split)):
        str_split[i] = str_split[i].strip()
    # 如果是生成自定义结构，等号后面第一个字符为'['
    if str_split[1][0] == '[':
        print('[生成自定义结构] 变量名：{0}, 参数：{1}'.format(str_split[0], str_split[1]))
        shape = analyze_structure(str_split[1])
        data = "".join(re.split(r"\[|\]| ", str_split[1])) # 去除'[] '
        print('参数：{0}'.format(data))
        data = data.split(',')
        globals()[str_split[0]] = init_by_data(shape, data) # 全局
    # 如果是其他生成
    else:
        if str_split[1][0] == 'r':   
            para = str_split[1][5:-1]
            print(para)
            print('[随机生成] 变量名：{0}, 形状：{1}'.format(str_split[0], para))
        elif str_split[1][0] == 'o':
            para = str_split[1][4:-1]
            print(para)
            print('[随机生成] 变量名：{0}, 形状：{1}'.format(str_split[0], para))
        elif str_split[1][0] == 'z':
            para = str_split[1][5:-1]
            print(para)
            print('[随机生成] 变量名：{0}, 形状：{1}'.format(str_split[0], para))
        else:
            print('输入错误')
        shape = para.strip("()").split(',') # 取出参数并存为list
        i = 0
        for i in range(len(shape)): # 去除多余空格并转换为int
             shape[i] = int(shape[i].strip()) 
        
        if str_split[1][0] == 'r': 
            globals()[str_split[0]] = init_random(shape)
        elif str_split[1][0] == 'o':
            globals()[str_split[0]] = init_one(shape)
        elif str_split[1][0] == 'z':
            globals()[str_split[0]] = init_zero(shape)

def init_random(shape):
    return Tensor(len(shape), shape, random(shape, 0))

def init_one(shape):
    return Tensor(len(shape), shape, one(shape, 0))

def init_zero(shape):
    return Tensor(len(shape), shape, zero(shape, 0))

def init_by_data(shape, data):
    return Tensor(len(shape), shape, create_tensor_by_structure(shape, data, 0))

#解析tensor元素
def get_tensor_data(tensor):
    if isinstance(tensor, list):
        i = 0
        for i in range(len(tensor)):
            get_tensor_data(tensor[i])
    else:
        print(tensor)

# TODO: 加法
def add(tensor1, tensor2, tensor3):
    if isinstance(tensor1, list):
        i = 0
        for i in range(len(tensor1)):
            add(tensor1[i], tensor2[i], tensor3)
    else:
        tensor3.append(tensor1 + tensor2)
    return tensor3
# 加法包装
def add_tensor(tensor1, tensor2):
    data = add(x,y,[])
    shape = analyze_tensor(x, [])
    return create_tensor_by_structure(shape, data, 0)

# TODO: 算术操作


# 测试
# a = [3, 3]
# z = [[7, 9, 8], [4, 3, 2], [0, 1, 7]]
# b = init_random(a)
# c = init_one(a)
# d = init_zero(a)
# print(b.data)
# print(c.data)
# print(d.data)
# print(b.ndim)
# print(analyze_tensor(b.data, []))
# str = "test1 = [1,2,3]"
# analyse_statement(str)
# a = "".join(re.split(r"\[|\]", a))
# str1 = "test1 = [[[1, 2], [4, 5], [7, 8]]]"
# analyse_statement(str1)
# print("test1:{0}".format(test1.data))

# str = "x = one((2,2))"
# analyse_statement(str)
# print("x:{0}".format(x.data))

x = [3, 3]
y = [4, 4]
z = add_tensor(x,y)
print(z)
