# covid
None of the countless services I subscribed to managed to send me an alert in "real-time". Honestly, didn't receive even one alert from any of these services - forget real-time. This led me to write it on my own. This script notifies users via Telegram channels about availability of Covid vaccine slots **in** real-time.

## Supported notifications
Use Telegram to search and join channel(s) of your interest from the table below:  

| District | Vaccine name | Minimum age limit | Telegram channel | Telegram channel status |
| --- | --- | :---: | --- | :---: |
| Gwalior | Covaxin | 45 | @gwl_covaxin_45 | 🟢 |
| Gwalior | Covishield | 18 | @gwl_covishield_18 | 🟢 |
| Gwalior | Covishield | 45 | @gwl_covishield_45 | 🟢 |
| Bangalore Rural | Covaxin | 45 | @blr_rural_covaxin_45 | 🟢 |
| Bangalore Rural | Covishield | 45 | @blr_rural_covishield_45 | 🟢 |
| Bangalore Urban | Covishield | 45 | @blr_urban_covishield_45 | 🟢 |
| BBMP | Covaxin | 45 | @blr_bbmp_covaxin_45 | 🟢 |
| BBMP | Covishield | 45 | @blr_bbmp_covishield_45 | 🟢 |
| Aurangabad | Covaxin | 18 | @awb_covaxin_18 | 🟢 |
| Aurangabad | Covaxin | 45 | @awb_covaxin_45 | 🟢 |
| Aurangabad | Covishield | 18 | @awb_covishield_18 | 🟢 |
| Aurangabad | Covishield | 45 | @awb_covishield_45 | 🟢 |

## Remarks
- If you wish to receive alerts for a different district, feel free to raise an issue, and I will add support for it.

- The script needs to pass `User-Agent` header to the co-vin api, and it seems they have put up cache also. Because of these factors, some of the alerts might not match the info that you see on the portal. We can't do much about these rare cases. So, when you see a notification in the channel, but can't find the same data on the portal, just try from different devices available to you, as because of these factors, different devices have potential to show different data. If you really want to minimise this, you can always run this code on your own and supply the relevant `User-Agent` value.

- When slots are available, channels would see a surge of alerts. Feel free to mute the channel for a given duration to avoid being disturbed if needed.

## Contributing new district
I, as an individual, have exhausted the number of channels that I can create on Telegram. So in order to add support for new districts, I will need your help. Follow the steps below to add support for a new district:
1. Create the Telegram channels following the existing convention. For example, say you want to add support for `Aurangabad` district for all four variants - covaxin 18, covaxin 45, covishield 18 and covishield 45. Then, following the convention `<district-prefix>_<vaccine-type>_<minimum-age-limit>`, you should create the four channels as:

  | Channel Name | Public Link | Description |
  | --- | --- | --- |
  | AWB_COVAXIN_18 | awb_covaxin_18 | Channel for Covaxin vaccination slot alerts for Aurangabad for people with minimum age of 18 years |
  | AWB_COVAXIN_45 | awb_covaxin_45 | Channel for Covaxin vaccination slot alerts for Aurangabad for people with minimum age of 45 years |
  | AWB_COVISHIELD_18 | awb_covishield_18 | Channel for Covishield vaccination slot alerts for Aurangabad for people with minimum age of 18 years |
  | AWB_COVISHIELD_45 | awb_covishield_45 | Channel for Covishield vaccination slot alerts for Aurangabad for people with minimum age of 45 years |
  
  District prefix can be anything(I chose `AWB` in this example) - just keep it same for all the different variants of a district.
  
2. While creating the channel(s), or post that, add `@feleena_bot` to the channel(s). Telegram would notify you to make this bot as admin, as bots can only be added as admins in Telegram channels. Add it. It is this bot that's gonna post real time alert messages to the channel.
3. Update README: Submit a pull request that updates the table in above `Supported notifications` section, and adds your name(if not already) in the below `Contributors` section.
4. I will update the relevant environment variable with the new channels information, and would restart the script to enable it to consider these new channels, and would merge the pull request. If you aren't comfortable with Step#3, just finish Step#1 and Step#2, and then raise an issue here, or DM me - I would take care of Step#3 myself.
5. Once the pull request is merged, consider notifications are enabled for these new channels. Feel free to share these newly supported channels in your circle at this point so that the help reaches maximum.
6. Wear mask and save your family.

## Contributors
1. [@viiicky](https://github.com/viiicky)
2. [Rohan Sethi](https://www.linkedin.com/in/rohan-sethi/)
3. [iamtarun1993](https://github.com/iamtarun1993)
