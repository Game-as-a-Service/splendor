def snake_to_camel(s: str) -> str:
    components = s.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(s: str) -> str:
    import re

    # 將大寫字母和小寫字母分開，並在它們之間插入下劃線
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    # 將小寫字母和大寫字母分開，並在它們之間插入下劃線
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    # 將下劃線後面的數字移到前面
    return re.sub(r"(?<!\d)(\d+)(?!<\d)", r"_\1", s2).lower()
