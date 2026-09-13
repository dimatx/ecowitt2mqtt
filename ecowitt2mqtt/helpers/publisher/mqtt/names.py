"""Define human-friendly entity names for Home Assistant MQTT Discovery.

The data in this module is deliberately kept as plain tables (rather than being folded
into the entity descriptions) for two reasons:

1. Entity descriptions are keyed by data point key, many of which are globs. A single
   glob such as ``temp`` matches ``temp``, ``temp1`` through ``temp8`` and ``tempin``,
   so a single name per description would label eight distinct sensors identically.
2. Keeping the names in standalone tables means a future locale module can supply the
   same shape without touching any of the discovery logic.

Names use sentence case to match Home Assistant conventions, and never repeat the
device (station) name, because Home Assistant already prefixes it in the UI.

Wording is cross-checked against Ecowitt's own Home Assistant integration
(https://github.com/Ecowitt/ha-ecowitt-iot) and the key tables maintained by
home-assistant-libs/aioecowitt.

Every name here must be traceable to at least one of: Ecowitt's own integration,
aioecowitt, this project's test fixtures, or a data point this project declares in
const.py. A key whose meaning rests only on inference, or on sources that contradict
each other, is deliberately left out so that it falls back to its raw payload key --
showing a user "thi_ch1" is honest, whereas showing them a confidently wrong name is
not. "ldspw_ch*", "noise_ch*", "peak_ch*" and "thi_ch*" are absent for this reason.
"""

from __future__ import annotations

import re
from typing import Final

from ecowitt2mqtt.const import (
    DATA_POINT_GLOB_BAROM,
    DATA_POINT_GLOB_BATT,
    DATA_POINT_GLOB_GAIN_PIEZO,
    DATA_POINT_GLOB_GUST,
    DATA_POINT_GLOB_HUMIDITY,
    DATA_POINT_GLOB_LEAK,
    DATA_POINT_GLOB_MOISTURE,
    DATA_POINT_GLOB_PM10,
    DATA_POINT_GLOB_PM25,
    DATA_POINT_GLOB_R_RAIN,
    DATA_POINT_GLOB_RAIN,
    DATA_POINT_GLOB_RAIN_PIEZO,
    DATA_POINT_GLOB_TEMP,
    DATA_POINT_GLOB_TF,
    DATA_POINT_GLOB_VOLT,
    DATA_POINT_GLOB_WETNESS,
    DATA_POINT_GLOB_WIND,
    DATA_POINT_GLOB_WINDDIR,
)
from ecowitt2mqtt.util import glob_search

CHANNEL_PATTERN: Final = re.compile(r"^(?P<stem>.*?)(?P<channel>\d+)$")

# Some keys end in a digit that belongs to the measurement's name rather than to a
# channel number. The WH45/WH46 air quality sensor is the important case: every one of
# its keys ends in "co2", so naive channel-splitting would turn "pm1_co2" into stem
# "pm1_co" plus channel "2":
NON_CHANNEL_TAIL_PATTERN: Final = re.compile(r"(?:^|_)(?:co2|pm1|pm4|pm10|pm25)$")

# Layer 1: names for exact payload keys. This covers every fixed, well-known Ecowitt
# key (i.e., everything that isn't distinguished by a channel number):
FRIENDLY_NAMES: Final[dict[str, str]] = {
    "baromabs": "Absolute pressure",
    "baromrel": "Relative pressure",
    "batt_co2": "Air quality sensor battery",
    "beaufortscale": "Beaufort scale",
    "bgt": "Black globe temperature",
    "bgtbatt": "WN38 battery",
    "co2": "CO2",
    "co2_24h": "CO2 (24-hour average)",
    "co2_batt": "Air quality sensor battery",
    "co2in": "Indoor CO2",
    "co2in_24h": "Indoor CO2 (24-hour average)",
    "console_batt": "Console battery voltage",
    "dailyrain": "Daily rain",
    "dewpoint": "Dew point",
    "drain_piezo": "Daily rain (piezo)",
    "erain_piezo": "Event rain (piezo)",
    "eventrain": "Event rain",
    "feelslike": "Feels like",
    "frostpoint": "Frost point",
    "frostrisk": "Frost risk",
    "gain10_piezo": "Piezo rain gain 10",
    "gain20_piezo": "Piezo rain gain 20",
    "gain30_piezo": "Piezo rain gain 30",
    "gain40_piezo": "Piezo rain gain 40",
    "gain50_piezo": "Piezo rain gain 50",
    "heap": "Free memory",
    "heatindex": "Heat index",
    "hourlyrain": "Hourly rain",
    "hrain_piezo": "Hourly rain (piezo)",
    "humi_co2": "Air quality sensor humidity",
    "humidex": "Humidex",
    "humidex_perception": "Humidex perception",
    "humidity": "Outdoor humidity",
    "humidityabs": "Absolute humidity",
    "humidityabsin": "Indoor absolute humidity",
    "humidityin": "Indoor humidity",
    "interval": "Update interval",
    "last24hrain": "Last 24 hours rain",
    "last24hrain_piezo": "Last 24 hours rain (piezo)",
    "lightning": "Lightning distance",
    "lightning_num": "Lightning strikes",
    "lightning_time": "Last lightning strike",
    "maxdailygust": "Max daily wind gust",
    "monthlyrain": "Monthly rain",
    "mrain_piezo": "Monthly rain (piezo)",
    "pm10_24h_co2": "Air quality sensor PM10 (24-hour average)",
    "pm10_co2": "Air quality sensor PM10",
    "pm1_24h_co2": "Air quality sensor PM1 (24-hour average)",
    "pm1_co2": "Air quality sensor PM1",
    "pm25_24h_co2": "Air quality sensor PM2.5 (24-hour average)",
    "pm25_co2": "Air quality sensor PM2.5",
    "pm4_24h_co2": "Air quality sensor PM4 (24-hour average)",
    "pm4_co2": "Air quality sensor PM4",
    "rainrate": "Rain rate",
    "relative_strain_index": "Relative strain index",
    "relative_strain_index_perception": "Relative strain index perception",
    "rrain_piezo": "Rain rate (piezo)",
    "runtime": "Runtime",
    "safe_exposure_time_skin_type_1": "Safe sun exposure time (skin type I)",
    "safe_exposure_time_skin_type_2": "Safe sun exposure time (skin type II)",
    "safe_exposure_time_skin_type_3": "Safe sun exposure time (skin type III)",
    "safe_exposure_time_skin_type_4": "Safe sun exposure time (skin type IV)",
    "safe_exposure_time_skin_type_5": "Safe sun exposure time (skin type V)",
    "safe_exposure_time_skin_type_6": "Safe sun exposure time (skin type VI)",
    "simmerindex": "Simmer index",
    "simmerzone": "Simmer zone",
    "solarradiation": "Solar irradiance",
    "solarradiation_lux": "Solar illuminance",
    "solarradiation_perceived": "Perceived solar irradiance",
    "srain_piezo": "Rain detected (piezo)",
    "temp": "Outdoor temperature",
    "tempin": "Indoor temperature",
    "tf_co2": "Air quality sensor temperature",
    "thermalperception": "Thermal perception",
    "totalrain": "Total rain",
    "train_piezo": "Total rain (piezo)",
    "uv": "UV index",
    "vpd": "Vapour pressure deficit",
    "wbgt": "Wet bulb globe temperature",
    "weeklyrain": "Weekly rain",
    "wh25batt": "WH25 battery",
    "wh26batt": "WH26 battery",
    "wh40batt": "WH40 battery",
    "wh57batt": "WH57 battery",
    "wh65batt": "WH65 battery",
    "wh68batt": "WH68 battery",
    "wh80batt": "WH80 battery",
    "wh85batt": "WH85 battery",
    "wh90batt": "WH90 battery",
    "wh90battpc": "WH90 battery",
    "windchill": "Wind chill",
    "winddir": "Wind direction",
    "winddir_avg10m": "Wind direction (10-minute average)",
    "winddir_name": "Wind direction (cardinal)",
    "windgust": "Wind gust",
    "windspdmph_avg10m": "Wind speed (10-minute average)",
    "windspeed": "Wind speed",
    "wn20batt": "WN20 battery",
    "wrain_piezo": "Weekly rain (piezo)",
    "ws85cap_volt": "WS85 capacitor voltage",
    "ws90_ver": "WS90 firmware version",
    "ws90cap_volt": "WS90 capacitor voltage",
    "yearlyrain": "Yearly rain",
    "yrain_piezo": "Yearly rain (piezo)",
}

# Layer 2: templates for payload keys that end in a channel number. The key is the
# payload key with its trailing digits removed:
CHANNEL_FRIENDLY_NAMES: Final[dict[str, str]] = {
    "air_ch": "Air gap {channel}",
    "batt": "Battery {channel}",
    # The WH54 laser distance sensor measures any distance (tank level, snow depth,
    # ...), so these names deliberately avoid implying a liquid. Note that "thi_ch*" is
    # deliberately absent: aioecowitt and WernerKr's WeeWX skin disagree about what it
    # means, so it falls back to its raw key rather than shipping a coin-flip name.
    "depth_ch": "Measured depth {channel}",
    "humidity": "Humidity {channel}",
    "ldsbatt": "LDS sensor battery {channel}",
    "ldsheat_ch": "LDS heater count {channel}",
    "leaf_batt": "Leaf wetness sensor battery {channel}",
    "leafwetness_ch": "Leaf wetness {channel}",
    "leak_ch": "Water leak {channel}",
    "leakbatt": "Water leak sensor battery {channel}",
    "pm25_avg_24h_ch": "PM2.5 sensor {channel} (24-hour average)",
    "pm25_ch": "PM2.5 sensor {channel}",
    "pm25batt": "PM2.5 sensor battery {channel}",
    "soil_ec": "Soil conductivity {channel}",
    "soil_ec_ad": "Soil conductivity raw AD {channel}",
    "soil_ec_batt": "Soil conductivity sensor battery {channel}",
    "soil_ec_hum": "Soil moisture {channel} (conductivity sensor)",
    "soil_ec_hum_ad": "Soil moisture raw AD {channel} (conductivity sensor)",
    "soil_ec_temp": "Soil temperature {channel}",
    "soilad": "Soil moisture raw AD {channel}",
    "soilbatt": "Soil moisture sensor battery {channel}",
    "soilmoisture": "Soil moisture {channel}",
    "temp": "Temperature {channel}",
    "tf_batt": "Temperature probe battery {channel}",
    "tf_ch": "Temperature probe {channel}",
}

# Layer 3: base names for glob data point keys. These only ever apply to payload keys
# that no other layer recognizes (e.g., keys introduced by newer firmware):
GLOB_FRIENDLY_NAMES: Final[dict[str, str]] = {
    DATA_POINT_GLOB_BAROM: "Pressure",
    DATA_POINT_GLOB_BATT: "Battery",
    DATA_POINT_GLOB_GAIN_PIEZO: "Piezo rain gain",
    DATA_POINT_GLOB_GUST: "Wind gust",
    DATA_POINT_GLOB_HUMIDITY: "Humidity",
    DATA_POINT_GLOB_LEAK: "Water leak",
    DATA_POINT_GLOB_MOISTURE: "Moisture",
    DATA_POINT_GLOB_PM10: "PM10",
    DATA_POINT_GLOB_PM25: "PM2.5",
    DATA_POINT_GLOB_R_RAIN: "Rain rate",
    DATA_POINT_GLOB_RAIN: "Rain",
    DATA_POINT_GLOB_RAIN_PIEZO: "Rain (piezo)",
    DATA_POINT_GLOB_TEMP: "Temperature",
    DATA_POINT_GLOB_TF: "Temperature probe",
    DATA_POINT_GLOB_VOLT: "Voltage",
    DATA_POINT_GLOB_WETNESS: "Wetness",
    DATA_POINT_GLOB_WIND: "Wind speed",
    DATA_POINT_GLOB_WINDDIR: "Wind direction",
}

# Leftover fragments that carry meaning once a glob has been matched:
GLOB_QUALIFIERS: Final[dict[str, str]] = {
    "in": "Indoor",
}


def _split_channel(key: str) -> tuple[str, str | None]:
    """Split a trailing channel number off of a key.

    Args:
        key: A key to split.

    Returns:
        A tuple of the remaining stem and the channel number (if one exists).
    """
    if NON_CHANNEL_TAIL_PATTERN.search(key):
        return (key, None)
    if match := CHANNEL_PATTERN.match(key):
        return (match["stem"], match["channel"])
    return (key, None)


def _get_glob_friendly_name(payload_key: str) -> str | None:
    """Derive a name for a payload key that only matches a glob data point key.

    The leftover characters (what remains of the payload key once the glob has been
    removed) must be fully understood – either empty, a known qualifier, or a channel
    number. If anything else remains, no name is derived; a partial name would be
    misleading and could collide with another entity's name.

    Args:
        payload_key: An Ecowitt payload key.

    Returns:
        A human-friendly name (if one can be derived).
    """
    glob_key, base_name = glob_search(GLOB_FRIENDLY_NAMES, payload_key)

    if glob_key is None or base_name is None:
        return None

    leftover, channel = _split_channel(payload_key.replace(glob_key, "", 1))
    leftover = leftover.strip("_")
    suffix = f" {channel}" if channel else ""

    if not leftover:
        return f"{base_name}{suffix}"

    if qualifier := GLOB_QUALIFIERS.get(leftover):
        return f"{qualifier} {base_name[0].lower()}{base_name[1:]}{suffix}"

    return None


def get_friendly_name(payload_key: str) -> str:
    """Get a human-friendly entity name for an Ecowitt payload key.

    Names are resolved in order of decreasing specificity:

    1. An exact payload key match.
    2. A channel template match (the payload key minus its trailing digits).
    3. A glob match, so long as the leftover characters are fully understood.
    4. The raw payload key, so that an unrecognized key is never dropped or blank.

    Args:
        payload_key: An Ecowitt payload key.

    Returns:
        A human-friendly name.
    """
    if name := FRIENDLY_NAMES.get(payload_key):
        return name

    stem, channel = _split_channel(payload_key)
    if channel and (template := CHANNEL_FRIENDLY_NAMES.get(stem)):
        return template.format(channel=channel)

    if name := _get_glob_friendly_name(payload_key):
        return name

    return payload_key
