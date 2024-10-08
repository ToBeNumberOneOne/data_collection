# Data Collection

通过mqtt协议订阅数据然后保存到influxdb数据库中。

测试环境及版本 

paho.mqtt = 2.1.0

influxdb_client = 1.44.0

python = 3.12.4

influxdb = 2.7.7

## 部署

1. influxdb安装配置，创建org和bucket,创建token
   
2. 安装mqtt broker 
   
3. 拉取代码并安装requirements.txt
    
4. 修改配置文件和dataframe_handler中数据解析部分程序,然后运行app.py

## 注意事项

1. 请确保mqtt broker和influxdb服务正常运行
   
2. 请确保influxdb中org和bucket存在
   
3. 请确保mqtt broker和influxdb服务的端口配置正确
   
4. 请确保mqtt client id和topic配置正确

5. test_script中的mosquito_pub.py用于测试批量发送主题数据

## 存在的问题及优化点

1. 性能优化，可以引入批量写入或者异步数据库客户端工具来缓解数据库写入压力
   
2. 配置文件中包含敏感信息如token等，需要加密处理
   
3. 数据处理方式硬编码，如果数据格式发生改变则需要修改相应部分的代码

4. 没有针对各模块的单元测试，使得代码在修改和扩展时容易引入新的问题

5. bug 数据库掉线时缓存的信息插入的时间不对，并且并发增大时的线程不会关闭

6. 缺少对收到数据长度的校验，数据解析时可能出现异常



- influxdb默认数据存储位置  var/lib/influxdb/engine/data/