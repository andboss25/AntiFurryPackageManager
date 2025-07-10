
import json

def GetPackData(pack_name):
    pck = json.loads(open("pack.json","r").read())
    
    if pck.get(pack_name) == None:
        return False,None
    
    return True,pck[pack_name]['zip_locs']