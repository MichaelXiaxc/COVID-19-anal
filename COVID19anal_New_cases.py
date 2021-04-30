'''
Documentation, License etc.

@package COVID19anal
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import tensorflow as tf
import tensorflow.compat.v1 as tf
import os

tf.disable_v2_behavior()
from data_anal import CN_covid_data


data=np.array(CN_covid_data['New_cases'])   #获取序列
print("model for new cases")
#data=np.array(CN_covid_data['New_deaths'])   #获取序列
#print("model for new deaths")
#data=np.array(CN_covid_data[Cumulative_cases'])   #获取序列
#print("model for cumulative cases")
#data=np.array(CN_covid_data['Cumulative_deaths'])   #获取序列
#print("model for cumulative deaths")
data=data[::-1]      #反转，使数据按照日期先后顺序排列
#以折线图展示data
plt.figure()
plt.plot(data)
plt.show()
normalize_data=(data-np.mean(data))/np.std(data)  #标准化
normalize_data=normalize_data[:,np.newaxis]       #增加维度
 
 
#生成训练集
#设置常量
time_step=20      #时间步
rnn_unit=10       #hidden layer units
batch_size=60     #每一批次训练多少个样例
input_size=1      #输入层维度
output_size=1     #输出层维度
lr=0.0006         #学习率
train_x,train_y=[],[]   #训练集
for i in range(len(normalize_data)-time_step-1):
    x=normalize_data[i:i+time_step]
    y=normalize_data[i+1:i+time_step+1]
    train_x.append(x.tolist())  #将数组转化成列表
    train_y.append(y.tolist()) 





 
 
#定义神经网络变量
X=tf.placeholder(tf.float32, [None,time_step,input_size])    #每批次输入网络的tensor/定义placeholder
Y=tf.placeholder(tf.float32, [None,time_step,output_size])   #每批次tensor对应的标签
#输入层、输出层权重、偏置
weights={
         'in':tf.Variable(tf.random_normal([input_size,rnn_unit])),
         'out':tf.Variable(tf.random_normal([rnn_unit,1]))
         }
biases={
        'in':tf.Variable(tf.constant(0.1,shape=[rnn_unit,])),
        'out':tf.Variable(tf.constant(0.1,shape=[1,]))
        }
 
 
 
#定义神经网络变量
def lstm(batch):      #参数：输入网络批次数目
    w_in=weights['in']
    b_in=biases['in']
    input=tf.reshape(X,[-1,input_size])  #需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
    input_rnn=tf.matmul(input,w_in)+b_in #表示矩阵乘法
    input_rnn=tf.reshape(input_rnn,[-1,time_step,rnn_unit])  #将tensor转成3维，作为lstm cell的输入
    cell=tf.nn.rnn_cell.BasicLSTMCell(rnn_unit)  #定义单个基本的LSTM单元
    init_state=cell.zero_state(batch,dtype=tf.float32)  #这个函数用于返回全0的state tensor
	#dynamic_rnn 用于创建由RNNCell细胞指定的循环神经网络，对inputs进行动态展开
	#output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
    output_rnn,final_states=tf.nn.dynamic_rnn(cell, input_rnn,initial_state=init_state, dtype=tf.float32)
    #函数的作用是将tensor变换为参数shape的形式。 	
    output=tf.reshape(output_rnn,[-1,rnn_unit]) 
    w_out=weights['out']
    b_out=biases['out']
    pred=tf.matmul(output,w_out)+b_out #表示矩阵乘法
    return pred,final_states
 
 
 
#训练模型
def train_lstm():
    global batch_size
    pred,_=lstm(batch_size) #调用的构建的lstm变量
    #损失函数 平均平方误差(MSE)
    loss=tf.reduce_mean(tf.square(tf.reshape(pred,[-1])-tf.reshape(Y, [-1])))
	#实现梯度下降算法的优化器，优化损失函数
    train_op=tf.train.AdamOptimizer(lr).minimize(loss)
	#保存和恢复模型的方法；方法返回checkpoint文件的路径。可以直接传给restore() 进行调用
    saver=tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        #重复训练10000次
        for i in range(100000):
            step=0
            start=0
            end=start+batch_size
            while(end<len(train_x)):
                _,loss_=sess.run([train_op,loss],feed_dict={X:train_x[start:end],Y:train_y[start:end]})
                start+=batch_size
                end=start+batch_size
                #每10步保存一次参数
                if step%10==0:
                    print(i,step,loss_)
                    print("保存模型：",saver.save(sess,'stock_c.model'))
                step+=1
 
 
train_lstm()
 
 
#预测模型
def prediction():
    pred,_=lstm(1)      #预测时只输入[1,time_step,input_size]的测试数据
    saver=tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        #参数恢复
        module_file = tf.train.latest_checkpoint(os.getcwd())
        saver.restore(sess, module_file) 
 
        #取训练集最后一行为测试样本。shape=[1,time_step,input_size]
        prev_seq=train_x[-1]
        predict=[]
        #得到之后100个预测结果
        for i in range(1000):
            next_seq=sess.run(pred,feed_dict={X:[prev_seq]})
            predict.append(next_seq[-1])
            #每次得到最后一个时间步的预测结果，与之前的数据加在一起，形成新的测试样本
            prev_seq=np.vstack((prev_seq[1:],next_seq[-1]))
        #以折线图表示结果
        plt.figure()
        plt.plot(list(range(len(normalize_data))), normalize_data, color='b')
        plt.plot(list(range(len(normalize_data), len(normalize_data) + len(predict))), predict, color='r')
        plt.show()
 
prediction()
 
 
