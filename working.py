# most current example I could find

from collections import namedtuple
import sys

class MovingAverageCrossAlgorithm(QCAlgorithm):

    def Initialize(self):
        '''Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''
        
        # self.Debug(sys.version)
        self.webhookFired = False

        Indic = namedtuple('Indic', 'symbol slow fast')
        self.previous_dict = {}

        self.SetStartDate(2020, 2, 1)
        self.SetEndDate(2020, 3, 1)
        self.SetCash(100000)
        # Find more symbols here: http://quantconnect.com/data
        # self.AddEquity("SPY")

        # create a 15 day exponential moving average
        # self.fast = self.EMA("SPY", 15, Resolution.Daily)

        # create a 30 day exponential moving average
        # self.slow = self.EMA("SPY", 30, Resolution.Daily)
        # self.previous = None
        
        # testing
        self.indics = []
        self.securities = ["IBM", "TSLA", "MSFT"]
        for s in self.securities:
            self.AddEquity(str(s))
            i = Indic(s, self.EMA(s, 30, Resolution.Hour), self.EMA(s, 15, Resolution.Hour))
            self.previous_dict[str(s)] = None
            self.indics.append(i)
        
        
    def fireWebhook(self, payload):
        if self.webhookFired == False:
            self.Debug("about to fire webhook")
            # self.Notify.Email("swearingendw@gmail.com", "My Quantconnect email test", "test from QuantConnect")
            # self.Notify.Web("https://hooks.zapier.com/hooks/catch/4808229/ogwmw0d/")
            self.webhookFired = True
            

# TODO: I may have to reset previous to None at a certain point ie the end of the day or after every trade...???
    def OnData(self, data):
        self.tolerance = 0.00015
        for ind in self.indics:
            # self.Debug(f"symbol: {ind.symbol} slow current value: {ind.slow.Current.Value}  fast current value: {ind.fast.Current.Value}")
            self.qty = self.Portfolio[str(ind.symbol)].Quantity
            #self.Debug(f"quantity: {self.qty}")
            self.holdings = self.Portfolio[ind.symbol].Quantity
            # self.Debug(f"holdings: {self.holdings}")
            
            if not ind.slow.IsReady:
                continue
            
            #if self.previous_dict[ind.symbol] is not None:
            #    self.Debug(f"compare: {self.previous_dict[ind.symbol].date()} to {self.Time.date()}")
                
            if self.previous_dict[ind.symbol] is not None and self.previous_dict[ind.symbol].date() == self.Time.date():
                # self.Debug("about to continue")
                continue
            
            # if the fast is greater than the slow, we'll go long
            if self.holdings <= 0 and ind.fast.Current.Value > ind.slow.Current.Value *(1 + self.tolerance):
                # self.fireWebhook(f"BUY, {ind.symbol}, {self.Time.date()}, {ind.slow.Current.Value}")
                self.Debug("BUY  >> {0} {1} {2}".format(ind.symbol, self.Securities[ind.symbol].Price, self.Time))
                # self.SetHoldings(ind.symbol, 1.0)
            elif self.holdings > 0 and ind.fast.Current.Value > ind.slow.Current.Value *(1 + self.tolerance): 
                self.Debug("SELL >> {0} {1} {2}".format(ind.symbol, self.Securities[ind.symbol].Price, self.Time))
                # self.Liquidate(ind.symbol)
                
            self.previous_dict[ind.symbol] = self.Time
    
    

    def OldOnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.'''
        # a couple things to notice in this method:
        #  1. We never need to 'update' our indicators with the data, the engine takes care of this for us
        #  2. We can use indicators directly in math expressions
        #  3. We can easily plot many indicators at the same time

        # wait for our slow ema to fully initialize
        if not self.slow.IsReady:
            return

        # only once per day
        if self.previous is not None and self.previous.date() == self.Time.date():
            return

        # define a small tolerance on our checks to avoid bouncing
        tolerance = 0.00015

        holdings = self.Portfolio["SPY"].Quantity

        # we only want to go long if we're currently short or flat
        if holdings <= 0:
            # if the fast is greater than the slow, we'll go long
            if self.fast.Current.Value > self.slow.Current.Value *(1 + tolerance):
                self.Log("BUY  >> {0}".format(self.Securities["SPY"].Price))
                self.SetHoldings("SPY", 1.0)

        # we only want to liquidate if we're currently long
        # if the fast is less than the slow we'll liquidate our long
        if holdings > 0 and self.fast.Current.Value < self.slow.Current.Value:
            self.Log("SELL >> {0}".format(self.Securities["SPY"].Price))
            self.Liquidate("SPY")

        self.previous = self.Time
