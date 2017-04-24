def create_args_string(num):
	'''
	生成指定长度的list，并用占位符？填充
	'''
	arr = []
	for n in range(num):
		arr.append('?')
	return (','.join(arr))