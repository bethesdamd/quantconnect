# most current example I could find

from collections import namedtuple
import sys

class MovingAverageCrossAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        
        self.Debug(sys.version)

        Indic = namedtuple('Indic', 'symbol previous slow fast')

        self.SetStartDate(2019, 4, 1)
        self.SetEndDate(2020, 5, 5)
        self.SetCash(100000)
        # Find more symbols here: http://quantconnect.com/data
        self.AddEquity("SPY")

        # create a 15 day exponential moving average
        self.fast = self.EMA("SPY", 15, Resolution.Daily)

        # create a 30 day exponential moving average
        self.slow = self.EMA("SPY", 30, Resolution.Daily)
        
        # testing
        self.indics = []
        self.securities = ["IBM", "TSLA", "MSFT"]
        for s in self.securities:
            self.AddEquity(str(s))
            i = Indic(s, None, self.EMA(s, 30, Resolution.Daily), self.EMA(s, 15, Resolution.Daily))
            self.indics.append(i)
        
        self.previous = None

    def OnData(self, data):
        tolerance = 0.00015
        self.Debug(f"Indics size in ondata is {len(self.indics)}")
        for ind in self.indics:
            self.Debug(f"type of ind:  {type(ind.slow)}   ------------")
            self.Debug(f"symbol: {ind.symbol} previous: {ind.previous} slow current value: {ind.slow.Current.Value}  fast current value: {ind.fast.Current.Value}")
            
            if not ind.slow.IsReady:
                continue
            
            # only once per day
            if ind.previous is not None and ind.previous.date() == self.Time.date():
                self.Debug("in second if")
                continue
            
            self.Debug("made it past second if")
            # if the fast is greater than the slow, we'll go long
            if ind.fast.Current.Value > ind.slow.Current.Value *(1 + tolerance):
                self.Debug("---- BUY -----")
                self.Log("BUY  >> {0}".format(self.Securities[ind.symbol].Price))
                self.SetHoldings(ind.symbol, 1.0)
            else: 
                self.Debug("in else ===================")
                self.Log("SELL >> {0}".format(self.Securities[ind.symbol].Price))
                self.Liquidate(ind.symbol)
        
            ind = ind._replace(previous = self.Time)
    
    
