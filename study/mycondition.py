
import functools
import asyncio
import asyncio
import functools
def set_event(event):
    print('setting event in callback')
    event.set()
async def test(name, event):
    print('{} waiting for event'.format(name))
    await event.wait()
    print('{} triggered'.format(name))
async def main(loop):
    event = asyncio.Event()
    print('event start state: {}'.format(event.is_set()))
    loop.call_later(
        2, functools.partial(set_event, event)
    )
    await asyncio.wait([test('e1', event), test('e2', event)])
    print('event end state: {}'.format(event.is_set()))
loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.close()

'''
async def consumer(condition,name,second):
	await asyncio.sleep(1)
	#print('x')
	with await condition as x:
		print('y')
		ret = await condition.wait()	
		print(x,ret,'consumer')
		
async def producer(condition):
	print(1)
	await asyncio.sleep(2)
	#print(2)
	for n in range(1,3):
		print(3)
		with await condition:
			print(4)
			print('producer')
			await asyncio.sleep(5)
			condition.notify_all()
		
		#print(5)
def task_num():
	return asyncio.Task.all_tasks()
async def main(loop):
	#print('3:',task_num())
	condition = asyncio.Condition()
	task = loop.create_task(producer(condition))
	#print('8:',task_num())
	#task.cancel()
	#print('4:',task_num())
	consumers = [consumer(condition,name,index) for index,name in enumerate(('c1','c2'))]
	#print('5:',task_num())
	await asyncio.wait(consumers)
	#print('6:',task_num())
	task.cancel()
	#print('7:',task_num())
#print('1:',task_num())
loop = asyncio.get_event_loop()
#print('2:',task_num())
loop.run_until_complete(main(loop))
'''