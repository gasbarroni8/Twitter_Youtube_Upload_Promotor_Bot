## Twitter_Youtube_Upload_Promotor_Bot

# Installation
I have provided a requirements.txt file in the root of this project to help install this scripts dependencies. Head over to the root of this project in the cmd or terminal and run the following command.

```
pip3 install -r "./requirements.txt"
```

Their is a small issue with one of the dependencies so i have included the repo code in this project until this is resolved but for now we need to run one more command, again from the root folder.

```
cd ./resources/bitly_api && python setup.py install && cd ../../
```

# Twitter Configuration
Before you start using this program you will need to configure a few things firstly you will need to configure an app on twitter. If you head over to developer.twitter.com and create a new app. you will have to signup and create a developer account before you will be able to create an application. 

One you have created a new application click on the permissions tab in the modal window on twitter. Copy the two visible acceesstoken and api key to the corrisoding variables below. After click on the generate button in the popup to create your application secrets, againg following the description below place those values in to the corrisponding variables.

- API key => TWITTER_CONSUMER_KEY
- API secret key => TWITTER_CONSUMER_SECRET
- Access token => TWITTER_ACCESS_KEY
- Access token secret => TWITTER_ACCESS_SECRET

# Google Configuration
Next you will need to enable the YoutubeDataV3 api from the google developer console this can be found at the following link, https://console.developers.google.com. Once the api have been activated on your account you will need to head over to the credentials tab and setup some api tokens. Once in the credentials tab you will be able to see a create credentials button near the top of the page, click that and select the option 'API KEY'. Copy the value it generates and place that into the YOUTUBE_DATA_API_KEY variable.

# MongoDb Configuration
Im am using mongoDb atlas as a cloud storage database so the example below will let you know how to configure this. Sign up for a free account and once you are in click new project and then new cluster. This could take around 1-3 minutes for atlas to spin up a cluster. Make sure you select all the free options when setting this up as for this project it will never consure more than 500mb of data. ONce the cluster is created head over to the left side menu and select the database access button. once the page has loaded you should see an option to add a database user. in the modal select the authentication method password. The setup a username and a password for this user in the password authentication section below. make sure both read and write privileges are set for the user and the click the add user button. Next you will have to navigate to the network access option in the left menu and select ip whitelist.Click add IP Address and click allow access from anywhere or the more secure option would be to head over to http://httpbin.org/ip and copy the origin string without the "" at the start and end & then paste it into the whitelist entry field.

Once confiugured head back to the main page of the project and click the collections button on the cluster. you get two options once the page loads if you click on the 'Add My Own Data' option a small modal will appear. in the database name field enter the string 'python_promoter' & then in the collection name enter the string 'trendsDATA'. once you click continue you will see a database under the namespaces search filed click the small plus next to python_promotor and then add a second collection called 'youtubeDATA'

After this is setup you can head to the 'Overview tab' then find the connect button. then in the popup click 'Connect Yopur Application'. you will see an long connection string in the popup click the copy button and pasted this into the MONGO_DB_CONNECTION_STRING in your .env file. Remember to replace the `<password>` section with the password of the database user created earlier.

# Bitly Configuration
Next you will need to head over to bit.ly and create an account, once thats done you should be able to request a generic access tocken from the profile menu. Copy that token and place it in the BITLY_API_ACCESS_TOKEN env variable. The reason you need this token is to allow the full youtube urls to be shrunk to maximise the amount of content you can push into a tweet.

Once you have the fields populated you should be in a good position to copy the data into the .env file that you will have to create in the root of this project.

```js
ENVIRONMENT="development"
TWITTER_ACCESS_KEY=""
TWITTER_ACCESS_SECRET=""
TWITTER_CONSUMER_KEY=""
TWITTER_CONSUMER_SECRET=""
TWITTER_USERNAME=""
YOUTUBE_CHANNEL_ID=""
YOUTUBE_DATA_API_KEY=""
BITLY_API_ACCESS_TOKEN=""

MONGO_DB_CONNECTION_STRING="mongodb+srv://<USERNAME>:<PASSWORD>@cluster0-otaue.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGO_DB_NAME="python_promoter"
MONGO_DB_COLLECTION_NAME="trendsDATA"
MONGO_DB_COLLECTION_NAME="youtubeDATA"
```

# How To Run
Head into a cmd prompt or a terminal of some form and navigate to the root of this project. Then type in the following command.

```
python3 start.py
```