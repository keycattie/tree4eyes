# tree4yeys

quick, dirty and sloppy app to help you browse tree command output easily!

*works with Windows' `tree` command output* 

![image](https://user-images.githubusercontent.com/77988565/132970861-14acfc07-26f5-4fb2-9cef-470ce0e58bc9.png)

# usage

you can get a tree file by running this for desired path (or without a path for current folder) in the command prompt

    tree <YOUR-PATH> /f /a > "%HOMEPATH%/Desktop/tree.txt"

after that you can run the app (granted you have Python installed) and browse through the tree. you can also copy selected element's path from context menu

you can download latest release at https://github.com/keycattie/tree4eyes/releases

**known issues:**

- can open and try to process literally any file;
- doesnt support command line arguments
- janky af

**license:** MIT
