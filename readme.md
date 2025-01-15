# Qwant Advanced search ( :fr: language)

## Description

This project is an academic project done last academic year (in french).

Following a search input entered by user, two modes are set :
    - Context based search : with a context entered by the user, the software searchs for the anwser
    - Vector based search : the user search with only a question asked. The software is set to answer based off the question asked.

## Limits
The context based search is not ideal as its needs the user to add context for the software to find the answer.

The vector based is not effective. If the question is too vague (`Où se trouve Paris ?`), it will return a wrong answer.

## How to start the project

For the vector based query, you will need to create a pinecone account alongside adding a project and appending an API key.

Once it's done, you can replace the value set in the `serving/.env` file by the API key from the Pinecone website.

```sh
cd serving
docker compose up -d --build
cd ../webapp
docker compose up -d --build
```

If everything is correctly set up, you can launch the application at `http://0.0.0.0:8081`.