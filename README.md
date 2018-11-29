# visualGhudio
visualization of github data

also a pun

let's see how it goes

# Setup Instructions
1. Create a config.txt file in resource folder and add your github personal access token as follows; replace $YOUR_PERSONAL TOKEN with your personal token. Follow [this instruction](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) to create a token if you don't have one handy.
```
[github.com]
PersonalToken = $YOUR_PERSONAL_TOKEN
```
2. Setup a MongoDB and add your MongoDB connection string (URI) as follows; replace $CONNECTION_STRING. Also, add the DB name and collection name.
```
[mongodb.com]
ConnectionString = $CONNECTION_STRING
DbName = DB_NAME
CollectionName = COLLECTION_NAME
```