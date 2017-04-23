class a(object):
	x = 100
	def __init__(self):
		self.x = self.x+1
		
a1 = a()
print(a1.x,a.x)
a2 = a()
print(a2.x,a.x)
a.x = 200
a3 = a()
print(a3.x,a.x)