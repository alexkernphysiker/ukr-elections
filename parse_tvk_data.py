from bs4 import BeautifulSoup
import json
import requests 
import warnings
import contextlib
import requests
from urllib3.exceptions import InsecureRequestWarning

#codes of election districts
crimea={1,2,3,4,5,6,7,8,9,10}
vin={11,12,13,14,15,16,17,18}
vol={19,20,21,22,23}
dp={24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40}
dn={41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61}
zhy={62,63,64,65,66,67}
zak={68,69,70,71,72,73}
zp={74,75,76,77,78,79,80,81,82}
fra={83,84,85,86,87,88,89}
kyiv_reg={90,91,92,93,94,95,96,97,98}
krop={99,100,101,102,103}
lg={104,105,106,107,108,109,110,111,112,113,114}
lv={115,116,117,118,119,120,121,122,123,124,125,126}
myk={127,128,129,130,131,132}
od={133,134,135,136,137,138,139,140,141,142,143}
pol={144,145,146,147,148,149,150,151}
riv={152,153,154,155,156}
sumy={157,157,158,159,160,161,162}
tern={163,164,165,166,167}
kharkiv={168,169,170,171,172,173,174,175,176,177,178,179,180,181}
kherson={182,183,184,185,186}
khmel={187,188,189,190,191,192,193}
cherk={194,195,196,197,198,199,200}
chernivtsi={201,202,203,204}
chernihiv={205,206,207,208,209,210}
kyiv_city={211,212,213,214,215,216,217,218,219,220,221,222,223}
sebastopol={224,225}


west=zak|fra|lv|tern|khmel|chernivtsi|riv|vol
center=vin|krop|cherk|pol|dp
north=zhy|kyiv_reg|chernihiv|sumy|kyiv_city
east=dn|lg|kharkiv
south=od|kherson|myk|zp|crimea|sebastopol
ua=west|east|north|south|center


def parse_election_tvk_data(elect, page, region):
    old_merge_environment_settings = requests.Session.merge_environment_settings
    @contextlib.contextmanager
    def  no_ssl_verification():
        opened_adapters = set()
        def merge_environment_settings(self, url, proxies, stream, verify, cert):
            opened_adapters.add(self.get_adapter(url))
            settings = old_merge_environment_settings(self, url, proxies, stream, verify, cert)
            settings['verify'] = False
            return settings
        requests.Session.merge_environment_settings = merge_environment_settings
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', InsecureRequestWarning)
                yield
        finally:
            requests.Session.merge_environment_settings = old_merge_environment_settings

            for adapter in opened_adapters:
                try:
                    adapter.close()
                except:
                    pass

    def get_page(elect, page):
        with no_ssl_verification():
            link = f"https://www.cvk.gov.ua/pls/{elect}/{page}"
            link_response = requests.get(link)
            if link_response.status_code == 200:
                return link_response.text
            else:
                return ""

    def parse_distr(link):
        soup=BeautifulSoup(get_page(elect,link),features="lxml")
        for row in soup.find_all('tr')[1:]:
            item=[]
            for i in row.find_all('td'):
                item.append(i.text.strip())
            try:
                if int(item[0])>0:
                    yield item
            except:
                pass

    link_soup = BeautifulSoup(get_page(elect,page),features="lxml")
    for row in link_soup.find_all('a', href=True):
        try:
            if int(row.text) > 0:
                for item in parse_distr(row['href']):
                    yield item
        except:
            pass

def prepare_data(source, attendance, candidates):
    voices=dict()
    for c in candidates.keys():
        voices[c]=[0.0]*100
    for row in source:
            att=attendance(row)
            if att>0:
                index=int(att*100)
                if index>=0 and index<100:
                    for c in voices.keys():
                        voices[c][index] += float(row[candidates[c]])/1000000.0
    return voices

#for item in parse_election_tvk_data("vp2014","wp335pt001f01=702",ua):
#    print(item)