# YouTube Downloader with an API
Download videos from YouTube and many more sites just by sending an API request to this container

# Usage

`docker run -dt --network <some-docker-network> --name youtube-downloader -v $PWD:/downloads -e FLASK_PORT=9001 christus02/youtube-downloader-api`
