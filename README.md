### 简易tensor语言设计与实现

#### 1.数据结构

```python
class Tensor(object):
    def __init__(self, ndim, shape, data, dtype):
        self.ndim = ndim #维数
        self.shape = shape #形状
        self.data = data #数据
        self.dtype = dtype #类型
```

包含了基本的属性，`ndim`代表维度数，`shape`代表tensor的形状，`data`代表其中的数据，`dtype`代表存储的数据类型。

#### 2. 数据初始化

数据生成的方法包括`rand`、`one`、`zero`

```python
def init_tensor(shape, index, data):
    #抽象生成函数
    if index >= len(shape):
        return data
    else:
        temp = []
        for i in range(0, shape[index]):
            temp.append(init_tensor(shape, index+1, data))
        return temp
```

生成`tensor`需要的参数包括`shape`、`data`，index递归构造过程中传递的参数。

**原理**：由于是多层结构，因此选择使用递归，目的是为了从底层从下而上构造，每一层通过新构造的`[]`拼接下一层构造完成的结构，最终就能生成按照`shape`生成的`tensor`。

```python
def init_random(shape):
    return Tensor(len(shape), shape, random(shape, 0), "Tensor")

def init_one(shape):
    return Tensor(len(shape), shape, init_tensor(shape, 0, 1), "Tensor")

def init_zero(shape):
    return Tensor(len(shape), shape, init_tensor(shape, 0, 0), "Tensor")
```

通过构造函数包装不同的方法生成对应的tensor

**结果测试**：

```python
shape = [3, 3]
b = init_random(shape)
c = init_one(shape)
d = init_zero(shape)
print("[rand]\nb_ndim:{0}, b_shape:{1}, b_dtype:{2}\nb_data:{3}".format(b.ndim, b.shape, b.dtype, b.data))
print("[one]\nc_ndim:{0}, c_shape:{1}, c_dtype:{2}\nc_data:{3}".format(c.ndim, c.shape, c.dtype, c.data))
print("[zero]\nd_ndim:{0}, d_shape:{1}, d_dtype:{2}\nd_data:{3}".format(d.ndim, d.shape, d.dtype, d.data))
```

**运行结果**：

```python
[rand]
b_ndim:2, b_shape:[3, 3], b_dtype:Tensor
b_data:[[5, 9, 2], [4, 4, 2], [0, 8, 9]]
[one]
c_ndim:2, c_shape:[3, 3], c_dtype:Tensor
c_data:[[1, 1, 1], [1, 1, 1], [1, 1, 1]]
[zero]
d_ndim:2, d_shape:[3, 3], d_dtype:Tensor
```

#### 3. 生成指定结构的tensor

由于python支持多层列表的识别，和生成，但是无法得到`shape`信息，因此需要生成`tensor`信息还需要分析`shape`信息。

```python
def analyze_tensor(tensor, shape):
    #分析结构返回shape
    if isinstance(tensor, list):
        shape.append(len(tensor))
        analyze_tensor(tensor[0], shape) 
    return shape
```

**原理**：这里同样使用递归来分析，使用`isinstance()`函数来判断当前遍历层的元素是否为list来判定是否遍历到最底层，在遍历每一层的时候使用`len()`得到当前层的个数信息，最后返回`shape`。

```python
def init_by_list(data):
    shape = analyze_tensor(data, [])
    return Tensor(len(shape), shape, data, "tensor")
```

**结果测试**：

```python
z = [[7, 9, 8], [4, 3, 2], [0, 1, 7]]
a = init_by_list(z)
print("[data]\na_ndim:{0}, a_shape:{1}, a_dtype:{2}\na_data:{3}".format(a.ndim, a.shape, a.dtype, a.data))
```

**运行结果：**

```python
[data]
a_ndim:2, a_shape:[3, 3], a_dtype:tensor
a_data:[[7, 9, 8], [4, 3, 2], [0, 1, 7]]
```

### 语法分析

现在假设通过解析字符串来生成对应的`tensor`。

```python
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

```

**原理**：首先通过等号将语句分成两部分，第一部分为变量名，第二部分为数据部分，将多余的空格去掉后，分析右边的语句，判断是否为按照指定结构生成还是按照函数来生成，分两种情况：

1. **按照指定结构生成**

   需要解析string字符串，通过`analyze_structure()`方法得到对应的`shape`信息。

   ```python
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
       print("分析当前字符串形状:{0}".format(shape))
       return shape
   ```

   **原理：**主要思路通过括号匹配，可以先通过`左中括号`得到维度数信息，然后统计第一个遇到的最底层list可以得到最后一个维度的大小，然后重新左到右匹配，遇到`左中括号`就弹入`栈`，遇到`右中括号`就将`栈`中最顶的`左中括号`弹出，弹出后当前`栈`内的`左中括号`个数代表当前括号组所在的层级，由于这样匹配会统计所有的同级组，因此在统计完之后需要修正，只需要从前到后除以后一个数就可以得到正确的`shape`信息。

   在得到shape信息后还需要得到生成的具体信息，只需要将所有的括号、空格去掉按照逗号分割，就可以得到`data`的一维数组信息。然后通过`create_tensor_by_structure()`生成对应的`tensor`。

   ```python
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
   def init_by_data(shape, data):
       return Tensor(len(shape), shape, create_tensor_by_structure(shape, data, 0), "tensor")
   ```

   **原理：**与前面生成方法类似，不同的是在返回数据的时候通过一维数组中取得，再包装成`init_by_data`方法生成`tensor`数据。

2. **利用函数构建**

   这里预先构建的函数包括`rand()`、`one()`、`zero()`，通过判断首字母的方法判定是使用哪个方法，然后通过`split`得到`shape`的list信息，再调用对应的方法构建

在最后的生成语句中，由于要使用变量来创建变量，因此用到`globals()`函数直接在全局变量表中添加对应的信息。

**结果测试**：

```python
str1 = "test1 = [[[1, 2], [4, 5], [7, 8]]]"
analyse_statement(str1)
print("test1:{0}".format(test1.data))
print("--------------------------------")
str2 = "test2 = one((2,2))"
analyse_statement(str2)
print("test2:{0}".format(test2.data))
```

**运行结果：**

```python
[生成自定义结构] 变量名：test1, 参数：[[[1, 2], [4, 5], [7, 8]]]
分析得到当前字符串形状:[1, 3, 2]
参数：1,2,4,5,7,8
test1:[[[1, 2], [4, 5], [7, 8]]]
--------------------------------
[one] 变量名：test2, 形状：(2,2)
test2:[[1, 1], [1, 1]]
```

### 算术操作

#### 1. 加法、点乘

**Tensor运算合法性**：从`shape`最后一维开始比较，如果相同，则比较前一位，如果不相同，有1则1的一方通过广播拓展成相同值，而维度数少的一方也可以通过广播数增加维度数达成一致。

```python
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
```

**原理：**首先判断输入是否具有0维tensor，如果有则广播成1维，如果维度数和维度都相同，则通过`cal_tensor()`计算结果；如果不同，从尾部开始比较，如果当前比较维度不相同，则判断是否存在1，如果存在1，则广播拓展后再运算。最后通过`create_tensor_by_structure()`使用`shape`和一维`data`构建结果的`tensor`。

> 广播：以1当前维度为分割线，将1后面维度的部分看成一个整体，shape为shape[0:len(shape) - i]，通过`init_tensor()`构建新的tensor后，则完成拓展；如果是维度数少的情况，则通过将整个tensor看成整体，shape为shape_x[0:(len(shape_x) - len(shape_y))]，再通过`init_tensor()`构建新tensor。

```python
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
```

**原理：**通过递归遍历多层list，遍历到数据的时候执行相对应的操作，最后返回一维数组。

**结果测试**：

```python
x = [[1, 2], [3, 4]]
y = [5, 6]
z = operate_tensor(x,y,'.')
print("result:{0}".format(z))
```

**运行结果：**

```python
tensor1: [[1, 2], [3, 4]] shape: [2, 2]
tensor2: [5, 6] shape: [2]
【执行运算...】
tensor1:[[1, 2], [3, 4]]
tensor2:[[5, 6], [5, 6]]
operator:.
【结果】：[[5, 12], [15, 24]]
result:[[5, 12], [15, 24]]
```

#### 2. 叉乘

```python
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
```

> 公式：`A[m1*n1*k1] * B[m2,n2,k2] = C[m1][n1][n2][k2]`
>
> 且k1 = m2
>
> `C[i][j][l][r] = sum_{t=1…k1} (A[i][j][t] * B[t][l][r])`

**原理：**因此需要将x的所有最底层与y的最顶层相乘，这里递归遍历x最底层，使用之前定义的操作对`tensor`进行运算，返回结果。

**结果测试**：

```python
x = [[1,2],[3,4]]
y = [[[5,6],[7, 8],[9,10]],[[5,6],[7, 8],[9,10]]] 
dot(x, y)
```

**运行结果：**

```python
➜  notebooks git:(master) ✗ python "/Users/welljun06/github/myTensor/tensor.py"
tensor1: [[1, 2], [3, 4]] shape: [2, 2]
tensor2: [5, 6] shape: [2]
【执行运算...】
tensor1:[[1, 2], [3, 4]]
tensor2:[[5, 6], [5, 6]]
operator:.
【结果】：[[5, 12], [15, 24]]
result:[[5, 12], [15, 24]]
tensor_x:[[1, 2], [3, 4]]
tensor_y:[[[5, 6], [7, 8], [9, 10]], [[5, 6], [7, 8], [9, 10]]]
tensor1: [[5, 6], [7, 8], [9, 10]] shape: [3, 2]
tensor2: [1] shape: [1]
【执行运算...】
tensor1:[[5, 6], [7, 8], [9, 10]]
tensor2:[[1, 1], [1, 1], [1, 1]]
operator:.
【结果】：[[5, 6], [7, 8], [9, 10]]
tensor1: [[5, 6], [7, 8], [9, 10]] shape: [3, 2]
tensor2: [0] shape: [1]
【执行运算...】
tensor1:[[5, 6], [7, 8], [9, 10]]
tensor2:[[0, 0], [0, 0], [0, 0]]
operator:+
【结果】：[[5, 6], [7, 8], [9, 10]]
tensor1: [[5, 6], [7, 8], [9, 10]] shape: [3, 2]
tensor2: [2] shape: [1]
【执行运算...】
tensor1:[[5, 6], [7, 8], [9, 10]]
tensor2:[[2, 2], [2, 2], [2, 2]]
operator:.
【结果】：[[10, 12], [14, 16], [18, 20]]
tensor1: [[10, 12], [14, 16], [18, 20]] shape: [3, 2]
tensor2: [[5, 6], [7, 8], [9, 10]] shape: [3, 2]
【执行运算...】
tensor1:[[10, 12], [14, 16], [18, 20]]
tensor2:[[5, 6], [7, 8], [9, 10]]
operator:+
【结果】：[[15, 18], [21, 24], [27, 30]]
tensor1: [[5, 6], [7, 8], [9, 10]] shape: [3, 2]
tensor2: [3] shape: [1]
【执行运算...】
tensor1:[[5, 6], [7, 8], [9, 10]]
tensor2:[[3, 3], [3, 3], [3, 3]]
operator:.
【结果】：[[15, 18], [21, 24], [27, 30]]
tensor1: [[15, 18], [21, 24], [27, 30]] shape: [3, 2]
tensor2: [0] shape: [1]
【执行运算...】
tensor1:[[15, 18], [21, 24], [27, 30]]
tensor2:[[0, 0], [0, 0], [0, 0]]
operator:+
【结果】：[[15, 18], [21, 24], [27, 30]]
tensor1: [[5, 6], [7, 8], [9, 10]] shape: [3, 2]
tensor2: [4] shape: [1]
【执行运算...】
tensor1:[[5, 6], [7, 8], [9, 10]]
tensor2:[[4, 4], [4, 4], [4, 4]]
operator:.
【结果】：[[20, 24], [28, 32], [36, 40]]
tensor1: [[20, 24], [28, 32], [36, 40]] shape: [3, 2]
tensor2: [[15, 18], [21, 24], [27, 30]] shape: [3, 2]
【执行运算...】
tensor1:[[20, 24], [28, 32], [36, 40]]
tensor2:[[15, 18], [21, 24], [27, 30]]
operator:+
【结果】：[[35, 42], [49, 56], [63, 70]]
shape_x:[2, 2]
shape_y;[2, 3, 2]
shape_z:[2, 3, 2]
【叉乘结果】:[[[15, 18], [21, 24], [27, 30]], [[35, 42], [49, 56], [63, 70]]]
```

**分析**：可以看到进行了多次广播操作。

### 形状操作

#### 1. shape

```python
def get_shape(tensor):
    shape = analyze_tensor(tensor, [])
    print("shape:{0}".format(shape))
```

直接使用上面实现的`analyze_tensor()`函数实现

**结果测试**：

```python
x = [[1, 2],[3, 4]]
y=[5,6]
get_shape(x)
get_shape(y)
```

**运行结果**：yu

```python
shape:[2, 2]
shape:[2]
```

#### 2. reshape

```python
def reshape_tensor(tensor, new_shape):
    # 对tensor进行reshape操作
    shape = analyze_tensor(tensor, [])
    size = shape_size(shape)
    new_size = shape_size(new_shape)
    if size != new_size:
        print("error")
    else:
        data = get_tensor_data(tensor, [])
        new_tensor = create_tensor_by_structure(new_shape, data, 0)
        return new_tensor
```

**原理**：分析原`shape`的`size`大小，与`new_shape`的`size`进行比较，如果合法则进行reshape操作，将原有数据一维化，利用`create_tensor_by_structure()`创建新`tensor`。

**结果测试**：

```python
x = [[1, 2],[3, 4]]
new_shape = [4, 1]
x_new = reshape_tensor(x, new_shape)
print("x_new:{0}".format(x_new))
```

**运行结果**：

```python
x_new:[[1], [2], [3], [4]]
```

#### 3. size

```python
def get_tensor_size(tensor):
    # 返回tensor的szie信息
    shape = analyze_tensor(tensor, [])
    size = shape_size(shape)
    print("size:{0}".format(size))
    return size
```

**原理**：与之前类似，分析`tensor`的形状，再根据`shape`信息得到`size`大小。

**结果测试**：

```python
x = [[1, 2],[3, 4]]
get_tensor_size(x)
```

**运行结果**：

```python
size:4
```

#### 4. slice操作

```python
def tensor_slice(inputs, begin, size):
    # tensor切片操作
    inputs = tensor_begin(begin, inputs)
    print(inputs)
    result_data = tensor_size(size, inputs, 0, [])
    result = init_by_data(size, result_data)
    print(result.data)
```

**原理**：slice函数需要三个参数

- inputs：需要操作的tensor
- begin：定位到开始切片的位置
- size：切片后的tensor的shape

首先处理的是begin参数

```python
def tensor_begin(begin, tensor):
    # 定位到开始位置
    for i in range(len(begin)):
        # print(begin[i])
        if begin[i] != 0:
            tensor = tensor[begin[i]:]
            if i != 0:
                tensor = tensor[0]
    return tensor
```

**原理**：遍历begin列表，如果当前遍历的begin数据不为0，则从begin[i]行开始取，如果不是第一次操作，则tensor取下一层。最后返回新的tensor，开头即为开始位置。

接下来处理size参数

```python
def tensor_size(shape, tensor, index, list):
    # 按照size遍历tensor
    if index >= len(shape):
        list.append(tensor)
    else:
        for i in range(0, shape[index]):
            print("tensor[i]:{0},index:{1}".format(tensor[i], index))
            tensor_size(shape, tensor[i], index + 1, list)
    return list
```

**原理**：即按照size的shape来当前tensor进行遍历，将访问到的元素存储为一维list

最后通过`init_by_data()`创建新的tensor即为slice后产生的tensor

**结果测试**：

```python
t = [[[1, 1, 1], [2, 2, 2]],[[3, 3, 3], [4, 4, 4]],[[5, 5, 5], [6, 6, 6]]]
begin = [1, 0, 0]
size = [1, 2, 3]
tensor_slice(t, begin, size)
```

**运行结果**：

```
[[[3, 3, 3], [4, 4, 4]]]
```

### 简易Tensor语言识别

这里定义两种语句，一种是赋值语句，一种执行语句

```python
def analyse_type(str):
    # tensor语言类型检测
    if '=' in str:
        str_split = str.split('=') # 将输入语句按照等号划分两半
        for i in range(len(str_split)):
            str_split[i] = str_split[i].strip()
        if '*' in str:
            # 叉乘
            argv = str_split[1].split('*')
            for i in range(len(argv)):
                argv[i] = argv[i].strip()
                print(argv[i])
            result = eval('dot({0}, {1})'.format(argv[0], argv[1]))
            shape = get_shape(result)
            exec_str = '{2} = dot({0}, {1})'.format(argv[0], argv[1], str_split[0])
            exec(exec_str, globals())
        else:
            exec(str, globals())
            shape = eval('get_shape({0})'.format(str_split[1]))
        print('{0}:tensor{1}'.format(str_split[0], shape))
    else:
        exec(str)  
```

**原理**：如果有等号，根据等号将语句划分，如果没有‘*’，则是赋值语句，只需要将语句执行后统计shape信息，这里注意`exec()`要使用`globals()`参数才能全局创建变量。如果是`叉乘`情况，则需要将变量取出后通过`eval()`调用`dot()`函数，最后一样统计`shape`信息即可。

**结果测试**：

```python
str1 = "x = [1, 2]"
analyse_type(str1)
```

**运行结果**：

```python
x:tensor[2]
```

**结果测试**：

```python
y = [[3,4,5],[6,7,8]]
str1 = "print(y)"
analyse_type(str1)
```

**运行结果**：

```python
[[3, 4, 5], [6, 7, 8]]
```

**结果测试**：

```python
x = [1,2]
y = [[3,4,5],[6,7,8]]
str1 = "z = x * y"
analyse_type(str1)
print("z:{0}".format(z))
```

**运行结果**：

```python
z:tensor[1, 3]
z:[[15, 18, 21]]
```

