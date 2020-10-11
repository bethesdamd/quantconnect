# First experiments with stuff like Relative Strength Indicators

class BootCampTask(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 6, 1)
        self.SetEndDate(2017, 6, 2)
        
        #1. Update the AddEquity command to request IBM data
        self.ibm = self.AddEquity("IBM", Resolution.Daily)
        self.rsi = self.RSI("IBM", 10,  MovingAverageType.Simple, Resolution.Daily)
        # set a warm-up period to initialize the indicator
        self.SetWarmUp(timedelta(20))
        
    def OnData(self, data):
        
        #2. Display the Quantity of IBM Shares You Own
        self.Debug("Number of IBM Shares: " + str(self.Portfolio["IBM"].Quantity))
        if self.rsi.IsReady:
            # get the current RSI value
            rsi_value = self.rsi.Current.Value
            # get the current average gain of rsi
            average_gain = self.rsi.AverageGain.Current.Value
            # get the current average loss of rsi
            average_loss = self.rsi.AverageLoss.Current.Value
            self.Debug(rsi_value)
            self.Debug(average_gain)
            self.Debug(average_loss)
            
            
