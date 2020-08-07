import matplotlib.pyplot as plt

def get_columns(total_count, source):
    with open(source, 'r') as content_file:
        content = content_file.read()
        pass
    counter=0
    prev=0
    for item in content.split():
        if (counter%total_count)==0:
            if counter>0:
                if line[0]<=prev:
                    print(line)
                    print("WRONG")
                    return
                yield line
                prev=line[0]
                pass
            line=[]
            pass
        line.append(float(item))
        counter+=1
        pass
    if counter>0:
        yield line
        pass
    pass

def prepare_data(compr,source, reg):
    hist=[0]*(100//compr+1)
    for (idn,count, attendance) in source:
        if idn in reg:
            index=int(attendance*100/compr)
            if index>=len(hist):
                print("out of range for id",idn)
                pass
            else:
                hist[index] += count
                pass
            pass
        pass
    return hist

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
kharkiv={168,169,170,171,172,173,174}
kharkiv_reg={175,176,177,178,179,180,181}
kherson={182,183,184,185,186}
khmel={187,188,189,190,191,192,193}
cherk={194,195,196,197,198,199,200}
chernivtsi={201,202,203,204}
chernihiv={205,206,207,208,209,210}
kyiv={211,212,213,214,215,216,217,218,219,220,221,222,223}
sebastopol={224,225}

west=zak|fra|lv|tern|khmel|chernivtsi|riv|vol
center=vin|krop|cherk|pol|dp
north=zhy|kyiv_reg|chernihiv|sumy|kyiv
east=dn|lg|kharkiv|kharkiv_reg
south=od|kherson|myk|zp|crimea|sebastopol
ua=west|east|north|south|center|{333}



#for item in get_columns(6,"elect/ukr_2019/3004-candidates.txt"):
#    print(item)
#    pass
