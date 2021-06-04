def actAndActionIdxDecide(actionIndex: int) -> dict:
    if actionIndex < 0 or actionIndex >= 4200:
        return {"act": "hold", "index": -1, "amount_rate": -1}
    elif actionIndex < 4000:
        return {"act": "buy", "index": actionIndex // 20, "amount_rate": (actionIndex % 20 + 1) / 20}
    else:
        actionIndex -= 4000
        return {
            "act": "sell",
            "index": actionIndex // 10,
            "amount_rate": (actionIndex % 10 + 1) / 10,
        }
