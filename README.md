# covid
This script notifies users via Telegram channels about availability of Covid vaccine slots.

## Supported notifications
| Location | Minimum age limit | Vaccine name | Telegram channel |
| --- | --- | --- | --- |
| Gwalior | 18 | Covaxin ||

## Remarks
1. If you wish to receive alerts for a different location/age-limit/vaccine-type, feel free to raise an issue, and I will add support for that kind. Or, if you can, you could just submit a pull request.

2. The script needs to pass `User-Agent` header to the co-vin api, and it seems they have put up cache also. Because of these factors, some of the alerts might not match the info that you see on the portal. We can't do much about these rare cases. If you really want to minimise this, you can always run this code on your own and supply the relevant `User-Agent` value.
