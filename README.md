# DataVisualization Workspace

本仓库包含 StarAtlas 星图可视化示例。以下步骤可确保在 Windows PowerShell 环境下的可复现安装与运行。

## 环境准备（Windows PowerShell）

1) 建议使用本目录下的虚拟环境来隔离依赖：

```powershell
# 在仓库根目录执行：
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) 安装固定版本依赖：

```powershell
pip install -U pip
pip install -r requirements.txt
```

3) 打开并运行 Notebook：

```powershell
code .
```

在 VS Code 中打开 `StarAtlas/StarAtlas.ipynb`，依次运行各单元。

## 数据文件

请将 `StarAtlas/hyglike_from_athyg_v32.csv.gz` 放在 `StarAtlas/` 目录内（已提供）。Notebook 默认使用相对路径读取。

## 常见问题

- 若内核找不到依赖，请确认已激活虚拟环境（命令提示符开头应显示 `(.venv)`）。
- 若遇到文件路径问题，请在 Notebook 中将 `file_path` 改为绝对路径或确保工作目录为 `StarAtlas/` 上级。

## 结构

```
README.md
requirements.txt
StarAtlas/
	├─ hyglike_from_athyg_v32.csv.gz
	└─ StarAtlas.ipynb
```
