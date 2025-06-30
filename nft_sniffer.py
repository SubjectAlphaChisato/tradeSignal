"""
Run with:
    mitmdump -s monitor.py --set block_global=false
Press Ctrl+C to stop.  Runs fine under pythonw or as a Windows service.
"""

from datetime import datetime
import json
import os

from pymongo import MongoClient, UpdateOne
from mitmproxy import http, ctx

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME   = "portals_market"
COL_NFTS  = "nfts"

client     = MongoClient(MONGO_URI)
collection = client[DB_NAME][COL_NFTS]
collection.create_index("id", unique=True)        # enforce uniqueness

TARGET_URL = "https://portals-market.com/api/market/actions/"

class PortalsSniffer:
    def response(self, flow: http.HTTPFlow):
        print("current url" + flow.request.pretty_url)
        if not flow.request.pretty_url.startswith(TARGET_URL):
            return
        
        try:
            data = json.loads(flow.response.text)
        except Exception as e:
            ctx.log.error(f"JSON decode failed: {e}")
            return

        actions = data.get("actions", [])
        bulk_ops = []

        for action in actions:
            nft = action.get("nft") or {}
            if not nft:
                continue

            # Flatten action info into the NFT doc
            nft_doc = {
                **nft,
                "last_action_type": action.get("type"),
                "last_action_amount": action.get("amount"),
                "last_action_ts": datetime.fromisoformat(action.get("created_at").rstrip("Z")),
            }

            # Upsert on NFT id
            bulk_ops.append(
                UpdateOne({"id": nft["id"]},
                          {"$set": nft_doc},
                          upsert=True)
            )

        if bulk_ops:
            result = collection.bulk_write(bulk_ops, ordered=False)
            ctx.log.info(
                f"Bulk upsert → inserted={result.upserted_count}, "
                f"modified={result.modified_count}"
            )

addons = [PortalsSniffer()]
print("data caught")