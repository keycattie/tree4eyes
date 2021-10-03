# tree4eyes

Small and simple app to help you browse tree command output files with ease!

*Supports Windows' `tree` command output in ASCII mode.* 

![image](https://user-images.githubusercontent.com/77988565/134831293-d8a7cff1-f6cd-413f-9692-005fe3f2735d.png)

## Usage

You can get a tree file by running this for desired path (or without a path for current folder) in the command prompt

    tree <YOUR-PATH> /f /a > output_file.txt

After that you can run the app (granted you have **Python with TKinter** installed) and browse through the tree.
To get help inside the app, navigate to `File > Help/About` or press `Ctrl+/`.

You can download the latest release at https://github.com/keycattie/tree4eyes/releases

#### Some known issues

- does not support command line arguments 
- can open and try to process literally any file you feed it
- `PgUP` and `PgDN` navigation is broken
- tree is not focused after oppening a file *(workaround: press `Tab`)*
- no logging file *(i dont think its needed for now)* 
- taskbar icon can default to default one
- sloppy and ugly help window
- hardcoded cache limit (it might be bigger)
- possible spelling mistakes and missed capitalization all over the place

## Development

Feel free to create issue reports or feature requests. This is a small project im working on in my free time, and so far im having fun :)

#### Roadmap

Before the app can be considered a finished one, there are some milestones to pass:
- [x] UI and engine prototype
- [ ] command line tools
- [ ] GIL support (for PyPy and others)
- [ ] plugin support and scalable architecture
- [ ] GNU tree parser plugin
- [ ] grid based plugin-expandable UI
- [ ] better tree navigation, multicolumn support, search
- [ ] multi tree view
- [ ] tree operations and tree export
- [ ] binary release
- [ ] finishing UI touches
- [ ] *`???`*

## License

MIT

## Changelog

`r0 v0.2` **caching patch**
- fixes
    - uncaching folders containing cached folders breaks: [`#2`](/../../issues/2)
    - tree is not cleared and can be interacted with while loading a new file *(`input is not blocked when loading a file`)*
    - some spelling in help window
- engine
    - removed threading for tree seeking
    - added more debug level logging
    - changed some logging messages
- progress UI
    - no UI updates if the thread is locked (eg. while seeking a folder)

`r0 v0.1` **first release**
- architecture overhaul
    - app and parser are separated
    - added logging (into console)
    - the file now resembles a normal Python project
- pooling engine:
    - tree is loaded from file on demand
    - much reduced memory usage
    - old collapsed cached folders get auto-unloaded  
- UI overhaul:
    - fancy tree, shows folders in bold and cached ones understriked
    - added menu instead of a button
    - improved progress monitoring
    - removed status bar
    - removed error message *(reason: it was unhelpful)*
    - keyboard shortcuts
    - added help window
    - updated folder and app icons
- fixes
    - hangs on large files
    - when file name contained 4 spaces parsing would break
    - broken path copying
    - when right clicking on a tree item it was not selected
    - top-level folder was always drive letter tree from header
    - random uncaught exceptions

`r0 v0.1-alpha` *pre-release*
- feature overview
    - can open Windows' tree files
    - basic progress monitoring
    - copy path of selected tree item
    - file and folder icons

