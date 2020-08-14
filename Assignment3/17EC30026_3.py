# 17EC30026 # Pranit Chawla # Assignment 3 # use python2 17EC30026_3.py to run the code


import numpy as np 
import math
import csv


def create_data (file): # function used to convert the data into two lists, X_train and X_test 
	X_train=[]
	X_test=[]
	list_params=[]
	weights=[]
	flag=0
	values={'pclass':['1st','2nd','3rd','crew'],'age':['adult','child'],'gender':['male','female']}
	with open(file,'rt') as f:
		data=csv.reader(f)
		for row in data:
			if flag!=0:
			# sep=line.split(",")
				x={}
				x['pclass']=row[0]
				x['age']=row[1]
				x['gender']=row[2]
				x['survived']=row[3]
				# if flag%100==0:
				# 	temp_dict={'pclass':row[0],'age':row[1],'gender':row[2],'survived':row[3]}
				# 	X_test.append(temp_dict)
				# else:
				X_train.append(x)
				flag+=1
			if flag==0:
				list_params=row
				list_params.remove('survived')
				flag+=1

	return X_train,list_params,values


def create_data_2 (file): # function used to convert the data into two lists, X_train and X_test 
	X_train=[]
	X_test=[]
	list_params=[]
	weights=[]
	flag=0
	values={'pclass':['1st','2nd','3rd','crew'],'age':['adult','child'],'gender':['male','female']}
	with open(file,'rt') as f:
		data=csv.reader(f)
		for row in data:
			
			# sep=line.split(",")
			x={}
			x['pclass']=row[0]
			x['age']=row[1]
			x['gender']=row[2]
			x['survived']=row[3]
			# if flag%100==0:
			# 	temp_dict={'pclass':row[0],'age':row[1],'gender':row[2],'survived':row[3]}
			# 	X_test.append(temp_dict)
			# else:
			X_train.append(x)
			flag+=1

	return X_train,list_params,values

def calc_entropy (p_yes,p_no): # function to calculate entropy 
	return (-p_yes*np.log2(p_yes+1e-5)-p_no*np.log2(p_no+1e-5))




def calc_max_gain(params,X_d): # function to calculate the element with the maximum gain and return it 
	p_yes=len([x for x in X_d if x['survived']=="yes"])
	p_no=len([x for x in X_d if x['survived']=="no"])
	total=p_yes+p_no
	p_yes=float(p_yes)/total
	p_no=float(p_no)/total
	inital_entropy=calc_entropy(p_yes,p_no)
	maxx=-3483208423
	max_param=""
	for param in params:
		gain=inital_entropy
		for value in values[param]:
			p_yes_sub=len([x for x in X_d if x['survived']=="yes" and x[param]==value])
			p_no_sub=len([x for x in X_d if x['survived']=="no" and x[param]==value])
			total_sub=p_yes_sub+p_no_sub
			if (total_sub!=0):
				p_yes_sub=float(p_yes_sub)/total_sub
				p_no_sub=float(p_no_sub)/total_sub
				entropy=calc_entropy(p_yes_sub,p_no_sub)
			else:
				entropy=0
			gain=gain-entropy*float(total_sub)/total
		if gain>maxx:
			maxx=gain
			max_param=param
	return max_param




def predict (dictionary,x,flag,parent): # function to predict the value in the test set 
	if dictionary=="no":
		# tot+=1
		# print (x,"predcited value: no","true value ",x['survived'])
		# print (x['survived'])
		return "no"
		# return cor,incor,tot

	elif dictionary=="yes":
		# tot+=1
		# print (x,"predcited value: yes","true value ",x['survived'])
		# print (x['survived'])
		return "yes"
		# return cor,incor,tot
	if flag==0:
		if dictionary is not None:
			for i in dictionary:
				# print (i)
				return predict(dictionary[i],x,1,i)
	else:
		if dictionary is not None:
			for i in dictionary:
				if i==x[parent]:
					return predict(dictionary[i],x,0,parent)


# def print_dict(dictionary, ident = ''): # function to print dictionary in nested form
#     for key, value in dictionary.iteritems():
#         if isinstance(value, dict):
#             print '%s%s' %(ident,key) 
#             print_dict(value, ident+'  ')
#         else:
#         	if value is not None:
# 	            print ident+'%s = %s' %(key, value)


def create_tree (params,X_f,parent): # main function which recursively forms the tree 
	if (len(X_f)==0):
		return
	if len(params)==0:
		p_yes=len([x for x in X_f if x['survived']=="yes"])
		p_no=len([x for x in X_f if x['survived']=="no"])
		if (p_yes>p_no):
			return "yes";
		else:
			return "no"
	else:
		answer=calc_max_gain(params,X_f)
		tree={answer:{}}
		params_new=[param for param in params if param != answer]
		for value in values[answer]:
			X_new=[x for x in X_f if x[answer]==value]
			subtree=create_tree(params_new,X_new,parent)
			tree[answer][value]=subtree
		return tree
	




# file=open("data3_19.csv")  # 
train_file="data3_19.csv"
X_train,list_params,values=create_data(train_file)
X_train_np=np.array(X_train)
weights=np.ones((len(X_train)))
weights=weights/len(X_train)

errors=[]
avals=[]
trees=[]
N_ada=3

for i in range (N_ada):
	sample=np.random.choice(X_train_np.shape[0],X_train_np.shape[0],True,weights)
	X_train1=X_train_np[sample]
	tree1=create_tree(list_params,X_train1,'root')
	trees.append(tree1)
	e1=0
	flag=0
	for x in X_train:
		ans=predict(tree1,x,0,"")
		if ans!=x['survived']:
			e1+=weights[flag]
		flag+=1
	e1=float(e1)/len(X_train)
	# print (e1)
	alpha1=0.5*np.log(float(1-e1)/e1)
	# print (e1,alpha1)
	flag=0
	for x in X_train:
		ans=predict(tree1,x,0,"")
		if ans!=x['survived']:
			weights[flag]=weights[flag]*np.exp(alpha1)
		else:
			weights[flag]=weights[flag]*np.exp(-alpha1)
		flag+=1
	weights=weights/sum(weights)
	print ("Value of alpha at the end of round of adaboost",i+1,"is ",alpha1)
	errors.append(e1)
	avals.append(alpha1)	

# print ("CHECK...........",errors,avals)





test_file="test3_19.csv"
X_test,list_params,values=create_data_2(test_file)
cor=0
for x in X_test:
	ans=[]
	for i in range (N_ada):
		ans1=predict(trees[i],x,0,"")
		ans.append(ans1)
	

	ayes=0
	ano=0
	# print (ans1,ans2,ans3)
	for i in range (N_ada):
		ayes=ayes+avals[i]*(ans[i]=="yes")
		ano=ano+avals[i]*(ans[i]=="no")
	# print (ayes,ano)
	if ayes>ano:
		fans="yes"
	else:
		fans="no"
	# print (fans,x['survived'])
	if fans==x['survived']:
		cor+=1
# print (len(X_test))
print ("Accuracy on the test set is",100*float(cor)/len(X_test))
# weights=weights/sum(weights)



