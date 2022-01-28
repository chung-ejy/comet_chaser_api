import pandas as pd
from datetime import datetime, timedelta
from comet_utils.processor.processor import Processor as p
from time import sleep
from comet_utils.analyzer.entry_strategy import EntryStrategy
from comet_utils.analyzer.exit_strategy import ExitStrategy


class Backtester(object):

    @classmethod
    def backtest(self,start,end,params,prices):
        status = "loads"
        symbols = params["symbols"]
        if "ALL" in symbols:
            symbols = prices["crypto"].unique()
        rt = params["retrack_days"]
        s = params["signal"]
        r = params["req"]
        value = params["value"]
        positions = params["positions"]
        conservative = params["conservative"]
        entry_strat = params["entry_strategy"]
        exit_strat = params["exit_strategy"]
        market = prices.pivot_table(index="date",columns="crypto",values="close").reset_index()
        market = p.column_date_processing(market)
        market = market.fillna(method="ffill")
        sim = market.melt(id_vars="date").copy()
        ns = []
        sim = sim[sim["value"] > 0]
        for crypto in [x.lower() for x in symbols]:
            crypto_sim = sim[sim["crypto"]==crypto].copy()
            crypto_sim.sort_values("date",inplace=True)
            crypto_sim["signal"] = crypto_sim["value"].pct_change(rt)
            crypto_sim["velocity"] = crypto_sim["signal"].pct_change(rt)
            crypto_sim["inflection"] = crypto_sim["velocity"].pct_change(rt)
            crypto_sim["p_sign_change"] = [row[1]["velocity"] * row[1]["inflection"] < 0 for row in crypto_sim.iterrows()]
            ns.append(crypto_sim)
        final = pd.concat(ns)
        final = final[(final["date"] < end) & (final["value"] > 0)].dropna()
        final.rename(columns={"value":"close"},inplace=True)
        signal = float(s/100)
        req = float(r/100)
        date = start
        trades = []
        for position in range(positions):
            date = start
            while date < end:
                try:
                    status = "entries"
                    offerings = EntryStrategy.backtest_entry_analysis(date,entry_strat,final,signal,value,conservative)
                    if offerings.index.size < 1:
                        date = date + timedelta(days=1)
                    else:
                        status = "exits"
                        if offerings.index.size < position:
                            date = date + timedelta(days=1)
                            continue
                        else:
                            trade = offerings.iloc[position]
                            trade = ExitStrategy.backtest_exit_analysis(exit_strat,final,trade,rt,req)
                            trade["signal"] = signal
                            trade["req"] = req
                            trade["retrack_days"] = rt
                            trade["value"] = value
                            trade["conservative"] = conservative
                            trade["entry_strategy"] = entry_strat
                            trade["exit_strategy"] = exit_strat
                            trade["position"] = position
                            trade["positions"] = positions
                            trades.append(trade)
                            status = "date adding"
                            date = trade["sell_date"] + timedelta(days=1)
                except Exception as e:
                    # print(date,status,trade,str(e))
                    date = date + timedelta(days=1)
        return pd.DataFrame(trades)
    
    @classmethod
    def pairs_trading_backtest(self,start,end,params,prices,correlations):
        status = "loads"
        rt = params["retrack_days"]
        s = params["signal"]
        r = params["req"]
        value = params["value"]
        conservative = params["conservative"]
        entry_strat = params["entry_strategy"]
        exit_strat = params["exit_strategy"]
        market = prices.pivot_table(index="date",columns="crypto",values="close").reset_index()
        market = p.column_date_processing(market)
        market = market.fillna(method="ffill")
        sim = market.melt(id_vars="date").copy()
        ns = []
        sim = sim[sim["value"] > 0]
        for crypto in sim["crypto"].unique():
            crypto_sim = sim[sim["crypto"]==crypto].copy()
            crypto_sim.sort_values("date",inplace=True)
            crypto_sim["signal"] = crypto_sim["value"].pct_change(rt)
            crypto_sim["velocity"] = crypto_sim["signal"].pct_change(rt)
            crypto_sim["inflection"] = crypto_sim["velocity"].pct_change(rt)
            crypto_sim["p_sign_change"] = [row[1]["velocity"] * row[1]["inflection"] < 0 for row in crypto_sim.iterrows()]
            ns.append(crypto_sim)
        final = pd.concat(ns)
        final = final[(final["date"] < end) & (final["value"] > 0)].dropna()
        final.rename(columns={"value":"close"},inplace=True)
        signal = float(s/100)
        req = float(r/100)
        date = start
        trades = []
        while date < end:
            try:
                status = "entries"
                offerings = EntryStrategy.backtest_entry_analysis(date,entry_strat,final,signal,value,conservative)
                if offerings.index.size < 1:
                    date = date + timedelta(days=1)
                else:
                    status = "exits"
                    trade_i = offerings.iloc[0]
                    trade_i = ExitStrategy.backtest_exit_analysis(exit_strat,final,trade_i,rt,req)
                    trade_i["signal"] = signal
                    trade_i["req"] = req
                    trade_i["retrack_days"] = rt
                    trade_i["value"] = value
                    trade_i["conservative"] = conservative
                    trade_i["entry_strategy"] = entry_strat
                    trade_i["exit_strategy"] = exit_strat
                    trade_i["position"] = 0
                    trades.append(trade_i)
                    date_2 = date
                    while date_2 < trade_i["sell_date"] and date_2 < end:
                        try:
                            status = "entries"
                            symbol_correlations = correlations[(correlations["crypto"]==trade_i["crypto"]) & (correlations["value"]<=-0.7)]["crypto_ii"].unique()
                            second_final = final[final["crypto"].isin(list(symbol_correlations)) & (final["date"] <= trade_i["sell_date"])].sort_values("date")
                            offerings = EntryStrategy.backtest_entry_analysis(date_2,entry_strat,second_final,float(signal/3),value,conservative)
                            if offerings.index.size < 1:
                                date_2 = date_2 + timedelta(days=1)
                            else:
                                status = "exits"
                                trade_ii = offerings.iloc[0]
                                trade_ii = ExitStrategy.backtest_exit_analysis(exit_strat,second_final,trade_ii,rt,float(req/3))
                                trade_ii["signal"] = signal
                                trade_ii["req"] = req
                                trade_ii["retrack_days"] = rt
                                trade_ii["value"] = value
                                trade_ii["conservative"] = conservative
                                trade_ii["entry_strategy"] = entry_strat
                                trade_ii["exit_strategy"] = exit_strat
                                trade_ii["position"] = 1
                                trades.append(trade_ii)
                                date_2 = trade_ii["sell_date"] + timedelta(days=1)
                        except Exception as e:
                            # print(date,status,trade_ii,str(e))
                            date_2 = date_2 + timedelta(days=1)
                    status = "date adding"
                    date = trade_i["sell_date"] + timedelta(days=1)
            except Exception as e:
                # print(date,status,trade_i,str(e))
                date = date + timedelta(days=1)
        return pd.DataFrame(trades)

    @classmethod
    def analyze(self,current_trades,final):
        viz = []
        row = current_trades.iloc[0]
        pv = 100
        start_date = row["date"]
        symbol = row["crypto"]
        amount = float(pv/row["buy_price"])
        end_date = row["sell_date"]
        pv2 = amount * row["sell_price"]
        viz.append({"date":start_date,"crypto":symbol,"amount":amount})
        viz.append({"date":end_date,"crypto":symbol,"amount":amount})
        track_date = start_date
        while track_date < end_date - timedelta(days=1):
            track_date = track_date + timedelta(days=1)
            viz.append({"date":track_date,"crypto":symbol,"amount":amount})
        for i in range(1,current_trades.index.size-1):
            row = current_trades.iloc[i]
            symbol = current_trades.iloc[i]["crypto"]
            start_date = row["date"]
            pv = pv2
            amount =  pv /row["buy_price"]
            viz.append({"date":start_date,"crypto":symbol,"amount":amount})
            track_date = start_date
            end_date = row["sell_date"]
            while track_date < end_date:
                track_date = track_date + timedelta(days=1)
                viz.append({"date":track_date,"crypto":symbol,"amount":amount})
            pv2 = amount * row["sell_price"]
            viz.append({"date":end_date,"crypto":symbol,"amount":amount})
        window = pd.DataFrame(viz)
        window["crypto"] = [x.upper() for x in window["crypto"]]
        example = final.merge(window,how="left",on=["date","crypto"])
        example = example.dropna().sort_values("date")
        example["actual"] = example["amount"] * example["close"]
        example["actual_delta"] = (example["actual"] - example["actual"].iloc[0]) / example["actual"].iloc[0]
        return example[["date","actual_delta"]]