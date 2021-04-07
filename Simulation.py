from GrocceryStore import *

def main():
    my_GS, packet_dict = Utility.parseTestFile()
    my_GS = Utility.preProcessPackets(my_GS, packet_dict)
    my_GS.processPackets()
    finalTime = my_GS.computeEndTime()
    
    print("Finished at: t={} minutes".format(finalTime))

if __name__ == "__main__":
    main()