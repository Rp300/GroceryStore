from os import times
import sys
from collections import deque

class Packet:
    """
    A container of all customers arriving at a specific time epoch.
    ...

    Attributes
    ----------
    time : int
        time epoch of packet
    customer_list : str
        the name of the animal
    """
    def __init__(self, time, customer_list):
        """
        Parameters
        ----------
        time : int
            time epoch of packet
        customer_list : list<Customer>
            the name of the animal
        """
        self.time = time
        self.customer_list = customer_list

class Customer:
    """
    A cutomer that checks out at a register in a Grocery store.
    ...

    Attributes
    ----------
    customer_type : str
        Attribute indicating customer type ('A' or 'B')
    arrival_time : int
        The name of the animal
    items : int
        Number of items customer currently has unprocessed

    Methods
    -------
    updateItemCount(itemsProcessed)
        Given number of items processed by register, update current customer item count.
    """
    def __init__(self, customer_type, arrival_time, items) -> None:
        """
        Parameters
        ----------
        customer_type : str
            Attribute indicating customer type ('A' or 'B')
        arrival_time : int
            The name of the animal
        items : int
            Number of items customer currently has unprocessed
        """
        self.customer_type = customer_type
        self.arrival_time = arrival_time
        self.items = items
    
    def __str__(self):
        """String representation of a Customer: (customer_type, time, items)"""
        return str((self.customer_type, self.arrival_time, self.items))
    
    def updateItemCount(self, itemsProcessed):
        """Given number of items processed by register, update current customer item count.

        Parameters
        ----------
        itemsProcessed : int
            Number of items processed by cutomer's register
        
        Returns
        -------
        int
            remaining items register can process
        """
        if self.items < itemsProcessed:
            rem = itemsProcessed-self.items
            self.items = 0
            return rem
        else:
            self.items-=itemsProcessed
            return 0

class Register:
    """
    A register in a Grocery store that is either in training or not. This status affects item processing rate.
    ...

    Attributes
    ----------
    register_number : int
        The identification number of a register. (num in [1,n])
    rate : float
        The rate at which register processes items. 1/min for normal and 1/2min for training register.
    time : int
        Current time of register and Grocery store, maintained by updateTime().
    customer_count : int
        Number of customers in register line.
    customer_list : deque<Customer>
        A queue to emulate a customer line for the register.

    Methods
    -------
    pushCustomer(next_customer)
        Add a customer to the register line.
    
    peekLastCustomer()
        Peek at number of items the last customer in line has at current time epoch.
    
    updateTime(new_time)
        Adjusts and simulates register item processing to the latest Grocery Store time provided.

    computeEndTime()
        Based on current customer queue, returns time when all customer items have been processed.

    show()
        Provides a simple visualization of current customer queue for register.
    """
    def __init__(self, number, training):
        """
        Parameters
        ----------
        number : int
            The register identification number
        training : bool
            If register is a training register or not
        """
        self.register_number = number
        self.rate = 0.5 if training else 1.0
        self.time = 0
        self.customer_count = 0 
        self.customer_list = deque([])

    def pushCustomer(self,next_customer):
        """ Add customer to register line and update customer count.

        Parameters
        ----------
        next_customer : Customer
            Cutomer entering register queue
        """
        self.customer_list.append(next_customer)
        self.customer_count+=1

    def peekLastCustomer(self):
        """ View last customer in line's item count remaining."""
        if self.customer_count == 0:
            return 0
        else:
            return self.customer_list[-1].items

    def updateTime(self, new_time):
        """Adjusts and simulates register item processing to the latest Grocery Store time.

        Parameters
        ----------
        new_time : int
            Latest time epoch inputed to Grocery store
        """
        timeElapsed = new_time - self.time
        itemsProcessed = self.rate * timeElapsed

        while len(self.customer_list) > 0 and itemsProcessed > 0:
            front_customer = self.customer_list[0]

            rem = front_customer.updateItemCount(itemsProcessed)
            if front_customer.items == 0:
                self.customer_list.popleft()
                self.customer_count-=1

            itemsProcessed = rem

        self.time = new_time

    def computeEndTime(self):
        """Based on current customer queue, returns time when all customer items have been processed.

        Returns
        -------
        int
            End time when all items have been processed and customer queue is empty.
        """
        if self.customer_list: 
            items = 0
            timeRemaining = 0
            for c in self.customer_list:
                items+=c.items
            timeRemaining = items/self.rate

            return self.time+timeRemaining
        else:
            return self.time
    
    def show(self):
        """Provides a simple visualization of current customer queue for register."""
        print("Register "+str(self.register_number))
        for c in self.customer_list:
            print(c)
        print()

class GroceryStore:
    """
    The object that represents the universe where the register-customer simulation takes place. There are the following steps: pre-processing, processing packets, and final time calculation that take place for a simulation test file.
    ...

    Attributes
    ----------
    time : int
        The current time epoch of the Grocery store, maintained by updateTime.
    register_count : int
        The number of registers in Grocery store.
    register_list : list<Register>
        A list of the register objects part of the Grocery store.
    time_packet_list : deque<Packet>
        A queue of time stamp Packets to process, ordered by time.

    Methods
    -------
    updateTime(new_time)
        Adjusts and simulates register item processing to the latest Grocery Store time provided.

    pushCustomer(next_customer)
        Add a customer to the appropriate register line based on customer type rules.

    addTimePacket(time_packet)
        Add customer time stamp packet to the Grocery store to be proccessed during simulation.
    
    processPackets()
        Iterate through packets in pre-proccessed queue, and propogate time update plus new customers for each.

    computeEndTime()


    show()
        Provides a simple visualization of current customer queue for each register in the Grocery Store.
    """
    def __init__(self,register_count):
        """ Initializes 'register_count' number of Register objects making the last one a Training register.

        Parameters
        ----------
        register_count : int
            The number of registers in Grocery store.
        """
        self.time = 0
        self.register_count = register_count
        self.register_list = []
        self.time_packet_list = deque([])

        for i in range(1, register_count+1):
            self.register_list.append(Register(i, i == register_count))

    def updateTime(self, new_time):
        """ Adjusts and simulates registers and customers to the latest Grocery Store time provided by latest time packet.

        Parameters
        ----------
        time_packet : Packet
            Container of all customers that check out at a given time.
        """
        for r in self.register_list:
            r.updateTime(new_time)
        self.time = new_time
    
    def pushCustomer(self, next_customer):
        """ Add a customer to the appropriate register line based on customer type rules.

        Parameters
        ----------
        next_customer : Customer
            The next customer to be added to a register queue.
        """
        type = next_customer.customer_type

        if type == 'A':
            '''Type A customers pick the shortest line, so sort register list by number of customers per register and pick the smallest.'''

            curr_register = sorted(self.register_list, key=lambda x: (x.customer_count))[0]
            curr_register.pushCustomer(next_customer)

        elif type == 'B':
            '''Type B customers pick the line where the last person in line has the fewest items. Use peek method to check each register and store the smallest, then add customer.'''
            
            curr_register = None
            min_items = float('Inf')

            for r in self.register_list:
                item_count = r.peekLastCustomer()
                if item_count < min_items:
                   min_items = item_count
                   curr_register = r

            curr_register.pushCustomer(next_customer)

    def addTimePacket(self, time_packet):
        """ Add customer time stamp packet to the Grocery store to be proccessed during simulation.

        Parameters
        ----------
        time_packet : Packet
            Container of all customers that check out at a given time.
        """
        self.time_packet_list.append(time_packet)
    
    def processPackets(self):
        """Iterate through packets in pre-proccessed queue, and propogate time update plus new customers for each."""
        while self.time_packet_list:
            p = self.time_packet_list.pop(0)

            # Propogate new time
            updated_time = p.time
            self.updateTime(updated_time)
            
            # Iterate through customers per packet
            for next_customer in p.customer_list:
                self.pushCustomer(next_customer)

    def computeEndTime(self):
        """Computes the end time for the Grocery store, once all customers checked out.
        
        Returns
        -------
        int
            the time after all registers have 0 customers and all packets proccessed.
        """
        final_time = float('-Inf')
        for r in self.register_list:
            final_time = max(final_time,r.computeEndTime())
        return final_time
    
    def show(self):
        """Provides a simple visualization of current customer queue for each register in the Grocery Store."""
        for r in self.register_list:
            r.show()    

class Utility:
    '''Generic Utility functions to read, parse, and digest test files.'''
    def parseTestFile():
        # Read in test file name from args and open file
        input_file = sys.argv[1]
        f = open(input_file, "r")

        # Parse first line for number of registers and initialize Grocery Store
        register_count = int(f.readline())
        my_GS = GroceryStore(register_count)

        # Create customer time packet dictionary while reading
        packet_dict = {}
        for l in f:
            new_customer = l.split()
            new_customer = Customer(new_customer[0],int(new_customer[1]),int(new_customer[2]))
            packet_time = new_customer.arrival_time

            if packet_time in packet_dict:
                packet_dict[packet_time].append(new_customer)
                packet_dict[packet_time] = sorted(packet_dict[packet_time],key=lambda x: (x.items, x.customer_type))
            else:
                packet_dict[packet_time] = [new_customer]
        
        return my_GS, packet_dict

    def preProcessPackets(my_GS, packet_dict):
        # Adding customer time packets to the Grocery store in pre-processing
        for timeStamp in packet_dict.keys():
            my_GS.addTimePacket(Packet(timeStamp,packet_dict[timeStamp]))

        my_GS.time_packet_list = sorted(my_GS.time_packet_list, key=lambda x: (x.time))

        return my_GS