import numpy as np


#collecting all positive and negative points in one numoy array datapts
datapts=np.zeros((2,1000))
datapts[0,0:500]=positive_pts[0,0:500]
datapts[1,0:500]=positive_pts[1,0:500]
datapts[0,500:1000]=negative_pts[0,0:500]
datapts[1,500:1000]=negative_pts[1,0:500]
# its one column is one datapoint

#datapts_label
datapts_label=np.zeros((1000))
datapts_label[0:500]=1
datapts_label[500:1000]=-1

#now we have 1000 datapoints having x and  y coordinates datapots[0] contains all x coordinates all 1000 datapoints





def sigma(x):
 y=np.zeros((len(x),1))
 for i in range(0,len(x)):
  if(x[i][0]>y[i][0]): y[i][0]=x[i][0]
 return y


def loss_L(w1,w2,b1,b2):
   sum=0
   for i in range(0,1000):
      #temp represents the temporary ith datapoint with label label[i]
      temp=np.zeros((2,1))
      temp[0:2,0]=datapts[0:2,i]
      #x_1 represents the output at the 1st layer and x_2 represents the output at layer 2nd and s_1 is the input vector to layer one and s_2 is input vector to the layer 2
      s_1=np.dot(w1,temp)+b1
      x_1=sigma(s_1)
      s_2=np.dot(w2,x_1)+b2
      x_2=sigma(s_2)
      sum=sum+np.log(1+np.exp(-datapts_label[i]*(x_2[0][0])))
   return sum/1000


#x1 represents the output at the 1st layer and x2 represents the output at layer 2nd and s1 is the input vector to layer one and s2 is input vector to the layer 2
w1=np.random.rand(4,2)
w2=np.random.rand(1,4)
b1=np.random.rand(4,1)
b2=np.random.rand(1,1)
x1=np.zeros((4,1))
x2=np.zeros((1,1))
s1=np.zeros((4,1))
s2=np.zeros((1,1))
x0=np.zeros((2,1))
#means gradient of loss for the ith random point wrt x_2..for the following notations.
#s1[k][0] means the input of the kth perceptron in the 1st layer and sigma(s1[k][0])=x1[k][0] which is output of the kth neuron in the 1st layer
grad_L_x2=np.zeros((1,1))
grad_L_x1=np.zeros((4,1))
grad_L_s2=np.zeros((1,1))
grad_L_s1=np.zeros((4,1))
grad_x2_s2=np.zeros((1,1))
grad_L_w2=np.zeros((1,4))
grad_L_w1=np.zeros((4,2))
grad_L_b2=np.zeros((1,1))
grad_L_b1=np.zeros((4,1))
lst=np.arange(1000)
eta=0.001


print("mean logistic loss before tarining",loss_L(w1,w2,b1,b2))

#e stands for no. of epochs
for e in range(0,500):
 #randomising datapts with the help of lst of numbers from 0 to 999 in random order
 datapts=datapts.T
 np.random.shuffle(lst)
 datapts=datapts[lst]
 datapts_label=datapts_label[lst]
 datapts=datapts.T
 for i in range(0,1000):
   x0[0:2,0]=datapts[0:2,i]
   s1=np.dot(w1,x0)+b1
   x1=sigma(s1)
   s2=np.dot(w2,x1)+b2
   x2=sigma(s2)

   grad_L_x2[0][0]=(-datapts_label[i]*np.exp(-datapts_label[i]*x2[0][0] ))/(1+np.exp(-datapts_label[i]*x2[0][0] ))
   

   if(s2[0][0]>0): grad_x2_s2[0][0]=1
   else: grad_x2_s2[0][0]=0


   grad_L_s2[0][0]=grad_L_x2[0][0]*grad_x2_s2[0][0]
   
   for k in range(0,4):
    grad_L_w2[0][k]=grad_L_s2[0][0]*x1[k][0]


   grad_L_b2[0][0]=grad_L_s2[0][0]*1


   for k in range(0,4):
    grad_L_x1[k][0]=grad_L_s2[0][0]*grad_L_w2[0][k]


   for k in range(0,4):
    temp=0
    #s1[k][0] means the input of the kth perceptron in the 1st layer and sigma(s1[k][0])=x1[k][0] which is output of the kth neuron in the 1st layer
    # below is the chain rule to find grad_L_s1[k][0] i.e. gradient of L loss wrt s1[k][0] here temp represents the gradient of x1[k][0] wrt s1[k][0] i.e. grad_x1[k][0]_s1[k][0 ]
    if(s1[k][0]>0): temp=1
    grad_L_s1[k][0]=temp*grad_L_x1[k][0]
   
   for j in range(0,4):
    for k in range(0,2):
     #w1[j][k] is present only in s1[j][0] i.e. in the input to j the perceptron in 1st layer 
     grad_L_w1[j][k]=grad_L_s1[j][0]*x0[k][0]
   
   for j in range(0,4):
    grad_L_b1[j][0]=grad_L_s1[j][0]*1
   
   b2=b2-eta*grad_L_b2
   w2=w2-eta*grad_L_w2
   b1=b1-eta*grad_L_b1
   w1=w1-eta*grad_L_w1

print("mean logistic loss after training",loss_L(w1,w2,b1,b2))
print("parameters"," ","w1:",w1,"w2:",w2,"b1:",b1,"b2:",b2)
#Improved


