from httptools import *

print(search({"q": "hello world & co"}))
print(search_url({"q": "python", "page": "2"}))
print(fetch_with_agent("MyBot/1.0"))
print(default_agent())
print(post_json({"name": "Ana", "age": 19, "tags": ["a", "b"]}))
print(post_form({"user": "ana", "city": "Bălți"}))
print(describe_status(200), describe_status(404), describe_status(503))
print(is_ok(204), is_ok(500))
print(count_redirects(3), final_url(2), first_hop(3))
print(cookie_demo("theme", "dark"), no_session_demo("theme", "dark"))
print(check_login("admin", "secret"), check_login("admin", "greșit"))

