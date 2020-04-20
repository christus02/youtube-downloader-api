#!/usr/bin/python3

from flask import Flask, request, send_file, redirect, url_for, jsonify
import youtube_dl
import urllib
import os

app = Flask(__name__)
FLASK_PORT = int(os.environ.get('FLASK_PORT', 8080))

# Globals
BASE_PATH = '/downloads';

# Inputs to all the routes will be in JSON data
@app.route("/server/status", methods = ['POST', 'GET'])
def hello():
    return jsonify(up=True, status=True, success=True)

@app.route("/video/quickdownload", methods = ['POST'])
def quickDownload():
    '''
    Function to download the Video with default settings
    '''

    try:
        req_data = request.get_json()
        url = req_data.get('url')
        download_path = req_data.get('download_path')
    except:
        return jsonify(success=False)

    url = urllib.parse.unquote(url)
    output_template = download_path + '%(title)s.%(ext)s'
    ytdl_options = {'outtmpl': output_template}

    out = youtube_dl.YoutubeDL(ytdl_options).extract_info(url) # Downloads the video and returns a dict()
    filename = youtube_dl.YoutubeDL(ytdl_options).prepare_filename(out) # Generates filename from the provided info dict()
    alternate_filename = None
    alternate_filename = filename.replace("."+out['ext'], '.mkv') # In some cases where audio and video cannot be merged to mp4, it will be merged to mkv

    return jsonify(success=True,
            filename=filename,
            alternate_filename=alternate_filename,
            sent_url=url)

@app.route("/video/download", methods = ['POST'])
def download():
    '''
    Function to do an extensive download
    '''

    try:
        req_data = request.get_json()
        url = req_data.get('url')
        download_path = req_data.get('download_path')
        start_time = req_data.get('start_time')
        end_time = req_data.get('end_time')
        only_audio = req_data.get('only_audio')
    except:
        return jsonify(success=False)

    url = urllib.parse.unquote(url)
    ydlOpts = dict()

    # Add support for only Start Time or End Time
    if ((start_time is not None) and (end_time is not None)):
        ydlOpts['postprocessor_args'] = ["-ss", str(start_time), "-to", str(end_time)]
        #ydlOpts['format'] = 'bestvideo[ext=mp4]/best[ext=mp4]/best'

    if only_audio:
        ydlOpts['format'] = 'bestaudio/best'
        ydlOpts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    output_template = download_path + '%(title)s.%(ext)s'
    ydlOpts['outtmpl'] = output_template

    out = youtube_dl.YoutubeDL(ydlOpts).extract_info(url) # Downloads the video and returns a dict()
    filename = youtube_dl.YoutubeDL(ydlOpts).prepare_filename(out) # Generates filename from the provided info dict()
    alternate_filename = None
    alternate_filename = filename.replace("."+out['ext'], '.mkv') # In some cases where audio and video cannot be merged to mp4, it will be merged to mkv

    return jsonify(success=True,
            filename=filename,
            alternate_filename=alternate_filename,
            sent_url=url)

@app.route("/video/info", methods = ['POST'])
def getVideoInfo():
    '''
    Function to get Info about the Video
    '''

    try:
        req_data = request.get_json()
        url = req_data.get('url')
    except:
        return jsonify(success=False)

    # decode the URL
    url = urllib.parse.unquote(url)
    with youtube_dl.YoutubeDL() as ydl:
        videoInfo = ydl.extract_info(url, download=False)
        videoURL = videoInfo.get("url", None)
        videoId = videoInfo.get("id", None)
        videoTitle = videoInfo.get('title', None)
        videoThumbnail = videoInfo.get("thumbnail", None)
        videoDescription = videoInfo.get("description", None)
        videoDuration = videoInfo.get("duration", None)

    return jsonify(info=videoInfo,
            url=videoURL,
            video_id=videoId,
            title=videoTitle,
            thumbnail=videoThumbnail,
            description=videoDescription,
            duration=videoDuration,
            success=True,
            sent_url=url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT)
