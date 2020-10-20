# numProcess.py
#  a simple program (numProcess.py) to read a
# collection of integers from a text file and produce a printed summary
#
# Name: Daeshaun Morrison
# Date: 10/6/2020

def main() :
    # User inputs file name that has numbers to calculate
    myFileName = input("What's your file name?(.txt): ")
    # Open that file by creating an object for it
        # Read this file
    myFile = open(myFileName, "r")
        # Write this file
    outFile = open("OUT"+ myFileName, "w")

    count = 1
    # Set the total, min and max value as 
    # the first value read from the file.
    minNum = int(myFile.readline().strip())
    maxNum = minNum
    total = minNum

    # Run as many times as there are values 
    # in the file
    for eachLine in myFile :
        eachNum = int(eachLine.strip())
        total = total + eachNum
        count = count + 1
        # If the read value is less than min num,
        #  set min to the new minNum
        if minNum > eachNum :
            minNum = eachNum
        # If the read value is more than max num,
        #  set max to the new maxNum
        elif maxNum < eachNum :
            maxNum = eachNum
    
    # avgNum = total / count

    # formatted_float = "{:.2f}".format(avgNum)

    avgNum = "{:10.2f}".format(total / count)
    # Write the result to an out file 
    # that starts with "OUT"
    outFile.write("-" * 32)
    outFile.write(f"""\n\
Number of values:     {count:7,}
Minimum value:        {minNum:7,}
Average value:        {avgNum}
Maximum value:        {maxNum:7,}                             
Total:                {total:7,}\
\n""")
    outFile.write("-" * 32 )
    # Tell user the file name
    print(f"The output file OUT{myFileName} has been created in this directory!")

    myFile.close()
    outFile.close()
main()