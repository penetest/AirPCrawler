import requests

h1 =""
h2 = ""
s = requests.Session()

resp1 = s.get('http://new.hnair.com/hainanair/ibe/deeplink/ancillary.do?DD1=2016-05-27&DD2=&TA=1&TC=0&TI=&ORI=PEK&DES=CAN&SC=Y&ICS=F&PT=F&PT=&FLC=1&NOR=&PACK=T')

resp2 = s.post('http://new.hnair.com/hainanair/ibe/deeplink/ancillary.do?DD1=2016-05-27&DD2=&TA=1&TC=0&TI=&ORI=PEK&DES=CAN&SC=Y&ICS=F&PT=F&PT=&FLC=1&NOR=&PACK=T&redirected=true')

resp3 = s.get('http://new.hnair.com/hainanair/ibe/deeplink/entryPointRedirect.do?QUERY=ancillaryIBESearch')

#resp4 = s.post('http://new.hnair.com/hainanair/ibe/deeplink/entryPointRedirect.do?redirected=true')

resp5 = s.get('http://new.hnair.com/hainanair/ibe/common/processSearchEntry.do?fromEntryPoint=true')

resp6 = s.get('http://new.hnair.com/hainanair/ibe/common/spinner.do')

#respwait = s.get('http://www.hnair.com/qt/dkggpic/wait/')

#resp7 = s.post('http://new.hnair.com/hainanair/ibe/common/processSearch.do')

#resp8 = s.get('http://new.hnair.com/hainanair/ibe/air/processSearch.do')

resp = s.get('http://new.hnair.com/hainanair/ibe/air/searchResults.do')

print resp.text




