<h2>Local backend-end deploy</h2>

```bash
docker-compose up --build
```

<h2>Database Migrations</h2>

```
alembic revision --autogenerate -m "create table"
alembic upgrade head
```

<h2>Local front-end deploy (iOS Emulator)</h2>

To deploy the project locally and run it on an iOS emulator, execute the following commands:
1. Install cocoapods using Homebrew:
```
brew install cocoapods
```

2. Navigate to the ascoach/mobile directory and install dependencies:
```
cd ascoach/mobile
yarn
```

3. Install CocoaPods dependencies:
```
cd ios
pod install
```

4. Run the application on the iOS simulator:
```
cd ..
yarn ios
```

<h2>Local Testing</h2>

```bash
export TEST_ENV=active
cd backend
pytest tests
```

<h2>Environments</h2>
Prod: http://50.16.210.223/docs

<h2>Figma UI</h2>
https://www.figma.com/file/l8H9Q4ZCd00mEOV9YPLDlP/Ascoach?type=design&node-id=30-16481&mode=design

<h2>Documentation</h2>
https://www.notion.so/AsCoach-a661dedab2334709a7d232e67658b3bb
