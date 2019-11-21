#!/usr/bin/python3

import pymysql

def msql(sql1):
    # 数据库配置
    db = pymysql.Connect(
        host='192.168.1.22',
        port=7306,
        user='root',
        passwd='123456',
        db='joom',
        charset='utf8'
    )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 查询语句
    sql = sql1
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results

    except:
        print('Error: 数据查询错误')

    # 关闭数据库连接
    db.close()

def mupdstesql(sql1):
    # 数据库配置
    db = pymysql.Connect(
        host='192.168.1.22',
        port=7306,
        user='root',
        passwd='123456',
        db='joom',
        charset='utf8'
    )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 查询语句
    sql = sql1
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print(sql)
        # 执行sql
        db.commit()

    except:
        print('Error: 数据查询错误')

    # 关闭数据库连接
    db.close()


# 获取订单中商品的sku

daipeisku_list = msql('SELECT product_sku FROM jorder')

# 删除重复数据
sku_b = []

# print(daipeisku_list)
for i in daipeisku_list:
    if i not in sku_b:
        sku_b.append(i)

print(sku_b)
f = 0
# 获取所有的虚拟sku列表
sku_list = msql('SELECT * FROM sku_xuni')
# 循环遍历sku列表
for row in sku_list:
    sku = row[0]
    xunisku = row[1]
    # print(xunisku)

    for row2 in sku_b:
        llsku = row2[0]
        daisku =";" + row2[0] + ";"
        # print(llsku)
        # print("111")


        if daisku in xunisku:
            f = f + 1
            updatesql = "UPDATE jorder SET product_sku = '" + str(sku) + "' WHERE product_sku = '" + str(llsku) +"'"
            mupdstesql(updatesql)
            print(f)
            # print("有匹配")
    # print(daipeisku_list)

# print(sku)
# print(xunisku)





