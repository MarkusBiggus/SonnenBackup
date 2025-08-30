# SonnenBackup

Read from the real-time API on Sonnen Batterie to manage Backup Reserve use.

Use Sonnen Batterie web portal or mobile app to set Backup Reserve percent.

* System state On Grid, Off Grid or Critical Error.
* Real time power, current and voltage.
* Battery levels, Charge/Discharge rate, time to fully charged.
* Backup reserve, time to reserve, time to fully discharge.
* MicroGrid status when Offgrid & Blackstart settings.
* Temperature and batterie health.

## Why use this package
This Home Assistant component helps manage Sonnen batterie backup reserve, particularly whilst batterie is 'OffGrid'.

The official Sonnen mobile app normally used to monitor the batterie relies on the cloud service the batterie reports to.  \
When grid power is off, it is likely Internet may also be out either due to the same event or eventually power is out long enough to deplete ISP equipment emergency power.

Without Internet access, Home Assistant server requires only the local home network to continue functioning using the Sonnen batterie backup reserve charge.  \
It is recommended to have an independant (small) UPS running off Sonnen batterie power for the LAN & Home Assistant server. There is a momentary power drop when Sonnen batterie switches to MicroGrid mode when grid power drops. A small UPS will prevent Home Assistant server from rebooting at the very moment it needs to alert you to the batterie going into MicroGrid mode.

## HACS

Install SonnenBackup integration.

Uses sonnen_api_v2 driver package which requires a readonly API Token created in the Sonnen Batterie management portal.

Configuration will require the IP address of the battery device and the readonly API token.  \
If the Batterie portal uses a non-standard port, other than 80, that can be configured too.  \
The API package does not support https (port 443) using a self-signed certificate.  \

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

| Package Property              | Unit  | HASS Sensor        | When Valid        |
|------------------------------:|:-----:|:-------------------|:-----------------:|
|battery_activity_state|string|activity_state|always|
|configuration_de_software|string|firmware_version|always|
|configuration_em_operatingmode|string|operating_mode|always|
|led_state|string|led_state|always|
|led_state_text|string|led_state_text|always|
|state_bms|string|state_bms|always|
|state_inverter|string|state_inverter|always|
|system_status|string|system_status|always|
|time_since_full|string|interval_since_full|always|
|time_to_fully_charged|string|interval_to_fully_charged|charging is true|
|time_to_fully_discharged|string|interval_to_fully_discharged|discharging is true|
|time_to_reserve|string|interval_to_reserve|*see notes below*|
|configuration_blackstart_time1|string|blackstart_time1|when configured|
|configuration_blackstart_time2|string|blackstart_time2|when configured|
|configuration_blackstart_time3|string|blackstart_time3|when configured|
|battery_cycle_count|integer|battery_cycle_count|always|
|battery_average_current|A|battery_average_current|always|
|backup_buffer_capacity_wh|Wh|reserve_capacity|always|
|battery_full_charge_capacity_wh|Wh|full_charge_capacity|always|
|battery_unusable_capacity_wh|Wh|unusable_capacity|always|
|capacity_to_reserve|Wh|capacity_to_reserve|always|
|capacity_until_reserve|Wh|capacity_until_reserve|always|
|usable_remaining_capacity_wh|Wh|usable_capacity|always|
|remaining_capacity_wh|Wh|remaining_capacity|always|
|used_capacity|Wh|used_capacity|always|
|kwh_consumed|kWh|kwh_consumed|always|
|kwh_produced|kWh|kwh_produced|always|
|status_frequency|hertz|frequency|always|
|battery_dod_limit|percent|depth_of_discharge_limit|always|
|battery_rsoc|percent|relative_charge|always|
|battery_usoc|percent|usable_charge|always|
|status_backup_buffer|percent|reserve_charge|always|
|charging|watts|charge_power|charging is true|
|consumption|watts|consumption_now|always|
|consumption_average |watts|consumption_average|always|
|discharging|watts|discharge_power|discharging is true|
|inverter_pac_total|watts|ongrid_pac|system_status is 'OnGrid'|
|inverter_pac_microgrid|watts|offgrid_pac|system_status is 'OffGrid'|
|production|watts|production_now|always|
|status_grid_export|watts|grid_export|always|
|status_grid_import|watts|grid_import|always|
|battery_min_cell_temp|celsius|min_battery_temp|always|
|battery_max_cell_temp|celsius|max_battery_temp|always|
|system_status_timestamp|timestamp|status_timestamp|always|
|fully_charged_at|timestamp|fully_charged_at|charging is true|
|fully_discharged_at|timestamp|fully_discharged_at|discharging is true|
|backup_reserve_at|timestamp|reserve_at|*see notes below*|
|last_time_full|timestamp|last_time_full|always|
|last_updated|timestamp|last_updated|always|
|time_since_full|deltatime|time_since_full|always|
|time_to_fully_charged|deltatime|time_to_fully_charged|charging is true|
|time_to_fully_discharged|deltatime|time_to_fully_discharged|discharging is true|
|time_to_reserve|deltatime|time_to_reserve|*see notes below*e|
|microgrid_enabled|bool|microgrid_enabled|system_status is 'OffGrid'|
|dc_minimum_rsoc_reached|bool|dc_minimum_rsoc|microgrid_enabled is true|
|mg_minimum_soc_reached|bool|microgrid_minimum_soc|microgrid_enabled is true|
|status_battery_charging|bool|charging|always|
|status_battery_discharging|bool|discharging|always|
|configuration_em_reenable_microgrid|bool|blackstart_enabled|when configured|


Some sensors have enumerated values:

```
system_status: ["Config", "OnGrid", "OffGrid", "Critical Error"]
activity_state: ["standby", "charging", "discharging", "discharging reserve", "charged", "discharged"]
operating_mode: {1: "Manual", 2: "Automatic", 6: "Extension module", 10: "Time of Use"}
```

### Backup Reserve sensors
Sensors that estimate when Reserve capacity will be reached are not always defined.  \
Calculations to Reserve capacity are only valid when:  \
     *usable_charge* is above *reserve_charge* whilst *discharging* is true  \
     *usable_charge* is below *reserve_charge* whilst *charging* is true   \
in both cases *time_to_reserve* is estimated using current *charge_power* or *discharge_power* values.


### activity_state
"standby" indicates the battery is neither charging nor discharging.
The battery could be fully charged, fully discharged or at backup reserve limit.
Must be read in conjuction with *relative_charge* to determine the reason for "standby".

### Timestamps
Sensors fully charged, fully discharged & backup reserve are calculated on current consumption/production.
When battery is in standby, these timestamp values are undefined, as will some when charging/discharging.
Times are calculated relative to Sonnen batterie server time, which is *system_status_timestamp*.
A slight discrepency will be apparent if HASS server time and batterie time are different.

### Deltatimes
Sensors prefixed with 'Interval' are deltatimes presented as a string format "D HH:MM:SS".
Home assistant doesn't handle deltatimes well, use these strings for logbook recording.
Sensors prefixed with 'time_to' or 'time_since' are delatime objects.
Sensors with 'seconds_' prefix are the values used to create the deltatime objects.

### led_state
Sensor indicates the state of the status LED on the side of the battery.
Only one element may be True, that element, with brightness, is returned as a string.  \
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

### led_state_text
The meaning of the current LED state as defined in the batterie user manual.  \
eg. "Normal Operation." is returned for LED state 'Pulsing White 100%'

### State of Charge
Sonnen batterie reports two State of Charge values, Relative and Usable. The difference between these two values is reported by sensor *depth_of_discharge_limit* (DoD). Depth of Discharge reserve is included in *relative_charge* (RSoC) overall values, like *full_charge_capacity*.
Specific usable values are based on *usable_charge* (USoC), like *usable_capacity*, which do not include the DoD limit reported by sensor *unusable_capacity*.

Importantly, the *reserve_charge* percent for backup buffer is based on USoC. eg. when sensor *activity_state* is 'standby' USoC equals Backup Reserve Charge, a little less than RSoC.

Sensors *capacity_to_reserve* & *capacity_until_reserve* are both zero when battery is in standby at *reserve_capacity*. Otherwise, only one has a value depending on USoC being above or below *reserve_charge*.

## Recording
Some sensor values do not change, some only change when configuration changes, some are of little value when not current. These sensors will waste space if recorded.

Suggested recording exclusions in configuration.yaml:
```
# Recorder filter to exclude specified entities, change placeholder names
# your actual sensor names.
# eg. "sonnenbackup_nnnnnn_full_charge_capacity"
#   where 'nnnnnn' is the battery serial number entered on the config form.
recorder:
  exclude:
    entities:
      - sensor.sonnenbackup_nnnnnn_full_charge_capacity
      - sensor.sonnenbackup_nnnnnn_unusable_capacity
      - sensor.sonnenbackup_nnnnnn_led_state
      - sensor.sonnenbackup_nnnnnn_reserve_charge
      - sensor.sonnenbackup_nnnnnn_backup_reserve_percent
      - sensor.sonnenbackup_nnnnnn_depth_of_discharge_limit
      - sensor.sonnenbackup_nnnnnn_status_frequency
      - sensor.sonnenbackup_nnnnnn_state_bms
      - sensor.sonnenbackup_nnnnnn_state_inverter
      - sensor.sonnenbackup_nnnnnn_seconds_since_full
      - sensor.sonnenbackup_nnnnnn_system_status_timestamp
      - sensor.sonnenbackup_nnnnnn_fully_charged_at
      - sensor.sonnenbackup_nnnnnn_fully_discharged_at
      - sensor.sonnenbackup_nnnnnn_backup_reserve_at
      - sensor.sonnenbackup_nnnnnn_last_time_full
      - sensor.sonnenbackup_nnnnnn_last_updated
      - sensor.sonnenbackup_nnnnnn_operating_mode
      - sensor.sonnenbackup_nnnnnn_time_to_fully_charged
      - sensor.sonnenbackup_nnnnnn_time_to_fully_discharged
      - sensor.sonnenbackup_nnnnnn_time_to_reserve
      - sensor.sonnenbackup_nnnnnn_time_since_full
      - sensor.sonnenbackup_nnnnnn_interval_to_fully_charged
      - sensor.sonnenbackup_nnnnnn_interval_to_fully_discharged
      - sensor.sonnenbackup_nnnnnn_interval_to_reserve
      - sensor.sonnenbackup_nnnnnn_interval_since_full
      - sensor.sonnenbackup_nnnnnn_blackstart_enabled
      - sensor.sonnenbackup_nnnnnn_blackstart_time1
      - sensor.sonnenbackup_nnnnnn_blackstart_time2
      - sensor.sonnenbackup_nnnnnn_blackstart_time3
```

## Config Energy Dashboard

### Create Helpers for Energy dashboard
Go to Settings then Devices & Services then select Helpers from the top menu.
Create each of the 6 integrals by clicking “+ CREATE HELPER”, lower right.

Choose  Integral Sensor -> Add Riemann sum integral sensor:
use Left rule for conservative values, Trapezoidal rule for more realistic values over longer periods.

|  Helper Name       |    SonnenBackup Input Sensor                               | Rule |Precision | Interval |
|-------------------:|:-----------------------------------------------------------|:----:|:--------:|:--------:|
| PowerConsumption   | sensor.sonnenbackup_nnnnnn_consumption_now| Trapezoidal | 1 | 10 seconds|
| PowerProduction| sensor.sonnenbackup_nnnnnn_production_now| Trapezoidal | 1 | 10 seconds|
| GridImport| sensor.sonnenbackup_nnnnnn_grid_import| Trapezoidal | 1 | 10 seconds|
| GridExport| sensor.sonnenbackup_nnnnnn_grid_export| Trapezoidal | 1 | 10 seconds|
| BatteryInput| sensor.sonnenbackup_nnnnnn_charging| Trapezoidal | 1 | 10 seconds|
| BatteryOutput| sensor.sonnenbackup_nnnnnn_discharging| Trapezoidal | 1 | 10 seconds|


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

## Strategies for managing backup reserve with Sonnen EVO batterie

Sonnen EVO Batterie has a black start feature that will attemp to restart the batterie after depletion. A small reserve is kept to enable solar production at set times in the morning. Check the configuration AC Microgrid is enabled with reenabling times also set to times solar production is usually available.

A weather event that will have no sunshine for several days, such as a cyclone, will exhaust black start retries before solar is available to charge the battery, leaving the battery off until grid power is restored.

The Batterie must be configured for Recharge Strategy "Green charging" to only charge from solar production.
![Recharge Strategy "Green"](Sonnen-EVO-RechargeStrategy.jpg)

###Strategy #1 ###

Isolate the battery from load before it turns itself off when USoC is low, under 15% or so. When solar production is available, enable the battery circuit and allow it to "green charge" normally.

###Strategy #2 ###

Have a generator option installed to your household powerboard to run the house from generator in absence of grid power for and extended period. Like, days after a severe weather event.

Let Batterie deplete and rely on Black Start feature. When Black Start feature hasn't worked after solar production can resume, use generator power to restart the battery.

*Do NOT use generator power to recharge the batterie without assurance from manufacturer that you have a supported configuration for your batterie with your model generator.*
