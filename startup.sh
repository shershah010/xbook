(cd xbook-frontend
npm start) &
(cd xbook-backend/meta_files
./meta_files/cloud_sql_proxy -instances=xbook010:us-west1:xbook-db=tcp:3307) &
(wait 10
cd xbook-backend
python3 main.py) && fg
