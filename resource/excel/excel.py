import xlwt
import time
from resource.excel import excel
from app.config import  setting
from resource.googleapi.model.sheetapi import googleSheet
import web
import json
from flask import request
from io import StringIO
from resource.selenium.index import selenium
import logging
urls = (
 '/rim_request','rim_request',
 '/rim_export','rim_export',
 '/(.*)', 'index'
)
@excel.route('/download')
def write_excel(date = '2019-06-01'):
    google = googleSheet(sheetID = setting.google_sheet['new_joiner']['SAMPLE_SPREADSHEET_ID'],range = setting.google_sheet['new_joiner']['SAMPLE_RANGE_NAME'])
    value = google.read_excel()
    # 实例话一个excel对象
    ex = xlwt.Workbook()
    web.header('Content-type', 'application/vnd.ms-excel')  # 指定返回的类型
    web.header('Transfer-Encoding', 'chunked')
    web.header('Content-Disposition', 'attachment;filename="export.xls"')
    sheet = ex.add_sheet('Sheet1', cell_overwrite_ok=True)
    a = 0
    for i in range(len(value)):
        # 对result的每个子元素作遍历，
        if len(value[i]) > 1 and value[i][8] != '' and time.strptime( date, "%Y-%m-%d") <= time.strptime(value[i][8],"%d/%m/%Y"):
            for j in range(len(value[i])):
                # 将每一行的每个元素按行号i,列号j,写入到excel中。
                sheet.write(a, j, value[i][j])
            a = a + 1
    sio = StringIO.StringIO()
    ex.save(sio)

    return sio.getvalue()


@excel.route('/read')
def read_excel():

    google = googleSheet(sheetID=setting.google_sheet['new_joiner']['SAMPLE_SPREADSHEET_ID'],
                         range=setting.google_sheet['new_joiner']['SAMPLE_RANGE_NAME'])
    value = google.read_excel()
    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    list = []
    data = {}
    ID_list = log_read()
    print(ID_list)
    for i in range(len(value)):
        # 对result的每个子元素作遍历，
        if len(value[i]) > 1 and value[i][8] != '' and time.strptime(date,"%Y-%m-%d") <= time.strptime(value[i][8],"%d/%m/%Y") :
            if value[i][16] == "Yes":
                if value[i][0] in ID_list:
                    value[i].insert(0,'close')
                else:
                    value[i].insert(0,'open')
                list.append(value[i])

    data = {"status":0,"data":list}
    return json.dumps(data)



@excel.route('/searchdata' , methods = ['post'])
def get_excel_data():

    if request.method == 'POST':


        google = googleSheet(sheetID=setting.google_sheet['new_joiner']['SAMPLE_SPREADSHEET_ID'],
                             range=setting.google_sheet['new_joiner']['SAMPLE_RANGE_NAME'])
        value = google.read_excel()
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        list = []
        data = {}
        ID_list =  request.get_json('data')['Idlist']
        print(ID_list)

        for i in range(len(value)):
            # 对result的每个子元素作遍历，
            print(value[i][0])
            if value[i][0] in ID_list:
                list.append(value[i])
        se = selenium()
        se.index(excel_list=list)
        log_write(ID_list)
        return json.dumps({'status': 0, 'data':'success'})
    else :
        return json.dumps({'status': -1, 'data':'error'})

@excel.route('/log')
def log_write(ID):
    res = ','.join(str(v).strip() for v in ID)
    with open('test.txt', 'a') as f:
       f.write(res)
    return json.dumps({'status': -1,'data':'aaa'})


def log_read():
    list_id = []
    with open('test.txt','r') as f:
        list = f.read().split(',')
        for i in list:
            list_id.append(i.strip())
    return list_id
