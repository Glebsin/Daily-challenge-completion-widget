<h1 align="center">
    DCCW (Daily challenge completion widget)
</h1>

<div align="center">This widget designed for tracking daily challenge completion</div>

<div align="center">
  <a href="https://github.com/Glebsin/Daily-challenge-completion-widget/releases/tag/2025.526.0">
    <img src="misc/images/button-download.png" alt="download" />
  </a>
</div>

# **WARNING**

**TESTED ONLY ON WINDOWS 10**

i don't know how to code

98% github copilot + 1% chatgpt + 1% me

# HOW TO USE

Download DCCW.zip in releases (**WARNING**: next to the executable file, a settings file widget_settings.json is created, it is better to open the executable file in a separate folder).

For statistics update you need create "New OAuth Application" here - https://osu.ppy.sh/home/account/edit#oauth (as an example in the "Application Callback URLs" field you can specify `http://localhost:3456/`), then you need open widget settings (right click) and paste **Client ID**, **Client Secret** and **username**.

Use context menu on right click to change settings (scaling, always on top toggle, run at startup toggle, change updating time, view last update statistic time, exit).

# Screenshots

<div align="center">
<table>
  <tr>
    <td align="center">
      <img src="misc/images/screenshot-uncompleted.png" alt="Uncompleted daily challenge widget"/><br>
      <sub>Uncompleted daily challenge widget</sub>
    </td>
    <td align="center">
      <img src="misc/images/screenshot-completed.png" alt="Completed daily challenge widget"/><br>
      <sub>Completed daily challenge widget</sub>
    </td>
  </tr>
    <tr>
    <td colspan="2" align="center">
      <img src="misc/images/screenshot-contextmenu.png" alt="Long preview" />
      <br>
      <sub>Context menu</sub>
    </td>
  </tr>
</table>
</div>

# Features

- Scaling from 100% to 500%
- Scaling and position save
- Sticking to the edge of the screen
- Always on top switch
- Precise movement of widget by arrows
- Autostart
- Manual update on button in context menu and on "F5"
- Ability to change widget update time
- Right colors for all number of days

# Todo
- Make android widget (?)
- Make theme customizing
- Make other statistic popup at hover
- Fix gradients (it seems to me that they are broken at some numbers)
- Make ability to switch the number of days to best streak or current streak or total participation (now its only total participation)
- Prevent opening more than one widget (and maybe later make possible create two or more widgets with saving their settings)
- Make tray icon
- Add program version to context menu

# My osu profile
- https://osu.ppy.sh/u/glebsin

<sub>727</sub>
