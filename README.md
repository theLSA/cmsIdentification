# cms识别工具cmsIdentification.py<br/>

### 概述<br/>

利用网站特有文件，独有文件的md5，关键字来识别cms，用协程提高识别速度。

### 功能描述<br/>

有5种识别模式
1.结合式：利用data.json的1400+指纹进行识别[关键字+md5]。<br/>
2.御剑式：利用御剑指纹识别的指纹进行识别[关键字]<br/>
3.主页式：利用fofa的规则对目标主页和返回头关键字进行识别[关键字]<br/>
该模式利用了[https://github.com/cuijianxiong/cmscan](https://github.com/cuijianxiong/cmscan)，感兴趣的读者可以访问该项目更新fofa规则，本人这里利用的还是老的规则<br/>
4.快速式：利用收集的cms00.txt进行识别[md5]<br/>
5.急速式：利用收集的cms1.txt进行识别[特有文件]<br/>

### 使用方法及效果图<br/>

python cmsIdentification.py http://www.xxx.com<br/>

御剑式：
![御剑式](https://github.com/theLSA/cmsIdentification/raw/master/demo/cms00.png)
<br/><br/>
快速式:
![快速式](https://github.com/theLSA/cmsIdentification/raw/master/demo/cms01.png)
<br/><br/>
急速式：
![急速式](https://github.com/theLSA/cmsIdentification/raw/master/demo/cms02.png)
<br/>

### 结语<br/>
改进方向：结合多种识别方式，形成统一的规则，就不用分那么多文件了。<br/>
由于时间仓促，脚本可能有Bug或不完善的地方，欢迎大家反馈或issue。<br/>
个人博客地址：http://www.lsablog.com

### 参考项目
https://github.com/cuijianxiong/cmscan
https://github.com/boy-hack/gwhatweb
https://github.com/junmoxiao/cms_identify