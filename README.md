# PDF_BatchDownload
功能：实现PDF的批量下载
使用步骤：
## 1. 将PDF的链接放在txt文本中
## 2. 运行PDF_Downloader的py脚本，将进行PDF文件的下载：
### get_raw_url函数：获取txt文本中的内容，返回一个含有pdf链接的url列表
#### get_File函数：
#### 参数urls：含有pdf链接的url列表
#### 参数progress：实例化的progress，用来记录下载的进度
#### 参数脚本的设定的睡眠时间，谨防被下载过快被断开网络
#### 参数flag记录下载文件的失败个数
#### 参数num_retries对于下载失败的文件会递归调用get_File函数再重试下载
#### Create_Excel函数：生成一个CSV：包含下载的URL，文件名字和该URL是否下载成功的情况
