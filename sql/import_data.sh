curl -o osnap_legacy.tar.gz https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz
tar -xvzf osnap_legacy.tar.gz
python import_data.py
rm osnap_legacy.tar.gz
rm -r osnap_legacy