# lineNumbers.py
# Purpose - A program that reads a file and output the content
# as numbered lines and paragraphs.
# The line numbers are formatted such that they are 
# right-justified in a field 5 characters wide, followed by a period, 
# then a space, then the line of text

# Name: Daeshaun Morrison
# Date: 10/7/2020

def main() :
    # Ask user what their input and output files are
    inputFileName = input("What's the input file's name?: ")
    onputFileName = input("What's the output file's name?: ")
    # Create a read or write object to handle data in the text
    inputFile = open(inputFileName, "r")
    outputFile = open(onputFileName, "w")

    count = 0
    # A for loop that runs as many times as the amount of lines in the text
    for eachLine in inputFile :
        # Count each line
        count = count + 1
        # store lines that are striped of white space
        formatLine = eachLine.strip()
        # Write formatted lines to user specified file.
        # If file doesn't exist, create it 
        outputFile.write(f"     {count}. {formatLine}\n")

    # Tell user the file name
    print(f"The output file {onputFileName} has been created in this directory!")
    # Close opened files 
    inputFile.close()
    outputFile.close()
# Start the program running
main()
