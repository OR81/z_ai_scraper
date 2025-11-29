### login:
```
curl --location 'http://127.0.0.1:5050/login_with_cookies' \
--header 'Content-Type: application/json' \
--data '{
    "prompt_card": "Al Slides"
}'
```

### send prompt:
```
curl --location 'http://127.0.0.1:5050/send_prompt' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "سلام یک اسلاید دو صفحه ای راجع به آخرین خبر روز دنیا همراه با عکس و متن زیبا میخوام",
    "session_id": "da442ee5e96b4e7cb4b37b37a14a1438"
}'
```

### download html file:
```
http://127.0.0.1:5050/download_file?file_path=temp_htmls\\merged_20251123_173111_346694c2013e42d095977c9333a246e7.html
```

### active driver's list:
```
curl --location 'http://127.0.0.1:5050/active_driver' \
--header 'Content-Type: application/json'
```

### logout
```
curl --location 'http://127.0.0.1:5050/close_driver' \
--header 'Content-Type: application/json' \
--data '{
    "session_id": "2d6b1ab6d8454f50b22496a3bc2a9caf"
}'
```