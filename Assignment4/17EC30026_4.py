# 17EC30026 # Pranit Chawla # Assignment 4 # use python3 17EC30026_4.py to run the code
import csv
import random
def create_data (file): # function used to convert the data into two lists, X_train and X_test 
	X_train=[]
	with open(file,'rt') as f:
		data=csv.reader(f)
		for row in data:
			if len(row)>0:
				X_train.append(row)
	return X_train

X_train=create_data("data4_19.csv")
k=3
n_iterations=10
centroids=[]
for i in range (k):
	ch=random.choice(X_train)
	emp=[]
	for c in ch:
		emp.append(c)
	centroids.append(emp)
# print (centroids)

flag=0
for i in range (n_iterations):
	for x in X_train:
		if flag==0:
			index=0
			min_dist=10000000
			# print (x[0],len(x))
			cluster=0
			for c in centroids:
				dist=(float(c[0])-float(x[0]))**2+(float(c[1])-float(x[1]))**2+(float(c[2])-float(x[2]))**2+(float(c[3])-float(x[3]))**2
				if dist<min_dist:
					cluster=index
					min_dist=dist
				index+=1
			x.append(cluster)
			# print (len(x))
		else:
			index=0
			min_dist=10000000
			cluster=0
			for c in centroids:
				dist=(float(c[0])-float(x[0]))**2+(float(c[1])-float(x[1]))**2+(float(c[2])-float(x[2]))**2+(float(c[3])-float(x[3]))**2
				if dist<min_dist:
					cluster=index
					min_dist=dist
				index+=1
			x[5]=cluster
	flag=1
	clus=[]
	for j in range (k):
		temp_list=[x for x in X_train if x[5]==j]
		clus.append(temp_list)
	for j in range (k):
		for k in range (4):
			temp=0
			for ele in clus[j]:
				temp+=float(ele[k])
			centroids[j][k]=float(temp)/len(clus[j])

# for x in X_train:
# 	print (x)


for i in range (len(centroids)):
	string1="Iris-virginica"
	string2="Iris-versicolor"
	string3="Iris-setosa"
	len_union1=len([x for x in X_train if x[5]==i])
	len_intersection1=len([x for x in X_train if x[5]==i and x[4]==string1])
	len_union2=len([x for x in X_train if x[5]==i])
	len_intersection2=len([x for x in X_train if x[5]==i and x[4]==string2])
	len_union3=len([x for x in X_train if x[5]==i])
	len_intersection3=len([x for x in X_train if x[5]==i and x[4]==string3])
	print ("For Cluster",i , "Jacquard distance with ")
	if len_union1>0:
		print (string1,"is ", 1-float(len_intersection1)/len_union1)
	else:
		print (string1,"is ",1)
	if len_union2>0:
		print (string2,"is ", 1-float(len_intersection2)/len_union2)
	else:
		print (string2,"is ",1)
	if len_union3>0:
		print (string3,"is ", 1-float(len_intersection3)/len_union3)
	else:
		print (string3,"is ",1)
	print ("Mean of this Cluster is ",centroids[i][0:4])


	

