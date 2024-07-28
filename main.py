import requests

TOKEN = ''  
HEADERS = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json'
}
DISCORD_API_BASE_URL = 'https://discord.com/api/v9'

def load_allowed_group_ids():
    with open('group_id.txt', 'r') as file:
        return {int(line.strip()) for line in file}

def get_user_groups():
    response = requests.get(f'{DISCORD_API_BASE_URL}/users/@me/channels', headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return []

def leave_group(group_id):
    response = requests.delete(f'{DISCORD_API_BASE_URL}/channels/{group_id}', headers=HEADERS)
    if response.status_code == 200:
        print(f"Left group (channel) with ID: {group_id}")
    else:
        print(f"Error leaving group (channel) {group_id}: {response.status_code}")

def main():
    while True:
        allowed_group_ids = load_allowed_group_ids()
        groups = get_user_groups()
        for group in groups:
            if group['type'] == 3:  
                group_id = int(group['id'])
                if group_id not in allowed_group_ids:
                    leave_group(group_id)

if __name__ == '__main__':
    main()
