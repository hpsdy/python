def create_args_string(num):
	'''
	����ָ�����ȵ�list������ռλ�������
	'''
	arr = []
	for n in range(num):
		arr.append('?')
	return (','.join(arr))