ssh -i /Users/richarddunks/Dropbox/Datapolitan/admin/datapolitan_com_virginia.pem ec2-user@52.20.51.98
scp -i /Users/richarddunks/Dropbox/Datapolitan/admin/datapolitan_com_virginia.pem keys.py keys_boro.py ec2-user@52.20.51.98:citibike_dock_bot/
