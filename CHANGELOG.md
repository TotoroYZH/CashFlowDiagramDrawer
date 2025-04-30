# Changelog

所有重要的更改都会记录在这个文件中。遵循 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) 规范，并使用 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。

## [0.1.0] - 2025-01-30
### Added
- 项目首次发布于CD培训群

## [1.0.0] - 2025-02-15
### Added
- 项目首次上传
- 添加了README.md文件
- 添加了LICENCE文件
- 添加了CHANGELOG.md文件

### Changed
- 将项目源代码文件中直接创建对象并运行的写法改为主程序入口保护写法`if __name__ == '__main__':`

### Fixed
- 修正了项目源代码文件中Drawer类的docstring中错误的Attributes和Example

### Removed
- 删除了原有的程序使用说明.md和.pdf文件

## [1.0.1] - 2025-02-22
### Fixed
- 修正了项目源代码文件中Drawer类创建参数`rd`和`sheet_name`没有被传入至`self.pd = pd.read_excel()`的错误

## [1.1.0] - 2025-03-15
### Added
- 为version 1的绘图工具设计了UI界面，并添加了许多绘图参数的更改方法

## [1.1.1] - 2025-04-30
### Added
- 增加了“显示缺失时间段”可调参数
