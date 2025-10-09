# Forbes AI 50 公司信息爬虫

这是一个用于爬取Forbes AI50榜单公司信息的Python脚本。

## 📋 功能说明

- 从Forbes AI50页面提取所有50家公司的信息
- 自动处理融资金额单位转换（M=百万, B=十亿）
- 自动提取年份信息
- 缺失的CEO和员工数用np.nan填充
- 数据保存为DataFrame格式并导出为CSV和Excel文件

## 🛠️ 安装步骤

### 1. 确保已安装Python

检查Python版本（需要Python 3.8或更高版本）：
```bash
python --version
```

或者：
```bash
python3 --version
```

如果没有安装Python，请访问 https://www.python.org/downloads/ 下载安装。

### 2. 安装所需的Python包

在VSCode中打开终端（Terminal），然后运行：

```bash
pip install -r requirements.txt
```

如果上面的命令不工作，尝试：
```bash
pip3 install -r requirements.txt
```

或者手动安装每个包：
```bash
pip install requests beautifulsoup4 pandas numpy lxml
```

## 🚀 运行方法

### 方法1：在VSCode中直接运行

1. 在VSCode中打开 `forbes_ai50_scraper.py` 文件
2. 按 `F5` 键或点击右上角的运行按钮 ▶️
3. 等待程序运行完成

### 方法2：在终端中运行

打开VSCode的终端，运行：
```bash
python forbes_ai50_scraper.py
```

或者：
```bash
python3 forbes_ai50_scraper.py
```

## 📊 输出结果

运行成功后，将生成以下文件：
- `forbes_ai50_companies.csv` - CSV格式的数据文件
- `forbes_ai50_companies.xlsx` - Excel格式的数据文件（需要安装openpyxl）

DataFrame结构：
| 列名 | 数据类型 | 说明 |
|------|---------|------|
| Name | object | 公司名称 |
| What_it_Does | object | 公司业务描述 |
| Funding | int | 融资金额（已转换为数字） |
| Year_Founded | int | 成立年份 |
| City | object | 城市 |
| Country | object | 国家 |
| Industry | object | 行业 |
| CEO | object | CEO姓名 |
| Employees | float | 员工数量 |

## 📝 数据示例

```
   Name          What_it_Does      Funding  Year_Founded         City        Country                    Industry         CEO  Employees
0  Abridge  AI notetaker...    458000000          2018  San Francisco  United States  Clinical documentation...    Shiv Rao      301.0
1  Anthropic  AI model...   17000000000          2020  San Francisco  United States  AI research and products  Dario Amodei  1500.0
```

## ⚠️ 注意事项

1. **网络连接**：确保你的网络可以访问Forbes网站
2. **访问频率**：脚本已设置每次请求后暂停1-2秒，避免被网站封禁
3. **网页结构变化**：如果Forbes网站更新了页面结构，可能需要调整选择器
4. **动态内容**：Forbes可能使用JavaScript动态加载内容，如果遇到问题，可能需要使用Selenium

## 🔧 故障排除

### 问题1：pip命令不存在
**解决方案**：尝试使用 `pip3` 或者 `python -m pip install` 或 `python3 -m pip install`

### 问题2：网络连接超时
**解决方案**：
- 检查网络连接
- 尝试使用VPN
- 增加timeout时间

### 问题3：找不到公司元素
**解决方案**：
- Forbes网站可能更新了结构
- 脚本会自动使用示例数据进行演示
- 需要检查网页HTML结构并更新选择器

### 问题4：Excel文件无法保存
**解决方案**：安装openpyxl包
```bash
pip install openpyxl
```

## 💡 使用建议

1. **先测试**：建议先运行脚本查看示例数据
2. **逐步调试**：如果需要修改选择器，可以先测试一两家公司
3. **保存数据**：数据会自动保存为CSV和Excel文件，便于后续分析

## 📞 帮助

如果遇到问题：
1. 检查Python版本是否 >= 3.8
2. 确保所有依赖包都已正确安装
3. 查看终端输出的错误信息
4. 检查网络连接

## 📄 文件说明

- `forbes_ai50_scraper.py` - 主程序文件
- `requirements.txt` - Python依赖包列表
- `README_AI50.md` - 本说明文件（你正在阅读）

---

祝使用愉快！🎉
