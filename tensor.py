#coding=utf-8
import random as ran
import re
import copy
class Tensor(object):
    def __init__(self, ndim, shape, data, dtype):
        self.ndim = ndim #维数
        self.shape = shape #形状
        self.data = data #数据
        self.dtype = dtype #类型
def random(x, index):
    # 随机生成
    if index >= len(x):
        return ran.randint(0,9)
    else:
        temp = []
        for i in range(0, x[index]):
            temp.append(random(x, index+1))
        return temp

def init_tensor(shape, index, data):
    #抽象生成函数
    if index >= len(shape):
        return data
    else:
        temp = []
        for i in range(0, shape[index]):
            temp.append(init_tensor(shape, index+1, data))
        return temp

def create_tensor_by_structure(shape, data, index):
    # 根据data和shape生成特定格式tensor
    if index >= len(shape):
        c = int(data[0])
        data.pop(0)
        return c
    else:
        temp = []
        for i in range(0, shape[index]):
            temp.append(create_tensor_by_structure(shape, data, index+1))
        return temp

def analyze_structure(str):
    # 分析指定结构字符串shape
    str = "".join(str.split(" "))
    shape = []
    count = 1 # 最后一维个数
    # 计算维度数和最后一维个数
    for c in str:
        if c == '[':
            shape.append(0)
        elif c == ',':
            count += 1
        elif c == ']':
            shape[len(shape) - 1] = count
            break
    stack = []
    i = 0
    for c in str:
        if c == '[':
            stack.append(c)
        elif c == ']':
            stack.pop()
            if len(stack) > 0:
                shape[len(stack)-1] += 1
    # 修正shape
    for i in range(1,len(shape)-1):
        shape[len(shape)-1 - i] = shape[len(shape) - 1 - i] / shape[len(shape) - 2 - i]
    print("分析得到当前字符串形状:{0}".format(shape))
    return shape

def analyze_tensor(tensor, shape):
    #分析结构返回shape
    if isinstance(tensor, list):
        shape.append(len(tensor))
        analyze_tensor(tensor[0], shape) 
    return shape

def analyse_statement(str):
    # 解析输入生成语句
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
            print('[rand] 变量名：{0}, 形状：{1}'.format(str_split[0], para))
        elif str_split[1][0] == 'o':
            para = str_split[1][4:-1]
            print('[one] 变量名：{0}, 形状：{1}'.format(str_split[0], para))
        elif str_split[1][0] == 'z':
            para = str_split[1][5:-1]
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
    return Tensor(len(shape), shape, random(shape, 0), "Tensor")

def init_one(shape):
    return Tensor(len(shape), shape, init_tensor(shape, 0, 1), "Tensor")

def init_zero(shape):
    return Tensor(len(shape), shape, init_tensor(shape, 0, 0), "Tensor")

def init_by_data(shape, data):
    return Tensor(len(shape), shape, create_tensor_by_structure(shape, data, 0), "tensor")

def init_by_list(data):
    shape = analyze_tensor(data, [])
    return Tensor(len(shape), shape, data, "tensor")

#遍历tensor元素
def get_tensor_data(tensor, data):
    if isinstance(tensor, list):
        for i in range(len(tensor)):
            get_tensor_data(tensor[i], data)
    else:
        data.append(tensor)
    return data


def cal_tensor(tensor1, tensor2, tensor3, operator):
    # 统一操作加减点乘（相同维度）
    if isinstance(tensor1, list):
        i = 0
        for i in range(len(tensor1)):
            cal_tensor(tensor1[i], tensor2[i], tensor3, operator)
    else:
        if operator == '+':
            tensor3.append(tensor1 + tensor2)
        elif operator == '-':
            tensor3.append(tensor1 - tensor2)
        elif operator == '.':
            tensor3.append(tensor1 * tensor2)
    return tensor3

def operate_tensor(tensor1, tensor2, operator):
    # 运算包装
    # 判断维度时候为0
    if not isinstance(tensor1, list):
        temp = tensor1
        tensor1 = []
        tensor1.append(temp)
    if not isinstance(tensor2, list):
        temp = tensor2
        tensor2 = []
        tensor2.append(temp)
    shape_x = analyze_tensor(tensor1, [])
    shape_y = analyze_tensor(tensor2, [])
    if len(shape_x) < len(shape_y): # 交换
        shape_x, shape_y = shape_y, shape_x
        tensor1, tensor2 = tensor2, tensor1
    print('tensor1: {1} shape: {0}'.format(shape_x, tensor1))
    print('tensor2: {1} shape: {0}'.format(shape_y, tensor2))
    # 如果维度相同
    if shape_x == shape_y: 
        print("【执行运算...】\ntensor1:{1}\ntensor2:{0}\noperator:{2}".format(tensor2,tensor1,operator))
        data = cal_tensor(tensor1, tensor2, [], operator)
    else:
        # 从尾部开始比较
        for i in range(len(shape_y)):
            if shape_x[len(shape_x) - i - 1] != shape_y[len(shape_y) - i - 1]:
                if shape_x[len(shape_x) - i - 1] == 1:
                    # print("【存在1拓展...】")
                    shape_x[len(shape_x) - i - 1] = shape_y[len(shape_y) - i - 1]
                    shape_temp = shape_x[0:len(shape_x) - i]
                    # print("更新shape_1: {0}".format(shape_x))
                    # 取得当前为1的内容
                    tensor_temp = tensor1
                    for j in range(len(shape_x) - i):
                        tensor_temp = tensor_temp[0]
                    tensor1 = init_tensor(shape_temp, 0, tensor_temp)
                    # print("更新tensor1: {0}".format(tensor1))
                elif shape_y[len(shape_y) - i - 1] == 1:
                    # print("【存在1拓展...】")
                    shape_y[len(shape_y) - i - 1] = shape_x[len(shape_x) - i - 1]
                    shape_temp = shape_y[0:len(shape_y) - i]
                    # print("更新shape_2: {0}".format(shape_y))
                     # 取得当前为1的内容
                    tensor_temp = tensor2
                    for j in range(len(shape_y) - i):
                        tensor_temp = tensor_temp[0]
                    tensor2 = init_tensor(shape_temp, 0, tensor_temp)
                    # print("更新tensor2: {0}".format(tensor2))
                else:
                    print("broadcasting failed!")
                    return
        # 确定新shape
        if len(shape_x) != len(shape_y):
            # print("【拓展维度...】")
            # 拓展tensor2
            shape = shape_x[0:(len(shape_x) - len(shape_y))]
            tensor2 = init_tensor(shape, 0, tensor2)
            # print('更新shape_2:{0}\n更新tensor2:{1}'.format(shape_x, tensor2))
        print("【执行运算...】\ntensor1:{1}\ntensor2:{0}\noperator:{2}".format(tensor2,tensor1,operator))
        data = cal_tensor(tensor1, tensor2, [], operator)
        # print("data:{0}".format(data))
    result = create_tensor_by_structure(analyze_tensor(tensor1, []), data, 0)
    print("【结果】：{0}".format(result))
    return result

def tra_tensor(tensor_x, tensor_y, result):
    # 叉乘底层
    temp = [0]
    if isinstance(tensor_x, list):   
        for i in range(len(tensor_x)):
            if isinstance(tensor_x[i], list):
                tra_tensor(tensor_x[i], tensor_y, result)
            else:
                temp_one = operate_tensor(tensor_x[i], tensor_y[i],'.')
                temp = operate_tensor(temp_one, temp, '+')
        if temp != [0]:
            result.append(temp)
    return result

def dot(tensor_x, tensor_y):
    # 叉乘外层
    print("tensor_x:{0}\ntensor_y:{1}".format(tensor_x, tensor_y))
    shape_x = analyze_tensor(tensor_x, [])
    shape_y = analyze_tensor(tensor_y, [])
    if shape_x[-1] == shape_y[0]:
        # x最底层与y顶层相乘
        # 遍历所有x底层
        result = tra_tensor(tensor_x, tensor_y, [])
        shape_z = analyze_tensor(result, [])
        print("shape_x:{0}\nshape_y;{1}\nshape_z:{2}".format(shape_x, shape_y, shape_z))
        print("【叉乘结果】:{0}".format(result))
    else:
        print("输入不合法！")

def tensor_begin(begin, tensor):
    # 定位到开始位置
    for i in range(len(begin)):
        # print(begin[i])
        if begin[i] != 0:
            tensor = tensor[begin[i]:]
            if i != 0:
                tensor = tensor[0]
    return tensor

def tensor_size(shape, tensor, index, list):
    # 按照size遍历tensor
    if index >= len(shape):
        list.append(tensor)
    else:
        for i in range(0, shape[index]):
            print("tensor[i]:{0},index:{1}".format(tensor[i], index))
            tensor_size(shape, tensor[i], index + 1, list)
    return list
            
def tensor_slice(inputs, begin, size):
    # begin
    inputs = tensor_begin(begin, inputs)
    print(inputs)
    result_data = tensor_size(size, inputs, 0, [])
    result = init_by_data(size, result_data)
    print(result.data)


# 测试
# 1.----
# shape = [3, 3]
# b = init_random(shape)
# c = init_one(shape)
# d = init_zero(shape)
# print("[rand]\nb_ndim:{0}, b_shape:{1}, b_dtype:{2}\nb_data:{3}".format(b.ndim, b.shape, b.dtype, b.data))
# print("[one]\nc_ndim:{0}, c_shape:{1}, c_dtype:{2}\nc_data:{3}".format(c.ndim, c.shape, c.dtype, c.data))
# print("[zero]\nd_ndim:{0}, d_shape:{1}, d_dtype:{2}\nd_data:{3}".format(d.ndim, d.shape, d.dtype, d.data))

# 2.----
# z = [[7, 9, 8], [4, 3, 2], [0, 1, 7]]
# a = init_by_list(z)
# print("[data]\na_ndim:{0}, a_shape:{1}, a_dtype:{2}\na_data:{3}".format(a.ndim, a.shape, a.dtype, a.data))

# 3.----
# str1 = "test1 = [[[1, 2], [4, 5], [7, 8]]]"
# analyse_statement(str1)
# print("test1:{0}".format(test1.data))
# print("--------------------------------")
# str2 = "test2 = one((2,2))"
# analyse_statement(str2)
# print("test2:{0}".format(test2.data))

# 4.----
x = [[1, 2], [3, 4]]
y = [5, 6]
z = operate_tensor(x,y,'.')
print("result:{0}".format(z))

# 5.----
x = [[1,2],[3,4]]
y = [[[5,6],[7, 8],[9,10]],[[5,6],[7, 8],[9,10]]] 
dot(x, y)

# t = [[[1, 1, 1], [2, 2, 2]],[[3, 3, 3], [4, 4, 4]],[[5, 5, 5], [6, 6, 6]]]
# begin = [1, 0, 0]
# size = [1, 1, 3]
# tensor_slice(t, begin, size)