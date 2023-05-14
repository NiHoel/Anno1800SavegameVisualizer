[![GitHub](https://img.shields.io/github/license/nihoel/Anno1800SavegameVisualizer)](https://github.com/nihoel/Anno1800SavegameVisualizer/blob/master/LICENSE) [![Discord](https://img.shields.io/discord/571011757317947406?label=help%2Fdiscord)](https://discord.gg/JJpHWRB)

**German/Deutsch**: https://github-com.translate.goog/NiHoel/Anno1800SavegameVisualizer?_x_tr_sl=auto&_x_tr_tl=de&_x_tr_hl=de&_x_tr_pto=wapp

# Stamp Converter
Generate layout images for all your stamps.

![Usage demo](imgs/stamp_converter_demo.gif)

1. Download and install .NET:  https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/sdk-6.0.407-windows-x64-installer
2. Download the `Anno1800SavegameVisualizer.zip` from: https://github.com/nihoel/Anno1800SavegameVisualizer/releases/latest
3. Extract the archive. Make sure to not change anything inside the tools folder!
4. Double click `stamp_converter.exe` to process all stamps in `Documents/Anno 1800/stamps`

## Advanced Usage
The executable can be used as a command line tool with many options (ask [ChatGPT](https://chat.openai.com) how to do it, paste the output of `stamp_converter.exe -h` to get tailored responses)
* Drop a single stamp onto the executable to only convert that one
* Save in `D:\Pictures`: `-d "D:\Pictures"`
* Generate Anno Designer files `-t ad`
* Exclude grid and building statistics: `-e grid statistics`

## Troubleshooting
* Re-do the instructions above!
* Make sure all paths and files only contain letters a-z
* Run the program from command line with verbose output `stamp_converter.exe -v` and send me the output.

# Anno 1800 Savegame Visualizer
Turn your [Anno 1800](https://www.ubisoft.com/de-de/game/anno-1800/) savegames into [Anno Designer](https://github.com/AnnoDesigner/anno-designer) layouts with just a few clicks! Eases the creation of production layout and the process of copying islands.

![Usage demo](imgs/savegame_visualizer_demo.gif)

## Getting started
1. Download and install Jupyter Lab: https://github.com/jupyterlab/jupyterlab-desktop/releases/latest - The installation process consists of two stages.
    1. Install Jupter Lab. At the end of the installation dialog choose to start the application.
    2. A welcome dialog appears with a warning at the bottom that no python environment is found. Click this message.
    3. A new dialog appears to install a JupyterLab Desktop Server. <span style="color: red;">The path must NOT contain spaces or special characters.</span>
2. Download and install .NET:  https://dotnet.microsoft.com/en-us/download/dotnet/thank-you/sdk-6.0.407-windows-x64-installer
3. Download the `Anno1800SavegameVisualizer.zip` from: https://github.com/nihoel/Anno1800SavegameVisualizer/releases/latest
4. Extract the archive. Make sure to not change anything inside the tools folder!
5. Double click on savegame_visualizer.ipynb (must open in Jupyter Lab).
6. The two images at the top of the software show which buttons you need to click to run the software.
7. If you have some basic coding skills in Python, you can open savegame_inspector.ipynb to further explore a savegame.

## Troubleshooting
#### The preview does not update and the button to open Anno Designer does nothing
Close all instances of Anno Designer (use the task manager) and restart the software.

#### Error displaying widget
![Error displaying widget](imgs/error_display_widget.png)

That is normal when you open the software. Run the software as usual and the user interface will appear.

#### Code expanded
![Code expanded](imgs/code_expanded.png)

If you have opened one of the two blocks depicted above: Click on the blue bar on the left to collapse it. Make sure you didn't change anything there by accident. If strange things happen afterwards, re-download the software

#### WinError in status bar
Some virus scanners identify `RdaConsole.exe` or `FileDBReader.exe` as virus
* Add the executable to the exception list of your virus scanner (you may re-do this after an update or moving the folder).
* Make sure no files were deleted by the anti-virus software after extracting the zip. Check the `tools` and `tools\FileDBReader` folders and compare them with the content of the zip.
* Make sure that windows allows to execute the `tools\RDAConsole.exe` and `tools\FileDBReader\FileDBReader.exe`. Double-click on them and if Windows displays a security warning, click on further information and allow it.

#### Error in the status bar
Contact me if you fail to understand or resolve the error displayed there. To help me solve the issue, open the log console and copy its content.

![Open log console](imgs/show_log_console.png)

## Contact and Feedback
* Join the Anno Designer discord: https://discord.gg/5CC2pz8B3j
* Ask questions or give feedback in the #savegame-visualizer channel or write me a message (user: DuxVitae#7882)
* I welcome any kind of feedback: Bugs, user experience improvements, feature suggestions.

## Special Thanks
* [StingMcRay](https://github.com/StingMcRay) for extracting and adding necessary information to the Anno Designer files
* DarKHawK for fixing the harbour areas of the DLC 12 islands
* The [Anno Designer](https://github.com/AnnoDesigner/anno-designer) team for their great tool (which is part of the distributed binaries)
* [Taubenangriff](https://github.com/taubenangriff) for his support on extracting savegames and the two tools included in the binaries:
    * [RdaConsole](https://github.com/anno-mods/RdaConsole)
    * [FileDBReader](https://github.com/anno-mods/FileDBReader)
    
## Known issues
* Older savegames may not work or show unexpected behaviour.
* Auto update fails silently if Anno Designer is running.
* New stuff from Game Update 16 is always red.

## Disclaimer
The software is provided without warranty of any kind. The work was NOT endorsed by Ubisoft Blue Byte in any kind. All the assets from Anno 1800 game are © by Ubisoft.


## License
[MIT](https://github.com/NiHoel/Anno1800SavegameVisualizer/blob/main/LICENSE)
