# YouTube Downloader with an API
Download videos from YouTube and many more sites just by sending an API request to this container

# Usage

### Run the Container
`docker run -dt --name youtube-downloader -v $PWD:/downloads -e FLASK_PORT=9001 raghulc/youtube-downloader-api:latest`

If you want this container to be reachable by its name, then use `docker network` and start the container using the below command

`docker run -dt --network <some-docker-network> --name youtube-downloader -v $PWD:/downloads -e FLASK_PORT=9001 raghulc/youtube-downloader-api:latest`

### Get the IP of the Container from docker
`CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' youtube-downloader)`

### Send a curl to check if the container is UP and Running
```
curl http://$CONTAINER_IP:9001/server/status
{"status":true,"success":true,"up":true}
```

### Download a video from YouTube using default options
```
curl http://$CONTAINER_IP:9001/video/quickdownload -X POST --header "Content-Type: application/json" --data '{"url":"https://www.youtube.com/watch?v=C0DPdy98e4c"}'
{"alternate_filename":"/downloads/TEST VIDEO.mkv","filename":"/downloads/TEST VIDEO.webm","sent_url":"https://www.youtube.com/watch?v=C0DPdy98e4c","success":true}
```

The Video would be downloaded in your current working directory
