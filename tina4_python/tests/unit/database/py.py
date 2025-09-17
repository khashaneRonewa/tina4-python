import fdb

try:
    con = fdb.connect(dsn='localhost/3050:test.fdb', user='sysdba', password='masterkey')
    print("✅ Firebird client found, connection OK")
    con.close()
except Exception as e:
    print("❌ Firebird client missing or connection failed:", e)
