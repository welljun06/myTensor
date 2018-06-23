#coding=utf-8
import random as ran
import re
class Tensor(object):
    def __init__(self, ndim, shape, data):
        self.ndim = ndim #维数
        self.shape = shape #形状
        self.data = data #数据
        # TODO:self.dtype = dtype #类型
#随机生成
def random(x, index):
    if index >= len(x):
        return ran.randint(0,9)
    else:
        temp = []
        for i in range(0, x[index]):
            temp.append(random(x, index+1))
        return temp
#抽象生成函数
def init_tensor(shape, index, data):
    if index >= len(shape):
            return data
    else:
        temp = []
        for i in range(0, shape[index]):
            temp.append(init_tensor(shape, index+1, data))
        return temp

# 生成特定格式tensor
def create_tensor_by_structure(shape, data, index):
    if index >= len(shape):
        c = int(data[0])
        data.pop(0)
        return c
    else:
        temp = []
        for i in range(0, shape[index]):
            temp.append(create_tensor_by_structure(shape, data, index+1))
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
            print('[rand] 变量名：{0}, 形状：{1}'.format(str_split[0], para))
        elif str_split[1][0] == 'o':
            para = str_split[1][4:-1]
            print(para)
            print('[one] 变量名：{0}, 形状：{1}'.format(str_split[0], para))
        elif str_split[1][0] == 'z':
            para = str_split[1][5:-1]
            print(para)
            print('[zero] 变量名：{0}, 形状：{1}'.format(str_split[0], para))
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
    return Tensor(len(shape), shape, init_tensor(shape, 0, 1))

def init_zero(shape):
    return Tensor(len(shape), shape, init_tensor(shape, 0, 0))

def init_by_data(shape, data):
    return Tensor(len(shape), shape, create_tensor_by_structure(shape, data, 0))

#遍历tensor元素
def get_tensor_data(tensor):
    if isinstance(tensor, list):
        i = 0
        for i in range(len(tensor)):
            get_tensor_data(tensor[i])
    else:
        print(tensor)

# 加法
def add(tensor1, tensor2, tensor3):
    if isinstance(tensor1, list):
        i = 0
        for i in range(len(tensor1)):
            add(tensor1[i], tensor2[i], tensor3)
    else:
        tensor3.append(tensor1 + tensor2)
    return tensor3
# 统一操作加减点乘（相同维度）
def cal_tensor(tensor1, tensor2, tensor3, operator):
    if isinstance(tensor1, list):
        i = 0
        for i in range(len(tensor1)):
            cal_tensor(tensor1[i], tensor2[i], tensor3, operator)
    else:
        if operator == '+':
            tensor3.append(tensor1 + tensor2)
        elif operator == '-':
            tensor3.append(tensor1 - tensor2)
        elif operator == '*':
            tensor3.append(tensor1 * tensor2)
    return tensor3
# 运算包装
def operate_tensor(tensor1, tensor2, operator):
    shape_x = analyze_tensor(tensor1, [])
    shape_y = analyze_tensor(tensor2, [])
    if len(shape_x) < len(shape_y): # 交换
        shape_x, shape_y = shape_y, shape_x
        tensor1, tensor2 = tensor2, tensor1
    print('tensor1: {1} shape: {0}'.format(shape_x, tensor1))
    print('tensor2: {1} shape: {0}'.format(shape_y, tensor2))
    # 如果维度相同
    if shape_x == shape_y: 
        print(True)
        data = cal_tensor(tensor1, tensor2, [], operator)
    else:
        # 从尾部开始比较
        for i in range(len(shape_y)):
            if shape_x[len(shape_x) - i - 1] != shape_y[len(shape_y) - i - 1]:
                print("broadcasting failed!")
                return
        # 确定新tensor2新shape
        shape = shape_x[0:(len(shape_x) - len(shape_y))]
        # 拓展tensor2
        print('拓展:shape:{0},tensor2:{1}'.format(shape, tensor2))
        tensor2 = init_tensor(shape, 0, tensor2)
        print("tensor1:{1}\ntensor2:{0}\noperator:{2}".format(tensor2,tensor1,operator))
        data = cal_tensor(tensor1, tensor2, [], operator)
        # print("data:{0}".format(data))
    return create_tensor_by_structure(analyze_tensor(tensor1, []), data, 0)

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


x = [1,2]
y = [[1, 2],[3, 4], [5, 6]]
z = operate_tensor(x,y,'+')
print("result:{0}".format(z))
# a = [1, 2]
# shape = [2, 2]
# z = init_tensor(shape, 0, a)
# print(z)