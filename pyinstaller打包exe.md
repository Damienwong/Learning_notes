## PyInstaller打包exe
pyinstalller自身打包的流程：读取编好的python脚本，分析其中调用的模块和库，然后收集这些文件的副本（包括Python的解释器）。最后把副本与脚本，可执行文件等放在一个文件夹下，或者可选的封装在一个可执行文件中。

 > PyInstaller bundles a Python application and all its dependencies into a single package. The user can run the packaged app without installing a Python interpreter or any modules.

### 使用步骤
#### 第一步：安装pyinstaller
```python
pip install pyinstaller
```
#### 第二步： 打开命令行，进入要打包的主程序目录下
#### 第三步： 输入一下命令
```python
D:\WORK\y21w15>pyinstaller -F test.py
```
成功之后当前目录会生成build和dist两个文件夹，dist文件夹里的test.exe文件就是我们生成的可执行文件。

exe可以双击打开，但是运行完程序会直接退出，程序报错也会直接退出；

可以shift+右击，选择Windows PowerShell打开进行程序调试。

## 注

pyinstaller常用的选项参数：

-F，--onefile	产生单个的可执行文件
>Create a one-file bundled executable.

-D，--onedir	产生一个目录（包含多个文件）作为可执行程序
>Create a one-folder bundle containing an executable (default)

-w，--windowed，--noconsolc	指定程序运行时不显示命令行窗口（仅对 Windows 有效）
>Windows and Mac OS X: do not provide a console window for standard i/o. On Mac OS X this also triggers building an OS X .app bundle. On Windows this option will be set if the first script is a ‘.pyw’ file. This option is ignored in *NIX systems.
-c，--nowindowed，--console	指定使用命令行窗口运行程序（仅对 Windows 有效）

--hidden-import=['MODULENAME'] 指定脚本里没有明文引用的import。
>Name an import not visible in the code of the script(s). This option can be used multiple times.

如：
```python
import serial
```
而windows安装的确实名为pyserial的库，打包并不会把pyserial打进去，所以需要具体指定该包。
即
```python
D:\WORK\y21w15>pyinstaller -F test.py
```

pyinstaller官方文档：
https://pyinstaller.readthedocs.io/en/latest/index.html#