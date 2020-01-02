# XBook
A terminal-esque interface for Facebook

## QuickStart
Ensure that port 3000 and port 8080 are free and your browser allows Cross Origin Access
```
git clone https://github.com/shershah010/xbook.git
cd xbook/xbook-frontend
npm install
cd ../xbook-backend
pip install -r requirements.txt
cd ..
./startup.sh
```

## Frontend
The frontend uses React. It also interfaces with the Facebook SDK and the Firebase Libraries. To host on Firebase, first check that you are on the `master` branch. Then run the following:
```
npm run-script build
firebase deploy
```

## Backend
The backend is Python with Flask. Right now it is simple as it is only one endpoint. Because most of the web app is interfacing with Facebook, the backend has few uses.

## Testing
The frontend tests are in jest but used through react's interface. All frontend tests should have `.test.js` extension. To run frontend tests go to the `xbook-frontend` directory and run the command `npm test`.

The backend tests are in unittest and they all live in the file `test.py`. In order to run the backend tests, go to the `xbook-backend` directory and run the command `python test.py`.

When a branch is pushed to github, circleci will run both frontend and backend tests on that branch. See the `.circleci/config.yml` for details.
