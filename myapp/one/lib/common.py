def create_args_string(num):
	'''
	鐢熸垚鎸囧畾闀垮害鐨刲ist锛屽苟鐢ㄥ崰浣嶇锛熷～鍏?
	'''
	arr = []
	for n in range(num):
		arr.append('?')
	return (','.join(arr))