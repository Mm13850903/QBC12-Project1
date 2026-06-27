class Line:
    def __init__(self, name, source, destination, station_count, stations):
        self.__name = name
        self.__source = source
        self.__destination = destination
        self.__station_count = station_count
        self.__stations = stations


        self.is_ready = True #We will enable this when we are done creating the variables


    def __setattr__(self, key, value): #This function controls any changes or creation of new variables
        if hasattr(self, 'is_ready'): #If the class is finished we do not allow changes.
            print(f"Security error: You are not allowed to change '{key}'!")

        super().__setattr__(key, value)#Permission to create variables is granted at --init-- execution time

    def get_name(self):
        return self.__name

    def get_source(self):
        return self.__source

    def get_destination(self):
        return self.__destination

    def get_station_count(self):
        return self.__station_count

    def get_stations(self):
        return self.__stations



my_line= Line(1,"tehran","shiraz",3,['a','b','c'])

my_line.__source = "tehran"
my_line.__destination = "shiraz"
