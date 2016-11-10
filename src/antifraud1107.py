import os
import sys
import csv
import linecache
maxInt = sys.maxsize


def streamProcessing(streamFile):
    #print "streamProcessing"
    csv_delimiter = ','
    debug = False
    csv.field_size_limit(sys.maxsize)
    with open(streamFile, 'rU') as csvfile:
      csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
      data = list(csvreader)
      #print "****"
    if (len(data) > 0):
        data.pop(0)
    else:
        return 0
    for trans in data:
        try:
            id1 = int(trans[1])
            id2 = int(trans[2])
        except IOError as ioe:
            #print row
            #sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
            continue
        except Exception as e:
            #print row
            #sys.stderr.write("Caught Exception: " + repr(e) + "\n")
            continue

        if id1 < id2:
          userId = id1
          secondUser = id2
        else:
          userId = id2
          secondUser = id1

        paymentProcessing(userId,secondUser)



def paymentProcessing(fromUserId,toUserId):
    #print "****paymentProcessing"
    transStatus = "unverified"

    transStatus = TransTo1stLevel(fromUserId,toUserId)
    setTransOutput(transStatus,1)

    #if  (transStatus == "unverified"):
    #    transStatus = TransTo2ndLevel(fromUserId,toUserId)
    #   setTransOutput(transStatus,2)
    #    if  (transStatus == "unverified"):
    #        transStatus = TransTo4thLevel(fromUserId,toUserId)
    #        setTransOutput(transStatus,4)
    return transStatus

def TransTo1stLevel(fromUserId,toUserId):
    #print "********TransTo1stLevel"
    transStatus = "unverified"
    transData = []
    transData = getFileBaseData(fromUserId)

    if len(transData) > 0:

        for userid in transData:
            #print userid[0] + "\\" + userid[1] + "***" + str(fromUserId) + "\\" + str(toUserId)
            if (toUserId == int(userid[0])) & (fromUserId == int(userid[1])):
                transStatus = "trusted"
                print userid[1] + "  " + userid[0] +" ****" + str(fromUserId) + "  " + str(toUserId) + "  " + transStatus
                break
            elif (fromUserId == int(userid[0]) ) & (toUserId == int(userid[1])):
                transStatus = "trusted"
                print userid[1] + "  " + userid[0] + " ****" + str(fromUserId) + "  " + str(toUserId) + "  " + transStatus
                break
            else:
                transStatus = "unverified"


    return transStatus

def TransTo2ndLevel(fromUserId,toUserId):
    transStatus = "unverified"
    transData = []

    transData = getFileBaseData(fromUserId)

    return transStatus

def TransTo4thLevel(fromUserId,toUserId):
    transStatus = "unverified"
    return transStatus

def setTransOutput(transStatus, outputLevel):
    outputFile = ""
    if (outputLevel == 1):
        outputFile = "output1.txt"
    elif (outputLevel == 2):
        outputFile = "output2.txt"
    else:
        outputFile = "output3.txt"

    outfile = open(outputFile, 'a+')
    outfile.writelines(transStatus+"\n")
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
        transData=  linecache.getline(fileBaseName, IndexNum)
        #with open(fileBaseName, 'rU') as csvfile:
        #  csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
        #  transData = list(csvreader)

    except IOError as ioe:
        debug = False
        #sys.stderr.write("Caught IOError: " + repr(ioe) + "\n")
    except Exception as e:
        debug = False
        #sys.stderr.write("Caught Exception: " + repr(e) + "\n")
    return transData

def updateFileBase(fromUserID, toUserId):
    return 1

def createFileBaseData(dirBath):
    initFileName = dirBath + "fileBase_"
    fileBaseName = ""
    incrmRate = 1000
    minID = 0
    maxID = 100000
    fileFlag = False
    userData = []
    while minID < maxID:
        if len(userData) > 0:  del userData[:]
        for i in range(0, incrmRate):
            userData.append(i+minID)
        fileBaseName = initFileName + str(minID)
        with open(fileBaseName, 'w') as file_handler:
            for item in userData:
                file_handler.write("{}\n".format(item))
            file_handler.close()
        minID += incrmRate


def setFileBaseData(inputFile):
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
    with open(inputFile, 'rU') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=csv_delimiter, quotechar='|')
        data = list(csvreader)

    data.pop(0)
    sortedData = sorted(data)
    for row in sortedData:
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

        if id1 < id2:
            userId = id1
            secondUser = id2
        else:
            userId = id2
            secondUser = id1

        if userId in userdata.keys():
            userdata["linkUsers"] += "," + secondUser
        else:
            userdata["IndexNum"] = userId
            userdata["linkUsers"] = secondUser
        fileBaseDetail = getFileBase(userId)
        fileBaseName = fileBaseDetail["fileBaseName"]
        IndexNum = fileBaseDetail["IndexNum"]
    print len(userdata)
    with open(fileBaseName, 'w') as csvfile:
        # fieldnames = ['IndexNum', 'linkUsers']
        csvWriter = csv.DictWriter(csvfile)  # , fieldnames=fieldnames)
        csvWriter.writerows(userdata)



        # print IndexNum
        # fileBaseBath = fileBaseDir + fileBaseName
        # outfile = open(fileBaseBath, 'a+')
        # outfile.writelines(str(secondUser)+",")
        # outfile.close()
        # fileName.close()


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
        if ( userID >= minID) & (userID < maxID  ):
            fileBaseName = initFileName + str(maxID)
            #fileBaseName += ".csv"
            IndexNum = userID - minID
            fileBaseDetail["fileBaseName"] = fileBaseDir = "D:\\Projects\\PayMo\\fileBase\\"+ fileBaseName
            fileBaseDetail["IndexNum"] = IndexNum
            fileFlag = True
        else:
            minID = maxID
            maxID = maxID + incrmRate
    return fileBaseDetail

def main():
  # Get the name from the command line, using 'World' as a fallback.
  dirBath = "D:\\Projects\\PayMo\\fileBase\\"
  file_name   = "D:\\Projects\\PayMo\\paymo_input\\batch_payment.csv"
  #streamFile  = "D:\\Projects\\PayMo\\paymo_input\\stream_payment.csv"
  #read_file(file_name)
  #streamProcessing(streamFile)
  createFileBaseData(dirBath)
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
