import pandas as pd
import json
import os

# -------- CONFIGURATION -------- #
DATA_DIR = r"C:\Users\umad3\PycharmProjects\eye"
FILE_NAMES = [
    "compoundV2_transactions_ethereum_chunk_0.json",
    "compoundV2_transactions_ethereum_chunk_1.json",
    "compoundV2_transactions_ethereum_chunk_2.json"
]

# -------- LOAD AND MERGE DATA -------- #
def load_and_merge_json_files(file_names, directory):
    merged_data = {
        'deposits': [],
        'withdraws': [],
        'borrows': [],
        'repays': [],
        'liquidates': []
    }

    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        with open(file_path, "r") as f:
            data = json.load(f)
            for key in merged_data.keys():
                merged_data[key].extend(data.get(key, []))
    
    return merged_data

# -------- FUNCTION TO EXTRACT WALLET TRANSACTIONS -------- #
from datetime import datetime

def extract_wallet_transactions(data):
    tx_types = ['deposits', 'withdraws', 'borrows', 'repays', 'liquidates']
    wallet_stats = {}

    def update_stat(wallet, tx_type, amount_usd, timestamp):
        if wallet not in wallet_stats:
            wallet_stats[wallet] = {
                'total_deposit': 0,
                'total_withdraw': 0,
                'total_borrow': 0,
                'total_repay': 0,
                'liquidated': False,
                'timestamps': [],
                'borrow_timestamps': [],
                'repay_timestamps': []
            }

        # Update transaction totals
        if tx_type in ['deposits', 'withdraws', 'borrows', 'repays']:
            wallet_stats[wallet][f'total_{tx_type[:-1]}'] += float(amount_usd)

        # Mark liquidation
        elif tx_type == 'liquidates':
            wallet_stats[wallet]['liquidated'] = True

        # Record timestamps
        if timestamp:
            wallet_stats[wallet]['timestamps'].append(timestamp)
            if tx_type == 'borrows':
                wallet_stats[wallet]['borrow_timestamps'].append(timestamp)
            elif tx_type == 'repays':
                wallet_stats[wallet]['repay_timestamps'].append(timestamp)

    # Parse all transaction types
    for tx_type in tx_types:
        txs = data.get(tx_type, [])
        for tx in txs:
            if tx_type == 'liquidates':
                liquidatee = tx.get('liquidatee', {}).get('id')
                timestamp = tx.get('timestamp')
                if liquidatee:
                    update_stat(liquidatee, tx_type, 0, timestamp)
            else:
                wallet = tx.get('account', {}).get('id')
                amount_usd = tx.get('amountUSD', 0)
                timestamp = tx.get('timestamp')
                if wallet and amount_usd:
                    update_stat(wallet, tx_type, amount_usd, timestamp)

    # Now compute additional time features
    for wallet, stats in wallet_stats.items():
        ts = sorted([int(t) for t in stats['timestamps'] if t])
        if ts:
            stats['first_activity'] = datetime.fromtimestamp(ts[0])
            stats['last_activity'] = datetime.fromtimestamp(ts[-1])
            stats['active_days'] = (stats['last_activity'] - stats['first_activity']).days
        else:
            stats['first_activity'] = stats['last_activity'] = None
            stats['active_days'] = 0

        # Average borrow-to-repay time in days
        borrow_times = sorted([int(t) for t in stats['borrow_timestamps']])
        repay_times = sorted([int(t) for t in stats['repay_timestamps']])
        if borrow_times and repay_times:
            pairs = zip(borrow_times, repay_times[:len(borrow_times)])
            time_diffs = [r - b for b, r in pairs if r > b]
            if time_diffs:
                avg_seconds = sum(time_diffs) / len(time_diffs)
                stats['avg_borrow_to_repay_days'] = round(avg_seconds / 86400, 2)
            else:
                stats['avg_borrow_to_repay_days'] = None
        else:
            stats['avg_borrow_to_repay_days'] = None

    return wallet_stats


# -------- FUNCTION TO SCORE WALLETS -------- #
def score_wallets(wallet_stats):
    results = []
    for wallet, stats in wallet_stats.items():
        deposit = stats['total_deposit']
        withdraw = stats['total_withdraw']
        borrow = stats['total_borrow']
        repay = stats['total_repay']
        liquidated = stats['liquidated']

        repay_ratio = repay / borrow if borrow else 0
        withdraw_ratio = withdraw / deposit if deposit else 0

        score = 50
        reasons = []

        if repay_ratio > 0.7:
            score += 20
            reasons.append("High repay-to-borrow ratio")

        if withdraw_ratio < 0.5:
            score += 15
            reasons.append("Keeps deposits mostly intact")

        if liquidated:
            score -= 30
            reasons.append("Got liquidated")

        if borrow > deposit:
            score -= 10
            reasons.append("High borrow balance")

        score = max(0, min(100, score))
        if not reasons:
            reasons.append("No notable positive/negative behaviors detected")

        results.append({
            "wallet": wallet,
            "score": round(score, 2),
            "reason_for_score": "; ".join(reasons)
        })

    return pd.DataFrame(results)

# -------- MAIN EXECUTION -------- #
merged_data = load_and_merge_json_files(FILE_NAMES, DATA_DIR)
wallet_stats = extract_wallet_transactions(merged_data)
scored_df = score_wallets(wallet_stats)

# Save output
OUTPUT_PATH = os.path.join(DATA_DIR, "wallet_scores.csv")
wallet_behavior_df = pd.DataFrame.from_dict(wallet_stats, orient='index')
wallet_behavior_df['wallet'] = wallet_behavior_df.index
wallet_behavior_df.to_csv("wallet_behavior_details.csv", index=False)
scored_df.to_csv(OUTPUT_PATH, index=False)

# Preview top 5
print(scored_df.head())
