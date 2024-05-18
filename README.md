# Home Assistant Integration for Home Assistant

This integration allows a user to integrate another Home Assistance instance's sensors into their instance. It works locally or remote and only needs a long lived access token.

## How to Install
Best install it through HACS. After installing it and rebooting Home Assistant:

1. Navigate to the 'Integrations' page in your Home Assistant instance.
2. Click on the '+' button to add a new integration.
3. Search for 'Home Assistant Integration' and select it.
4. Enter the required information including the long-lived access token.

## How to use
After adding another Home Assistant instance through the integration all the detected sensors are disabled. Please choose which ones you would like to use by just enabling them.

## Limitations
Websocket connections are not supported yet and the sensor date is polled instead. Also auto-discovery is not set up.

## Thanks

Based on [integration_blueprint](https://github.com/ludeeus/integration_blueprint) by Ludeeus