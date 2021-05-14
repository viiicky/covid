# covid
None of the countless services I subscribed to managed to send me an alert in "real-time". Honestly, didn't receive even one alert from any of these services - forget real-time. This led me to write it on my own. This script notifies users via Telegram channels about availability of Covid vaccine slots **in** real-time.

## Supported notifications
Use Telegram to search for channel(s) of your interest from the below table:  

| District | Minimum age limit | Vaccine name | Telegram channel |
| --- | --- | --- | --- |
| Gwalior | 45 | Covaxin | @gwl_covaxin_45 |
| Gwalior | 18 | Covishield | @gwl_covishield_18 |
| Gwalior | 45 | Covishield | @gwl_covishield_45 |

## Remarks
- If you wish to receive alerts for a different district, feel free to raise an issue, and I will add support for it. Or, if you can, you could just submit a pull request.

- The script needs to pass `User-Agent` header to the co-vin api, and it seems they have put up cache also. Because of these factors, some of the alerts might not match the info that you see on the portal. We can't do much about these rare cases. If you really want to minimise this, you can always run this code on your own and supply the relevant `User-Agent` value.

- When slots are available, these channels would see a surge of alerts. Feel free to mute the channel for a given duration to avoid being disturbed if needed.
