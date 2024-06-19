import os, sys
import json
from urllib.parse import urlparse, parse_qs
import google.oauth2.credentials
import googleapiclient.discovery
from googleapiclient.errors import HttpError

scopes = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/youtube",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
]

videos = [
    "https://www.youtube.com/watch?v=QwZ4HGgcFz8&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-",
    "https://www.youtube.com/watch?v=psd4rJvBF8E&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-&index=2",
    "https://www.youtube.com/watch?v=qYgmDdSzTNs&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-&index=3",
    "https://www.youtube.com/watch?v=ba3125ppXXU&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-&index=4",
    "https://www.youtube.com/watch?v=CahOdjudiTI&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-&index=5",
    "https://www.youtube.com/watch?v=eSYhqiMt_lw&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-&index=6",
    "https://www.youtube.com/watch?v=kV-q5R4DP24&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-&index=7",
    "https://www.youtube.com/watch?v=wCO783BxZjA&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-&index=8",
    "https://www.youtube.com/watch?v=MWrLzO5LdVg&list=PL1hdtOv5_bcceSo65HWoU51wmLVBNK2C-&index=9",
]


def list(youtube):
    request = youtube.playlists().list(
        part="snippet", channelId="UCo5V3CHVRTl_c_BkJtpoDaQ"
    )
    return request.execute()


def extract_id(url) -> str:
    query = urlparse(url).query
    return parse_qs(query).get("v")


def get_video_ids():
    return [id for v in map(extract_id, videos) for id in v if v]


def create(
    youtube, title="Muruga Saranam", description="Vetrivael Muruganukku! Arohara!"
):
    request = youtube.playlists().insert(
        part="snippet,status,id",
        body={
            "snippet": {
                "title": title,
                "description": description,
            },
            "status": {"privacyStatus": "public"},
        },
    )
    return request.execute()


def insert_video(youtube, playlist_id, video_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id},
            }
        },
    )
    return request.execute()


def insert_videos(youtube, playlist_id):
    res = []
    for id in get_video_ids():
        res.append(insert_video(youtube, playlist_id, id))
    return res


def delete(youtube, playlist_id):
    try:
        request = youtube.playlists().delete(id=playlist_id)
        response = request.execute()
    except HttpError as e:
        print(f"Error deleting playlist {playlist_id}: {e}")
        return {}
    else:
        return response


def get_api_client():
    api_service_name = "youtube"
    api_version = "v3"
    token = {}
    token_str = os.getenv("API_TOKEN_JSON")
    if token_str:
        print("Using token from Environment...")
        token = json.loads(token_str)
    else:
        import credentials

        token = credentials.token
    # Get credentials and create an API client
    credentials = google.oauth2.credentials.Credentials(**token)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )
    return youtube


def main():
    youtube = get_api_client()
    response = ""

    command = sys.argv[1]
    if command == "list":
        response = list(youtube)
    elif command == "create":
        response = create(youtube)
    elif command == "delete":
        playlist_id = sys.argv[2]
        print(f"Deleting playlist ID: [{playlist_id}]...")
        response = delete(youtube, playlist_id)
    elif command == "fill":
        playlist_id = sys.argv[2]
        print(f"Adding videos to playlist ID: [{playlist_id}]")
        response = insert_videos(youtube, playlist_id)
    elif command == "publish":
        print("Creating Playlist...")
        response = create(youtube)
        playlist_id = response.get("id")
        if playlist_id:
            print(f"Created playlist: [{playlist_id}]. Adding videos to it...")
            response = insert_videos(youtube, playlist_id)
    else:
        print(f"Unknown command: {command}")
    print(json.dumps(response))


if __name__ == "__main__":
    main()
