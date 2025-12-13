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


### update_storage
```
curl --location 'http://127.0.0.1:5050/update_storage' \
--header 'Content-Type: text/plain' \
--data 'Cookies:
_ga	GA1.1.929170509.1765614867	.z.ai	/	2027-01-17T08:34:40.192Z	29						Medium
_ga_Z8QTHYBHP3	GS2.1.s1765614866$o1$g1$t1765614885$j41$l0$h0	.z.ai	/	2027-01-17T08:34:45.236Z	59						Medium
_gcl_au	1.1.847586300.1765614867	.z.ai	/	2026-03-13T08:34:26.000Z	31						Medium
acw_tc	0a094e6517656148679171618e4ec628874172403fa4108ee13988844199ed	chat.z.ai	/	2025-12-13T09:04:25.722Z	68	✓					Medium
oauth_id_token	eyJhbGciOiJSUzI1NiIsImtpZCI6IjEzMGZkY2VmY2M4ZWQ3YmU2YmVkZmE2ZmM4Nzk3MjIwNDBjOTJiMzgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI4MDA0MjQzOTE5MjgtcXNxOTZ2YTN0cHVmcTRhamE4YTRhYmlvYm05MTBha3MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI4MDA0MjQzOTE5MjgtcXNxOTZ2YTN0cHVmcTRhamE4YTRhYmlvYm05MTBha3MuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDM4NjU2NzA1MDY1OTE2MDkyNDIiLCJlbWFpbCI6ImFtaXJraG9zcmF2aXlhbjIwMDVAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJVdl8tNWV4eHRtR1I5Qlc0eDh3WE5nIiwibm9uY2UiOiJZc1NvMTNJRVdmQ3lnN1hKV1dnTyIsIm5hbWUiOiJBbWlyIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0x6MjhVVDY4Q0l5VUNvM1NVeFppaGc4MUVEaXN3SzVHeEdlSjVZRDdqdXJvTGg0Zz1zOTYtYyIsImdpdmVuX25hbWUiOiJBbWlyIiwiaWF0IjoxNzY1NjE0ODgxLCJleHAiOjE3NjU2MTg0ODF9.Vw18qHNtsUUJYNQYgfHWdEtAYwMeRsICq3AlboE1lW78WKgcveyO51W3aG7jS7q9OKqA_xkReGHBl56Hy6mInBzZFcue509I7XfdDR2jfbcLmrt6X7EDJZNigaJX-CTQ56rXb5Q3S2UCa-vPgT3wXxUTYESvV0p9OJhLhn858M1hDX0ZMJ9zkgGm5745Ow6sV7gWQFPcMKBOV_c68JrIyaAh3P15IClTv01-3rMWeJ459f1x_TaLKE5LgKi3prkyTry3QXG4uuzu5E4a63KrZKXfHrariYbHDSM_XhvdKMklKWykB5ZVCsg0seOLCJwH0VFLXwK0w2A_kuuRuoLypA	chat.z.ai	/	Session	1172	✓	✓	Lax			Medium
ssxmod_itna	1-eqUxuD97qiwxgDfxe9BxekGDmx0xQKGOehDzxC5iOHDu6xjKidDRDB_rZinFOxbe_K1SDDIOQYW_imzDBTHEWDCdKGfDQao8qY9qxx_rn=BgQ4NKnwxq_=M06oM5=oQkFu96k09=lZ6sdNl3xhbDB3DbT3qIEmOS4GGD0oDt4DIDAYDDxDWDYoEDGUWDG=D7rTi5pWtxi3DboaDmqrFC=FD03P=EW9oDDtDiq2N7ET_DDN_FIYKiDbe_PD_iW9W/YWqmzGxneDM7xGX_YC_nlH2ovYWpFkUs6o3xB=gxBQbyPnNfETadZa52GICmbnpOnhbehvjGtlD9mDKAe10IOmGnlD4Weqm2nmIUB2bDDASxrbThS4qnioIvZ0HfmR/3x4gKzfOz32Kvx44q4S0Ob7NY0N44qz0RIreSbez0qiDbi8wQBqeD	.z.ai	/	2025-12-13T09:05:00.000Z	449						Medium
ssxmod_itna2	1-eqUxuD97qiwxgDfxe9BxekGDmx0xQKGOehDzxC5iOHDu6xjKidDRDB_rZinFOxbe_K1SDDIOQYW_imbDGfWe_pS0GxGaQQuD9YuYDGNdFEZDMGXe5kGGa5swO7kjYq0RB6w2r35V1h2_hD7E6cDZ=Dh1Gpxs=T1QG0_ha9Q3801H=0QbFHQc6Www=qhypK=k9Hew2Fs2=FmH/pGX3gQpE8szUpwbKqxEhDE/PrIVpLtPti12Sdk1cLtFhYnF23wP4dw3Sp1T3=syxvaARBE7cLxf3Q=18OgRhkB1KoqNe3=wu0QsEXAeRAt9nCjFwYbmlnrBb7AqGIxU95qWWQiGpUwhePsU97CyZWp//be7wq9mR70OlmaDK7A2aITXRwvFIlzGDVaXKadsDsYRkR4klexF93riOAxi0RiBvxbwtzYV/ER0R/QnN1afAYGIItABkYOy7EajeNcppBAUznV0qkIFUBKL45bm9a8M8rpPTEaiD4/br8u4mIKFOWwhOPwvAy/_xQuTkpB8/3ezPhbC49YBSEfYjOHSf9b00wA9RhRC9/RwonOKGMQTazqk7aezTOR7HpFkjH1bTHDoGmSH/E1XyFi48SZUpqftOUgbg9W8z0G0LwUd/ATAYeN=cvtobtY_Ike6HQPakGdzHScxC54qor126i8K_BOkcjvCFKDNVQ3rZQi5Sr8ANzF4csLHWoGgPxKkC9yrb1DZieHT1nGbuqKFGxvx1pxahP4R1lH8Anl78RVa4b2o4PZDxlqxrZieKrW7_RAxnqIADD	.z.ai	/	2025-12-13T09:05:00.000Z	800						Medium
token	eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQyMTg3ZWNiLWZiZjYtNDE3OS1iNjRlLTFhNmJkYWY0MWI2MyIsImVtYWlsIjoiYW1pcmtob3NyYXZpeWFuMjAwNUBnbWFpbC5jb20ifQ.g78iabkZ5K89nP0ybvqcVdGt_AdSqjwbxX1DMQBDhxmkCIu0GYkYXmVLw2hgQepQV8vOP92q7UTr0T7TuJY2dw	chat.z.ai	/	Session	243	✓	✓	Lax			Medium


Session:
sveltekit:scroll	{"1765614866368":{"x":0,"y":0},"1765614866369":{"x":0,"y":0},"1765614879958":{"x":0,"y":0},"1765614879959":{"x":0,"y":0}}
sveltekit:snapshot	{}


local:
__00b204e9800998__	1736314395a19b16d8cf7f||1781166866307
_arms_session	7e596b5c73c54371898354b1a6f0ae75-1-1765614866180-1765614892750
_arms_uid	uid_v21rotc6lfz2qvvh
_gcl_ls	{"schema":"gcl","version":1,"gcl_ctr":{"value":{"value":0,"timeouts":0,"creationTimeMs":1765614866622},"expires":1773390866622}}
lastCancelTime	1765614885237
locale	en-US
modelRecommendTime	1
shouldSuggestModel	1
sidebar	false
theme	light
token	eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQyMTg3ZWNiLWZiZjYtNDE3OS1iNjRlLTFhNmJkYWY0MWI2MyIsImVtYWlsIjoiYW1pcmtob3NyYXZpeWFuMjAwNUBnbWFpbC5jb20ifQ.g78iabkZ5K89nP0ybvqcVdGt_AdSqjwbxX1DMQBDhxmkCIu0GYkYXmVLw2hgQepQV8vOP92q7UTr0T7TuJY2dw
'

```