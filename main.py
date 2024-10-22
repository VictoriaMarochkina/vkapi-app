import requests
import json
import os

VK_TOKEN = ""
VK_API_URL = "https://api.vk.com/method/"


def get_user_data(user_id):
    url = VK_API_URL + "users.get"
    params = {
        "user_ids": user_id,
        "fields": "followers_count",
        "access_token": VK_TOKEN,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    return response.json()


def get_followers(user_id):
    url = VK_API_URL + "users.getFollowers"
    params = {
        "user_id": user_id,
        "access_token": VK_TOKEN,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    return response.json()


def get_followers_info(follower_ids):
    url = VK_API_URL + "users.get"
    params = {
        "user_ids": ",".join(map(str, follower_ids)),
        "fields": "first_name,last_name",
        "access_token": VK_TOKEN,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    return response.json()


def get_subscriptions(user_id):
    url = VK_API_URL + "users.getSubscriptions"
    params = {
        "user_id": user_id,
        "access_token": VK_TOKEN,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    return response.json()


def get_groups_info(group_ids):
    url = VK_API_URL + "groups.getById"
    params = {
        "group_ids": ",".join(map(str, group_ids)),
        "fields": "name",
        "access_token": VK_TOKEN,
        "v": "5.131"
    }
    response = requests.get(url, params=params)
    return response.json()


def save_to_json(data, filename="vk_user_data.json"):
    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Данные сохранены в файл {file_path}")


def main():
    if not VK_TOKEN:
        return

    user_id_input = input("Введите ID пользователя или его screen_name: ")

    user_data = get_user_data(user_id_input)

    if user_data and 'response' in user_data:
        user_info = user_data['response'][0]
        user_id = user_info['id']

        if user_info.get('is_closed', True):
            followers_data, subscriptions_data = {}, {}
        else:
            followers_data = get_followers(user_id)
            if 'response' in followers_data:
                follower_ids = followers_data['response']['items']
                followers_info = get_followers_info(follower_ids)
                followers_data['details'] = followers_info['response']

            subscriptions_data = get_subscriptions(user_id)
            if 'response' in subscriptions_data and 'groups' in subscriptions_data['response']:
                group_ids = subscriptions_data['response']['groups']['items']
                groups_info = get_groups_info(group_ids)
                subscriptions_data['details'] = groups_info['response']

        data = {
            "user": user_data,
            "followers": followers_data,
            "subscriptions": subscriptions_data
        }
        save_to_json(data)
    else:
        return


if __name__ == "__main__":
    main()
