## Install packages
```bash
pip install -r configs/requirements.txt
```

## Get VK token
```bash
python3 service\vk_get_token.py --phone 'YOU PHONE' --password 'YOU PASS' --client_id 'YOU client_id' --client_secret 'YOU client_secret'
```

## Setup config file

Make file like this:

`vk_config.yml`
```yml
url: "https://vk.com/video-203677279_456241182"
keywords:
  - "Уралсиб"
  - "уралсиб"
save_output_to_file: "comments_output.json"
vk_token: "you token like vk1.a.***" (if you don't run service\vk_get_token.py)
```

## Run script
```
python3 main.py --config vk_config.yml
```

`Example`
```bash
user@DESKTOP:/mnt/d/develop/mention_tracker$ python3 main.py --config vk_config.yml

▶🔄 Fetching comments for video https://vk.com/video-203677279_456241182
        ▶✅ Found 605 comments (including threads)

▶🔍 Searching for keywords...
        ▶✅ Found 2 matches for Уралсиб уралсиб
                ▶📍 {'id': 231862, 'from_id': 62105247, 'date': 1730655803, 'text': 'Интересно, в курсе ли Уралсиб, что персонаж, которого в
интеграции играет Арсений, в ГП постоянно врал?))))'}
                ▶📍 {'id': 232466, 'from_id': 221625211, 'date': 1730809792, 'text': 'Понравилась реклама Уралсиба. Не понравилась реклама пьянства (
все герои в истории пьяные), одновременно сексуально озабоченные и любят игрушки для взрослых. И самое главное - просто скучно. Для кого история - для
элиты, которая всем присытилась и ей больше делать нечего?'}

▶✒️ Write response output to file comments_output.json
```