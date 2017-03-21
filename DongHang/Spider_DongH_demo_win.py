#! coding:utf-8
import requests
import sys
from bs4 import BeautifulSoup
import csv
import urllib
import json
import time,datetime
import re
from adsl import Adsl
import codecs

reload(sys)
sys.setdefaultencoding('utf8')
headers = {'Host': 'www.ceair.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
           'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'X-Requested-With': 'XMLHttpRequest',
           'Cache-Control': 'max-age=0',
           'Referer': 'http://www.ceair.com/flight2014/tsn-can-160506_CNY.html',
           #'Content-Length': 276,
           'Cookie': 'Webtrends=111.160.254.58.1462351208398886; JSESSIONID=0000DuDwmvMYdgo7Wz4C30bzC4-:17o8bn5vs; __utma=101442195.150811979.1462349750.1462349750.1462349750.1; __utmb=101442195.7.9.1462350503370; __utmc=101442195; __utmz=101442195.1462349750.1.1.utmcsr=Baidu_pc|utmccn=znq|utmcmd=brandzone|utmctr=baoti; _pzfxuvpc=1462349750500%7C7252670210684283865%7C4%7C1462350503391%7C1%7C%7C9878633999122401270; _pzfxsvpc=9878633999122401270%7C1462349750500%7C4%7C; _pzfxsfc=u1.c1566.g1567.k1438553095041.pz; _gscu_1605927201=62349750ciitqd54; _gscs_1605927201=62349750biw0y254|pv:4; _gscbrs_1605927201=1; TRAVELLER=0000wpQ9eZeXQcrR2UbexpZ3lZy:1a1lkcgt1; _gsref_1605927201=http://www.ceair.com/flight2014/tsn-can-160426_CNY.html?utm_source=Baidu_pc&utm_medium=brandzone&utm_term=baoti&utm_campaign=znq&fc=u1.c1566.g1567.k1438553095041.pz; __utmt=1',
           'Connection': 'keep-alive'
           }


#爬取数据
##from_h:出发地 to_h： 到达地 date_h： 出发时间，
def data_Crawling(from_h,to_h,date_h,i_orgcity, i_dstCity):
    url = 'http://www.ceair.com/otabooking/flight-search!doFlightSearch.shtml?rand=0.9983412510479111'
    data ='searchCond={"tripType":"OW","adtCount":1,"chdCount":0,"infCount":0,"currency":"CNY","sortType":"a","segmentList":[{"deptCd":"'+from_h+'","arrCd":"'+to_h+'","deptDt":"'+date_h+'","deptCdTxt":"'+i_orgcity+'","arrCdTxt":"'+i_dstCity+'","deptCityCode":"'+from_h+'","arrCityCode":"'+to_h+'"}],"sortExec":"a","page":"0"}'
    try:
        resp1 = requests.post(url,data = data,headers = headers,timeout = 15)
        return resp1.text,resp1.status_code
    except requests.exceptions.ReadTimeout:
        return -1,-1
    except requests.exceptions.ConnectionError:
        return -2,-2
# 解析数据
def data_analyze(loaddata,filename):
    # 采用BeautifulSoup解析网页
    writer = csv.writer(codecs.open(filename, "a",encoding='GBK'), dialect='excel')
    # soup = BeautifulSoup(loaddata.decode('utf-8'), "html.parser")
    # info = soup.find_all("table",class_="__cabin_table__")
    #loaddata = json.loads(loaddata)
    #shopLandFlightResultNum = loaddata['shopLandFlightResultNum']
    #print loaddata

    # loaddata=json.loads( loaddata["airResultDto"])
    loaddata = loaddata['airResultDto']['productUnits']
    #print len(loaddata)
    for data in loaddata:
        productInfo_code=data['productInfo']['productCode']
        productInfo_name=str(data['productInfo']['productName']).encode('ISO-8859-1')
        saleprice = data['fareInfoView'][0]['fare']['salePrice']

        data = data['oriDestOption'][0]
        #print data
        data = data['flights'][0]
        arrivalAirport = str(data['arrivalAirport']['cityContext']).encode('ISO-8859-1') + str(data['arrivalAirport']['codeContext']).encode('ISO-8859-1')
        departureAirport = str(data['departureAirport']['cityContext']).encode('ISO-8859-1') + str(data['departureAirport']['codeContext']).encode('ISO-8859-1')
        arrivalAirportcode = data['arrivalAirport']['cityCode']
        departureAirportcode = data['departureAirport']['cityCode']

        arrivalDateTime= data['arrivalDateTime']
        departureDateTime=data['departureDateTime']
        flightNumber= data['flightNumber']
        marketingAirline = str(data['marketingAirline']['codeContext']).encode('ISO-8859-1')
        # print str(data['marketingAirline'])
        # print str(marketingAirline).encode('ISO-8859-1')
        #print str(u'\xe4\xb8\x9c\xe6\x96\xb9\xe8\x88\xaa\xe7\xa9\xba').encode('ISO-8859-1')
        operatingAirline = str(data['operatingAirline']['codeContext']).encode('ISO-8859-1')
        airEquipType= data['equipment']['airEquipType']
        duration= str(data['duration']).encode('ISO-8859-1')

        #print data
        reData = flightNumber+","+arrivalAirport+","+arrivalAirportcode+","+departureAirport+","+departureAirportcode+","+arrivalDateTime+","+departureDateTime+","+duration+","+airEquipType+","+marketingAirline+","+operatingAirline+","+productInfo_code+","+productInfo_name+","+saleprice
        writer.writerow([reData])
def city_to_code(i_orgcity,i_dstCity):
    #设置是否找到代码
    str_szm="WUS,CJU,HND,NRT,ZQZ,TLV,MFM,AKU,ALA,AAT,AMS,AAQ,TSE,AKA,AQG,AKL,MCO,ORL,BAR,BWI,BAK,CDG,DPS,BCN,PER,BAV,BSD,BHY,PEK,AEB,FRU,BOS,PDX,BUD,BHK,BNE,BRU,CZX,CHG,CTU,CIF,OKA,DRW,KIX,DLU,DLC,DAT,DQA,DXB,DIG,DTW,DOY,DUS,DNH,YTO,DSN,ENH,ERL,FRA,PHL,FOC,FUG,KVD,CPH,CAN,KWE,KWL,HRB,HIA,HAK,HMI,HLD,HAM,HZG,HDG,HGH,HFE,HTN,HAN,HEL,HET,WAW,WAS,JGD,JXA,IEV,KUL,TNA,KGD,JMU,JGN,JJN,JZH,KHG,KRT,CAI,CBR,CGN,KJA,CLE,KRL,KMG,LXA,LAS,LHW,RDM,LYS,RIX,LIS,LJG,LLB,LYI,KOJ,LON,LAD,LAX,MAD,MLA,GDX,MNL,NZH,BKK,LUM,MXP,MOW,MEL,MDG,MUC,KHN,NKG,NNG,NAO,NCE,NGB,NYC,PIT,HKT,NDG,JIQ,CIT,TAO,IQN,SYX,XMN,SWA,SHA,PVG,SZX,SHE,LED,SAN,SJW,SYM,STO,STR,ZRH,TCG,TAS,TPE,TYN,TVS,TCZ,TSN,THQ,TGO,TLQ,VAR,WEH,VCE,VIE,WEF,WNZ,WUA,ULN,HLH,URC,WUX,WUH,XIY,XNN,JHG,SEA,SYD,XIL,HKG,SIN,OVB,ACX,HOU,XUZ,YKS,ATL,YNT,ENY,YNJ,YNZ,SVX,IKT,YIN,YIH,INC,UYN,YCU,CTS,ZHA,DYG,CGQ,CSX,CIH,CGO,CHI,ZHY,CKG,ZUH,GVA,BKI,TYO,ADD,NBO,AUH,PUS,XNT,AOG,JNZ,LYA,NNY,IST,CCU,KOW,HTA,PO1,HAJ,ES1,DO1,DU1,DR1,BO1,MA1,BN1,HE1,HG1,CMB,BOM,KCA,BHX,ABJ,NUE,ODS,ROM,SFO,TRN,SCN,ATH,MEM,MAN,PHX,YVR,MLE,JIU,LYG,FLR,NTG,MIG,DEN,OAK,YYJ,BER,XFN,OSL,GOT,ZAG,BUH,PRG,CKY,MLW,DKR,FNA,FIH,BJL,YAO,TLS,BIO,PUW,GEG,ANC,EUG,SAC,SJC,BOI,PSC,YUL,ADL,WLG,KRY,DFW,YTY,JNG,MSO,RNO,MRS,SHP,BPE,NLT,YOW,ZYI,HJJ,MSP,HYN,BPL,YZY,HZH,IQM,YYC,MIA,YYT,YYG,YQM,YQT,YQB,YHZ,WNH,YIW,LZH,JUH,CGD,DDG,HEK,JDZ,JIL,KJI,LZO,MXZ,OHE,RLK,TEN,YBP,TXN,YIC,YIE,ZJO,LLV,JUZ,KHH,HEL,KHV,LYS,LCX,LPF,WDS"
    str_cs_cn="武夷山|济州|东京羽田|东京成田|张家口|特拉维夫|澳门|阿克苏|阿拉木图|阿勒泰|阿姆斯特丹|阿纳帕|阿斯塔纳|安康|安庆|奥克兰(新西兰)|奥兰多|奥兰多赫恩登|博鳌|巴尔蒂摩|巴库|巴黎|巴厘岛|巴塞罗那|柏斯|包头|保山|北海|北京|百色|比什凯克|波士顿|波特兰|布达佩斯|布哈拉|布里斯本|布鲁塞尔|常州|朝阳|成都|赤峰|冲绳|达尔文|大阪|大理|大连|大同|大庆|迪拜|迪庆|底特律|东营|杜塞尔多夫|敦煌|多伦多|鄂尔多斯|恩施|二连浩特|法兰克福|费城|福州|阜阳|甘贾|哥本哈根|广州|贵阳|桂林|哈尔滨|淮安|海口|哈密|海拉尔|汉堡|汉中|邯郸|杭州|合肥|和田|河内|赫尔辛基|呼和浩特|华沙|华盛顿|加格达奇|鸡西|基辅|吉隆坡|济南|加里宁格勒|佳木斯|嘉峪关|泉州|九寨沟|喀什|喀土穆|开罗|堪培拉|科隆|克拉斯诺亚尔斯克|克利夫兰|库尔勒|昆明|拉萨|拉斯维加斯|兰州|雷德蒙德|里昂|里加|里斯本|丽江|荔波|临沂|鹿儿岛|伦敦|罗安达|洛杉矶|马德里|马尔他|马加丹|马尼拉|满洲里|曼谷|芒市|米兰|莫斯科|墨尔本|牡丹江|慕尼黑|南昌|南京|南宁|南充|尼斯|宁波|纽约|匹兹堡|普吉|齐齐哈尔|黔江|奇姆肯特|青岛|庆阳|三亚|厦门|揭阳|上海虹桥|上海浦东|深圳|沈阳|圣彼得堡|圣地亚哥|石家庄|思茅|斯德哥尔摩|斯图加特|苏黎世|塔城|塔什干|台北桃园|太原|唐山|腾冲|天津|天水|通辽|吐鲁番|瓦纳|威海|威尼斯|维也纳|潍坊|温州|乌海|乌兰巴托|乌兰浩特|乌鲁木齐|无锡|武汉|西安|西宁|西双版纳|西雅图|悉尼|锡林浩特|香港|新加坡|新西伯利亚|兴义|休斯顿|徐州|雅库茨克|亚特兰大|烟台|延安|延吉|盐城|叶卡捷琳堡|伊尔库茨克|伊宁|宜昌|银川|榆林|运城|札幌|湛江|张家界|长春|长沙|长治|郑州|芝加哥|中卫|重庆|珠海|日内瓦|沙巴|东京|亚的斯亚贝巴|内罗毕|阿布扎比|釜山|邢台|鞍山|锦州|洛阳|南阳|伊斯坦布尔|加尔各答|赣州|赤塔|波茨坦|汉诺威|埃森|多特蒙德|杜伊斯堡|德累斯顿|波鸿|曼海姆|波恩|海德堡|哈根|科伦坡|孟买|库车|伯明翰|阿比让|纽伦堡|奥德萨|罗马|旧金山|都灵|萨尔布吕肯|雅典|孟菲斯|曼彻斯特|菲尼克斯|温哥华|马累|九江|连云港|佛罗伦萨|南通|绵阳|丹佛|奥克兰（美国）|维多利亚|柏林|襄阳|奥斯陆|哥德堡|萨格勒布|布加勒斯特|布拉格|科纳克里|蒙罗维亚|达喀尔|弗里敦|金沙萨|班珠尔|雅温得|图卢兹|毕尔巴鄂|普尔曼|斯波坎|安克雷奇|尤金|萨克拉门托|圣何塞|博伊西|帕斯科|蒙特利尔|阿德莱德|惠灵顿|克拉玛依|达拉斯|扬州|济宁|米苏拉|雷诺|马赛|秦皇岛(山海关)|秦皇岛(北戴河)|那拉提|渥太华|遵义|怀化|明尼阿波利斯|台州|博乐|张掖|黎平|且末|卡尔加里|迈阿密|圣约翰斯|夏洛特|蒙克顿|雷湾|魁北克|哈利法克斯|文山|义乌|柳州|九华山|常德|丹东|黑河|景德镇|吉林|喀纳斯|泸州|梅州|漠河|巴彦淖尔|铜仁|宜宾|黄山|宜春|阿尔山|张家口|吕梁|衢州|高雄|赫尔辛基|哈巴罗夫斯克|里昂|龙岩|六盘水|十堰"
    list_szm = str_szm.split(',')
    list_cs_cn = str_cs_cn.split('|')
    try:
        oflag = list_cs_cn.index(i_orgcity)
    except ValueError:
        print "对不起，不支持该出发地".encode("GBK")
        return -1,-1
    try:
        dflag = list_cs_cn.index(i_dstCity)
    except ValueError:
        print "对不起，不支持该目的地".encode("GBK")
        return -1,-1
    return (list_szm[oflag],list_szm[dflag])

#往返城市
def swap_o_d(i_dstCity, i_orgcity, i_startDate):
    # 出发城市代码
    # orgcity = "PEK"
    # 到达城市代码
    # dstCity = "CGO"
    # 将城市名转换成城市代码
    (orgcity, dstCity) = city_to_code(i_orgcity, i_dstCity)
    if(orgcity == -1 or dstCity == -1):
        return -1
    # 出发日期，格式为：2016-05-15
    startDate = i_startDate
    # 保存数据文件名
    currdatatime = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = "DongH-"+currdatatime+"-"+ startDate + ".csv"

    print "正在抓取和解析数据...".encode("GBK")
    for n in range(9):
        loaddata, status_code = data_Crawling(orgcity, dstCity, startDate,i_orgcity, i_dstCity)
        #超时异常处理，若是超时将等待6分钟
        if( loaddata == -1 or status_code == -1 ):
            print "请求超时,下次请求将在5s后进行,请耐心等待...".encode("GBK")
            aa = Adsl()
            aa.reconnect()
            time.sleep(5)
            continue
        elif( loaddata == -2 or status_code == -2 ):
            print "连接中断,下次请求将在5s后进行,请耐心等待...".encode("GBK")
            aa = Adsl()
            aa.reconnect()
            time.sleep(5)
            continue
        try:
            loaddata = json.loads(loaddata)
            #print loaddata
            flag = loaddata['airResultDto']
        except ValueError:
            #print loaddata
            print '页面抓取失败..,尝试重新抓取'.encode("GBK")
            aa = Adsl()
            aa.reconnect()
            time.sleep(5)
            continue
        except TypeError:
            #print loaddata
            print '页面抓取失败..,尝试重新抓取'.encode("GBK")
            aa = Adsl()
            aa.reconnect()
            time.sleep(5)
            continue
        except KeyError:
            #print loaddata
            print '页面抓取失败..,尝试重新抓取'.encode("GBK")
            aa = Adsl()
            aa.reconnect()
            time.sleep(5)
            continue
        #print loaddata

        if (flag!=None):
            break
            # IsDirect = loaddata['IsDirect']
            # if(IsDirect == True):
            #     break
            # else:
            #     return 0
        else:
            return 0
            # if (flag):
            #     return 0
            # else:
            #     print("抓取失败，3s后尝试第%d次抓取数据....." % n)
            #     #print loaddata,status_code
            #     time.sleep(3)
    if (n >= 8):
        print "抓取失败次数在太多了，无能为力...".encode("GBK")
        #fairleCount = fairleCount+1
        return -1

        # fp = open("data2.html",'w')
        # fp.write(loaddata)
        # fp.close()
        # fpr = open("data2.html")
        # loaddata = fpr.read()
        # fpr.close()
    data_analyze(loaddata, filename)
    # data_analyze(loaddata,"PEK-CAN2016-05-20.csv")


#主函数
def main():
    list_o_d = [('广州','上海浦东'),
                ('广州','上海虹桥'),
                ('上海浦东','厦门'),
                ('上海虹桥','厦门'),
                ('成都','深圳'),
                ('重庆','深圳'),
                ('杭州','深圳'),
                ('长沙','北京'),
                ('长沙','上海浦东'),
                ('长沙','上海虹桥'),
                ('喀什','乌鲁木齐'),
                ('成都','拉萨'),
                ('郑州','昆明'),
                ('贵阳','北京'),
                ('兰州','北京'),
                ('成都','杭州'),
                ('贵阳','深圳'),
                ('银川','北京'),
                ('昆明','丽江'),
                ('成都','南京'),
                ('重庆','西安'),
                ('重庆','长沙'),
                ('阿克苏','乌鲁木齐'),
                ('南昌','上海虹桥'),
                ('南昌','上海浦东'),
                ('武汉','厦门'),
                ('成都','长沙'),
                ('北京','珠海'),
                ('海拉尔','北京'),
                ('成都','丽江'),
                ('上海虹桥','揭阳'),
                ('杭州','贵阳'),
                ('重庆','济南'),
                ('杭州','厦门'),
                ('成都','青岛'),
                ('重庆','乌鲁木齐'),
                ('济南','西安'),
                ('西双版纳','丽江'),
                ('广州','义乌'),
                ('天津','西安'),
                ('杭州','天津'),
                ('广州','长春'),
                ('成都','兰州'),
                ('南昌','昆明'),
                ('广州','揭阳'),
                ('广州','桂林'),
                ('郑州','贵阳'),
                ('成都','石家庄'),
                ('大庆','北京'),
                ('贵阳','南京'),
                ('重庆','贵阳'),
                ('沈阳','深圳'),
                ('武夷山','厦门')]
    days = [3,7,14,21]
    for day in days:
        i_startDate = (datetime.datetime.now()+datetime.timedelta(days=day)).strftime('%Y-%m-%d')
        for data in list_o_d:
            i_orgcity = data[0]
            i_dstCity = data[1]
            #i_startDate = "2016-05-29"
            print "目前采集的数据信息为（往来航班）：".encode("GBK"), i_orgcity.encode("GBK"),i_dstCity.encode("GBK"),i_startDate.encode("GBK")
            flag1 = swap_o_d(i_dstCity, i_orgcity, i_startDate)
            if(flag1 == 0):
                print "查询当日无航班!或无直达航班".encode("GBK")
                continue
            elif(flag1 == -1):
                continue
            else:
                print '*********往，结束*********'.encode("GBK")
            #半中场休息
            time.sleep(3)
            flag2 = swap_o_d(i_orgcity, i_dstCity, i_startDate)
            if(flag2 == 0):
                print "查询当日无航班!或无直达航班".encode("GBK")
                continue
            elif(flag2 == -1):
                continue
            else:
                print '*********来，结束*********'.encode("GBK")
            #中场休息
            time.sleep(3)
    print "任务完成".encode("GBK")


if __name__ == "__main__":
    main()
    #( loaddata,code)= data_Crawling('WUH','XMN','2016-06-27','武汉','厦门')
    # print loaddata
    # with open("donghang.json",'w') as fp:
    #     json.dump(loaddata.encode('utf-8'),fp)
    # with open("donghang.json",'r') as fpr:
    #     loaddata = json.load(fpr)
    #data_analyze(loaddata,"shanh.csv")
