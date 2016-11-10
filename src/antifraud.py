import os
import sys
import csv
import linecache
import ConfigParser
import glob
import platform

maxInt = sys.maxsize
def getConfigValues(section, configItem):

    retValue = ""
    config = ConfigParser.RawConfigParser()
    if platform.system() == 'Windows':
        config.read('configFile.cfg')
    else:
        config.read('./src/configFile.cfg')

    retValue = config.get(section,configItem)
    return retValue

def setConfigValues(section, configItem, configValue):
    print section
    config = ConfigParser.RawConfigParser()
    config.add_section(section)
    config.set(section, configItem , configValue)

    # Writing our configuration file to 'example.cfg'
    with open('configFile.cfg', 'wb') as configfile:
        config.write(configfile)


def test2(inputFile):
    inFile = open(inputFile, 'r').readlines()
    outFile = open('2.csv', 'w')
    firstLine = inFile.pop(0)
    listLines = []
    print  inputFile
    for line in inFile:
        data = line.split(",")
        raw = data[1] + "," +data[2]

        if raw in listLines:
            continue

        else:
            outFile.write(raw)
            listLines.append(raw)

    outFile.close()

    #inFile.close()

def createFileBase(inputFile):
    fileName = open(inputFile, 'r').readlines()
    fileBaseDir = "D:\\Projects\\PayMo\\fileBase\\"
    fileBaseBath = ""
    fileBase = ""
    outfile = ""
    fileBaseName = ""
    firstLine = fileName.pop(0)
    id1 = 0
    id2 = 0
    userId = 0
    for line in fileName:
        data = line.split(",")
        # time, id1, id2, amount, message = data
        id1 = int(data[1])
        id2 = int(data[2])
        if id1 < id2:
            userId = id1
        else:
            userId = id2
        fileBaseName = getFileBase(id1)
        fileBaseBath =  fileBaseName["fileBaseName"]
        outfile = open(fileBaseBath, 'a+')
        outfile.write(str(id1) + "," + str(id2))
        outfile.write("\n")
        outfile.close()

        fileBaseName = getFileBase(id2)
        fileBaseBath = fileBaseName["fileBaseName"]
        outfile = open(fileBaseBath, 'a+')
        outfile.write(str(id2) + "," + str(id1))
        outfile.write("\n")
        outfile.close()

    #fileName.close()


def iniFileBaseData(inputFile):
    # fileName = open(inputFile, 'r')
    fileBaseDir = "D:\\Projects\\PayMo\\fileBase\\"
    fileBaseBath = ""

    fileBaseName = ""
    # firstLine = fileName.pop(0)
    id1 = 0
    id2 = 0
    secondUser = 0
    userId = 0
    IndexNum = 0
    fileBaseDetail = {}
    csv_delimiter = ','
    debug = False
    csv.field_size_limit(sys.maxsize)
    userdata = {}
    sortedData= {}
    tempData = []
    with open(inputFile, 'rU') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
        data = list(csvreader)
    data.pop(0)
    for row in data:
        # line.pop(0)
        # data = line.split(",")

        outfile = ""
        # time, id1, id2, amount, message = data
        if len(row) < 1:
            print row
            continue
        try:
            id1 = int(row[1])
            id2 = int(row[2])
        except IOError as ioe:
            # print row
            # sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
            continue
        except Exception as e:
            # print row
            # sys.stderr.write("Caught Exception: " + repr(e) + "\n")
            continue
        '''
        if id1 < id2:
            userId = id1
            secondUser = id2
        else:
            userId = id2
            secondUser = id1
        '''
        if id1 in userdata.keys():
            tempData = userdata[id1]
            tempData.append(id2)
            userdata.update({id1: tempData})
        else:
            userdata.update({id1: [id2]})

        fileBaseDetail = getFileBase(id1)
        fileBaseName = fileBaseDetail["fileBaseName"]
        IndexNum = fileBaseDetail["IndexNum"]

    sortedData = sorted(userdata.iteritems())

    minID = 0
    maxId = 1000
    limited = 1000

    userdata.clear()
    userdata = dict(sortedData)
    fileName =  ""
    fileBaseDetail = {}
    csv_delimiter = ','
    print len(userdata)
    i = 0
    for key in userdata:
        print i
        i += 1
        if len(data) > 0 : del data[:]
        fileBaseDetail = getFileBase(key)
        fileBaseName = fileBaseDetail["fileBaseName"]
        IndexNum = fileBaseDetail["IndexNum"]
        with open(fileBaseName, 'r') as csvfile:
            csvreader1 = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
            data = list(csvreader1)
            csvfile.close()
        #data1 = data.split(",")
        data[IndexNum] = userdata[key]
        with open(fileBaseName, 'w') as file_handler:
            for item in data:
                file_handler.write("{}\n".format(item))
            file_handler.close()



def updateFileBaseData(fromUserID, toUserId):
    fileBaseDetail = {}
    userData = []
    userTrans = []
    fileBaseDetail = getFileBase(fromUserID)
    fileBaseName = fileBaseDetail["fileBaseName"]
    IndexNum = fileBaseDetail["IndexNum"]
    del userData[:]
    print fileBaseName
    with open(fileBaseName, 'r') as file_handler:
        userData = file_handler.readlines()
        file_handler.close()

    del userTrans[:]
    userTrans = userData[IndexNum]

    print str(fromUserID) + "---" + str(IndexNum)
    userTrans = "," + str(toUserId)
    userData[IndexNum] = userTrans

    del userData[:]

    fileBaseDetail = getFileBase(toUserId)
    fileBaseName = fileBaseDetail["fileBaseName"]
    IndexNum = fileBaseDetail["IndexNum"]
    with open(fileBaseName, 'r') as file_handler:
        userData = file_handler.readlines()
        file_handler.close()
    userTrans = userData[IndexNum]
    userTrans = "," + str(fromUserID)

    userData[IndexNum] = userTrans
    return 1


def streamProcessing(streamFile, outfil1 ,outfil2 , outfil3):
    # print "streamProcessing"
    csv_delimiter = ','
    debug = False
    csv.field_size_limit(sys.maxsize)
    with open(streamFile, 'rU') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
        data = list(csvreader)
        # print "****"
    if (len(data) > 0):
        data.pop(0)
    else:
        return 0
    for trans in data:
        try:
            id1 = int(trans[1])
            id2 = int(trans[2])
        except IOError as ioe:
            # print row
            # sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
            continue
        except Exception as e:
            # print row
            # sys.stderr.write("Caught Exception: " + repr(e) + "\n")
            continue

        if id1 < id2:
            userId = id1
            secondUser = id2
        else:
            userId = id2
            secondUser = id1

        paymentProcessing(userId, secondUser, outfil1 ,outfil2 , outfil3)


def paymentProcessing(fromUserId, toUserId, outfil1 ,outfil2 , outfil3):
    # print "****paymentProcessing"
    transStatus = "unverified"
    outputTrans = []
    transStatus , outputTrans = TransTo1stLevel(fromUserId, toUserId)

    if  (transStatus == "unverified"):
        transStatus = TransTo2ndLevel(fromUserId,toUserId , outputTrans)
        if (transStatus == "unverified"):
            #transStatus = TransTo4thLevel(fromUserId, toUserId, outputTrans)
            setTransOutput(transStatus, outfil1)
            setTransOutput(transStatus, outfil3)
        else:
            setTransOutput(transStatus, outfil2)
            setTransOutput(transStatus, outfil1)
    else:
        setTransOutput(transStatus, outfil1)
    #   setTransOutput(transStatus,2)
    #    if  (transStatus == "unverified"):
    #        transStatus = TransTo4thLevel(fromUserId,toUserId)
    #        setTransOutput(transStatus,4)
    return transStatus

def TransTo2ndLevel2(fromUserId, toUserId, TransUsers):
    #getFileBaseData(userId)
    print str(fromUserId )+ "----" + str(toUserId)
    transStatus = "unverified"
    transData = []
    #transData = getFileBaseData(fromUserId)
    transData = sorted(TransUsers)
    #print transData
    #print TransUsers
    i = 0
    commUserID = 0
    if len(transData) > 0:
        for data in transData:
            userid = data.split(",")
            # print userid[0] + "\\" + userid[1] + "***" + str(fromUserId) + "\\" + str(toUserId)
            if (fromUserId == int(userid[0])):
                commUserID = int(userid[1])
                for data2 in transData:
                    userid2 = data2.split(",")
                    if (commUserID ==  int(userid2[0])) & ((userid2[1]) == toUserId ):
                        print userid[0] + "\\" + userid[1] + "***" + str(fromUserId) + "\\" + str(toUserId)
                        transStatus = "trusted"
                        break
                    elif (commUserID ==  int(userid2[1])) & ((userid2[0]) == toUserId ):
                        transStatus = "trusted"
                        break
            if (fromUserId == int(userid[1])):
                commUserID = int(userid[0])
                for data2 in transData:
                    userid2 = data2.split(",")
                    if (commUserID ==  int(userid2[0])) & ((userid2[1]) == toUserId ):
                        transStatus = "trusted"
                        break
                    elif (commUserID ==  int(userid2[1])) & ((userid2[0]) == toUserId ):
                        transStatus = "trusted"
                        break
            if ( toUserId== int(userid[0])):
                commUserID = int(userid[1])
                for data2 in transData:
                    userid2 = data2.split(",")
                    if (commUserID ==  int(userid2[0])) & ((userid2[1]) == fromUserId ):
                        transStatus = "trusted"
                        break
                    elif (commUserID ==  int(userid2[1])) & ((userid2[0]) == fromUserId ):
                        transStatus = "trusted"
                        break
            if ( toUserId== int(userid[1])):
                commUserID = int(userid[0])
                for data2 in transData:
                    userid2 = data2.split(",")
                    if (commUserID ==  int(userid2[0])) & ((userid2[1]) == fromUserId ):
                        transStatus = "trusted"
                        break
                    elif (commUserID ==  int(userid2[1])) & ((userid2[0]) == fromUserId ):
                        transStatus = "trusted"
                        break

            else:
                transStatus = "unverified"

    return transStatus

# to get common user
def TransTo2ndLevel(fromUserId, toUserId, TransUsers):
    transStatus = "unverified"
    transData = []
    srcCommn = []
    #transData = sorted(TransUsers)
    commUserID = 0

    if len(TransUsers) > 0:
        print 1
        for data in TransUsers:
            userid = data.split(",")
            # print userid[0] + "\\" + userid[1] + "***" + str(fromUserId) + "\\" + str(toUserId)
            if (fromUserId == int(userid[0])):
                srcCommn = getFileBaseData(int(userid[1]))

                if len(srcCommn) > 0:
                    for retUsers in srcCommn:
                        #retUsers = data2.split(",")
                        if retUsers[1] == toUserId:
                            transStatus = "trusted"
                            print transStatus
                            break
            elif (fromUserId == int(userid[1])):
                srcCommn = getFileBaseData(int(userid[0]))
                if len(srcCommn) > 0:
                    for retUsers in srcCommn:
                        if retUsers[1] == toUserId:
                            transStatus = "trusted"
                            print transStatus
                            break
            if (toUserId == int(userid[0])):
                srcCommn = getFileBaseData(int(userid[1]))
                if len(srcCommn) > 0:
                    for retUsers in srcCommn:

                        #retUsers = data2.split(",")
                        if retUsers[1] == fromUserId:
                            transStatus = "trusted"
                            print transStatus
                            break
            elif (toUserId == int(userid[1])):
                srcCommn = getFileBaseData(int(userid[0]))
                if len(srcCommn) > 0:
                    for retUsers in srcCommn:

                        #retUsers = data2.split(",")
                        if retUsers[1] == fromUserId:
                            transStatus = "trusted"
                            print transStatus
                            break

    return transStatus

def TransTo1stLevel(fromUserId, toUserId):
    # print "********TransTo1stLevel"
    transStatus = "unverified"
    transData = []
    outputTrans = []
    transData = getFileBaseData(fromUserId)

    if len(transData) > 0:
        for userid in transData:
            # print userid[0] + "\\" + userid[1] + "***" + str(fromUserId) + "\\" + str(toUserId)
            if (toUserId == int(userid[0])) & (fromUserId == int(userid[1])):
                transStatus = "trusted"
                break
            elif (fromUserId == int(userid[0])) & (toUserId == int(userid[1])):
                transStatus = "trusted"
                break
            else:
                transStatus = "unverified"
                if (fromUserId == int(userid[0])):
                    outputTrans.append(userid[0] + "," + userid[1])
                elif(fromUserId == int(userid[1])):
                    outputTrans.append(userid[1] + "," +userid[0])
                if(toUserId == int(userid[0])):
                    outputTrans.append(userid[0] + "," + userid[1])
                elif(toUserId == int(userid[1])):
                    outputTrans.append(userid[1] + "," + userid[0])

    return transStatus , outputTrans



def TransTo4thLevel(fromUserId, toUserId):
    transStatus = "unverified"
    return transStatus


def setTransOutput(transStatus, outputFile):
    outfile = open(outputFile, 'a+')
    outfile.writelines(transStatus + "\n")
    outfile.close()


def getFileBaseData(userId):
    csv_delimiter = ','
    debug = False
    csv.field_size_limit(sys.maxsize)
    transData = []
    fileBaseDetail = {}
    fileBaseDetail = getFileBase(userId)
    fileBaseName = fileBaseDetail["fileBaseName"]
    IndexNum = fileBaseDetail["IndexNum"]
    try:
        #transData = linecache.getline(fileBaseName, IndexNum)
         with open(fileBaseName, 'rU') as csvfile:
          csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
          transData = list(csvreader)

    except IOError as ioe:
        debug = False
        # sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
    except Exception as e:
        debug = False
        # sys.stderr.write("Caught Exception: " + repr(e) + "\n")
    return transData


def getFileBase(inUserID):
    # To generate partining file base ordered by userID
    # each file contains 10K Users ID
    initFileName = "fileBase_"
    fileBaseName = ""
    incrmRate = 1000
    minID = 0
    maxID = 1000
    fileFlag = False
    userID = int(inUserID)
    IndexNum = 0
    fileBaseDetail = {}
    while fileFlag == False:
        if (userID >= minID) & (userID < maxID):
            fileBaseName = initFileName + str(minID)
            fileBaseName += ".csv"
            IndexNum = userID - minID
            fileBaseDetail["fileBaseName"] = fileBaseDir = "D:\\Projects\\PayMo\\fileBase\\" + fileBaseName
            fileBaseDetail["IndexNum"] = IndexNum
            fileFlag = True
        else:
            minID = maxID
            maxID = maxID + incrmRate
    return fileBaseDetail

def clearOutFile(outputDir):
    outputDir =  outputDir + '*'
    files = glob.glob(outputDir)
    for f in files:
        os.remove(f)

def main():
    # Get the name from the command line, using 'World' as a fallback.
    # read_file(file_name)
    #createFileBase(file_name)
    #setConfigValues('Directories' , 'outFile1', 'test')
    outputDir = getConfigValues('Directories', 'outputDir')
    clearOutFile(outputDir)

    if len(sys.argv) >= 4:
        file_name = sys.argv[1]
        streamFile = sys.argv[1]
        outfil1 = sys.argv[2]
        outfil2 = sys.argv[3]
        outfil3 = sys.argv[4]
    else:
        print "Use Default Runing !"
        file_name = getConfigValues('Directories', 'batchFile')
        streamFile = getConfigValues('Directories', 'streamFile')
        outfil1 = getConfigValues('Directories', 'outfil1')
        outfil2 = getConfigValues('Directories', 'outfil2')
        outfil3 = getConfigValues('Directories', 'outfil3')

        if getConfigValues('DataFiles', 'is_created') == '0':
            if len(file_name) > 0:
                iniFileBaseData(file_name)
            else:
                print "Warning: You have to define directory of input files!"

    streamProcessing(streamFile , outfil1 ,outfil2 , outfil3)


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
