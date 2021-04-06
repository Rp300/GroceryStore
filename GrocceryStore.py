from os import times
import sys
from collections import deque

class customer:

    def __init__(self, type, arrivalTime, items) -> None:

        self.type = type
        self.arrivalTime = arrivalTime
        self.items = items
    
    def __str__(self):
        return str((self.type, self.arrivalTime, self.items))
    
    def updateItemCount(self, itemsProcessed):
        if self.items < itemsProcessed:
            self.items = 0
            return itemsProcessed-self.items
        else:
            rem = self.items - itemsProcessed
            self.items-=itemsProcessed
            return rem

class packet:

    def __init__(self, time, customer_list) -> None:
        self.time = time
        self.customer_list = customer_list

    def __str__(self) -> str:
        return str(self.customer_list)


class GrocceryStore:

    def __init__(self,register_count) -> None:
        self.time = 0
        self.register_count = 0
        self.timePacketList = []
        self.registers = []

        for i in range(1, register_count+1):
            self.registers.append(register(i, i == register_count))

    def addTimePacket(self, timePacket):
        self.timePacketList.append(timePacket)
    
    def processPacket(self):
        p = self.timePacketList.pop(0)

        # Propogate new time
        updated_time = p.time
        self.updateTime(updated_time)

        # Iterate through customers per packet
        for next_customer in p.customer_list:
            self.pushCustomer(next_customer)
        
    
    def updateTime(self, newTime):
        for r in self.registers:
            r.updateTime(newTime)
        self.time = newTime
    
    def pushCustomer(self, next_customer):
        type = next_customer.type

        if type == 'A':
            curr_register = self.findRegisterA()
            curr_register.pushCustomer(next_customer)
        elif type == 'B':
            minItems = float('Inf')
            curr_register = None

            for r in self.registers:
                custCount = r.peekLastCustomer()
                if custCount < minItems:
                   minItems = custCount
                   curr_register = r
                # Add a check if none are found
            curr_register.pushCustomer(next_customer)

    def findRegisterA(self):
        return sorted(self.registers, key=lambda x: (-x.numberCustomers))[0]
    
        

class register:

    def __init__(self, number, training) -> None:
        self.time = 0
        self.numberCustomers = 0
        # self.number = number
        # self.training = training
        self.rate = 0.5 if training else 1
        self.customers = deque([])

    
    def updateTime(self, newTime):
        timeElapsed = newTime - self.time
        itemsProcessed = self.rate * timeElapsed

        while len(self.customers) > 0 and itemsProcessed > 0:
            front_customer = self.customers[0]
            rem = front_customer.updateItemCount(itemsProcessed)
        
            if front_customer.items == 0:
                self.customers.popleft()
                self.numberCustomers-=1
            itemsProcessed = rem
        self.time = newTime
    
    def pushCustomer(self,next_customer):
        self.customers.append(next_customer)
        self.numberCustomers+=1
    
    def peekLastCustomer(self):
        if self.numberCustomers == 0:
            return 0
        else:
            return self.customers[-1].items

    def computeEndTime(self):
        if self.customers: 
            items = 0
            timeRemaining = 0
            for c in self.customers:
                items+=c.items
            timeRemaining = items/self.rate

            return self.time+timeRemaining
        else:
            return self.time

def main():
    input_file = sys.argv[1]
    f = open(input_file, "r")

    register_count = int(f.readline())
    my_GS = GrocceryStore(register_count)

    # Create customer time packet dictionary
    d = {}
    for l in f:
        new_customer = l.split()
        new_customer = customer(new_customer[0],int(new_customer[1]),int(new_customer[2]))
        packet_time = new_customer.arrivalTime

        if packet_time in d:
            d[packet_time].append(new_customer)
            d[packet_time] = sorted(d[packet_time],key=lambda x: (x.items, x.type))
        else:
            d[packet_time] = [new_customer]

    # Adding customer time packets to the groccery store in pre-processing
    for timeStamp in d.keys():
        my_GS.addTimePacket(packet(timeStamp,d[timeStamp]))

    my_GS.timePacketList = sorted(my_GS.timePacketList, key=lambda x: (x.time))

    for i in my_GS.timePacketList:
        print(i)
    
    # We have all the packets of customers sorted and inputed into the store. 

    while my_GS.timePacketList:
        my_GS.processPacket()
    
    finalTime = float('-Inf')
    for r in my_GS.registers:
        print(r.computeEndTime())
        finalTime = max(finalTime,r.computeEndTime())
    
    print("Finished at: t={} minutes",finalTime)
    

if __name__ == "__main__":
    main()