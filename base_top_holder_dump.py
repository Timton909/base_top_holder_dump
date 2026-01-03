import requests, time

def top_holder_dump():
    print("Base — Top Holder Dump Detector (top wallet sells >$50k)")
    seen = set()

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=400")
            for tx in r.json().get("transactions", []):
                txid = tx["hash"]
                if txid in seen or tx.get("side") != "sell" or tx.get("valueUSD", 0) < 50000:
                    continue
                seen.add(txid)

                pair = tx["pairAddress"]
                seller = tx["from"].lower()

                # Get top holders for pair
                pair_data = requests.get(f"https://api.dexscreener.com/latest/dex/pairs/base/{pair}").json()["pair"]
                top_holders = pair_data.get("topHolders", [])[:5]
                top_addresses = [h["address"].lower() for h in top_holders]

                if seller in top_addresses:
                    token = pair_data["baseToken"]["symbol"]
                    rank = top_addresses.index(seller) + 1
                    print(f"TOP HOLDER DUMPING\n"
                          f"#{rank} holder sold ${tx['valueUSD']:,.0f} of {token}\n"
                          f"Wallet: {seller[:10]}...\n"
                          f"https://dexscreener.com/base/{pair}\n"
                          f"https://basescan.org/address/{seller}\n"
                          f"→ Smart money exiting — watch for cascade\n"
                          f"{'TOP DUMP'*20}")

        except:
            pass
        time.sleep(1.9)

if __name__ == "__main__":
    top_holder_dump()
