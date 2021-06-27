import  json
import csv


def readcsv(fname:str) -> (list):
    memdata = []
    with open(fname, newline='', encoding='utf-8') as csvfile:    
        for item in csvfile:
            item = item.encode('utf-8').decode('utf-8-sig').strip()
            data = item.split(',')
            memdata.append(data)
            #print(memdata)
    return memdata

def csv2json(uniquefname:str, commonfname:str) -> (dict):
    list_uniquedata = []
    list_commondata = []
    memdata = readcsv(uniquefname)
    commondata = readcsv(commonfname)

    for i in range(len(memdata)-1):
        member =  dict(zip(memdata[0], memdata[i+1]))            
        list_uniquedata.append(member)
    #print(list_uniquedata)


    # read common data merge both in a dict and write to output
    for i in range(len(commondata)-1):
        common = dict(zip(commondata[0], commondata[i+1]))
        list_commondata.append(common)
    #print(list_commondata)

    res_dict = {"common_data": list_commondata, "unique_data": list_uniquedata}

    return res_dict  
            


if __name__ == "__main__":
    uniquefname = input() #'./memberdata.csv'
    commonfname = input() #'./commondata.csv'
    try:
        list_res = csv2json(uniquefname, commonfname)
        out = (str(list_res))
        out = out.replace("'", '"')
        #print(str(list_res))
        resjson = './tmp.json'
    
        with open(resjson, 'w', newline='', encoding='utf-8') as outjson:
        #    json.dump(out.strip('"'), outjson, indent=4)
            outjson.write(out)
        print("Convert the data to tmp.json file!")
    except FileNotFoundError:
        print("Enter the right file name")
        pass
    
    
    