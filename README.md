# NFT Sniffer

This tool monitors and captures NFT marketplace activity from the Portals Market platform by intercepting API traffic and storing the data in MongoDB.

## Setup Instructions

### 1. Install Python Dependencies

```powershell
# Install required Python packages
py -m pip install --upgrade mitmproxy pymongo dnspython
```

Alternatively, you can use the requirements.txt file:

```powershell
py -m pip install -r requirements.txt
```

### 2. MongoDB Setup

Ensure MongoDB is running either:
- Locally at `localhost:27017` (default)
- Or through MongoDB Atlas (cloud)

The database `portals_market` will be created automatically when the script runs.

### 3. One-time Certificate Setup

1. Run mitmproxy once by executing either:
   ```
   mitmproxy
   ```
   or
   ```
   mitmweb
   ```

2. Open the built-in certificate page in Chrome: http://mitm.it

3. Download the Windows certificate (`mitmproxy-ca-cert.cer`)

4. Install the certificate:
   - Double-click the downloaded file
   - Select "Install Certificate"
   - Choose "Trusted Root Certification Authorities" as the store location
   - Complete the wizard

5. Restart Chrome

### 4. Running the NFT Sniffer

Start the proxy with the NFT sniffer script:

```powershell
mitmdump -s nft_sniffer.py
```

The script will now monitor traffic to `portals-market.com` and capture NFT activity in your MongoDB database.

## Environment Variables

- `MONGO_URI`: Override the default MongoDB connection string (default: `mongodb://localhost:27017`)