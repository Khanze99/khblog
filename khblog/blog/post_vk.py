from requests import get, post, exceptions
import logging

from django.conf import settings


logger = logging.getLogger('CELERY')


class API:
    def __init__(self, path_image=None, access_token=settings.ACCESS_TOKEN_VK, user_id=169002303, group_id=-135184895,
                 message='testing api', attachments='http://www.khanze.com,'):
        self.url = "https://api.vk.com/method/{}"
        self.path_image = path_image
        self.expires_in = 0
        if path_image is not None:
            self.path_image = settings.BASE_DIR + path_image
        self.user_id = user_id
        self.group_id = group_id
        self.access_token = access_token
        self.v = 5.52
        self.message = message
        self.attachments = attachments

    def get_wall_upload_server(self):
        try:
            logger.info('Get upload_url')
            return get(self.url.format('photos.getWallUploadServer'), params={'access_token': self.access_token,
                                                                              'v': self.v,
                                                                              'expires_in': self.expires_in}).json()['response']['upload_url']
        except KeyError:
            response = get(self.url.format('photos.getWallUploadServer'), params={'access_token': self.access_token,
                                                                             'v': self.v,
                                                                             'expires_in': self.expires_in}).json()
            logger.warning(f'Error message: {response["error"]["error_msg"]}')

    def upload_image(self):
        response_server = post(self.get_wall_upload_server(), files={'file1': open(self.path_image, mode='rb')}).json()
        logger.info('Upload image to vk server')
        return response_server

    def save_wall_photo(self):
        upload_info = self.upload_image()
        response_post = get(self.url.format('photos.saveWallPhoto'), params={'access_token': self.access_token,
                                                                             'photo': upload_info['photo'],
                                                                             'server': upload_info['server'],
                                                                             'hash': upload_info['hash'],
                                                                             'v': self.v,
                                                                             'uid': self.user_id,
                                                                             'expires_in': self.expires_in}).json()
        logger.info('Save wall photo vk')
        return response_post['response'][0]['id']

    def send(self):
        try:
            if self.path_image is not None:
                response_wall_post = get(self.url.format('wall.post'), params={'access_token': self.access_token,
                                                                               'message': self.message,
                                                                               'attachments': self.attachments+'photo{owner_id}_{media_id},'.format(owner_id=self.user_id, media_id=self.save_wall_photo()),
                                                                               'owner_id': self.group_id,
                                                                               'v': self.v,
                                                                               'expires_in': self.expires_in}).json()
                logger.info('request post to vk with image')
                return response_wall_post
            response_wall_post = get(self.url.format('wall.post'), params={'access_token': self.access_token,
                                                                           'message': self.message,
                                                                           'attachments': self.attachments,
                                                                           'owner_id': self.group_id,
                                                                           'v': self.v,
                                                                           'expires_in': self.expires_in}).json()
            logger.info('send post to vk')
            return response_wall_post
        except exceptions.MissingSchema:
            logger.warning('Request error')