"""Define tests for Home Assistant MQTT Discovery entity names."""

from __future__ import annotations

import pytest

from ecowitt2mqtt.helpers.publisher.mqtt.names import (
    CHANNEL_FRIENDLY_NAMES,
    FRIENDLY_NAMES,
    GLOB_FRIENDLY_NAMES,
    get_friendly_name,
)


@pytest.mark.parametrize(
    "payload_key,expected_name",
    [
        # Exact matches:
        ("baromabs", "Absolute pressure"),
        ("baromrel", "Relative pressure"),
        ("co2_24h", "CO2 (24-hour average)"),
        ("drain_piezo", "Daily rain (piezo)"),
        ("heap", "Free memory"),
        ("humidityabsin", "Indoor absolute humidity"),
        ("humidityin", "Indoor humidity"),
        ("lightning_time", "Last lightning strike"),
        ("maxdailygust", "Max daily wind gust"),
        ("pm25_co2", "Air quality sensor PM2.5"),
        ("safe_exposure_time_skin_type_4", "Safe sun exposure time (skin type IV)"),
        ("solarradiation", "Solar irradiance"),
        ("srain_piezo", "Rain detected (piezo)"),
        ("temp", "Outdoor temperature"),
        ("tempin", "Indoor temperature"),
        ("tf_co2", "Air quality sensor temperature"),
        ("vpd", "Vapour pressure deficit"),
        ("winddir_avg10m", "Wind direction (10-minute average)"),
        ("winddir_name", "Wind direction (cardinal)"),
        ("windspdmph_avg10m", "Wind speed (10-minute average)"),
        ("ws90cap_volt", "WS90 capacitor voltage"),
        # Channel templates:
        ("batt3", "Battery 3"),
        ("humidity8", "Humidity 8"),
        ("leaf_batt1", "Leaf wetness sensor battery 1"),
        ("leafwetness_ch1", "Leaf wetness 1"),
        ("leak_ch2", "Water leak 2"),
        ("pm25_avg_24h_ch1", "PM2.5 sensor 1 (24-hour average)"),
        ("soilbatt5", "Soil moisture sensor battery 5"),
        ("soilmoisture2", "Soil moisture 2"),
        ("temp1", "Temperature 1"),
        ("tf_batt7", "Temperature probe battery 7"),
        ("tf_ch4", "Temperature probe 4"),
    ],
)
def test_get_friendly_name(payload_key: str, expected_name: str) -> None:
    """Test resolving exact and channel-based friendly names.

    Args:
        payload_key: An Ecowitt payload key.
        expected_name: The name the payload key should resolve to.
    """
    assert get_friendly_name(payload_key) == expected_name


@pytest.mark.parametrize(
    "payload_key,expected_name",
    [
        # A glob match with nothing left over:
        ("barom", "Pressure"),
        ("wetness", "Wetness"),
        # A glob match with a known qualifier left over:
        ("baromin", "Indoor pressure"),
        ("wetnessin", "Indoor wetness"),
        # A glob match with a channel number left over:
        ("gust4", "Wind gust 4"),
        ("moisture3", "Moisture 3"),
    ],
)
def test_get_friendly_name_glob_fallback(payload_key: str, expected_name: str) -> None:
    """Test deriving a friendly name from a glob data point key.

    Args:
        payload_key: An Ecowitt payload key.
        expected_name: The name the payload key should resolve to.
    """
    assert payload_key not in FRIENDLY_NAMES
    assert get_friendly_name(payload_key) == expected_name


@pytest.mark.parametrize(
    "payload_key",
    [
        # A glob match whose leftover characters aren't understood:
        "soilmoisturexyz",
        # No match of any kind:
        "xyzzy",
        "zzzz_not_a_key",
    ],
)
def test_get_friendly_name_raw_fallback(payload_key: str) -> None:
    """Test that an unrecognized payload key is returned unchanged.

    Args:
        payload_key: An Ecowitt payload key.
    """
    assert get_friendly_name(payload_key) == payload_key


def test_friendly_name_tables_are_well_formed() -> None:
    """Test that the name tables hold usable, consistently styled data."""
    for name in (*FRIENDLY_NAMES.values(), *GLOB_FRIENDLY_NAMES.values()):
        assert name
        assert name == name.strip()
        assert name[0].isupper()

    for template in CHANNEL_FRIENDLY_NAMES.values():
        assert "{channel}" in template
        assert template[0].isupper()


# Payload keys known to be emitted by real Ecowitt hardware, gathered from this
# project's fixtures, live gateways, Ecowitt's own Home Assistant integration and the
# key tables in home-assistant-libs/aioecowitt. Every one of these must resolve.
#
# This is the regression guard for the most likely failure mode of this feature: a key
# that no fixture happens to contain silently falling back to its raw form. When
# support for new hardware is added, add its keys here.
KNOWN_PAYLOAD_KEYS = (
    # Gateway diagnostics:
    "console_batt",
    "heap",
    "interval",
    "runtime",
    # Indoor/outdoor:
    "baromabs",
    "baromrel",
    "humidity",
    "humidityabs",
    "humidityabsin",
    "humidityin",
    "temp",
    "tempin",
    "vpd",
    # Multi-channel (WN31):
    "batt1",
    "batt8",
    "humidity1",
    "humidity8",
    "temp1",
    "temp8",
    # Wind:
    "maxdailygust",
    "winddir",
    "winddir_avg10m",
    "windgust",
    "windspdmph_avg10m",
    "windspeed",
    # Solar/UV:
    "solarradiation",
    "solarradiation_lux",
    "uv",
    # Tipping-bucket rain:
    "dailyrain",
    "eventrain",
    "hourlyrain",
    "last24hrain",
    "monthlyrain",
    "rainrate",
    "totalrain",
    "weeklyrain",
    "yearlyrain",
    # Piezo rain (WS85/WS90):
    "drain_piezo",
    "erain_piezo",
    "gain10_piezo",
    "gain50_piezo",
    "hrain_piezo",
    "last24hrain_piezo",
    "mrain_piezo",
    "rrain_piezo",
    "srain_piezo",
    "train_piezo",
    "wrain_piezo",
    "yrain_piezo",
    # Sensor arrays:
    "wh85batt",
    "wh90batt",
    "wh90battpc",
    "ws85cap_volt",
    "ws90_ver",
    "ws90cap_volt",
    # Lightning (WH57):
    "lightning",
    "lightning_num",
    "lightning_time",
    # Air quality (WH45/WH46) -- note that every one of these ends in a digit:
    "batt_co2",
    "co2",
    "co2_24h",
    "co2_batt",
    "co2in",
    "co2in_24h",
    "humi_co2",
    "pm10_24h_co2",
    "pm10_co2",
    "pm1_24h_co2",
    "pm1_co2",
    "pm25_24h_co2",
    "pm25_co2",
    "pm4_24h_co2",
    "pm4_co2",
    "tf_co2",
    # Standalone PM2.5 (WH41/WH43):
    "pm25_avg_24h_ch1",
    "pm25_ch1",
    "pm25batt1",
    # Soil moisture (WH51):
    "soilad1",
    "soilad16",
    "soilbatt1",
    "soilmoisture1",
    # Soil conductivity (WH52):
    "soil_ec1",
    "soil_ec_ad1",
    "soil_ec_batt1",
    "soil_ec_hum1",
    "soil_ec_hum_ad1",
    "soil_ec_temp1",
    # Temperature probes (WN34):
    "tf_batt1",
    "tf_ch1",
    # Leaf wetness (WN35):
    "leaf_batt1",
    "leafwetness_ch1",
    # Water leak (WH55):
    "leak_ch1",
    "leakbatt1",
    # Laser distance (WH54):
    "air_ch1",
    "depth_ch1",
    "ldsbatt1",
    "ldsheat_ch1",
    # Heat stress (WN38):
    "bgt",
    "bgtbatt",
    "wbgt",
    # Batteries:
    "wh25batt",
    "wh26batt",
    "wh40batt",
    "wh57batt",
    "wh65batt",
    "wh68batt",
    "wh80batt",
    "wn20batt",
    # Calculated data points:
    "beaufortscale",
    "dewpoint",
    "feelslike",
    "frostpoint",
    "frostrisk",
    "heatindex",
    "humidex",
    "humidex_perception",
    "relative_strain_index",
    "relative_strain_index_perception",
    "safe_exposure_time_skin_type_1",
    "safe_exposure_time_skin_type_6",
    "simmerindex",
    "simmerzone",
    "solarradiation_perceived",
    "thermalperception",
    "windchill",
    "winddir_name",
)


@pytest.mark.parametrize("payload_key", KNOWN_PAYLOAD_KEYS)
def test_known_payload_keys_all_resolve(payload_key: str) -> None:
    """Test that every known real-world payload key resolves to a friendly name.

    Args:
        payload_key: An Ecowitt payload key.
    """
    name = get_friendly_name(payload_key)
    assert name != payload_key, f"{payload_key} fell back to its raw payload key"
    assert name[0].isupper()


@pytest.mark.parametrize(
    "payload_key,expected_name",
    [
        # Every WH45/WH46 key ends in the "2" of "co2", which must never be mistaken
        # for a channel number:
        ("co2", "CO2"),
        ("humi_co2", "Air quality sensor humidity"),
        ("pm10_co2", "Air quality sensor PM10"),
        ("pm1_co2", "Air quality sensor PM1"),
        ("pm25_co2", "Air quality sensor PM2.5"),
        ("pm4_co2", "Air quality sensor PM4"),
        ("tf_co2", "Air quality sensor temperature"),
    ],
)
def test_co2_keys_are_not_treated_as_channels(
    payload_key: str, expected_name: str
) -> None:
    """Test that trailing digits belonging to a measurement name aren't channels.

    Args:
        payload_key: An Ecowitt payload key.
        expected_name: The name the payload key should resolve to.
    """
    name = get_friendly_name(payload_key)
    assert name == expected_name
    assert not name.endswith(" 2")


@pytest.mark.parametrize("payload_key", ["pm5_co2", "pm2_co2", "voc_co2"])
def test_unknown_co2_keys_are_not_given_a_channel(payload_key: str) -> None:
    """Test that the channel guard protects air quality keys absent from the tables.

    The keys above don't exist today. They stand in for whatever a future WH4x sensor
    emits: the point is that an unrecognized "..._co2" key must fall back to its raw
    form rather than being silently labelled as channel 2 of something.

    Args:
        payload_key: An Ecowitt payload key.
    """
    name = get_friendly_name(payload_key)
    assert name == payload_key
    assert not name.endswith(" 2")


@pytest.mark.parametrize(
    "payload_key,expected_name",
    [
        # The raw analog reading behind soil moisture, not a second moisture value:
        ("soilad1", "Soil moisture raw AD 1"),
        ("soilad16", "Soil moisture raw AD 16"),
        # Distinct sensors reporting the same quantity:
        ("rainrate", "Rain rate"),
        ("rrain_piezo", "Rain rate (piezo)"),
        # A state flag that looks like an accumulation key:
        ("srain_piezo", "Rain detected (piezo)"),
        # Outdoor readings must not collapse onto channel 1:
        ("temp", "Outdoor temperature"),
        ("temp1", "Temperature 1"),
        ("humidity", "Outdoor humidity"),
        ("humidity1", "Humidity 1"),
    ],
)
def test_easily_confused_keys(payload_key: str, expected_name: str) -> None:
    """Test keys whose obvious reading is wrong or collides with another key.

    Args:
        payload_key: An Ecowitt payload key.
        expected_name: The name the payload key should resolve to.
    """
    assert get_friendly_name(payload_key) == expected_name


@pytest.mark.parametrize(
    "payload_key",
    [
        # Meanings that rest only on inference, or on sources that contradict each
        # other, stay unnamed rather than shipping a coin-flip name:
        "thi_ch1",
        "ldspw_ch1",
        "noise_ch1",
        "peak_ch1",
    ],
)
def test_undocumented_keys_stay_unnamed(payload_key: str) -> None:
    """Test that deliberately unnamed keys fall back to their raw payload key.

    Args:
        payload_key: An Ecowitt payload key.
    """
    assert get_friendly_name(payload_key) == payload_key
