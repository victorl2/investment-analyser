# Investment Analyser
Scrappe and analyse investment data from various sources on the web

## Configuration
You need to setup the required variables in a `.env` at the root of the project.

It should contain a coma separated list for sources
```
sources="http://source1.com,http://source2.com"
```

## Execution
You need [Docker](https://www.docker.com/) installed on your machine in order to run the project.

+ Build the image
```
docker build -t investment-analyser .
```

+ Run the container
```
docker run investment-analyser
```