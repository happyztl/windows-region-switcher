import subprocess
import tkinter as tk
from tkinter import ttk

def run_powershell(command):
    """执行powershell命令，返回stdout"""
    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    return result.stdout.strip(), result.returncode

def get_current_culture():
    # 获取当前区域格式文化名 zh-CN / en-US
    out, _ = run_powershell("(Get-Culture).Name")
    return out

def get_current_geoid():
    # 获取当前国家/地区GeoID
    out, _ = run_powershell("(Get-WinHomeLocation).GeoId")
    try:
        return int(out)
    except ValueError:
        return -1

def set_region(geoid, culture_name):
    # 1. 修改【国家或地区】
    cmd1 = f"Set-WinHomeLocation -GeoId {geoid}"
    # 2. 修改【区域格式】
    cmd2 = f"Set-Culture -CultureInfo {culture_name}"
    full_cmd = f"{cmd1}; {cmd2}"
    out, code = run_powershell(full_cmd)
    return code == 0

def refresh_status():
    """刷新界面上当前区域状态"""
    cult = get_current_culture()
    geo = get_current_geoid()
    label_cult.config(text=f"当前区域格式：{cult}")
    label_geo.config(text=f"当前国家GeoID：{geo}")
    if cult == "zh-CN":
        label_loc.config(text="📍 当前位置：中国")
    elif cult == "en-US":
        label_loc.config(text="📍 当前位置：美国")
    else:
        label_loc.config(text="📍 当前位置：未知")

def toggle_region():
    """切换区域按钮事件（移除弹窗，改用底部标签显示结果）"""
    current_culture = get_current_culture()
    if current_culture == "zh-CN":
        target_geoid = 244
        target_culture = "en-US"
        target_name = "美国"
    elif current_culture == "en-US":
        target_geoid = 45
        target_culture = "zh-CN"
        target_name = "中国"
    else:
        target_geoid = 45
        target_culture = "zh-CN"
        target_name = "中国"

    ok = set_region(target_geoid, target_culture)
    if ok:
        status_msg.config(text=f"✅ 已切换到【{target_name}】，重启设置窗口查看效果")
    else:
        status_msg.config(text="❌ 区域切换命令执行失败！")
    refresh_status()

# ========== 构建GUI界面 ==========
root = tk.Tk()
root.title("Windows区域一键切换工具 CN ↔ US")
root.geometry("420x260")
root.resizable(False, False)

# 主框架
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

label_title = ttk.Label(main_frame, text="Windows 国家/地区 + 区域格式切换", font=("微软雅黑",12,"bold"))
label_title.pack(pady=(0,15))

label_loc = ttk.Label(main_frame, text="📍 当前位置：---", font=("微软雅黑",11))
label_loc.pack(anchor="w")

label_cult = ttk.Label(main_frame, text="当前区域格式：---")
label_cult.pack(anchor="w")

label_geo = ttk.Label(main_frame, text="当前国家GeoID：---")
label_geo.pack(anchor="w")

# 分割线
ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(pady=12, fill="x")

# 切换按钮
btn_toggle = ttk.Button(main_frame, text="一键切换 CN ↔ US", command=toggle_region)
btn_toggle.pack(pady=5)

# 新增底部状态提示标签（替代弹窗）
status_msg = ttk.Label(main_frame, text="就绪", foreground="#333333")
status_msg.pack(pady=(10,0))

# 刷新状态
refresh_status()

root.mainloop()
