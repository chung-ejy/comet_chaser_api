from cmath import nan
from datetime import timedelta, datetime
from re import M
import pandas as pd
from comet_utils.processor.processor import Processor as p
import pickle
from database.comet_historian import CometHistorian
import os
from dotenv import load_dotenv
load_dotenv()
mongouser = os.getenv("MONGOUSER")
mongokey = os.getenv("MONGOKEY")
class ExitStrategy(object):

    @classmethod
    def exit_analysis(self,exit_strat,incomplete_trade,final,req):
        size = round(incomplete_trade["size"],6)
        buy_price = incomplete_trade["price"]
        product_id = incomplete_trade["product_id"]
        symbol = product_id.split("-")[0]
        incomplete_trade["size"] = size
        incomplete_trade["exit_strat"] = exit_strat
        product_data =  final[(final["crypto"]==symbol)]
        product_data["delta"] = (product_data["price"] - buy_price) / buy_price
        if exit_strat == "due_date":
            analysis = self.due_date(product_data,req)
        else:
            if exit_strat =="hold":
                analysis = self.hold(product_data,req)
            else:
                if exit_strat =="adaptive_due_date":
                    analysis = self.adaptive_due_date(product_data,req)
                else:
                    if exit_strat =="adaptive_hold":
                        analysis = self.adaptive_hold(product_data,req)
                    else:
                        if exit_strat == "ai":
                            analysis = self.ai_driven(product_data)
                        else:
                            analysis = pd.DataFrame([{}])
        if analysis.index.size > 0:
            incomplete_trade["sell_price"] = product_data["ask"].item()
        return incomplete_trade
    
    @classmethod
    def backtest_exit_analysis(self,exit_strat,final,trade,rt,req):
        if exit_strat == "due_date":
            analysis = self.backtest_due_date(final,trade,rt,req)
        else:
            if exit_strat =="hold":
                analysis = self.backtest_hold(final,trade,rt,req)
            else:
                if exit_strat =="adaptive_due_date":
                    analysis = self.backtest_adaptive_due_date(final,trade,rt,req)
                else:
                    if exit_strat =="adaptive_hold":
                        analysis = self.backtest_adaptive_hold(final,trade,rt,req)
                    else:
                        if exit_strat =="ai":
                            analysis = self.backtest_ai(final,trade,rt,req)
                        else:
                            analysis = pd.DataFrame([{}])
        return analysis

    @classmethod
    def ai_driven(self,final):
        comet_historian = CometHistorian()
        comet_historian.cloud_connect()
        models = comet_historian.retrieve("coinbase_models")
        comet_historian.disconnect()
        factors = ["signal","velocity","concavity"]
        models["model"] = [pickle.loads(x) for x in models["model"]]
        final.rename(columns={"inflection":"concavity"},inplace=True)
        predictions = []
        for row in final.iterrows():
            try:
                symbol = row[1]["crypto"]
                model = models[models["symbol"]==symbol]["model"].item()
                prediction = model.predict(final[final["crypto"]==symbol][factors])[0]
                predictions.append(prediction)
            except:
                predictions.append(nan)
        final["prediction"] = predictions
        print(final)
        offerings = final[final["prediction"]==False]
        return offerings

    @classmethod
    def due_date(self,final,trade,rt,req):
        profits = final[(final["delta"] >= req)]
        return profits

    @classmethod
    def hold(self,final,req):
        profits = final[(final["delta"] >= req)]
        return profits

    @classmethod
    def adaptive_hold(self,final):
        profits = final[(final["delta"] > 0)
                        & (final["p_sign_change"]==True)
                        & (final["velocity"] <= 3)
                        & (final["velocity"] > 0)
                        & (final["inflection"] <= 1)
                        & (final["inflection"] >= -1)]
        return profits

    @classmethod
    def adaptive_due_date(self,final):
        profits = final[(final["delta"] >= 0)
                        & (final["p_sign_change"]==True)
                        & (final["velocity"] <= 3)
                        & (final["velocity"] > 0)
                        & (final["inflection"] <= 1)
                        & (final["inflection"] >= -1)]
        return profits

    @classmethod
    def backtest_ai(self,final,trade,rt,req):
        symbol = trade["crypto"]
        exits = final[(final["date"]>trade["date"]) & (final["crypto"]==symbol)]
        bp = float(trade["close"])
        exits["delta"] = (exits["close"] - bp) / bp
        profits = exits[exits["prediction"]==False]
        if profits.index.size < 1:
            the_exit = exits.iloc[-1]
            trade["type"] = "held"
            trade["sell_price"] = the_exit["close"]
        else:
            the_exit = profits.iloc[0]
            trade["type"] = "profit"
            trade["sell_price"] = the_exit["close"]
        trade["sell_date"] = the_exit["date"]
        trade["buy_price"] = bp
        trade["delta"] = (trade["sell_price"] - trade["buy_price"])/ trade["buy_price"]
        return trade

    @classmethod
    def backtest_due_date(self,final,trade,rt,req):
        symbol = trade["crypto"]
        exits = final[(final["date"]>trade["date"]) & (final["crypto"]==symbol)]
        bp = float(trade["close"])
        due_date = trade["date"]+timedelta(days=rt)
        exits["delta"] = (exits["close"] - bp) / bp
        profits = exits[(exits["delta"] >= req) & (exits["date"] <= due_date)]
        breakeven = exits[(exits["delta"]>=0) & (exits["date"] > due_date)]
        if profits.index.size < 1:
            if breakeven.index.size < 1:
                the_exit = exits[(exits["date"] > due_date)].iloc[-1]
                trade["sell_price"] = the_exit["close"]
                trade["type"] = "loss"
            else:
                the_exit = breakeven.iloc[0]
                trade["type"] = "breakeven"
                trade["sell_price"] = bp
        else:
            the_exit = profits.iloc[0]
            trade["type"] = "profit"
            trade["sell_price"] = bp * (1+req)
        trade["sell_date"] = the_exit["date"]
        trade["buy_price"] = bp
        trade["delta"] = (trade["sell_price"] - trade["buy_price"])/ trade["buy_price"]
        return trade

    @classmethod
    def backtest_hold(self,final,trade,rt,req):
        symbol = trade["crypto"]
        exits = final[(final["date"]>trade["date"]) & (final["crypto"]==symbol)]
        bp = float(trade["close"])
        exits["delta"] = (exits["close"] - bp) / bp
        profits = exits[(exits["delta"] >= req) & (exits["date"] > trade["date"])]
        if profits.index.size < 1:
            the_exit = exits.iloc[-1]
            trade["type"] = "held"
            trade["sell_price"] = the_exit["close"]
        else:
            the_exit = profits.iloc[0]
            trade["type"] = "profit"
            trade["sell_price"] = bp * (1+req)
        trade["sell_date"] = the_exit["date"]
        trade["buy_price"] = bp
        trade["delta"] = (trade["sell_price"] - trade["buy_price"])/ trade["buy_price"]
        return trade

    @classmethod
    def backtest_adaptive_hold(self,final,trade,rt,req):
        symbol = trade["crypto"]
        exits = final[(final["date"]>trade["date"]) & (final["crypto"]==symbol)]
        bp = float(trade["close"])
        exits["delta"] = (exits["close"] - bp) / bp
        profits = exits[(exits["date"] > trade["date"])
                        & (exits["delta"] > req)
                        & (exits["p_sign_change"]==True)
                        & (exits["velocity"] <= 3)
                        & (exits["velocity"] > 0)
                        & (exits["inflection"] <= 1)
                        & (exits["inflection"] >= -1)]
        if profits.index.size < 1:
            the_exit = exits.iloc[-1]
            trade["type"] = "held"
        else:
            the_exit = profits.iloc[0]
            trade["type"] = "profit"
        trade["sell_price"] = the_exit["close"]
        trade["sell_date"] = the_exit["date"]
        trade["buy_price"] = bp
        trade["delta"] = (trade["sell_price"] - trade["buy_price"])/ trade["buy_price"]
        return trade

    @classmethod
    def backtest_adaptive_due_date(self,final,trade,rt,req):
        symbol = trade["crypto"]
        exits = final[(final["date"]>trade["date"]) & (final["crypto"]==symbol)]
        bp = float(trade["close"])
        exits["delta"] = (exits["close"] - bp) / bp
        due_date = trade["date"]+timedelta(days=rt)
        profits = exits[(exits["date"] <= due_date)
                        & (exits["delta"] >= req)
                        & (exits["p_sign_change"]==True)
                        & (exits["velocity"] <= 3)
                        & (exits["velocity"] > 0)
                        & (exits["inflection"] <= 1)
                        & (exits["inflection"] >= -1)].sort_values("date")
        breakeven = exits[(exits["delta"]>=0) & (exits["date"] > due_date)].sort_values("date")
        if profits.index.size < 1:
            if breakeven.index.size < 1:
                the_exit = exits[(exits["date"] > due_date)].iloc[-1]
                trade["sell_price"] = the_exit["close"]
                trade["type"] = "loss"
            else:
                the_exit = breakeven.iloc[0]
                trade["type"] = "breakeven"
                trade["sell_price"] = bp
        else:
            the_exit = profits.iloc[0]
            trade["type"] = "profit"
            trade["sell_price"] = the_exit["close"]
        trade["sell_date"] = the_exit["date"]
        trade["buy_price"] = bp
        trade["delta"] = (trade["sell_price"] - trade["buy_price"]) / trade["buy_price"]
        return trade