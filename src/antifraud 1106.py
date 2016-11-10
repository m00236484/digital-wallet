
import sys

def read_file(inputFile):
      fileName = open(inputFile, 'r').readlines()
      fileBaseDir = "D:\\Projects\\PayMo\\fileBase\\"
      fileBaseBath = ""
      fileBase = ""
      outfile =""
      fileBaseName = ""
      firstLine = fileName.pop(0)
      id1 = 0
      id2 = 0
      userId = 0
      for line in fileName:
          data = line.split(",")
          #time, id1, id2, amount, message = data
          id1 = int(data[1])
          id2 = int(data[2])
          if id1 < id2:
            userId = id1
          else:
            userId = id2
          fileBaseName = getFileBase(userId)
          fileBaseBath = fileBaseDir + fileBaseName
          outfile = open(fileBaseBath, 'a+')
          outfile.write(str(id1) + "," + str(id2))
          outfile.write("\n")
          outfile.close()
      fileName.close()

def getFileBase(inUserID):
    # To generate partining file base ordered by userID
    # each file contains 10K Users ID
    initFileName = "fileBase_"
    fileBaseName = ""
    incrmRate = 10000
    minID = 0
    maxID = 10000
    fileFlag = False
    userID = int(inUserID)

    while fileFlag == False:
        if ( userID >= minID) & (userID < maxID  ):
            fileBaseName = initFileName + str(maxID)
            fileFlag = True
        else:
            minID = maxID
            maxID = maxID + incrmRate
    return fileBaseName


def main():
  # Get the name from the command line, using 'World' as a fallback.
  file_name = "D:\\Projects\\PayMo\\paymo_input\\batch_payment.csv"
  read_file(file_name)

# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
