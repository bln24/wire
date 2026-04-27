#!/bin/bash
# WIRE auto-deploy to SiteGround
# Runs after every git push to instantly update wire.bln24.com

WIRE_DIR="/Users/t24/Desktop/T24/wire"
SG_HOST="ssh.briann50.sg-host.com"
SG_PORT="18765"
SG_USER="u1954-3paantqe2j9n"
SG_KEY="/Users/t24/.ssh/wire_siteground_deploy"
SG_PATH="~/www/wire.briann50.sg-host.com/public_html"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deploying WIRE to SiteGround..."

scp -i "$SG_KEY" \
    -o StrictHostKeyChecking=no \
    -o ConnectTimeout=15 \
    -P "$SG_PORT" \
    "$WIRE_DIR/index.html" \
    "$WIRE_DIR/opps-data.js" \
    "$SG_USER@$SG_HOST:$SG_PATH/"

if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ WIRE deployed successfully to wire.bln24.com"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Deploy failed — check SSH key and connection"
    exit 1
fi
