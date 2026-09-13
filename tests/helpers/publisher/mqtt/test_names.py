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
        ("temp", "Temperature"),
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
