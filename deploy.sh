cd xbook-frontend
npm install
npm run-script build
firebase deploy
cd ../xbook-backend
pip3 install -r meta_files/requirements.txt
gcloud run deploy
