def AlertUser(self):
        timer = self.time
        #add input test
        #work = int(self.timeoutPeriod.get())
        #print('timeout: ', self.timeoutPeriod)
        work = int(self.timeoutPeriod)
        #add input test
        #rest = int(self.restPeriod.get())
        #print('rest: ', self.restPeriod)
        rest = int(self.restPeriod)

        #what do these variables do???
        wDone = True
        rDone = True


        if (timer % ((work + rest) * 100) == ((work) * 100)):
        #if (timer == work):
            print ("Take a break!")
            print('work: ', work)
            print('rest: ', rest)
            return 1
        elif (timer % ((work + rest) * 100) == 0 and timer != 0):
        #elif (timer == (work + rest)):
            print ("Back to work!")
            print('work: ', work)
            print('rest: ', rest)
            return 2
        return 0

