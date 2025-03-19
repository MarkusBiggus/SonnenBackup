# SonnenBackup

Read from the real-time API on Sonnen Batterie to manage Backup Reserve use.

Use Sonnen Batterie web portal or mobile app to set Backup Reserve percent.

* System state On Grid, Off Grid or Critical Error.
* Real time power, current and voltage.
* Battery levels, Charge/Discharge rate, time to fully charged.
* Backup reserve, time to reserve, time to fully discharged.
* Temperature and batterie health.

## Why use this package
This Home Assistant component helps manage Sonnen batterie backup reserve, particularly whilst batterie is 'OffGrid'.

The official Sonnen mobile app normally used to monitor the batterie relies on the cloud service the batterie reports to.  \
When grid power is out, there is a possibility Internet may also be out either due to the same event or because power
has been out long enough to deplete ISP equipment emergency power.

Without Internet access, Home Assistant server requires only the local home network to continue functioning using the Sonnen batterie backup reserve charge.  \
It is recommended to have an independant (small) UPS running off Sonnen batterie power for the LAN & Home Assistant server. There is a momentary power drop
when Sonnen batterie switch to microGrid mode when grid power drops. A small UPS will prevent Home Assistant server from rebooting at the very moment
it needs to alert you to the batterie going into microGrid mode.

## HACS

Install SonnenBackup integration.

Uses sonnen_api_v2 driver package which requires a readonly API Token created in the
Sonnen management portal.

Configuration will require the IP address of the battery device and the readonly API token.  \
If the Batterie portal uses a non-standard port, other than 80, that can be configured too.  \
It does not support https (port 443) using a self-signed certificate.  \

## Usage

Install sonnenbackup with hacs.  \
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=MarkusBiggus&repository=https%3A%2F%2Fgithub.com%2FMarkusBiggus%2FSonnenBackup&category=integration)

### Manual Integration to HACS

Open HACS -> Home Assistant Community Store page  \
From Overflow Menu: 3 vertical dots upper right, choose custom repositories.  \
Enter github URL: https://github.com/MarkusBiggus/SonnenBackup  \
The component is added to HACS and the form redisplayed - click cancel to return to HACS.  \

Search HACS for the component just added, SonnenBackup.  \
Click the Integration to see its details page (readme file).  \
On the component details page click the download button lower right.  \
Return to HACS (upper left arrow) where "Pending Restart" is displayed.  \

Restart HASS from Settings/System restart button, upper far right.

### Add Integration

From Settings/Devices & Services, click Add Integration button, lower right.


## Sensors

HASS Sensor is the name used by Home Assistant from the sonnen_api_v2 package property.

| Package Property              | Unit  | HASS Sensor        |
|------------------------------:|:-----:|:-------------------|
|battery_activity_state|string|sonnenbackup_state|
|configuration_de_software|string|firmware_version|
|configuration_em_operatingmode|string|operating_mode|
|led_state|string|led_state|
|led_state_text|string|led_state_text|
|state_bms|string|state_bms|
|state_inverter|string|state_inverter|
|system_status|string|system_status|
|battery_cycle_count|integer|battery_cycle_count|
|battery_average_current|A|battery_average_current|
|backup_buffer_capacity_wh|Wh|reserve_capacity|
|battery_full_charge_capacity_wh|Wh|full_charge_capacity|
|battery_unusable_capacity_wh|Wh|unusable_capacity|
|capacity_to_reserve|Wh|capacity_to_reserve|
|capacity_until_reserve|Wh|capacity_until_reserve|
|usable_remaining_capacity_wh|Wh|usable_capacity|
|remaining_capacity_wh|Wh|remaining_capacity|
|used_capacity|Wh|used_capacity|
|kwh_consumed|kWh|kwh_consumed|
|kwh_produced|kWh|kwh_produced|
|status_frequency|hertz|frequency|
|battery_dod_limit|percent|depth_of_discharge_limit|
|battery_rsoc|percent|relative_state_of_charge|
|battery_usoc|percent|usable_state_of_charge|
|status_backup_buffer|percent|reserve_charge|
|charging|watts|charge_power|
|consumption|watts|consumption_now|
|consumption_average |watts|consumption_average|
|consumption_total_w|watts|consumption_daily|
|discharging|watts|discharge_power|
|inverter_pac_total|watts|ongrid_pac|
|inverter_pac_microgrid|watts|offgrid_pac|
|production|watts|production_now|
|production_total_w|watts|production_daily|
|status_grid_export|watts|grid_export|
|status_grid_import|watts|grid_import|
|battery_min_cell_temp|celsius|min_battery_temp|
|battery_max_cell_temp|celsius|max_battery_temp|
|system_status_timestamp|timestamp|status_timestamp|
|fully_charged_at|timestamp|fully_charged_at|
|fully_discharged_at|timestamp|fully_discharged_at|
|backup_reserve_at|timestamp|reserve_at|
|last_time_full|timestamp|last_time_full|
|last_updated|timestamp|last_updated|
|time_since_full|deltatime|interval_since_full|
|dc_minimum_rsoc_reached|bool|dc_minimum_rsoc|
|mg_minimum_soc_reached|bool|microgrid_minimum_soc|
|microgrid_enabled|bool|microgrid_enabled|
|status_battery_charging|bool|is_charging|
|status_battery_discharging|bool|is_discharging|


Some sensors have enumerated values:

```
system_status: ["Config", "OnGrid", "OffGrid", "Critical Error"]
sonnenbackup_state: ["standby", "charging", "discharging", "discharging reserve", "charged", "discharged"]
operating_mode: {1: "Manual", 2: "Automatic", 6: "Extension module", 10: "Time of Use"}
```

### sonnenbackup_state
"standby" indicates the battery is neither charging nor discharging.
The battery could be fully charged, fully discharged or at back reserve limit.
Must be read in conjuction with "relative_state_of_charge" to determine the reason for "standby".

### Timestamps
Sensors fully charged, fully discharged & backup reserve are calculated on current consumption/production.
When battery is in standby, these timestamp values are undefined, as will some when charging/discharging.
Times are calculated relative to Sonnen batterie server time, which is "system_status_timestamp".
A slight discrpency will be apparent if hass server time and batterie time are different.

### led_state
Sensor indicates the state of the status LED on the side of the battery.
Only one element may be True, that element, with brightness, is returned as a string.
e.g 'Pulsing White 100%'
```
"Eclipse Led":{
    "Blinking Red":true,   # undocumented - call installer
    "Brightness":100,
    "Pulsing Green":true,  # Off Grid, in MicroGrid (backup) mode
    "Pulsing Orange":true, # no internet connection
    "Pulsing White":true,  # normal operation
    "Solid Red":true       # serious problem - call installer
}
```
All values False indicates Off Grid operation, the string "Off Grid." is returned.

### State of Charge
The batterie reports two State of Charge values, Relative and Usable. The difference between these two values is reported by
sensor depth_of_discharge_limit (DoD). Depth of Discharge reserve is included in Relative State of Charge (RSoC) overall values, like full_charge_capacity.
Specific usable values are based on Usable State of Charge (USoC), like usable_capacity, which do not include the DoD limit reported by sensor unusable_capacity.

Importantly, the reserve_charge percent for backup buffer is based on USoC. eg when sensor sonnenbackup_state is 'standby' USoC equals Backup Reserve Charge, a little less than RSoC.

## Recording
Some sensor values do not change, some only change when configuration changes, some are of little value when not current. These sensors will waste space if recorded.

Suggested recording exclusions in configuration.yaml:
```
# Recorder filter to exclude specified entities, change placeholder names
# your actual sensor names. eg "sonnenbackup.backupbatterie_nnnnnn_sonnenbackup_full_charge_capacity"
#   where 'nnnnnn' is the battery serial number entered on the config form.
recorder:
  exclude:
    entities:
      - sonnenbackup.full_charge_capacity
      - sonnenbackup.led_state
      - sonnenbackup.led_state_text
      - sonnenbackup.backup_reserve_capacity
      - sonnenbackup.status_frequency
      - sonnenbackup.backup_reserve_percent
      - sonnenbackup.state_bms
      - sonnenbackup.state_inverter
      - sonnenbackup.interval_since_full
      - sonnenbackup.seconds_since_full
      - sonnenbackup.system_status_timestamp
      - sonnenbackup.fully_charged_at
      - sonnenbackup.fully_discharged_at
      - sonnenbackup.backup_reserve_at
      - sonnenbackup.last_time_full
      - sonnenbackup.last_updated
      - sonnenbackup.operating_mode
```

## Config Energy Dashboard

### Create Helpers for Energy dashboard
Go to Settings then Devices & Services then select Helpers from the top menu.
Create each of the 6 integrals by clicking “+ CREATE HELPER”, lower right.

Choose  Integral Sensor -> Add Riemann sum integral sensor:
use Left rule for conservative values, Trapezoidal rule for more realistic values over longer periods.

|  Helper Name       |    SonnenBackup Input Sensor                               | Rule |Precision | Interval |
|-------------------:|:-----------------------------------------------------------|:----:|:--------:|:--------:|
| PowerConsumption   | sensor.backupbatterie_XXXXX_sonnenbackup_consumption_now| Trapezoidal | 1 | 10 seconds|
| PowerProduction| sensor.backupbatterie_XXXXX_sonnenbackup_production_now| Trapezoidal | 1 | 10 seconds|
| GridImport| sensor.backupbatterie_XXXXX_sonnenbackup_grid_import| Trapezoidal | 1 | 10 seconds|
| GridExport| sensor.backupbatterie_XXXXX_sonnenbackup_grid_export| Trapezoidal | 1 | 10 seconds|
| BatteryInput| sensor.backupbatterie_XXXXX_sonnenbackup_charging| Trapezoidal | 1 | 10 seconds|
| BatteryOutput| sensor.backupbatterie_XXXXX_sonnenbackup_discharging| Trapezoidal | 1 | 10 seconds|


XXXXX will be the Batterie serial number entered on the configuration form.  \
Metric prefix is blank, all package sensor integer values are single units.  \
Use default time unit Hours for all integrals.

### Use Helpers to Configure Energy Dashboard

|  Energy Dashboard Metric      |  Helper Sensor     |
|------------------------------:|:-------------------|
|Grid Consumption|GridImport|
|Grid Production|GridExport|
|Battery In|BatteryInput|
|Battery Out|BatteryOutput|
|Solar Production|PowerProduction|

Solar production may also be provided by a sensor from your solar inverter component.
Given Sonnen batterie is AC coupled, the Sonnen production value will be slightly less and so a more realistic value to use.

## Confirmed Supported Batteries

These batteries have been tested and confirmed to be working. If your batterie is not listed below, this library may still work provided your battery admin portal can generate an API read token and responds to Sonnen API V2 endpoints.
Newer Sonnen Batteries are not provisoned with user accounts for API access.
Whilst the installer account could be used, that is not a wise cybersecurity choice to use those credentials for this purpose.

* Power unit Evo IP56


API token will return status 401 if used with V1 of the API. Use Weltmeyer/ha_sonnenbatterie package if user/password authentication is required.
