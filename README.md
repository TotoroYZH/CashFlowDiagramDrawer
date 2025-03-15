### 现金流量图绘图工具使用说明

**如何下载项目文件到本地？**：点击仓库最上方的绿色Code按钮，点击Download Zip即可下载项目文件的压缩包

该绘图工具项目仓库的目录结构如下：

```bash
CashFlowDiagramDrawer-main/
├── README.md
├── LICENCE
├── CHANGELOG.md
├── main_window.exe
├── cash_flow_diagram.py
├── main_window.py
├── data.xlsx
├── colors.txt
├── CashFlowDiagram.png
├── icon.ico
└── md_pic/
    └── ...
```

以下是各文件/文件夹用途：

| 文件/文件夹                     | 用途                                                   |
| ------------------------------ | ------------------------------------------------------ |
| README.md                      | 项目的说明文件                                          |
| LICENCE                        | 项目的开源协议                                          |
| CHANGELOG.md                   | 项目的更新日志                                          |
| main_window.exe                | 绘图工具的可执行文件                                     |
| cash_flow_diagram.py           | 绘图工具的Python源代码                                   |
| main_window.py                 | 绘图工具的Python源代码                                   |
| data.xlsx                      | 数据文件的模板案例                                       |
| colors.txt                     | 颜色设置文件的模板案例                                    |
| CashFlowDiagram.png            | 绘图工具根据data.xlsx和colors.txt用默认参数生成的现金流量图 |
| icon.ico                       | 可执行文件的图标                                         |
| md_pic                         | README.md中的图片源                                     |

以下是绘图工具的使用方法：

1. **提供数据文件**

   在`.xlsx`文件中填入数据（数据一般存放在名为Cash Flow Diagram的Sheet中），具体格式请模仿模板案例。

   <img src="md_pic/data.png" alt="img" style="zoom:50%;" />

   A列应当**按格式从小到大**填入已提供数据对应的年份，如果中间有一些年份的数据和前后几乎一致，可忽略（如上图中的数据缺少2076-2117年）。在缺失的时间区间内，绘图工具将不会绘制其柱状图部分，而只会将其前一年份和后一年份的折线部分用直线连接。

   除了A列和最后一列，中间所有列应当**按格式**填入柱状图部分数据，如上图中填入了project expenditure、operational costs和revenue（具体含义见iws手册14.9，下同）。

   最后一列（上图中是E列）应当**按格式**填入折线图部分数据，如上图中填入了total profits。

   我们建议，除A列代表时间的数据会作为x轴外，请在其余数据的表头的最后加入其对应y轴方向的提示，如上图中的(l)和(r)。

2. **提供颜色设置文件**：具体格式参考`colors.txt`，一行一个十六进制字符串来表示颜色（如`#FF0000`表示红色），行数不限。
   
3. **运行绘图工具程序**

   下面我们给出两种方案来运行绘图工具程序：

   **方案1**：直接运行可执行文件。具体的绘图参数可以在UI界面上设置。

   **方案2**：对Python源代码文件进行修改后再运行。这需要你拥有合适的Python3环境和相关第三方库，并且保证`main_window.py`和`cash_flow_diagram.py`处在同一目录下。

   | 第三方库     | 下载第三方库的pip指令     | 备注                                     |
   | ------------ | ------------------------- | ---------------------------------------- |
   | `pandas`     | `pip install pandas`      |                                          |
   | `xlrd`       | `pip install xlrd==1.2.0` | 只有2.0以下版本的xlrd才支持读取.xlsx文件 |
   | `matplotlib` | `pip install matplotlib`  |                                          |
   | `PYQt5`      | `pip install PyQt5`       |                                          |

   运行源代码文件`main_window.py`，会跳出PyQt的UI界面。其他使用方法与方案1相同。

如果使用者想更加深入地研究绘图工具程序的代码逻辑、对程序做进一步的修改以适应自己的绘图需求，Python源代码文件中已经写好了较为详细的注释，请自行阅读。

