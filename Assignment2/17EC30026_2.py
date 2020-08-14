import numpy as np 
import pandas as pd
import csv


def load_data (file):
	list_data=[]
	with open(file,"rt") as f:
		data=csv.reader(f)
		# print (data)
		f=0
		for line in data:
			temp_dict={}
			if f==0:
				f=1
			else:
				temp_dict={}
				list_params=line[0].split(',')
				# print (list_params)
				temp_dict['D']=list_params[0]
				temp_dict['X1']=list_params[1]
				temp_dict['X2']=list_params[2]
				temp_dict['X3']=list_params[3]
				temp_dict['X4']=list_params[4]
				temp_dict['X5']=list_params[5]
				temp_dict['X6']=list_params[6]
				list_data.append(temp_dict)
	return list_data




def find_probs (train_data):
	len_happy=len([x for x in train_data if x['D']=='1'])
	len_unhappy=len([x for x in train_data if x['D']=='0'])
	p_happy=float(len([x for x in train_data if x['D']=='1']))/len(train_data)
	p_unhappy=float(len([x for x in train_data if x['D']=='0']))/len(train_data)

	list_of_vals=['1','2','3','4','5']

	p_happy_attributes=np.zeros((7,6))
	p_unhappy_attributes=np.zeros((7,6))

	for i in range (1,7):
		for j in list_of_vals:
			val='X'+str(i)
			len_ph=len([x for x in train_data if x['D']=='1' and x[val]==str(j)])
			len_pu=len([x for x in train_data if x['D']=='0' and x[val]==str(j)])
			# print (i,j)
			p_happy_attributes[i][int(j)]=(float(len_ph)+1)/(len_happy+c)
			p_unhappy_attributes[i][int(j)]=(float(len_pu)+1)/(len_unhappy+c)
	return p_happy_attributes,p_unhappy_attributes,p_happy,p_unhappy


def find_accuracy (test_data,p_happy_attributes,p_unhappy_attributes,p_happy,p_unhappy):
	count_true=0
	for data in test_data:
		p_happy_temp=p_happy
		p_unhappy_temp=p_unhappy
		res=0
		for i in range (1,7):
			val='X'+str(i)
			p_happy_temp*=p_happy_attributes[i][int(data[val])]
			p_unhappy_temp*=p_unhappy_attributes[i][int(data[val])]
		if p_happy_temp>p_unhappy_temp:
			res='1'
		else:
			res='0'
		if (res==data['D']):
			count_true+=1
		print (data,"predicted value is ",res)
	return float(count_true)/len(test_data)
	# print (float(count_true)/len(test_data))


c=5  #number of attributes 
train_data=load_data("data2_19.csv")
p_happy_attributes,p_unhappy_attributes,p_happy,p_unhappy=find_probs(train_data)
test_data=load_data("test2_19.csv")
print ("TEST SET ACCURACY .....")
accuracy=find_accuracy(test_data,p_happy_attributes,p_unhappy_attributes,p_happy,p_unhappy)
# print (p_unhappy_attributes[1:,1:])
print ("accuracy on the test set is ",accuracy*100)




