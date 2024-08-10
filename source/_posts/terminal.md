---
title: 狂拽酷炫的terminal，你值得拥有
date: 2018-10-01 21:36:38
tags: "iterm,zsh,terminal"
---

![](https://user-gold-cdn.xitu.io/2018/4/20/162e0b8ec4885875?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

命令行是程序员日常工作中的重要组成部分，一个优秀的命令行环境不仅要功能强大，其外观更要造化钟神秀，这样才能让程序员有一个更加轻松愉悦的工作心情。或许你目前的命令行是长下面这样:

![](https://user-gold-cdn.xitu.io/2018/4/20/162e0bf83be9651d?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

你是否幻想过拥有一个如黑客帝国一般的命令行:

![](https://user-gold-cdn.xitu.io/2018/4/20/162e0c1002fc6cc6?imageslim)

当然这是不现实的，但我们至少可以让我们的命令行拥有如下所示的颜值:

![](https://user-gold-cdn.xitu.io/2018/4/20/162e0c39d8006d6e?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)

下面我们就来看看要怎么配置才能实现这样的效果，友情提示，本文所提到的配置都是针对 mac terminal 哦。

## 开始

### 升级你的 terminal

请安装[iterm](https://www.iterm2.com/features.html),[oh-my-zsh](https://ohmyz.sh/)

### 下载，安装，并使用字体色

1.  进入[gist](https://gist.github.com/rdempsey/596193b8ede69767719c#file-matrix_color_scheme_iterm2)后，点击‘download zip’，可以先在你的桌面创建一个目录 itermThemes,解压之前下载好的 zip 文件后，将解压目录中的文件(注意，仅需要目标文件，不要整个文件夹)移至 itermThemes 中.打开 terminal，进入 itermThemes 目录(cd Desktop/itermThemes)，然后 copy 下面的代码到命令行中，按回车执行, 这段代码会遍历该目录下的 color codes,然后将结果命名为‘matrix_color_scheme_2’并存储在 iterm 的自定义 colors 中

```sh
for f in *; do
 THEME=$(basename "$f")
 defaults write -app iTerm 'Custom Color Presets' -dict-add "$THEME" "$(cat "$f")"
done
```

2. 在 terminal 的 preferences 中配置使用该 color,具体路径是 iTerm2, Preferences, Profiles, Colors, Color Presets，“matrix_color_scheme_iterm2”，如下图所示:  
   ![](https://user-gold-cdn.xitu.io/2018/4/20/162e10fb15268f36?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
    字体色配置完成后，现在你的 terminal 将会达到初步的酷炫效果：  
   ![](https://user-gold-cdn.xitu.io/2018/4/20/162e110ca534c481?imageslim)  
    要实现我们之前设定的效果，还有更重要的一步要做。

### 安装主题－Powerlevel9k，以及 powerline 字体

Powerlevel9k 是一个强大的主题，可以实时展示你当前所处的目录，你的当前 git 分支以及你输入指令的执行耗时：  
 ![](https://user-gold-cdn.xitu.io/2018/4/20/162e1174e80931de?imageslim)

1. 在你的 terminal 中执行以下命令,该命令会将 Powerlevel9k 的仓库 clone 下来到你的 oh-my-zsh 自定义主题文件夹中

```sh
$ git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
```

2. 用你熟悉的编辑器打来你的 zsh 配置，然后替换 zsh 主题。比如：

```sh
vim ~/.zshrc
ZSH_THEME="powerlevel9k/powerlevel9k"
```

3. 通过如下指令安装 powerline 字体:

```sh
# clone
git clone https://github.com/powerline/fonts.git --depth=1
# install
cd fonts
./install.sh
# clean-up a bit
cd ..
rm -rf fonts
```

4. 在 iterm preferences 中选择 powerline 字体并使用它，操作路径是 iTerm, Preferences, Profiles, Text, Change Font, Select Meslo LG M for Powerline。如下图所示:
   ![](https://user-gold-cdn.xitu.io/2018/4/20/162e1200a73d690b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)  
   现在你将拥有一个狂拽酷炫的 terminal,这会让你的工作环境更加赏心悦目  
   ![](https://user-gold-cdn.xitu.io/2018/4/20/162e122ab07fce3c?imageslim)

## 节语

配置完成其实只是个开始，关于 iTerm，oh-my-zsh,以及 Powerlevel9k 还有更多有趣的特性和自定义配置以及插件可以去深入玩耍，比如我可以在 zshrc 中添加下面的配置来缩短每行命令中展示的文件路径，从而给你输入的指令腾出更多的空间：

```sh
#Shorten directory shown
POWERLEVEL9K_SHORTEN_DIR_LENGTH=1
POWERLEVEL9K_SHORTEN_DELIMITER=””
POWERLEVEL9K_SHORTEN_STRATEGY=”truncate_from_right”
#Set default user to avoid showing 'user' on every line
DEFAULT_USER=”whoami”
```

诚然，每个人有每个人的审美，你也可以选择使用其他的颜色或字体，重要的是你开心就好。  
![](https://user-gold-cdn.xitu.io/2018/4/20/162e12b5c36bbad5?imageslim)
