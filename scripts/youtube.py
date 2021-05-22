import httpx
import os
import aiofiles
from youtubesearchpython.__future__ import VideosSearch
from youtubesearchpython import Video, StreamURLFetcher


class YouTube:
    def __init__(self):
        self.streamURL = StreamURLFetcher()
    
    async def VideoGet(self, url):
        video = await Video.get(url)
        return video
    
    async def fetchURL(self, video, id):
        url = await self.streamURL.get(video, id)
        return url

    async def download(self, videoName: str) -> dict:
        if 'youtu' not in videoName:
            ''' Searching Video '''
            video = await self.__getVideo(videoName)
            if not video:
                return None
            videoId = video['id']
        else:
            videoId = self.__getVideoId(videoName)
        ''' Getting Stream URL '''
        video = Video.get(videoId)
        videoUrl = self.streamURL.get(video, 251)
        if not videoUrl:
            ''' Fallback AAC '''
            videoUrl = self.streamURL.get(video, 140)
        if os.path.isfile(f'{videoId}.webm'):
            return video
        elif type(video) is dict:
            ''' Saving Track File '''
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    videoUrl,
                    timeout=None,
                    headers={'Range': 'bytes=0-'}
                )
            if response.status_code in [200, 206]:
                async with aiofiles.open(f'{videoId}.webm', 'wb') as file:
                    await file.write(response.content)
            return video
        else:
            return None
            
    def __getVideoId(self, videoLink: str) -> str:
        if 'youtu.be' in videoLink:
            if videoLink[-1] == '/':
                return videoLink.split('/')[-2]
            return videoLink.split('/')[-1]
        elif 'youtube.com' in videoLink:
            if '&' not in videoLink:
                return videoLink[videoLink.index('v=') + 2:]
            return videoLink[videoLink.index('v=') + 2: videoLink.index('&')]
        else:
            return videoLink

    async def __getVideo(self, videoName):
        search = VideosSearch(videoName, limit=1)
        result = await search.next()
        return result['result'][0]
