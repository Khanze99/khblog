from requests import get, post
from django.conf import settings


class API:
    def __init__(self, path_image=None, access_token=settings.ACCESS_TOKEN_VK, user_id=169002303, group_id=-135184895,
                 message='testing api', attachments='http://www.khanze.com,'):
        self.url = "https://api.vk.com/method/{}"
        self.path_image = path_image
        if path_image is not None:
            self.path_image = settings.BASE_DIR + path_image
        self.user_id = user_id
        self.group_id = group_id
        self.access_token = access_token
        self.v = 5.50
        self.message = message
        self.attachments = attachments

    def get_wall_upload_server(self):
        try:
            return get(self.url.format('photos.getWallUploadServer'), params={'access_token': self.access_token, 'v': self.v}).json()['response']['upload_url']
        except KeyError:
            print(get(self.url.format('photos.getWallUploadServer'), params={'access_token': self.access_token, 'v': self.v}).json())

    def upload_image(self):
        response_server = post(self.get_wall_upload_server(), files={'file1': open(self.path_image, mode='rb')}).json()
        return response_server

    def save_wall_photo(self):
        upload_info = self.upload_image()
        response_post = get(self.url.format('photos.saveWallPhoto'), params={'access_token': self.access_token,
                                                                             'photo': upload_info['photo'],
                                                                             'server': upload_info['server'],
                                                                             'hash': upload_info['hash'],
                                                                             'v': self.v,
                                                                             'uid': self.user_id}).json()
        return response_post

    def send(self):
        if self.path_image is not None:
            response_wall_post = get(self.url.format('wall.post'), params={'access_token': self.access_token,
                                                                           'message': self.message,
                                                                           'attachments': self.attachments+'photo{owner_id}_{media_id},'.format(owner_id=self.user_id, media_id=self.save_wall_photo()['response'][0]['id']),
                                                                           'owner_id': self.group_id,
                                                                           'v': self.v}).json()
            return response_wall_post
        response_wall_post = get(self.url.format('wall.post'), params={'access_token': self.access_token,
                                                                       'message': self.message,
                                                                       'attachments': self.attachments,
                                                                       'owner_id': self.group_id,
                                                                       'v': self.v}).json()
        return response_wall_post


# request = API('/home/khanze/Pictures/Wallpapers/code.jpg')
# request.send()
# photo{owner_id}_{media_id},
