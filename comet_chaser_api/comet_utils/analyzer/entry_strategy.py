import pandas as pd
class EntryStrategy(object):

    @classmethod
    def entry_analysis(self,entry_strat,final,signal,value,conservative):
        if entry_strat == "standard":
            offerings = self.standard(final,signal,value,conservative)
        else:
            if entry_strat == "signal_based":
                offerings = self.signal_based(final,signal,value,conservative)
            else:
                if entry_strat == "parameter_defined":
                    offerings = self.parameter_defined(final,signal,value,conservative)
                else:
                    if entry_strat == "research_parameter_defined":
                        offerings = self.research_parameter_defined(final,signal,value,conservative)
                    else:
                        if entry_strat == "all":
                            offerings = self.all(final,signal,value,conservative)
                        else:
                            offerings = pd.DataFrame([{}])
        offerings["entry_strat"] = entry_strat
        offerings["value"] = value
        offerings["signal"] = signal
        offerings["conservative"] = conservative
        return offerings


    @classmethod
    def backtest_entry_analysis(self,date,entry_strat,final,signal,value,conservative):
        if entry_strat == "standard":
            offerings = self.backtest_standard(final,date,signal,value,conservative)
        else:
            if entry_strat == "signal_based":
                offerings = self.backtest_signal_based(final,date,signal,value,conservative)
            else:
                if entry_strat == "parameter_defined":
                    offerings = self.backtest_parameter_defined(final,date,signal,value,conservative)
                else:
                    if entry_strat == "research_parameter_defined":
                        offerings = self.backtest_research_parameter_defined(final,date,signal,value,conservative)
                    else:
                        if entry_strat == "all":
                            offerings = self.backtest_all(final,date,signal,value,conservative)
                        else:
                            offerings = pd.DataFrame([{}])
        offerings["entry_strat"] = entry_strat
        offerings["value"] = value
        offerings["signal"] = signal
        offerings["conservative"] = conservative
        return offerings

    @classmethod
    def standard(self,final,signal,value,conservative):
        if value:
            offerings = final[(final["signal"] < -signal)
                        ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["signal"] > signal)
                                ].sort_values("signal",ascending=sorting)
        return offerings

    @classmethod
    def research_parameter_defined(self,final,signal,value,conservative):
        if value:
            offerings = final[(final["signal"] < -signal)
                                & (final["velocity"] >= -3)
                                & (final["velocity"] < 0)
                                & (final["inflection"] >= -1)
                                & (final["inflection"] <= 1)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["signal"] > signal)
                                & (final["velocity"] > 0)
                                & ((final["inflection"] <= 1)
                                | (final["inflection"] >= -1))
                                ].sort_values("signal",ascending=sorting)
        return offerings
    @classmethod
    def parameter_defined(self,final,signal,value,conservative):
        if value:
            offerings = final[(final["signal"] < -signal)
                                & (final["velocity"] >= -3)
                                & (final["velocity"] < 0)
                                & (final["inflection"] >= -1)
                                & (final["inflection"] <= 1)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["signal"] > signal)
                                & (final["velocity"] > 0)
                                & ((final["inflection"] >= 1)
                                & (final["inflection"] <= -1))
                                ].sort_values("signal",ascending=sorting)
        return offerings
    @classmethod
    def signal_based(self,final,signal,value,conservative):
        if value:
            offerings = final[(final["signal"] < -signal)
                                & (final["p_sign_change"]==True)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["signal"] > signal)
                                & (final["p_sign_change"]==True)
                                ].sort_values("signal",ascending=sorting)
        return offerings

    @classmethod
    def all(self,final,signal,value,conservative):
        if value:
            offerings = final[(final["signal"] < -signal)
                                & (final["p_sign_change"]==True)
                                & (final["velocity"] >= -3)
                                & (final["velocity"] < 0)
                                & (final["inflection"] >= 0)
                                & (final["inflection"] <= 1)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["signal"] > signal)
                                & (final["p_sign_change"]==True)
                                    & (final["velocity"] > 0)
                                & ((final["inflection"] <= 0)
                                | (final["inflection"] >= -1))
                                ].sort_values("signal",ascending=sorting)
        return offerings

    @classmethod
    def backtest_standard(self,final,date,signal,value,conservative):
        if value:
            offerings = final[(final["date"]==date) 
                                & (final["signal"] < -signal)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["date"]==date) 
                                & (final["signal"] > signal)
                                ].sort_values("signal",ascending=sorting)
        return offerings

    @classmethod
    def backtest_research_parameter_defined(self,final,date,signal,value,conservative):
        if value:
            offerings = final[(final["date"]==date) 
                                & (final["signal"] < -signal)
                                & (final["velocity"] >= -3)
                                & (final["velocity"] < 0)
                                & (final["inflection"] >= -1)
                                & (final["inflection"] <= 1)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["date"]==date) 
                                & (final["signal"] > signal)
                                & (final["velocity"] > 0)
                                & ((final["inflection"] <= 1)
                                | (final["inflection"] >= -1))
                                ].sort_values("signal",ascending=sorting)
        return offerings

    @classmethod
    def backtest_parameter_defined(self,final,date,signal,value,conservative):
        if value:
            offerings = final[(final["date"]==date) 
                                & (final["signal"] < -signal)
                                & (final["velocity"] >= -3)
                                & (final["velocity"] < 0)
                                & (final["inflection"] >= -1)
                                & (final["inflection"] <= 1)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["date"]==date) 
                                & (final["signal"] > signal)
                                & (final["velocity"] > 0)
                                & ((final["inflection"] >= 1)
                                & (final["inflection"] <= -1))
                                ].sort_values("signal",ascending=sorting)
        return offerings

    @classmethod
    def backtest_signal_based(self,final,date,signal,value,conservative):
        if value:
            offerings = final[(final["date"]==date) 
                                & (final["signal"] < -signal)
                                & (final["p_sign_change"]==True)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["date"]==date) 
                                & (final["signal"] > signal)
                                & (final["p_sign_change"]==True)
                                ].sort_values("signal",ascending=sorting)
        return offerings

    @classmethod
    def backtest_all(self,final,date,signal,value,conservative):
        if value:
            offerings = final[(final["date"]==date) 
                                & (final["signal"] < -signal)
                                & (final["p_sign_change"]==True)
                                & (final["velocity"] >= -3)
                                & (final["velocity"] < 0)
                                & (final["inflection"] >= 0)
                                & (final["inflection"] <= 1)
                                ].sort_values("signal",ascending=conservative)
        else:
            sorting = not conservative
            offerings = final[(final["date"]==date) 
                                & (final["signal"] > signal)
                                & (final["p_sign_change"]==True)
                                    & (final["velocity"] > 0)
                                & ((final["inflection"] <= 0)
                                | (final["inflection"] >= -1))
                                ].sort_values("signal",ascending=sorting)
        return offerings