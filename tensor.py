#coding=utf-8
import random as ran
import re
import copy
class Tensor(object):
    def __init__(self, ndim, shape, data):
        self.ndim = ndim #维数
        self.shape = shape #形状
        self.data = data #数据
        # TODO:self.dtype = dtype #类型
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
    # 生成特定格式tensor
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
    print("tensor:{0}".format(str))
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
    print("分析当前字符串形状:{0}".format(shape))
    return shape

def analyze_tensor(tensor, shape):
    #分析结构返回shape
    if isinstance(tensor, list):
        # print('yes')
        shape.append(len(tensor))
        analyze_tensor(tensor[0], shape) 
    return shape

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
def get_tensor_data(tensor, data):
    if isinstance(tensor, list):
        for i in range(len(tensor)):
            get_tensor_data(tensor[i], data)
    else:
        data.append(tensor)
    return data

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
        elif operator == '.':
            tensor3.append(tensor1 * tensor2)
    return tensor3
# 运算包装
def operate_tensor(tensor1, tensor2, operator):
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

def cal_one_index(dgree, value):
    # 计算下标
    result = 0
    for i in range(len(dgree)):
        result += dgree[i] * value[i]
    return result

def cal_dot(shape, index, dgree, list):
    # 递归计算dgree 
    if index >= len(shape):
        print("当前dgree:{0} ".format(dgree))
        new_dgree = copy.copy(dgree) # 注意此处要使用复制
        list.append(new_dgree)
    else:
        for i in range(0,(shape[index])):
            dgree[index] = i
            cal_dot(shape, index + 1, dgree, list)
    return list

def cal_dgree_value(shape):
    # 计算dgree对应value
    value = init_one([len(shape)]).data
    for i in range(1, len(value)):
        print(value[-i - 1])
        print(value[-i], shape[-i])
        value[-i - 1] = value[-i] * shape[-i]
        print(value[-i], shape[-i])
    print("value:{0}".format(value))
    return value
def cal_by_expression(dgree_list, tensor_x, tensor_y):
    shape_x = analyze_tensor(tensor_x, [])
    shape_y = analyze_tensor(tensor_y, [])
    data_x = get_tensor_data(tensor_x, [])
    data_y = get_tensor_data(tensor_y, [])
    value_x = cal_dgree_value(shape_x)
    value_y = cal_dgree_value(shape_y)
    for dgree in dgree_list:
        dgree_x = dgree[:len(shape_x)-1]
        dgree_y = dgree[len(shape_x)-1:]
        dgree_x.append(0)
        dgree_y.insert(0,0)
        #计算一个块的结果值
        for i in range(0, shape_y[0]):
            dgree_x[-1] = i
            dgree_y[0] = i
            # 取得当前dgree对应的下标
            index_x = cal_one_index(dgree_x, value_x)
            index_y = cal_one_index(dgree_y, value_y)
            print(data_x[index_x], data_y[index_y])
        print("-----")
    pass
def dot(tensor_x, tensor_y):
    # 叉乘外层
    print("tensor_x:{0}\ntensor_y:{1}".format(tensor_x, tensor_y))
    shape_x = analyze_tensor(tensor_x, [])
    shape_y = analyze_tensor(tensor_y, [])
    print("shape_x:{0}\nshape_y;{1}".format(shape_x, shape_y))
    if shape_x[-1] == shape_y[0]:
        shape_z = shape_x[:-1] + shape_y[1:]
        z = init_zero(shape_z)
        data_z = get_tensor_data(z.data, [])
        
        dgree_z = init_tensor([len(shape_z)], 0, 0)
        
        value_z = cal_dgree_value(shape_z)
        list_z = cal_dot(shape_z, 0, dgree_z, [])
        # 根据公式计算结果
        cal_by_expression(list_z, tensor_x, tensor_y)
        # print("list:{0}".format(list))
        # z = init_by_data(shape_z, data)
        # print("【结果】：{0}".format(z.data))
        # shape_z = analyze_tensor(result, [])
        # print("shape_x:{0}\nshape_y;{1}\nshape_z:{2}".format(shape_x, shape_y, shape_z))
        # print("【叉乘结果】:{0}".format(result))
        pass
    else:
        print("输入不合法！")

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


# x = [[1, 2], [3, 4]]
# y = 5
# z = operate_tensor(x,y,'.')
# print("result:{0}".format(z))
# a = [1, 2]
# shape = [2, 2]
# z = init_tensor(shape, 0, a)
# print(z)

# analyze_structure("[[[1,2,3], [1,2,3]],[[1,2,3], [1,2,3]],[[1,2,3], [1,2,3]]]")

x = [[[1,2,3],[1,2,3],[1,2,3]], [[1,2,3],[1,2,3],[1,2,3]]]
y = [[[5,6],[7, 8],[9,10]],[[5,6],[7, 8],[9,10]], [[5,6],[7, 8],[9,10]]]
dot(x, y)