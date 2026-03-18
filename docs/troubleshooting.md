# Troubleshooting

If you encounter a problem with Anki, please try the following steps in order:

## 1. Restart Anki

Close Anki, then start it again. If unable to close due to an error message, use your task manager or restart your computer. Anki saves periodically, so minimal work loss should occur.

If the problem doesn't reoccur, skip remaining steps.

## 2. Check add-ons

Close Anki and open it in safe mode by holding Shift while starting. Continue holding until the message confirms safe mode activation. On Linux, run `anki --safemode`.

If the problem disappears, an add-on is responsible. Remove unnecessary add-ons and disable half of the others. If problems persist, test the other half. Repeat until identifying the problematic add-on, then report it to the author using the Copy Debug Info button.

## 3. Check your Anki version

Find the version you're using in the Help > About or Anki > About menu. If not the latest from https://apps.ankiweb.net, install the latest version and restart.

For Linux users: verify you can reproduce the error using the packaged version from the Anki website, as distributions sometimes provide broken versions.

## 4. Check your database

After restarting Anki, use **Tools > Check Database** to ensure your collection has no issues.

## 5. Restart your computer

Sometimes restarting may resolve the problem.

## 6. Change the Video Driver

Display issues and crashes can stem from video drivers. Test all available driver options, restarting after each change.

For Anki 23.10+: Open **Tools > Preferences** (or **Anki > Preferences** on Mac) and select a different driver from the dropdown.

For older versions, manually modify the gldriver file:
- [Windows](https://docs.ankiweb.net/platform/windows/display-issues.html)
- [Mac](https://docs.ankiweb.net/platform/mac/display-issues.html)
- [Linux](https://docs.ankiweb.net/platform/linux/display-issues.html)

## 7. Reset window sizes

Press the **reset window sizes** button in the preferences screen immediately after starting Anki.

## 8. If the problem remains

If you've confirmed you are using the latest Anki version, and are still receiving errors even with add-ons disabled, please report the problem, including the next error received in your post.
