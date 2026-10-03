# Windows Region Switcher

一个运行在 Windows 上的轻量小工具，用于一键切换系统的「国家或地区」与「区域格式」，在中美两种区域配置之间快速往返。

图形界面基于 Python 标准库 `tkinter`，不依赖任何第三方包，下载即可运行。

## 功能特性

- 显示当前区域格式（如 `zh-CN`、`en-US`）
- 显示当前国家或地区的 GeoID
- 一键在「中国」与「美国」之间切换
- 底部状态栏直接反馈执行结果，无弹窗打扰
- 纯标准库实现，无需额外安装依赖

## 切换内容

| 目标区域 | 国家/地区 GeoID | 区域格式 |
| --- | --- | --- |
| 中国 | 45 | `zh-CN` |
| 美国 | 244 | `en-US` |

## 运行环境

- Windows 10 或 Windows 11
- Python 3（官方安装包默认自带 `tkinter`）
- 管理员权限：修改系统区域设置需要管理员权限，否则命令会执行失败

## 使用方法

1. 以管理员身份运行脚本：

   ```powershell
   pythonw region_switcher.pyw
   ```

   也可以右键脚本选择「以管理员身份运行」，或直接双击。

2. 界面会显示当前的区域格式与 GeoID。
3. 点击「一键切换 CN ↔ US」按钮完成切换。
4. 重新打开「设置」窗口或相关应用后生效。

## 实现说明

工具通过 PowerShell 调用以下两条系统命令完成设置：

- `Set-WinHomeLocation -GeoId <id>` 修改国家或地区
- `Set-Culture -CultureInfo <name>` 修改区域格式

切换只影响区域相关设置，不会修改系统显示语言、时区或键盘布局。建议在修改前记下原始设置，方便随时切回。

## 项目结构

```
windows-region-switcher/
├── LICENSE
├── README.md
└── region_switcher.pyw
```

## 许可证

本项目基于 [MIT License](LICENSE) 发布，可自由使用、修改与分发。
