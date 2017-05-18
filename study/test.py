#-*- coding:utf-8 -*-
import requests
import chardet
import io,sys 
from collections import Iterable,Iterator
from bs4 import BeautifulSoup 


html = """<div class="article block untagged mb15" id='qiushi_tag_119040409'>

<div class="author clearfix">
<a href="/users/33563226/" target="_blank" rel="nofollow">
<img src="//pic.qiushibaike.com/system/avtnew/3356/33563226/medium/20170410082148.JPEG" alt="豆豆她亲妈"/>
</a>
<a href="/users/33563226/" target="_blank" title="豆豆她亲妈">
<h2>豆豆她亲妈</h2>
</a>
<div class="articleGender womenIcon">47</div>
</div>



<a href="/article/119040409" target="_blank" class='contentHerf' >
<div class="content">



<span>最近总是听人说邻村有人和我长得像，这不闲着没事，我路过邻村，顺便问了一下，别说，还真有热心人，一个大姐非要去把她叫来和我说话，我怀着激动的心情等待着。<br/>一大会儿，大姐带着人远远的走来了，近了一看，我的个乖乖，门帘头，洼登眼，小嘴撅撅着，我的心啊，拔凉拔凉的，<br/>原来我在别人眼里是这个样的啊</span>


</div>
</a>





<div class="stats">
<span class="stats-vote"><i class="number">275</i> 好笑</span>
<span class="stats-comments">


<span class="dash"> · </span>
<a href="/article/119040409" data-share="/article/119040409" id="c-119040409" class="qiushi_comments" target="_blank">
<i class="number">3</i> 评论
</a>



</span>
</div>
<div id="qiushi_counts_119040409" class="stats-buttons bar clearfix">
<ul class="clearfix">
<li id="vote-up-119040409" class="up">
<a href="javascript:voting(119040409,1)" class="voting" data-article="119040409" id="up-119040409" rel="nofollow">
<i></i>
<span class="number hidden">276</span>
</a>
</li>
<li id="vote-dn-119040409" class="down">
<a href="javascript:voting(119040409,-1)" class="voting" data-article="119040409" id="dn-119040409" rel="nofollow">
<i></i>
<span class="number hidden">-1</span>
</a>
</li>

<li class="comments">
<a href="/article/119040409" id="c-119040409" class="qiushi_comments" target="_blank">
<i></i>
</a>
</li>

</ul>
</div>
<div class="single-share">
<a class="share-wechat" data-type="wechat" title="分享到微信" rel="nofollow">微信</a>
<a class="share-qq" data-type="qq" title="分享到QQ" rel="nofollow">QQ</a>
<a class="share-qzone" data-type="qzone" title="分享到QQ空间" rel="nofollow">QQ空间</a>
<a class="share-weibo" data-type="weibo" title="分享到微博" rel="nofollow">微博</a>
</div>
<div class="single-clear"></div>




</div>
"""

html = BeautifulSoup(html,'html.parser')
print(str(html.find('div',class_='content').span.string))
data = []
for x in html.find('div',class_='content').span.strings:
	data.append(x)


print('\n\n'.join(data))




