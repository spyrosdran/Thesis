from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urlparse, parse_qs


class YouTubeCommentScraper:

    def __init__(self):
        self.api_key = "API_KEY"
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def get_video_id(self, value):
        query = urlparse(value)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        # Failed to get the video ID
        return None

    def scrape_comments(self, url):
        video_id = self.get_video_id(url)
        try:
            # Make the API request to retrieve comments
            response = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100,  # Set the maximum number of comments to retrieve per page
            ).execute()

            comments = []
            # Saving the comments into the comments array
            while response:
                for item in response["items"]:
                    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                    comments.append(comment)

                if "nextPageToken" in response:
                    response = self.youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=100,
                        pageToken=response["nextPageToken"]
                    ).execute()
                else:
                    break

            return comments

        except HttpError as e:
            return "Something went wrong"
