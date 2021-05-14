# covid
None of the countless services I subscribed to managed to send me an alert in "real-time". Honestly, didn't receive even one alert from any of these services - forget real-time. This led me to write it on my own. This script notifies users via Telegram channels about availability of Covid vaccine slots **in** real-time.

## Supported notifications
Use Telegram to search and join channel(s) of your interest from the table below:  

| District | Vaccine name | Minimum age limit | Telegram channel | Telegram channel status |
| --- | --- | :---: | --- | :---: |
| Gwalior | Covaxin | 45 | @gwl_covaxin_45 | 🟢 |
| Gwalior | Covishield | 18 | @gwl_covishield_18 | 🟢 |
| Gwalior | Covishield | 45 | @gwl_covishield_45 | 🟢 |
| Bangalore Urban | Covaxin | 18 | @blr_urban_covaxin_18 | 🟢 |
| Bangalore Urban | Covaxin | 45 | @blr_urban_covaxin_45 | 🟢 |
| Bangalore Urban | Covishield | 18 | @blr_urban_covishield_18 | 🟢 |
| Bangalore Urban | Covishield | 45 | @blr_urban_covishield_45 | 🟢 |

## Remarks
- If you wish to receive alerts for a different district, feel free to raise an issue, and I will add support for it.

- The script needs to pass `User-Agent` header to the co-vin api, and it seems they have put up cache also. Because of these factors, some of the alerts might not match the info that you see on the portal. We can't do much about these rare cases. If you really want to minimise this, you can always run this code on your own and supply the relevant `User-Agent` value.

- When slots are available, channels would see a surge of alerts. Feel free to mute the channel for a given duration to avoid being disturbed if needed.
