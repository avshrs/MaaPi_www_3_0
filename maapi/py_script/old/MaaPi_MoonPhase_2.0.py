import datetime

def moon_phase(month, day, year):
    ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    if day == 31:
        day = 1
    days_into_phase = ((ages[(year + 1) % 19] +
                        ((day + offsets[month-1]) % 30) +
                        (year < 1900)) % 30)

    light = int(2 * days_into_phase * 100/29)
    if light > 100:
        light = light - 200;
    return light


d=datetime.datetime.now()
hour_v = d.hour
hour=0.04166666 * hour_v
month = d.month
day = d.day + hour
year = d.year
light = moon_phase(month, day, year)
