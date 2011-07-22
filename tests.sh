#!/bin/bash
DROPBOX_TSIN32_TXT="~/Dropbox/linux/common/tsin32.txt"

# backup
cp ~/.gcin/tsin32 tsin32.bak

echo "=== Python 2 ==="
echo "==  Merge     =="
python merge_gcin_tsin_from.py $DROPBOX_TSIN32_TXT || exit -1
echo ""

echo "=== Python 3 ==="
echo "==  Merge     =="
python3 merge_gcin_tsin_from.py $DROPBOX_TSIN32_TXT || exit -1
echo ""

echo "=== Python 2 ==="
echo "==  Push      =="
python push_gcin_tsin.py $DROPBOX_TSIN32_TXT || exit -1
echo ""

echo "=== Python 3 ==="
echo "==  Push      =="
python3 push_gcin_tsin.py $DROPBOX_TSIN32_TXT || exit -1
echo ""

# restore
cp tsin32.bak ~/.gcin/tsin32

exit 0
