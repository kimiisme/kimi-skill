# Kimi Skill Collection

这是一个根据个人需求开发的 Claude Skill 技能集合，包含了各种实用的自定义技能，旨在增强 Claude 的功能以满足特定场景需求。

## 包含的技能

### workdays - 中国工作日计算

一个实用的中国工作日计算工具，能够准确计算两个日期之间的工作日数量，考虑了中国法定节假日、周末和补班工作日。

**适用场景：**
- 计算距离某个日期还有多少个工作日
- 查询某个日期范围的工作日数量
- 列出指定年份的所有节假日和补班日期

**主要功能：**
- 自动识别中国法定节假日（如春节、国庆节等）
- 排除周末和法定假期
- 包含补班工作日
- 支持多种日期格式输入
- 本地缓存提高查询效率
- 详细模式可显示节假日和补班详情

**使用示例：**

```bash
# 计算从今天到12月31日的工作日数量
python scripts/workdays.py 12-31

# 显示详细的节假日和补班信息
python scripts/workdays.py 12-31 --detail

# 计算两个日期之间的工作日
python scripts/workdays.py 2024-12-31 2024-12-01

# 计算N个工作日后是哪天
python scripts/workdays.py 23个工作日

# 列出2026年的所有节假日和补班
python scripts/workdays.py --list 2026
```

**支持的日期格式：**
- `2024-12-31` 或 `2024/12/31` - 完整日期
- `12-31` 或 `12/31` - 月日（默认当年）
- `12月31日` - 中文格式

## 安装

1. 克隆此仓库到本地：
   ```bash
   git clone https://github.com/kimiisme/kimi-skill.git
   cd kimi-skill
   ```

2. 确保已安装 Python 3.7+ （用于 workdays 技能）

3. 安装必要的依赖：
   ```bash
   pip install requests
   ```

## 使用方法

### workdays 技能

在 Claude 中使用自然语言提问：
- "离12月31号还有几个工作日"
- "到下周五还有多少工作日"
- "计算从现在到春节还有多少工作日"

或者直接运行脚本：
```bash
cd workdays
python scripts/workdays.py [参数]
```

## 技术说明

### workdays 技能

- 使用 [ChinaHolidayAPI](https://holiday.dreace.top) 获取假期数据
- 支持年份：2023-2026
- 数据缓存位置：`workdays/scripts/cache/holiday_cache.json`
- 计算规则：从开始日期的**次日**开始计算，包含目标日期（如果是工作日）

## 贡献

欢迎提交 Issue 和 Pull Request！

如果你有好的技能想法或改进建议，请随时分享。

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

如有问题或建议，请通过 [GitHub Issues](https://github.com/kimiisme/kimi-skill/issues) 联系。
