import sys
import urllib2
import re
import datetime

#function to remove duplicates from the list
def removeduplicates(x):
    returnlist = []
    for i in x:
        if i not in returnlist:
            returnlist.append(i)
    return returnlist
def is_valid_date(date, dateformat):
    try:
        datetime.datetime.strptime(date, dateformat)
        return True
    except ValueError:
        return False

#global lists
trIDs=[]
featureIDs=[]
TRList=[]
FeatureList=[]
DPIList=[]
SDKList=[]
format1 = "%Y-%m-%d"
format2 = "%Y-%m-%d %H:%M:%S"
build_provided=False
if(len(sys.argv) == 2):
    limit="50"
    from_date=""
    to_date=""
else:
    limit="1000"

epg_branch_list = ['EPG_2.16_27','EPG_2.14_27','EPG_2.15_27','EPG_3.7_28','EPG_3.9_28','EPG_3.10_28','EPG_3.11_28','EPG_3.12_28','EPG_3.13_28','EPG_3.14_28','EPG_3.15_28','EPG_3.16_28','EPG_3.17_28','EPG_3.18_28','EPG_3.19_28','EPG_3.20_28','EPG_3.21_28']

#buildUrlResponse = urllib2.urlopen("https://epgweb.sero.wh.rnd.internal.ericsson.com/deliverable/api/getDeliverablesForBuild?build_id=EPG_28R69TY01_210907_090244").read()
#contents = urllib2.urlopen("https://epgweb.sero.wh.rnd.internal.ericsson.com/build/api/getBuilds?limit=&filter[product_name]=EPG_3.18_28&filter[official]=1&end=2021-08-02%2007:38:14").read()

#help for script usage
if(len(sys.argv) == 1 or sys.argv[1] == "--help" or sys.argv[1] == "--h"):
    print "\nUsage - python gatherConsolidatedDeliverables.py <BranchName> <From Date/Build> <To Date/Build>\nBranchName is mandatory, rest are optional, if From,To information is not provided the last 50 builds are picked by default"
    print "\nUsage examples:\n\npython gatherConsolidatedDeliverables.py EPG_3.18_28\npython gatherConsolidatedDeliverables.py EPG_3.18_28 2021-09-06 2021-09-07\npython gatherConsolidatedDeliverables.py EPG_3.18_28 \"2021-09-06 09:06:20\" \"2021-09-07 14:05:17\"\npython gatherConsolidatedDeliverables.py EPG_3.18_28 EPG_28R63XV01_210906_090620 EPG_28R63XZ01_210907_140517"
    sys.exit()

#gather commandline arguments
if(len(sys.argv) < 2):
    print "\nERROR:Branch Information is missing"
    print "\nUsage - python gatherConsolidatedDeliverables.py <BranchName> <From Date/Build> <To Date/Build>\nBranchName is mandatory, rest are optional, if From,To information is not provided the last 50 builds are picked by default"
    print "\nUsage examples:\n\npython gatherConsolidatedDeliverables.py EPG_3.18_28\npython gatherConsolidatedDeliverables.py EPG_3.18_28 2021-09-06 2021-09-07\npython gatherConsolidatedDeliverables.py EPG_3.18_28 \"2021-09-06 09:06:20\" \"2021-09-07 14:05:17\"\npython gatherConsolidatedDeliverables.py EPG_3.18_28 EPG_28R63XV01_210906_090620 EPG_28R63XZ01_210907_140517"
    sys.exit()

#check for valid BranchName and fetch the same
if sys.argv[1] not in epg_branch_list:
    print "\nERROR:",sys.argv[1],"is not valid/supported EPG BranchName, Please enter a valid EPG brachName from below:\n",epg_branch_list
    print "\n\nFor help regarding script usage please use \"python gatherConsolidatedDeliverables.py --help\""
    sys.exit()
else:
    branchName=sys.argv[1]

#check for valid from/to date and fetch the same
if(len(sys.argv) > 2):
    if(len(sys.argv) < 4):
        print "\nERROR:Only From Date/Build is provided, please provide To Date/Build.\n\nUsage Examples below: \n\npython gatherConsolidatedDeliverables.py EPG_3.18_28\npython gatherConsolidatedDeliverables.py EPG_3.18_28 2021-09-06 2021-09-07\npython gatherConsolidatedDeliverables.py EPG_3.18_28 \"2021-09-06 09:06:20\" \"2021-09-07 14:05:17\"\npython gatherConsolidatedDeliverables.py EPG_3.18_28 EPG_28R63XV01_210906_090620 EPG_28R63XZ01_210907_140517"
        sys.exit()
    else:
        if re.search("EPG_28R", sys.argv[2]):
            build_provided=True
            fromdate=datetime.datetime.strptime(datetime.datetime.strptime("20"+sys.argv[2].split("_")[2]+" "+sys.argv[2].split("_")[3], '%Y%m%d %H%M%S').strftime('%Y-%m-%d %H:%M:%S'), format2)
            todate=datetime.datetime.strptime(datetime.datetime.strptime("20"+sys.argv[3].split("_")[2]+" "+sys.argv[3].split("_")[3], '%Y%m%d %H%M%S').strftime('%Y-%m-%d %H:%M:%S'), format2)
            if(fromdate < todate):
                from_date=str(fromdate - datetime.timedelta(seconds=7080)).replace(" ", "%20")
                to_date=str(todate - datetime.timedelta(seconds=6960)).replace(" ", "%20")
            else:
                from_date=str(todate - datetime.timedelta(seconds=7080)).replace(" ", "%20")
                to_date=str(fromdate - datetime.timedelta(seconds=6960)).replace(" ", "%20")
        else:
            if(is_valid_date(sys.argv[2], format1)):
                if(is_valid_date(sys.argv[3], format1)):
                    fromdate=datetime.datetime.strptime(sys.argv[2], format1)
                    todate=datetime.datetime.strptime(sys.argv[3], format1)
                    if(fromdate < todate):
                        from_date=str(fromdate - datetime.timedelta(seconds=7080)).replace(" ", "%20")
                        to_date=str(todate - datetime.timedelta(seconds=6960)).replace(" ", "%20")
                    else:
                        from_date=str(todate - datetime.timedelta(seconds=7080)).replace(" ", "%20")
                        to_date=str(fromdate - datetime.timedelta(seconds=6960)).replace(" ", "%20")
                else:
                    print "\nERROR: Invalid date format. Supported data formats are YYYY-MM-DD and YYYY-MM-DD HH:MM:SS"
                    sys.exit()
            elif(is_valid_date(sys.argv[2], format2)):
                if(is_valid_date(sys.argv[3], format2)):
                    fromdate=datetime.datetime.strptime(sys.argv[2], format2)
                    todate=datetime.datetime.strptime(sys.argv[3], format2)
                    if(fromdate < todate):
                        from_date=str(fromdate - datetime.timedelta(seconds=7080)).replace(" ", "%20")
                        to_date=str(todate - datetime.timedelta(seconds=6960)).replace(" ", "%20")
                    else:
                        from_date=str(todate - datetime.timedelta(seconds=7080)).replace(" ", "%20")
                        to_date=str(fromdate - datetime.timedelta(seconds=6960)).replace(" ", "%20")
                else:
                    print "\nERROR: Invalid date format. Supported data formats are YYYY-MM-DD and YYYY-MM-DD HH:MM:SS"
                    sys.exit()
            else:
                print "\nERROR: Invalid date format. Supported data formats are YYYY-MM-DD and YYYY-MM-DD HH:MM:SS"
                sys.exit()
                  
            
buildUrl="https://epgweb.sero.wh.rnd.internal.ericsson.com/build/api/getBuilds?limit="+limit+"&filter[product_name]="+branchName+"&filter[official]=1&from="+from_date+"&to="+to_date+"&filter[tags][version_update_build]=1"
buildUrlResponse = urllib2.urlopen(buildUrl).read()
buildIds=re.findall(r"EPG_28\w+", buildUrlResponse)
last_build=""
for i in range(10):
    if(len(buildIds[len(buildIds)-(i+1)].split("_")) == 4):
        last_build=buildIds[len(buildIds)-(i+1)]
        break
print "Gathering deliverables from ",last_build," to ",buildIds[0]
for buildId in buildIds:
    if(len(buildId.split("_")) > 4):
        continue
    deliverableUrl="https://epgweb.sero.wh.rnd.internal.ericsson.com/deliverable/api/getDeliverablesForBuild?build_id="+buildId
    deliverableUrlResponse=urllib2.urlopen(deliverableUrl).read()
    sdkIds=re.findall(r"Merge-branch-dev-\w+.\w+.\w+.\w+.\w+.\w+", deliverableUrlResponse)
    for sdkId in sdkIds:
        SDKList.append(sdkId.split("-")[3])
    trIDs=re.findall(r"PCTR-\w+", deliverableUrlResponse)
    for trId in trIDs:
        TRList.append(trId)
    DpIDs=re.findall(r"DPI-\w+.\w+.\w+-\w+", deliverableUrlResponse)
    for DpID in DpIDs:
        DPIList.append(DpID)
    featureIDs=re.findall(r"PCPB-\w+", deliverableUrlResponse)
    for featureID in featureIDs:
        FeatureList.append(featureID)
consolidatedTRList = removeduplicates(TRList)
consolidatedFeatureList = removeduplicates(FeatureList)
consolidatedDPIList = removeduplicates(DPIList)
consolidatedSDKList = removeduplicates(SDKList)
#print buildIds
print "\n\n**********   Consolidated Feature list   **********\n"
if consolidatedFeatureList:
    print consolidatedFeatureList
elif build_provided:
    print "No features were delivered across the builds"
else:
    print "No features were delivered across the builds generated during the provided dates"
print "\n\n**********  Consolidated DPI deliveries **********\n"
if consolidatedDPIList:
    print consolidatedDPIList
elif build_provided:
    print "No DPI deliveries found across the builds"
else:
    print "No DPI deliveries found across the builds generated during the provided dates"
print "\n\n**********  Consolidated SDK deliveries **********\n"
if consolidatedSDKList:
    print consolidatedSDKList
elif build_provided:
    print "No SDK deliveries found across the builds"
else:
    print "No SDK deliveries found across the builds generated during the provided dates"
print "\n\n**********     Consolidated TR list      **********\n"
if consolidatedTRList:
    print consolidatedTRList
    print "\n\nTo fetch the possible PCG TR candidates please use the below JIRA query"
    print "\nproject = \"PDU PC TR Tool\" AND key in ("+str(consolidatedTRList)[1:-1]+") and (\"Node product\" in (\"PCG 1 (AXM 901 07/1)\") or \"Impacted products and NFs (CNOM)\" in (PCG,PCUP) or \"Impacted products and NFs (CRE)\"  in (PCG,PCUP) or \"Impacted products and NFs (EPG 3)\"  in (PCG,PCUP) or \"Impacted products and NFs (PC ADP Reusable Service)\"  in (PCG) or \"Impacted products and NFs (PCC)\"  in (PCG) or \"Impacted products and NFs (PCG)\"  is not EMPTY  or \"Impacted products and NFs (PCUP)\"  is not EMPTY )"
    print "\n\nTo fetch the possible PCC TR candidates please use the below JIRA query"
    print "\nproject = \"PDU PC TR Tool\" AND key in ("+str(consolidatedTRList)[1:-1]+") and (\"Node product\" = \"PCC 1 (AXB 250 19/1)\" or \"Impacted products and NFs (CNOM)\" in (PCC,\"PC SM (cSMF & GW-C)\") or \"Impacted products and NFs (CRE)\"  in (PCC,\"PC SM (cSMF & GW-C)\") or \"Impacted products and NFs (EPG 3)\"  in (\"PC SM (cSMF & GW-C)\") or \"Impacted products and NFs (PC ADP Reusable Service)\"  in (PCC) or \"Impacted products and NFs (PCC)\" is not EMPTY  or \"Impacted products and NFs (PCG)\"  in (PCC) or \"Impacted products and NFs (PC SM (cSMF & GW-C))\"  is not EMPTY or \"Impacted products and NFs (PCUP)\"  in (PCC,\"PC SM (cSMF & GW-C)\") or \"Impacted products and NFs\"  in (PCC) or \"Impacted products and NFs (SGSN-MME)\" in (\"PCC - AMF\",\"PCC - AMF PCC - MME SGSN-MME - AMF SGSN-MME - SGSN SGSN-MME - MME\",\"PCC - AMF PCC - MME SGSN-MME - AMF SGSN-MME - SGSN SGSN-MME - MME\",\"PCC - AMF PCC - MME\",\"PCC - AMF PCC - SMF\",\"PCC - AMF SGSN-MME - AMF\",\"PCC - MME PCC - SMF\",\"PCC - AMF PCC - MME\",\"PCC - MME\"))"

elif build_provided:
    print "No TRs were delivered across the builds"
else:
    print "No TRs were delivered across the builds generated during the provided dates"

sys.exit()
