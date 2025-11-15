# 数据路径问题修复总结

## 问题描述

在运行新能源汽车行业分析系统时，出现了多个数据文件不存在的错误。错误信息显示系统无法找到预期的数据文件，尽管这些文件实际上存在于某个目录中。

## 问题原因

经过分析，发现了主要问题：

1. **数据路径配置错误**：环境变量`DATA_ROOT_PATH`设置为`data`，但实际数据文件可能位于不同的位置
2. **文件路径混淆**：存在两个可能的数据目录：
   - `f:\Industry_analysis\data` - 上级目录中的data文件夹
   - `f:\Industry_analysis\agent_analysis_project\data` - 项目目录中的data文件夹
3. **数据加载器不够灵活**：原始数据加载器只在配置的路径中查找文件，不会尝试其他可能的位置

## 解决方案

### 1. 修改环境变量配置

更新了`.env`文件中的数据路径配置：

```env
# 数据路径配置
DATA_ROOT_PATH=../data
OUTPUT_PATH=./output
```

将数据路径从`data`改为`../data`，指向上级目录的data文件夹。

### 2. 增强数据加载器功能

修改了`src/tools/mapped_data_loader.py`文件，增强了数据加载器的功能：

- 添加了多位置查找功能：当在配置路径找不到文件时，自动尝试在备选位置查找
- 添加了详细的错误信息：当文件在所有位置都找不到时，提供详细的错误信息，包括已尝试的所有路径
- 备选位置包括：
  - `../data` - 上级目录的data文件夹
  - `../../数据` - 上上级目录的"数据"文件夹
  - `data` - 当前目录的data文件夹

### 3. 创建测试脚本

创建了`test_data_path.py`测试脚本，用于验证数据路径配置和数据加载功能：

- 测试不同的数据路径配置
- 检查每个路径是否存在以及包含的文件
- 测试数据加载器的文件查找功能
- 尝试加载一个示例文件

## 测试结果

1. **数据路径测试**：测试脚本成功运行，显示数据加载器能够在多个位置查找文件
2. **文件加载测试**：成功加载了`gdp.csv`文件，形状为(44, 11)
3. **完整程序测试**：运行`main.py --focus 宏观经济`，程序成功执行并生成了分析结果

## 代码修改

### 1. `.env`文件修改

```diff
- DATA_ROOT_PATH=data
+ DATA_ROOT_PATH=../data
```

### 2. `src/tools/mapped_data_loader.py`文件修改

在`load_data`方法中添加了多位置查找功能：

```python
# 检查文件是否存在
if not file_path.exists():
    logger.error(f"数据文件不存在: {file_path}")
    
    # 尝试在备选位置查找文件
    alternative_paths = [
        Path("../data") / actual_file_name,  # 上级目录的data文件夹
        Path("../../数据") / actual_file_name,  # 上上级目录的"数据"文件夹
        Path("data") / actual_file_name,  # 当前目录的data文件夹
    ]
    
    found_path = None
    for alt_path in alternative_paths:
        if alt_path.exists():
            found_path = alt_path
            logger.info(f"在备选位置找到文件: {alt_path}")
            break
    
    if found_path:
        file_path = found_path
    else:
        # 提供更详细的错误信息
        error_msg = f"数据文件不存在: {file_path}\n"
        error_msg += f"已尝试的备选位置:\n"
        for alt_path in alternative_paths:
            error_msg += f"  - {alt_path}\n"
        error_msg += f"\n请确保数据文件已正确放置，或检查DATA_ROOT_PATH配置。\n"
        error_msg += f"当前DATA_ROOT_PATH配置为: {self.data_root_path}"
        
        raise FileNotFoundError(error_msg)
```

## 优势

1. **灵活性**：数据加载器现在可以在多个位置查找数据文件，适应不同的项目结构
2. **健壮性**：即使数据文件位置发生变化，系统也能自动找到文件
3. **可维护性**：提供了详细的错误信息，便于排查问题
4. **向后兼容**：保留了原有的数据加载逻辑，不影响现有功能

## 建议

1. **统一数据目录**：建议将所有数据文件集中存放在一个位置，避免混淆
2. **文档说明**：在项目文档中明确说明数据文件的存放位置和命名规范
3. **环境变量**：考虑使用环境变量来指定数据文件位置，便于不同环境下的配置
4. **数据验证**：添加数据文件验证功能，确保数据完整性和格式正确性

## 后续工作

1. 测试其他数据文件的加载，确保所有数据都能正确加载
2. 添加更多备选位置，支持更灵活的文件组织结构
3. 考虑添加数据文件自动下载功能，从远程仓库获取缺失的数据文件
4. 优化错误提示，提供更明确的解决方案建议