FROM alpine
MAINTAINER Raghul Christus

RUN set -xe \
    && apk add --no-cache ca-certificates \
                          ffmpeg \
                          openssl \
                          python3 \
                          aria2 \
    && pip3 install youtube-dl flask

RUN mkdir /downloads
COPY youtube_downloader.py /code/
WORKDIR /code

CMD ["python3", "/code/youtube_downloader.py"]
