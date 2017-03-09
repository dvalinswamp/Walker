import re
class RDB:
    def __init__(self, direct_nexthop, rid, out_iface):
        self.direct_nexthop =direct_nexthop
        self.rid = rid
        self.out_iface = out_iface
        self.metric = ""

    def tostring(self):

        return(self.direct_nexthop+";"+ self.rid +";"+ self.out_iface
+";"+ self.metric)

class OSPFRoute:
    def __init__(self, prefix, ad, metric, type):
            self.protocol = "OSPF"
            self.prefix = prefix
            self.blocks = []
            self.ad = ad
            self.metric = metric
            self.type = type

    def addRDB(self, direct_nexthop, rid, out_iface):
        self.blocks.insert = RDB(direct_nexthop, rid, out_iface)

    def tostring(self):
        for i in self.blocks:
            print(self.prefix +";"+ self.ad +";"+ self.metric +";"+self.type +";"+
                  i.tostring()+self.warning())
        if (len(self.blocks)>=2):
            print("Warning! ECMP detected")

    def warinig(self):
        if (len(self.blocks)>=2):
            return("Warning! ECMP detected")

def ipv4_route_processing(list):

    REO = {}
    REO['routing_entry'] = re.compile("^Routing entry for .*")
    REO['Known_via'] = re.compile("^\s*Known via.*")
    REO['Installed'] = re.compile("^\s*Installed.*")
    REO['rdbs'] = re.compile("^\s*Routing Descriptor Blocks$")
    REO['from'] = re.compile("^\s*.*from.*via")
    REO['metric'] = re.compile("^\s*Route metric is")
    protocols = {}
    protocols['ospf'] = re.compile("ospf")
    protocols['bgp'] = re.compile("bgp")
    protocols['isis'] = re.compile("isis")

    state = "G"

    for i in list:
        i = i.strip('\n')
        print(i)
        if REO['routing_entry'].match(i) and state == "G":
            print("routing_entry")
            state = "I"
            prefix = re.split(" ", i)[3]
            #print (prefix)

        elif REO['Known_via'].match(i) and state == "I":
            print("Known_via")
            state = "I"
            split = (re.split(",", i))
            process = split[0].replace("  Known via ","").replace("\"", "").lstrip()
            distance = split[1].replace(" distance ", "").lstrip()
            metric = split[2].replace(" metric ", "").lstrip()
            type = split[3].replace(" type ", "").lstrip()
            #print (split)
            #print (process, distance, metric, type)
            if protocols['ospf'].match(process):
                route = OSPFRoute(prefix, distance, metric, type)
        elif REO['Installed'].match(i) and state == "I":
            print("Installed")
            state = "I"

        elif REO['rdbs'].match(i) and state == "I":
            print("rdbs")
            state = "RDB"

        elif REO['from'].match(i) and state == "RDB":
            print("from")
            split = (re.split(",", i))
            direct_nexthop = split[0].replace("\s", "").lstrip()
            rid = split[1].replace(" from ", "").lstrip()
            out_iface = split[2].replace(" via ", "").lstrip()
            print(direct_nexthop, rid, out_iface)
            route.blocks.append(RDB(direct_nexthop, rid, out_iface))

        elif REO['metric'].match(i) and state == "RDB":
            print("metric")
            metric = i.replace("Route metric is", "").replace("\s", "").lstrip()
            print(metric)
        else:
            print("Nevedomaja huinya. Sostojanie \"" + state + "\"; Line :" + i)

    return route

def

if __name__ == "__main__":
    f = open('route_sample')
    print(f)
    route = ipv4_route_processing(f)
    print(route.tostring())
