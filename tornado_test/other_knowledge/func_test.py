# one=[{'na':1},{'na':12},{'na':11}]
# for item in range(len(one)):
# 	if one[item]['na']==12:
# 		print('dfdf')
all_user={'1':1,'2':2}
key=None
for k, v in all_user.items():
	if v == 1:
		key=k
		# break
		all_user.pop(key)
print(all_user)