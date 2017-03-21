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
      'Host':'et.airchina.com.cn',
      'Proxy-Connection':'keep-alive',
      'Upgrade-Insecure-Requests':1,
      'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'
      }
#爬取数据
##from_h:出发地 to_h： 到达地 date_h： 出发时间，
def data_Crawling(from_h,to_h,date_h):
    s = requests.Session()
    dates = date_h.split('-')
    year = dates[0]
    month =  dates[1]
    day =  dates[2]
    try:
        resp =s.get('http://et.airchina.com.cn/InternetBooking/AirLowFareSearchExternal.do?&tripType=OW&searchType=FARE&flexibleSearch=false&directFlightsOnly=false&fareOptions=1.FAR.X&outboundOption.originLocationCode='+from_h+'&outboundOption.destinationLocationCode='+to_h+'&outboundOption.departureDay='+day+'&outboundOption.departureMonth='+month+'&outboundOption.departureYear='+year+'&outboundOption.departureTime=NA&guestTypes%5B0%5D.type=ADT&guestTypes%5B0%5D.amount=1&guestTypes%5B1%5D.type=CNN&guestTypes%5B1%5D.amount=0&pos=AIRCHINA_CN&lang=zh_CN&guestTypes%5B2%5D.type=INF&guestTypes%5B2%5D.amount=0',headers=h1,timeout=60)
        resp2 = s.post('http://et.airchina.com.cn/InternetBooking/AirLowFareSearchExt.do?ajaxAction=true',headers=h1,timeout=60)
        resp1 = s.get('http://et.airchina.com.cn/InternetBooking/AirFareFamiliesFlexibleForward.do',headers=h1,timeout=60)
        return resp1.text,resp1.status_code
    except requests.exceptions.ReadTimeout:
        return -1,-1
    except requests.exceptions.ConnectionError:
        return -2,-2

# 解析数据
def data_analyze(loaddata,filename,startdate):
    # 采用BeautifulSoup解析网页
    writer = csv.writer(codecs.open(filename, "a",encoding="GBK"), dialect='excel')
    #data = "\u003ctbody id=\"1123718803\"\u003e\n\t\t\t\t\t\t\u003ctr class=\"rowFirst rowOdd\"\u003e\n\t\t\u003ctd class=\"colFlight\"\u003e\n\t\t\t\u003cdiv\u003e\n\t\t\t\t\u003ca href=\"#\" onclick=\"javascript:showFlightDetailsPopUp(\'AirFlightDetailsGetAction.do?airlineCode=CA&flightNumber=1365&origin=PEK&destination=CAN&departureDay=28&departureMonth=5&departureYear=2016&classOfTravel=A&operatingAirlineCode=&cabinClass=First\');return false;\"\u003eCA1365\u003c/a\u003e\u003c/div\u003e\n\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colDepart\"\u003e\n\t\t\t\u003cdiv \u003e16:00\u003c/div\u003e\n            \u003c/td\u003e\n\t\t\u003ctd class=\"colArrive\"\u003e\n\t\t\t\u003cdiv \u003e19:25\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colAirports\"\u003e\n\t\t\t\t\u003cdiv\u003e\n\t\t\t\t\t\u003cspan onMouseOver=\"toolTip.over(this, event);\"\u003e\n\t\t\t\t\t\t\t\tPEK-CAN\u003cdiv class=\"toolTipInfo\"\u003e\n\t\t\t\t\t\t\t\t\t\u003cdiv class=\"simpleToolTip\"\u003e\u003cp\u003e\n\t\t\t\t\t\t\t\t\t\t北京首都国际机场 (PEK) - 广州白云机场 (CAN)\u003c/p\u003e\u003c/div\u003e\n\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\u003c/span\u003e\n\t\t\t\t\t\t\u003cspan id=\"ORIGIN_DESTINATION_0_0_0\" style=\"display:none\"\u003ePEK-CAN\u003c/span\u003e\n\t\t\t\t\t\u003cspan id=\"ITINERARY_0_0_0\" style=\"display:none\"/\u003e\n\t\t\t\t\t\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colType\"\u003e\n\t\t\t\t\u003cdiv\u003e\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\u003ca href=\"#\" onclick=\"javascript:showEquipmentTypePopUp(\'AirFlightEquipmentTypeAction.do?equipmentType=32A\');return false;\"\u003e32A\u003c/a\u003e\n\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003ctd id=\"itineraryPriceCell_0_43\" class=\"colCost colCost1 colCost_NDF\" rowspan=\"1\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t\u003ctable\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colRadio\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cinput type=\"radio\" name=\"flightItineraryId[0]\" value=\"43\" id=\"flightSelectGr_0_43\"  onclick=\"selectFareFamily(0, 0, \'NDF\'); fareFamiliesFlightSelection.selectFlight(this); reloadItinerarySummaryInfo(this)\" /\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colPrice\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003clabel for=\"flightSelectGr_0_43\"\u003e1,910\u003c/label\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\t\t\t\t\t\u003c/table\u003e\n\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colCostDetailsWrap\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c!----\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colLimSeat colLimSeatHot\" onMouseOver=\"toolTip.over(this, event)\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"toolTipInfo\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"simpleToolTip\"\u003e\u003cp\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t这个价格还\u003cb\u003e剩余8 个座位\u003c/b\u003e\u003cbr /\u003e\u003c/p\u003e\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cb\u003e8\u003c/b\u003e\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\u003cspan id=\"FARE_FAMILY_0_0_0_NDF\" style=\"display:none\"/\u003e\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003ctd id=\"itineraryPriceCell_0_\" class=\"colCost colCost2 colCostNotAvail colCost_NDC\" rowspan=\"1\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t-\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003ctd id=\"itineraryPriceCell_0_30\" class=\"colCost colCost3 colCost_NDY1\" rowspan=\"1\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t\u003ctable\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colRadio\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cinput type=\"radio\" name=\"flightItineraryId[0]\" value=\"30\" id=\"flightSelectGr_0_30\"  onclick=\"selectFareFamily(0, 0, \'NDY1\'); fareFamiliesFlightSelection.selectFlight(this); reloadItinerarySummaryInfo(this)\" /\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colPrice\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003clabel for=\"flightSelectGr_0_30\"\u003e1,890\u003c/label\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\t\t\t\t\t\u003c/table\u003e\n\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colCostDetailsWrap\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c!----\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\u003cspan id=\"FARE_FAMILY_0_0_0_NDY1\" style=\"display:none\"/\u003e\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003ctd id=\"itineraryPriceCell_0_13\" class=\"colCost colCost4 colCost_NDY2\" rowspan=\"1\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t\u003ctable\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colRadio\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cinput type=\"radio\" name=\"flightItineraryId[0]\" value=\"13\" id=\"flightSelectGr_0_13\"  onclick=\"selectFareFamily(0, 0, \'NDY2\'); fareFamiliesFlightSelection.selectFlight(this); reloadItinerarySummaryInfo(this)\" /\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colPrice\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003clabel for=\"flightSelectGr_0_13\"\u003e980\u003c/label\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\t\t\t\t\t\u003c/table\u003e\n\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colCostDetailsWrap\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c!----\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\u003cspan id=\"FARE_FAMILY_0_0_0_NDY2\" style=\"display:none\"/\u003e\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003ctd id=\"itineraryPriceCell_0_2\" class=\"colCost colCost5 colCost_NDY3 colCostLast\" rowspan=\"1\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t\u003ctable\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colRadio\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cinput type=\"radio\" name=\"flightItineraryId[0]\" value=\"2\" id=\"flightSelectGr_0_2\"  onclick=\"selectFareFamily(0, 0, \'NDY3\'); fareFamiliesFlightSelection.selectFlight(this); reloadItinerarySummaryInfo(this)\" /\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colPrice\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003clabel for=\"flightSelectGr_0_2\"\u003e650\u003c/label\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\t\t\t\t\t\u003c/table\u003e\n\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colCostDetailsWrap\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c!----\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\u003cspan id=\"FARE_FAMILY_0_0_0_NDY3\" style=\"display:none\"/\u003e\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003c/tr\u003e\n\u003c/tbody\u003e\n\t\t\t\t"

    #data = "\u003ctbody id=\"-108273447\"\u003e\n\t\t\t\t\t\t\u003ctr class=\"rowLast combineRows rowEven\"\u003e\n\t\t\u003ctd class=\"colFlight\"\u003e\n\t\t\t\u003cdiv\u003e\n\t\t\t\t\u003ca href=\"#\" onclick=\"javascript:showFlightDetailsPopUp(\'AirFlightDetailsGetAction.do?airlineCode=CA&flightNumber=4114&origin=PEK&destination=CTU&departureDay=28&departureMonth=5&departureYear=2016&classOfTravel=A&operatingAirlineCode=&cabinClass=First\');return false;\"\u003eCA4114\u003c/a\u003e\u003c/div\u003e\n\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colDepart\"\u003e\n\t\t\t\u003cdiv \u003e12:00\u003c/div\u003e\n            \u003c/td\u003e\n\t\t\u003ctd class=\"colArrive\"\u003e\n\t\t\t\u003cdiv \u003e15:10\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colAirports\"\u003e\n\t\t\t\t\u003cdiv\u003e\n\t\t\t\t\t\u003cspan onMouseOver=\"toolTip.over(this, event);\"\u003e\n\t\t\t\t\t\t\t\tPEK-CTU\u003cdiv class=\"toolTipInfo\"\u003e\n\t\t\t\t\t\t\t\t\t\u003cdiv class=\"simpleToolTip\"\u003e\u003cp\u003e\n\t\t\t\t\t\t\t\t\t\t北京首都国际机场 (PEK) - 成都双流机场 (CTU)\u003c/p\u003e\u003c/div\u003e\n\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\u003c/span\u003e\n\t\t\t\t\t\t\u003cspan id=\"ORIGIN_DESTINATION_0_9_0\" style=\"display:none\"\u003ePEK-CTU\u003c/span\u003e\n\t\t\t\t\t\u003cspan id=\"ITINERARY_0_9_0\" style=\"display:none\"/\u003e\n\t\t\t\t\t\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colType\"\u003e\n\t\t\t\t\u003cdiv\u003e\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\u003ca href=\"#\" onclick=\"javascript:showEquipmentTypePopUp(\'AirFlightEquipmentTypeAction.do?equipmentType=33A\');return false;\"\u003e33A\u003c/a\u003e\n\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003ctd id=\"itineraryPriceCell_0_47\" class=\"colCost colCost1 colCost_NDF\" rowspan=\"2\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t\u003ctable\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colRadio\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cinput type=\"radio\" name=\"flightItineraryId[0]\" value=\"47\" id=\"flightSelectGr_0_47\"  onclick=\"selectFareFamily(0, 9, \'NDF\'); fareFamiliesFlightSelection.selectFlight(this); reloadItinerarySummaryInfo(this)\" /\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colPrice\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003clabel for=\"flightSelectGr_0_47\"\u003e3,970\u003c/label\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\t\t\t\t\t\u003c/table\u003e\n\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colCostDetailsWrap\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c!----\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colLimSeat colLimSeatHot\" onMouseOver=\"toolTip.over(this, event)\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"toolTipInfo\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"simpleToolTip\"\u003e\u003cp\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t这个价格还\u003cb\u003e剩余2 个座位\u003c/b\u003e\u003cbr /\u003e\u003c/p\u003e\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cb\u003e2\u003c/b\u003e\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\u003cspan id=\"FARE_FAMILY_0_9_0_NDF\" style=\"display:none\"/\u003e\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003ctd id=\"itineraryPriceCell_0_\" class=\"colCost colCost2 colCostNotAvail colCost_NDC\" rowspan=\"2\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t-\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003ctd id=\"itineraryPriceCell_0_46\" class=\"colCost colCost3 colCost_NDY1\" rowspan=\"2\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t\u003ctable\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003ctr\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colRadio\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cinput type=\"radio\" name=\"flightItineraryId[0]\" value=\"46\" id=\"flightSelectGr_0_46\"  onclick=\"selectFareFamily(0, 9, \'NDY1\'); fareFamiliesFlightSelection.selectFlight(this); reloadItinerarySummaryInfo(this)\" /\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\u003ctd\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colPrice\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003clabel for=\"flightSelectGr_0_46\"\u003e3,030\u003c/label\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/tr\u003e\n\t\t\t\t\t\t\t\t\t\t\u003c/table\u003e\n\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"colCostDetailsWrap\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"specialFaresTick\" onMouseOver=\"toolTip.over(this,event)\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"toolTipInfo\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cdiv class=\"simpleToolTip\"\u003e\u003cp\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t行程中包含超级经济舱航段\u003c/p\u003e\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003cimg src=\"//static.airchina.wscdns.com/InternetBooking/pictures/icons/i_super_saver_tick.gif?version=201602241308\" width=\"24\" height=\"23\"\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\u003c!----\u003e\n\t\t\t\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\t\t\u003cspan id=\"FARE_FAMILY_0_9_0_NDY1\" style=\"display:none\"/\u003e\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003ctd id=\"itineraryPriceCell_0_\" class=\"colCost colCost4 colCostNotAvail colCost_NDY2\" rowspan=\"2\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t-\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003ctd id=\"itineraryPriceCell_0_\" class=\"colCost colCost5 colCostNotAvail colCost_NDY3 colCostLast\" rowspan=\"2\"\u003e\n\t\t\t\t\t\t\t\u003cdiv \u003e\n\t\t\t\t\t\t\t\t-\u003c/div\u003e\n\t\t\t\t\t\t\u003c/td\u003e\n\t\t\t\t\t\u003c/tr\u003e\n\u003ctr class=\"rowLast connectedRow rowEven\"\u003e\n\t\t\u003ctd class=\"colFlight\"\u003e\n\t\t\t\u003cdiv\u003e\n\t\t\t\t\u003ca href=\"#\" onclick=\"javascript:showFlightDetailsPopUp(\'AirFlightDetailsGetAction.do?airlineCode=CA&flightNumber=4303&origin=CTU&destination=CAN&departureDay=28&departureMonth=5&departureYear=2016&classOfTravel=A&operatingAirlineCode=&cabinClass=First\');return false;\"\u003eCA4303\u003c/a\u003e\u003c/div\u003e\n\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colDepart\"\u003e\n\t\t\t\u003cdiv \u003e17:00\u003c/div\u003e\n            \u003c/td\u003e\n\t\t\u003ctd class=\"colArrive\"\u003e\n\t\t\t\u003cdiv \u003e19:25\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colAirports\"\u003e\n\t\t\t\t\u003cdiv\u003e\n\t\t\t\t\t\u003cspan onMouseOver=\"toolTip.over(this, event);\"\u003e\n\t\t\t\t\t\t\t\tCTU-CAN\u003cdiv class=\"toolTipInfo\"\u003e\n\t\t\t\t\t\t\t\t\t\u003cdiv class=\"simpleToolTip\"\u003e\u003cp\u003e\n\t\t\t\t\t\t\t\t\t\t成都双流机场 (CTU) - 广州白云机场 (CAN)\u003c/p\u003e\u003c/div\u003e\n\t\t\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\t\t\t\t\u003c/span\u003e\n\t\t\t\t\t\t\u003cspan id=\"ORIGIN_DESTINATION_0_9_1\" style=\"display:none\"\u003eCTU-CAN\u003c/span\u003e\n\t\t\t\t\t\u003cspan id=\"ITINERARY_0_9_1\" style=\"display:none\"/\u003e\n\t\t\t\t\t\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003ctd class=\"colType\"\u003e\n\t\t\t\t\u003cdiv\u003e\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\u003ca href=\"#\" onclick=\"javascript:showEquipmentTypePopUp(\'AirFlightEquipmentTypeAction.do?equipmentType=321\');return false;\"\u003e321\u003c/a\u003e\n\t\t\t\t\t\t\u003c/div\u003e\n\t\t\t\u003c/td\u003e\n\t\t\u003c/tr\u003e\n\u003c/tbody\u003e\n\t\t\t\t"
    # soup = BeautifulSoup(data.decode('utf-8'), "html.parser")
    #print data.replace('\u003c','<').replace('\u003e','>')

    loaddata =loaddata.replace('\u003c','<').replace('\u003e','>')
    #print loaddata
    datas = re.findall(r'\"-?[\d]{3,10}\": \"(.*?)</tbody>',loaddata)
    #print datas
    for data in datas:
        #默认是国航
        cy="中国国际航空股份有限公司"
        soup = BeautifulSoup(data.encode("utf-8"), "html.parser")
        #leng1 = len( re.findall(r'<tr class=\\"rowLast combineRows rowEven\\">',data))
        leng2 = len( re.findall(r'<tr class=\\"[\w]*\s?combineRows\s?[\w]*\\">',data))
        if(leng2 >0):
            continue
        #print soup.prettify()
        #info = soup.find("a")
        #print info.text
        #print soup.td.find_all_next(text=True)
        #print data
        flightNo =  soup.td.find_all_next(text=True)[2]
        index = 6
        #print str(soup.td.find_all_next(text=True)[6])
        if(str(soup.td.find_all_next(text=True)[6]).find("承运航空公司")== -1):
            pass
        else:
            cy = str(soup.td.find_all_next(text=True)[6]).split("：")[1]
            index = index + 6
        #print index
        if(str(soup.td.find_all_next(text=True)[index]).find("中途停靠") == -1):
            pass
        else:
            index = index + 7
        #print index
        startd= soup.td.find_all_next(text=True)[index]
        index +=4
        endd= soup.td.find_all_next(text=True)[index]
        if(soup.td.find_all_next(text=True)[index+1] == '+1'):
            index+=1
        #aircode =  soup.td.find_all_next(text=True)[index+5]
        air =  soup.td.find_all_next(text=True)[index+7]
        air = str(air).replace('\\n\\t\\t\\t\\t\\t\\t\\t\\t\\t\\t','').split("-")
        aircode =  soup.td.find_all_next(text=True)[index+11].split("-")
        flighttype =  soup.td.find_all_next(text=True)[index+18]
        info = cy+","+flightNo+","+startdate+","+startd+","+endd+","+air[0]+","+air[1]+","+aircode[0]+","+aircode[1]+","+flighttype
        priceinfos =  soup.find_all(id=re.compile(r'\\"itineraryPriceCell_[\d]{0,2}_[\d]{0,2}\\"(.*?)'))
        #print price
        #priceinfos = re.findall(r'<td id=\\"itineraryPriceCell_[\d]{0,2}_[\d]{0,2}\\"(.*?)</td>',data)
        #print priceinfos
        for price in priceinfos:
            price = re.findall(r'<label for=\'\\"flightSelectGr_[\d]{0,2}_[\d]{0,2}\\"\'>(.*?)</label>',str(price))
            if(len(price) < 1):
                info = info + ","+"-"
            else:
                info = info +',' +str(price[0]).replace(",","")
        #print(info)
        writer.writerow([info])

#将城市名转化成城市代码
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
    filename = "GH-"+currdatatime+"-"+ startDate + ".csv"

    print "正在抓取和解析数据...".encode("GBK")
    for n in range(9):
        loaddata, status_code = data_Crawling(orgcity, dstCity, startDate)
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
        soup = BeautifulSoup(loaddata.decode('utf-8'), "html.parser")
        loaddata =loaddata.replace('\u003c','<').replace('\u003e','>')
        datas = re.findall(r'\"-?[\d]{3,10}\": \"(.*?)</tbody>',loaddata)
        if (len(datas) < 1):
            if (soup.title.string == "错误"):
                return 0
            else:
                print("抓取失败，3s后尝试第%d次抓取数据.....".encode("GBK") % n)
                #print loaddata,status_code
                time.sleep(3)
        else:
            break
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
    data_analyze(loaddata, filename,i_startDate)
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
                print "抱歉，该日期无座位或航班。".encode("GBK")
                continue
            elif(flag1 == -1):
                continue
            else:
                print '*********往，结束*********'.encode("GBK")
            #半中场休息
            time.sleep(3)
            flag2 = swap_o_d(i_orgcity, i_dstCity, i_startDate)
            if(flag2 == 0):
                print "抱歉，该日期无座位或航班。".encode("GBK")
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
    # loaddata,code =data_Crawling('WUS','SZX',"2016-05-31")
    # with open("guohang3.html","w") as fp:
    #     fp.write(loaddata)
    # with open("guohang2.html","r") as fpr:
    #     loaddata = fpr.read()
    # data_analyze(loaddata,"guoh.csv","2016-05-31")
