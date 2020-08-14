import numpy as np 
import math

values={'pclass':['1st','2nd','3rd','crew'],'age':['adult','child'],'gender':['male','female']}

def create_data (file):
	X=[]
	flag=0
	for line in file.readlines():	
		if flag==1:
			sep=line.split(",")
			x={}
			x['pclass']=sep[0]
			x['age']=sep[1]
			x['gender']=sep[2]
			x['survived']=sep[3].split("\r")[0]
			X.append(x)
			# print (sep[3].split("\r")[0])
		if flag==0:
			flag=1
	return X

def calc_entropy (p_yes,p_no):
	return (-p_yes*math.log2(p_yes+1e-5)-p_no*math.log2(p_no+1e-5))



def calc_max_gain(params,X):
	p_yes=len([x for x in X if x['survived']=="yes\n"])
	p_no=len([x for x in X if x['survived']=="no\n"])
	total=p_yes+p_no
	p_no/=total
	p_yes/=total
	inital_entropy=calc_entropy(p_yes,p_no)
	maxx=-3483208423
	max_param=""
	# print (list_params,)
	for param in params:
		# if param not in visit:
		# print (param)
		gain=inital_entropy
		for value in values[param]:
			# print (value)
			p_yes=len([x for x in X if x['survived']=="yes\n" and x[param]==value])
			p_no=len([x for x in X if x['survived']=="no\n" and x[param]==value])
			total_sub=p_yes+p_no
			# print (total,total_sub)
			if total_sub==p_yes:
				return ("yes")
			if total_sub==p_no:
				return ("no")
			p_yes=p_yes/total_sub
			p_no=p_no/total_sub
			entropy=calc_entropy(p_yes,p_no)
			gain=gain-entropy*(total_sub/total)
		if gain>maxx:
			maxx=gain
			max_param=param
	# print (max_param)
	return max_param


tree={}



	




file=open("/home/pranit/Desktop/Machine_Learning_CS60050_assignments/Assignment1/data1_19.csv")
X=create_data(file)

list_params=['pclass','age','gender']
visited=[]



# create_tree('root',0,list_params,values,X,visited)
# print (X[0])
# p_yes=len([x for x in X if x['survived']=="yes"])
# p_no=len([x for x in X if x['survived']=="no"])
# print (p_yes,p_no)
# print (tree['female'])

stack=[]
stack.append(['root',0,list_params,X])
while len(stack)>0:
	# print (len(stack))
	temp=stack.pop()
	name=temp[0]
	check=temp[1]
	params=temp[2]
	X_d=temp[3]
	# print (name,len(X_d))
	p_yes=len([x for x in X_d if x['survived']=="yes\n"])
	p_no=len([x for x in X_d if x['survived']=="no\n"])
	# print (params)
	if len(params)==0 or name=="yes" or name=="no":
		if (p_yes>p_no):
			tree[name]="yes"
		else:
			tree[name]="no"
	elif check==0:
		child=calc_max_gain(params,X_d)
		print (child)
		tree[name]=child
		params_pass=[param for param in params if param is not child]
		if (name=="yes" or name=="no"):
		# print (name,params_pass,params,child)
			print ("done")
		else:
			stack.append([child,1,params_pass,X_d])
	else:
		for value in values[name]:
			if name=="age":
				print (value)
			temp=[]
			X_pass=[x for x in X_d if x[name]==value]
			temp.append(value)
			stack.append([value,0,params,X_pass])
		# tree[name]=temp
		print (temp)

# print (tree['pclass'])

