# 文字转语音（TTS）程序

一个支持中文和英文的文字转语音程序，优先使用系统内置语音引擎，提供在线语音引擎作为备选方案。

## 功能特性

- ✅ 支持中文和英文文本转语音
- ✅ 优先使用系统内置语音引擎（离线，无需网络）
- ✅ 提供在线语音引擎备选方案（Google TTS）
- ✅ 命令行交互界面
- ✅ 支持语速和音量调整
- ✅ 交互模式支持实时参数调整
- ✅ 自动语言检测
- ✅ 异常处理和错误恢复

## 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# macOS系统可能需要额外安装
brew install portaudio  # 如果pyttsx3安装失败
```

## 使用方法

### 快速启动（推荐）

```bash
# 使用启动器，可选择GUI或命令行模式
python3 start.py
```

### GUI图形界面（推荐）

```bash
# 启动图形界面
python3 gui_tts.py
```

GUI界面功能：
- 📝 **文本输入区域**：支持多行文本输入
- 🎛️ **实时参数调整**：语速和音量滑块调节
- 🔧 **引擎选择**：自动选择、离线引擎、在线引擎
- ⌨️ **快捷键支持**：Ctrl+Enter播放，Esc停止
- 📋 **示例文本**：一键加载测试文本
- 📊 **状态显示**：实时显示程序运行状态
- 🛡️ **稳定性优化**：完善的异常处理，确保界面不会意外退出

### 命令行使用

#### 基本使用

```bash
# 播放中文语音
python3 tts.py "你好，这是一个测试"

# 播放英文语音
python3 tts.py "Hello, this is a test"

# 强制使用在线引擎
python3 tts.py "你好世界" --online
```

### 参数选项

```bash
# 调整语速（默认200）
python3 tts.py "测试语速" --rate 150

# 调整音量（0.0-1.0，默认0.9）
python3 tts.py "测试音量" --volume 0.7

# 详细输出模式
python3 tts.py "测试" --verbose

# 查看帮助
python3 tts.py --help
```

### 交互模式

```bash
# 进入交互模式
python3 tts.py --interactive

# 或者
python3 tts.py -i
```

在交互模式中，支持以下命令：
- `:rate <数值>` - 设置语速
- `:volume <数值>` - 设置音量（0.0-1.0）
- `:online` - 切换到在线模式
- `:offline` - 切换到离线模式
- `quit` 或 `exit` - 退出程序

### 使用示例

```bash
# 示例1：基本使用
$ python3 tts.py "你好，欢迎使用文字转语音程序"
[播放语音]: 你好，欢迎使用文字转语音程序

# 示例2：英文语音
$ python3 tts.py "Welcome to the text-to-speech program"
[播放语音]: Welcome to the text-to-speech program

# 示例3：调整参数
$ python3 tts.py "这是一个慢速语音测试" --rate 100 --volume 0.8
[播放语音]: 这是一个慢速语音测试

# 示例4：交互模式
$ python3 tts.py -i
进入交互模式，输入 'quit' 或 'exit' 退出
支持的命令:
  :rate <数值>   - 设置语速
  :volume <数值> - 设置音量
  :online        - 切换到在线模式
  :offline       - 切换到离线模式
请输入文本: 你好世界
[播放语音]: 你好世界
请输入文本: :rate 150
语速设置为: 150
请输入文本: Hello World
[播放语音]: Hello World
请输入文本: quit
```

## 技术实现

### 离线语音引擎
- 使用 `pyttsx3` 库调用系统内置TTS引擎
- macOS: 使用 NSSpeechSynthesizer
- Windows: 使用 SAPI5
- Linux: 使用 espeak

### 在线语音引擎
- 使用 Google Text-to-Speech (gTTS)
- 通过 `pygame` 播放生成的音频
- 自动清理临时文件

### 语言检测
- 自动检测中文字符（Unicode范围：\u4e00-\u9fff）
- 默认中文语音，包含英文字符时使用英文语音

## 依赖说明

- `pyttsx3`: 离线TTS引擎接口
- `gTTS`: Google文字转语音API
- `pygame`: 音频播放
- `requests`: HTTP请求（gTTS依赖）

## 故障排除

### 常见问题

1. **离线引擎初始化失败**
   ```
   # macOS
   brew install portaudio
   pip install --upgrade pyttsx3
   
   # Linux
   sudo apt-get install espeak espeak-data libespeak-dev
   ```

2. **在线引擎网络错误**
   - 检查网络连接
   - 确认防火墙设置
   - 尝试使用代理

3. **音频播放问题**
   ```bash
   # 重新安装pygame
   pip uninstall pygame
   pip install pygame
   ```

4. **权限问题**
   ```bash
   # macOS可能需要授权麦克风权限
   # 系统偏好设置 > 安全性与隐私 > 隐私 > 麦克风
   ```

### 调试模式

```bash
# 启用详细输出查看错误信息
python3 tts.py "测试" --verbose
```

## 开发说明

### 项目结构
```
text2Voice/
├── README.MD           # 项目说明
├── requirements.txt    # Python依赖
├── start.py           # 程序启动器（推荐）
├── gui_tts.py         # GUI图形界面程序
├── tts.py             # 命令行程序入口
├── demo.py            # 功能演示脚本
└── src/
    └── tts.py         # 主程序逻辑
```

### 扩展功能

程序设计为模块化结构，可以轻松扩展：
- 添加更多语音引擎
- 支持更多语言
- 添加语音效果
- 集成语音识别

## 许可证

本项目采用 MIT 许可证。

## 贡献

欢迎提交 Issue 和 Pull Request！