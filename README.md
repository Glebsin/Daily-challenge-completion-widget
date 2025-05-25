<h1 align="center">
    DCCW (Daily challenge completion widget)
</h1>

<div align="center">
  <a href="https://github.com/Glebsin/Daily-challenge-completion-widget/releases/tag/2025.524.0">
    <img src="misc/images/button-download.png" alt="download" />
  </a>
</div>

## **WARNING**

**TESTED ONLY ON WINDOWS 10**

i don't know how to code

98% github copilot + 1% chatgpt + 1% me

This widget is designed for tracking daily challenge completion

## HOW TO USE:

Download executable in releases or compile widget.py (ask copilot or chatgpt how) (**WARNING**: next to the executable file, a settings file widget_settings.json is created, it is better to open the executable file in a separate folder).

For statistics update you need create "New OAuth Application" here - https://osu.ppy.sh/home/account/edit#oauth (as an example in the "Application Callback URLs" field you can specify `http://localhost:3456/`), then you need open widget settings (right click) and paste Client ID, Client Secret and username.

Use context menu on right click to change settings (scaling, always on top toggle, run at startup toggle, change updating time, view last update statistic time, exit).

Functions:

1. scaling from 100 to 500%
2. scaling and position save
3. sticking to the edge of the screen
4. always on top switch
5. precise movement of the widget by arrows
6. autostart
7. manual update
8. ability to change widget update time

Todo:
1. make theme customizing
2. make other statistic popup at hover
3. give the ability to switch the number of days to best streak or current streak or total participation (now its only total participation)
4. make right colors for all number of days

<sub>727</sub>
