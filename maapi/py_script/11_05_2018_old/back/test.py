from MaaPi_DB_connection import MaaPiDBConnection

d=MaaPiDBConnection().order_by('dev_id').filters_eq(dev_id=1).get_table("devices")
print(d[1]['dev_value'],d[1]['dev_value_old'],d[1]['dev_user_id'],d[1]['dev_user_name'])
