import re

class BgpNeighbor():
    def __init__ (self, ip):
        self.ip = ip
        self.rAS = None
        self.lAS = None
        self.descr = None
        self.remote_rid = None
        self.clid = None
        self.state = None
        self.NSRstate = None
        self.GRES = None
        self.RestartTime = None
        #self.Caps = []
        #self.afis = {}

    def stringer(self):
        print(self.ip + self.descr + self.rAS + self.remote_rid + self.state + self.NSRstate + self.GRES + self.RestartTime + self.warnings())

    def warnings(self):
        warnings = None
        if not self.ip == self.remote_rid:
            warnings += "IP not equal Remote_RID"
        return(warnings)

    def find_route(self):
        pass

class AFI():
    def __init__(self, name):
        self.name = name
        self.is_rrc = ''
        self.af_caps = []


def bgp_ne_s(list):
    neighbors = {}
    BN = {}
    BN['global'] = re.compile("^BGP neighbor is .*")
    BN['AS_line'] = re.compile("^ Remote AS [0-9]*, local AS [0-9]*,")
    BN['Descr'] = re.compile("^ Description:.*")
    BN['RID'] = re.compile("^ Remote router ID .*")
    BN['CLID'] = re.compile("^ Cluster ID .*")
    BN['state'] = re.compile("^  BGP state = [a-zA-Z]*, up for .*")
    BN['NSR_state'] = re.compile("^  NSR State: .*")
    BN['NSR_ready'] = re.compile("^  Non-stop routing is .*")
    BN['GRES_ready'] = re.compile("^  Graceful restart is .*")
    BN['RTI'] = re.compile("^  Restart time is .*")
    BN['Stale_path'] = re.compile("^  Stale path timeout time is .*")
    BN['MPCR'] = re.compile("^  Multi-protocol capability received")
    BN['NCap'] = re.compile("^  Neighbor capabilities:")
    BN['Route_refresh'] = re.compile("^    Route refresh: advertised(old + new) and received (old + new)")
    BN['Graceful_Restart'] = re.compile("^    Graceful Restart (GRAwareness): advertised")
    BN['4-byte_AS'] = re.compile("^    4-byte AS: advertised and received")
    BN['AFIIPv4'] = re.compile("^    Address family IPv4 Unicast:advertised and received")
    BGP_AFI = {}
    BGP_AFI['AF_start'] = re.compile("^ For Address Family: ")
    BGP_AFI['RRC'] = re.compile("^  Route-Reflector Client ")
    BGP_AFI['AFCaps'] = re.compile("^  AF-dependent capabilities:")
    BGP_AFI['GRES'] = re.compile("^    Graceful Restart capability")
    BGP_AFI['Pol_in'] = re.compile("^  Policy for incoming advertisements is ")
    BGP_AFI['Pol_out'] = re.compile("^  Policy for outgoing advertisements is")
    BGP_AFI['Pfx_data'] = re.compile("^  [0-9]* accepted prefixes[0-9]* are bestpaths")
    BGP_AFI['AIGP'] = re.compile("^  AIGP is enabled")
    state = "G"
    counter = 0
    for i in list:
        #        print(i)
        if BN['global'].match(i):
            state = "G"
            #            print ("Global")
            ip = i.replace("BGP neighbor is ", "")
            neighbors[ip] = BgpNeighbor(ip)
            counter += 1
        elif BN['AS_line'].match(i) and state == "G":
            #            print("found AS_line")
            split = re.split(",", i)
            ras = split[0].replace(" Remote AS ", "")
            neighbors[ip].rAS = ras
            #print(neighbors[ip].rAS)
        elif BN['Descr'].match(i) and state == "G":
            #print("Descr")
            descr = i.replace(" Description: ", "")
            neighbors[ip].descr = descr
        elif BN['RID'].match(i) and state == "G":
            #print("RID")
            neighbors[ip].remote_rid = i.replace(" Remote router ID ", "")
        #elif BN['CLID'].match(i) and state == "G":
            #print("CLID")
        elif BN['state'].match(i) and state == "G":
            state = "session"
            re.split(",", i)[0].replace("", "")
            #            print("state")
        #elif BN['NSR_state'].match(i) and state == "session":
            #print("NSR_state")
        #elif BN['NSR_ready'].match(i) and state == "session":
            #            print("NSR_ready")
        #elif BN['GRES_ready'].match(i) and state == "session":
            #            print("GRES_ready")
        #elif BN['RTI'].match(i) and state == "session":
            #            print("RTI")
        #elif BN['Stale_path'].match(i) and state == "session":
            #            print("Stale_path")
        #elif BN['MPCR'].match(i) and state == "session":
            #            print("MPCR")
        elif BN['NCap'].match(i) and state == "session":
            state = "Ncaps"
            #            print("NCap")
        #elif BN['Route_refresh'].match(i) and state == "Ncaps":
        #    print("Route_refresh")
        #elif BN['Graceful_Restart'].match(i) and state == "Ncaps":
        #            print("Graceful_Restart")
        #elif BN['4-byte_AS'].match(i) and state == "Ncaps":
        #            print("byte_AS")
        #elif BN['AFIIPv4'].match(i) and state == "Ncaps":
        #            print("AFIIPv4")
        elif BGP_AFI['AF_start'].match(i):
            state = "AFI"
#            print("AFI LINE")
        #elif BGP_AFI['RRC'].match(i) and state == "AFI":
#            print("RRC")
        #elif BGP_AFI['AFCaps'].match(i) and state == "AFI":
#            print("AFCaps")
        #elif BGP_AFI['GRES'].match(i) and state == "AFI":
#            print("GRES")
        #elif BGP_AFI['Pol_out'].match(i) and state == "AFI":
#            print("Pol_out")
        #elif BGP_AFI['Pol_in'].match(i) and state == "AFI":
#            print("Pol_in")
        #elif BGP_AFI['Pfx_data'].match(i) and state == "AFI":
#            print("Pfx_data")
        #elif BGP_AFI['AIGP'].match(i) and state == "AFI":
#            print("AIGP")
    print(counter)
    return neighbors

if __name__ == "__main__":
    f = open('bgp_example')
    data = bgp_ne_s(f)
    print(len(data))

