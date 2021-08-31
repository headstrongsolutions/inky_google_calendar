# Inky Impression Google Calendar

I needed a on-desk live calendar but as this only needs to update a couple of times a day (at best) I opted for a Pimoroni Inky Impression e-ink screen as this supports 7 colours and has a resolution of 600 X 488.

[Pimoroni Inky Impression](https://shop.pimoroni.com/products/inky-impression)

This Python project is mostly hacked together from both the Pimoroni Inky examples and the Google Calendar API Python example.

*!DANGER!* - the .gitignore in this project will try to ignore any credentials.json and/or token.json files that the Google Authentication will create when it is run, however be aware that these files are very dangerous to share online, so if you use this do not share these files!

I've made this mostly configurable for day tile sizes etc, however it was hacked together quickly so needs a bit of spit and polish.
