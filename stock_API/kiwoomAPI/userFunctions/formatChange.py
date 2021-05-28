def change_format(data):
    strip_data = data.lstrip("-0")
    if strip_data == "" or strip_data == ".00":
        strip_data = "0"

    try:
        format_data = format(int(strip_data), ",d")
    except:
        format_data = format(float(strip_data))
    if data.startswith("-"):
        format_data = "-" + format_data

    return format_data


def change_format2(data):
    strip_data = data.lstrip("-0")

    if strip_data == "":
        strip_data = "0"

    if strip_data.startswith("."):
        strip_data = "0" + strip_data

    if data.startswith("-"):
        strip_data = "-" + strip_data

    return strip_data


def date14digit_to_easyRead(date14digit):
    year = date14digit[0:4]
    month = date14digit[4:6]
    day = date14digit[6:8]
    hour = date14digit[8:10]
    minute = date14digit[10:12]
    second = date14digit[12:14]

    return year + "년 " + month + "월 " + day + "일 " + hour + "시 " + minute + "분 " + second + "초"
