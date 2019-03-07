import requests
import json
from faker import Faker
from faker.providers import internet
from django.utils.text import slugify
import configparser
import random

fake = Faker()
fake.add_provider(internet)


config = configparser.ConfigParser()
config.read('config.ini')

NUMBER_OF_USERS = config['MAIN']['NUMBER_OF_USERS']
MAX_POSTS_PER_USER = config['MAIN']['MAX_POSTS_PER_USER']
MAX_LIKES_PER_USER = config['MAIN']['MAX_LIKES_PER_USER']
URL = 'http://127.0.0.1:8000'


def create_user():
    data = {'username': fake.user_name(),
            'password': fake.password(length=16, special_chars=True, digits=True, upper_case=True, lower_case=True),
            'email': fake.email()}
    response = requests.post(url=URL + '/api/auth/users/', data=data)
    if response.status_code == 201:
        login_response = requests.post(url=URL + '/api/auth/jwt/create/', data={'username': data.get('username'),
                                       'password': data.get('password')})
        data = json.loads(login_response.content)
        return data
    return None


def jwt_verify(data):
    jwt_access = data.get('access')
    jwt_refresh = data.get('refresh')
    jwt_verification = requests.post(url=URL + '/api/auth/jwt/verify',
                                     headers={'Authorization': f"JWT {jwt_access}"},
                                     data={'token': jwt_access})
    if jwt_verification.status_code != 200:
        response = requests.post(url=URL + '/api/auth/jwt/refresh/',
                                 headers={'Authorization': f"JWT {jwt_refresh}"})
        auth_data = json.loads(response.content)
        jwt_access = auth_data.get('access')
        jwt_refresh = auth_data.get('refresh')
    return jwt_access, jwt_refresh


def create_posts(data):
    for _ in range(random.randint(1, int(MAX_POSTS_PER_USER))):
        name = fake.sentence(nb_words=4, variable_nb_words=True, ext_word_list=None)
        post_data = {
            'name': name,
            'slug': slugify(name),
            'text': fake.text(max_nb_chars=250, ext_word_list=None)
        }
        jwt_access, jwt_refresh = jwt_verify(data=data)
        response = requests.post(url=URL + '/api/blog/post/',
                                 headers={'Authorization': f"JWT {jwt_access}"},
                                 data=post_data)
        if response.status_code == 201:
            create_likes(data)


def create_likes(data):
    jwt_access, jwt_refresh = jwt_verify(data=data)
    response = requests.get(url=URL + '/api/blog/post/',
                            headers={'Authorization': f"JWT {jwt_access}"})
    posts = json.loads(response.text)

    for _ in range(random.randint(1, int(MAX_LIKES_PER_USER))):
        slug = posts[len(posts) - 1].get('slug')
        response = requests.post(url=URL + f'/api/blog/post/{slug}/like',
                                 headers={'Authorization': f"JWT {jwt_access}"})
        if response.status_code == 401:
            jwt_access, jwt_refresh = jwt_verify(data=data)
            requests.post(url=URL + f'/api/blog/post/{slug}/like',
                          headers={'Authorization': f"JWT {jwt_access}"})


if __name__ == "__main__":
    posts_counter = 0

    for _ in range(int(NUMBER_OF_USERS)):
        auth_data = create_user()
        create_posts(data=auth_data)

    print('DONE!!!')
