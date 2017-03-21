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
h1 = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Encoding':'gzip, deflate, sdch',
      'Accept-Language':'zh-CN,zh;q=0.8',
      #Cookie:Webtrends=111.160.254.58.1464136223732083; BIGipServerpool_sc_122.119.122.51=830109562.20480.0000; JSESSIONID=0000M2suWXhIhzAP_5BzKDkE78S:1a5jgnqlj; OZ_1U_671=vid=v744f3c10a3ea8.0&ctime=1464140663&ltime=1464140662; OZ_1Y_671=erefer=-&eurl=http%3A//sc.travelsky.com/scet/queryAv.do%3Flan%3Dcn%26countrytype%3D0%26travelType%3D0%26cityNameOrg%3D%25E5%258C%2597%25E4%25BA%25AC%26cityCodeOrg%3DPEK%26cityNameDes%3D%25E5%258E%25A6%25E9%2597%25A8%26cityCodeDes%3DXMN%26takeoffDate%3D2016-05-28%26returnDate%3D2016-05-28%26cabinStage%3D0%26adultNum%3D1%26childNum%3D0&etime=1464139715&ctime=1464140663&ltime=1464140662&compid=671
      'Host':'www.scal.com.cn',
      'Proxy-Connection':'keep-alive',
      'Upgrade-Insecure-Requests':1,
      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
      }


#爬取数据
##from_h:出发地 to_h： 到达地 date_h： 出发时间，
def data_Crawling(from_h,to_h,date_h,i_orgcity, i_dstCity):
    s = requests.Session()
    data = '{"AirlineType":"Single","IsFixedCabin":false,"RouteList":[{"RouteIndex":1,"RouteName":"单    程","OrgCity":"'+from_h+'","DesCity":"'+to_h+'","OrgCityName":"'+i_orgcity+'","DesCityName":"'+i_dstCity+'","FlightDate":"'+date_h+'"}],"AVType":0}'
    #data = urllib.urlencode(data)
    data = urllib.quote(data)
    data = 'http://www.scal.com.cn/Web/ETicket/AirlineList?AirlineParamJSON='+data
    try:
        resp = s.post(data,timeout=15)
        url = re.search(r'arrPageValue.AirlineParamJSON = (.*?);',resp.text)
        #print url.group(1)
        data = json.loads( url.group(1))
        #print(data)
        data1 = re.search(r'arrPageValue.AirlineParamJSON = .*\[(.*?)\].*;',resp.text).group(1).replace("}","")
        #data1 = str(data['RouteList'][0]).replace("}","")
        data11 = data['AirlineType']
        data1 += ',\"AirlineType\":\"'+data11+'\"'
        data11 = data['AVType']
        data1 += ',\"AVType\":'+str(data11)
        data1 += ',\"CardFlag\":null'
        data11 = data['Flag']
        data1 += ',\"Flag\":null'
        data11 = data['BuyerType']
        data1 += ',\"BuyerType\":'+str(data11)
        data11 = data['IsFixedCabin']
        data1 += ',\"IsFixedCabin\":'+str(data11).lower()
        data11 = data['PassKey']
        data1 += ',\"PassKey\":\"'+data11+'\"}'
        data1 = json.loads(data1)
        resp1 = s.post('http://www.scal.com.cn/Web/ETicket/GetSingleChina',json=data1)
        return resp1.text,resp1.status_code
    except requests.exceptions.ReadTimeout:
        return -1,-1
    except requests.exceptions.ConnectionError:
        return -2,-2
    except AttributeError:
        #print resp.text
        return -1,-1
# 解析数据
def data_analyze(loaddata,filename,i_orgcity, i_dstCity):
    # 采用BeautifulSoup解析网页
    writer = csv.writer(codecs.open(filename, "a",encoding="GBK"), dialect='excel')
    # soup = BeautifulSoup(loaddata.decode('utf-8'), "html.parser")
    # info = soup.find_all("table",class_="__cabin_table__")
    # loaddata = json.loads(loaddata)
    #print loaddata

    loaddata=json.loads( loaddata["AirlineListJSON"])
    DesCity = loaddata['DesCity']
    #DesCityName = loaddata['DesCityName']
    DesCityName =i_orgcity
    OrgCity = loaddata['OrgCity']
    #OrgCityName = loaddata['OrgCityName']
    OrgCityName = i_dstCity
    FlightDateText = loaddata['FlightDateText']
    headinfo = DesCity+","+DesCityName+","+OrgCity+","+OrgCityName+","+FlightDateText
    #print len(loaddata['SRI_FlightList'])
    allpriceinfo = loaddata['SRI_FlightList']
    for price in allpriceinfo:
        #print price
        FlightNo = price["FlightNo"]
        PlaneModel = price["PlaneModel"]
        PlaneModelName = price["PlaneModelName"]
        TakeOffTimeShort = price["TakeOffTimeShort"]
        ArriveTimeShort = price["ArriveTimeShort"]
        TotalFlightTime = price["TotalFlightTime"]
        AirTax = str(price["AirTax"])
        #FlightCS = price["FlightCS"]
        info = headinfo+","+FlightNo+","+PlaneModel+","+PlaneModelName+","+TakeOffTimeShort+","+ArriveTimeShort+","+TotalFlightTime+","+AirTax

        CabinModel = price["CabinModel"]
        CabinRebate = CabinModel['CabinRebate']
        SellCode = CabinModel['SellCode']
        SaleRuleParam = CabinModel['SaleRuleParam']
        RealPriceText = str(CabinModel['RealPriceText'])
        CabinNO = CabinModel['CabinNO']
        OldPrice = str(CabinModel['OldPrice'])
        CheckINAndMeal = CabinModel['CheckINAndMeal']
        FareBasis = CabinModel['FareBasis']
        NewPrice = str(CabinModel['NewPrice'])
        OperateTypePrice = CabinModel['OperateTypePrice']
        RealPrice = str(CabinModel['RealPrice'])
        CabinRuleDescription = str(CabinModel['CabinRuleDescription']).replace(",",";")
        CabinName = CabinModel['CabinName']

        #info1= info+ ","+CabinRebate+","+SellCode+","+SaleRuleParam+","+RealPriceText+","+CabinNO+","+OldPrice+","+CheckINAndMeal+","+FareBasis+","+NewPrice+","+OperateTypePrice+","+RealPrice+","+CabinRuleDescription+","+CabinName
        info1 = info+ ","+RealPriceText+","+CabinNO
        writer.writerow([info1])
        SRI_CabinList = price["SRI_CabinList"]
        for CabinModel in SRI_CabinList:
            CabinRebate = CabinModel['CabinRebate']
            SellCode = CabinModel['SellCode']
            SaleRuleParam = CabinModel['SaleRuleParam']
            RealPriceText = str(CabinModel['RealPriceText'])
            CabinNO = CabinModel['CabinNO']
            OldPrice = str(CabinModel['OldPrice'])
            CheckINAndMeal = CabinModel['CheckINAndMeal']
            FareBasis = CabinModel['FareBasis']
            NewPrice = str(CabinModel['NewPrice'])
            OperateTypePrice = CabinModel['OperateTypePrice']
            RealPrice = str(CabinModel['RealPrice'])
            CabinRuleDescription = str(CabinModel['CabinRuleDescription']).replace(",",";")
            CabinName = CabinModel['CabinName']

            #info2 =  info+","+CabinRebate+","+SellCode+","+SaleRuleParam+","+RealPriceText+","+CabinNO+","+OldPrice+","+CheckINAndMeal+","+FareBasis+","+NewPrice+","+OperateTypePrice+","+RealPrice+","+CabinRuleDescription+","+CabinName
            info2 = info+ ","+RealPriceText+","+CabinNO
            writer.writerow([info2])
            #print loaddata["DefaultCabinRuleForCH"]

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
    filename = "ChuanH-"+currdatatime+"-"+ startDate + ".csv"

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
            flag = loaddata['Result']
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

        if (flag == True):
            IsDirect = loaddata['IsDirect']
            if(IsDirect == True):
                break
            else:
                return 0
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
    data_analyze(loaddata, filename,i_orgcity, i_dstCity)
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
    # ( loaddata,code)= data_Crawling('PEK','CAN','2016-06-28')
    # print loaddata
    # with open("chuanhang.json",'w') as fp:
    #     json.dump(loaddata,fp)
    # with open("chuanhang.json",'r') as fpr:
    #     loaddata = json.load(fpr)
    # data_analyze(loaddata,"shanh.csv")
