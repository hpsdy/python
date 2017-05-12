from urllib import parse
qs='appid=ios&sign=%24%7Bsign%7D&v=7.1.0&os=9.1.0&timestamp=1493010013044&bduss=BDUSS&location=40.0413624%2C116.2676376&cityid=100010000&cuid=ab7da4b328d542855d9d22d077af1de0&uuid=461543498&device=iPhone%206%20Plus&tn=ios&terminal_type=ios&swidth=1242&sheight=2208&net=wifi&channel=bainuo_wap&area_id=0&parent_area_id=0&area_type=0&sort_id=0&sub_category_id=898&category=0&catg=0&page_num=0&city_id=100010000&locate_city_id=100010000&uid=461543498&page_size=10'

r1 = parse.parse_qs(qs,True)
print(r1)


def t():
	pass


print(t)
print(type(t))

print(1,t())
print(2,type(t()))
import asyncio
if asyncio.iscoroutinefunction(t):
	print('yes')
t = asyncio.coroutine(t)
if asyncio.iscoroutinefunction(t):
	print('yes')
print(t)
print(type(t))