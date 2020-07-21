生产脚本(Flask版本)  
Author：wameide   
Time: 2020.07  





#Python版本  
Python3.6  

#Flask框架  
pip install -i https://mirrors.aliyun.com/pypi/simple --default-timeout=6000 --trusted-host mirrors.aliyun.com flask==1.1.2  

#SQLAlchemy数据库框架  
pip install -i https://mirrors.aliyun.com/pypi/simple Flask-SQLAlchemy==2.4.1  

#MySQL驱动  
pip install -i https://mirrors.aliyun.com/pypi/simple flask-mysqldb==0.2.0 mysqlclient==1.4.6  

#内部有调用pymysql操作SQL  
pip install -i https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com pymysql==0.9.3  

#数据库迁移插件，生产不需要   
pip install -i https://mirrors.aliyun.com/pypi/simple flask-migrate==2.5.3  

#图片验证码  
pip install -i https://mirrors.aliyun.com/pypi/simple pillow==7.1.2  
验证码字体文件：/usr/share/fonts/arial.ttf  

#Form表单  
pip install -i https://mirrors.aliyun.com/pypi/simple flask-wtf==0.14.3  

#定时任务框架  
pip install -i https://mirrors.aliyun.com/pypi/simple APScheduler==3.6.3 Flask-APScheduler==1.11.0  



Jenkins的Dockerfile配置：  
JKPROJECT=opadmin  
REPOSITORY=registry-vpc.cn-hangzhou.aliyuncs.com  
NAMESPACE="xxxx"  
REP_USER='xxxx'  
REP_PASS='xxx'  
echo $REP_PASS|docker login --username=$REP_USER --password-stdin $REPOSITORY  
cat > Dockerfile << EOF  
FROM $REPOSITORY/$NAMESPACE/base:uwsgi-flask  
ENV FLASK_ENV="pro"  
ADD uwsgi.ini /etc/  
ADD nginx.conf /etc/nginx/conf.d/  
ADD manager.py /var/www/html/  
ADD yzgscript  /var/www/html/yzgscript  
RUN pip3 install --no-cache-dir --default-time=4000 -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com redis redis-py-cluster email xlwt xlrd elasticsearch XlsxWriter  
EOF  
docker build -t $REPOSITORY/$NAMESPACE/$JKPROJECT:latest .  
docker push $REPOSITORY/$NAMESPACE/$JKPROJECT:latest  
docker rmi $REPOSITORY/$NAMESPACE/$JKPROJECT:latest  