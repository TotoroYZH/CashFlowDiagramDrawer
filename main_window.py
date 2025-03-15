import sys
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QColorDialog, QFileDialog, QMessageBox)
import cash_flow_diagram

def is_color(color):
    if len(color) != 7 or color[0] != '#':
        return False
    for bit in color[1:]:
        if not('0' <= bit <= '9' or 'A' <= bit <= 'F' or 'a' <= bit <= 'f'):
            return False
    return True

class SubWindow(QDialog):
    
    # 定义一个信号，用于传递参数
    closed = pyqtSignal(tuple, str, str, str, str)  # 参数类型可以根据需要调整
    
    def __init__(self, current_args):
        super().__init__()
        self.setWindowTitle("详细设置")
        self.setGeometry(150, 150, 300, 200)
        
        # 创建控件
        self.figsize_x = QLineEdit(str(current_args[0][0]))
        self.figsize_y = QLineEdit(str(current_args[0][1]))
        self.legend1_loc = QComboBox()
        self.legend1_loc.addItems(['upper left','upper right','lower left','lower right'])
        self.legend2_loc = QComboBox()
        self.legend2_loc.addItems(['upper left','upper right','lower left','lower right'])
        self.title_fontweight = QComboBox()
        self.title_fontweight.addItems(['bold','normal','heavy','light','ultralight','medium','semibold','ultrabold','black'])
        self.color_btn = QPushButton("颜色设置文件") # 选择文件按钮
        self.color_path = QLineEdit(current_args[4]) # 文件路径显示框
        self.color_path.setReadOnly(True)  # 禁止用户直接编辑路径
        self.save_set = QPushButton("保存设置")

        # 根据变量设置默认选项
        self.legend1_loc.setCurrentText(current_args[1])
        self.legend2_loc.setCurrentText(current_args[2])
        self.title_fontweight.setCurrentText(current_args[3])

        main_layout = QVBoxLayout()
        
        row1_layout = QHBoxLayout()
        row1_layout.addWidget(QLabel("画布尺寸(in):"))
        row1_layout.addWidget(self.figsize_x)
        row1_layout.addWidget(QLabel("x"))
        row1_layout.addWidget(self.figsize_y)
        row1_layout.addWidget(QLabel("标题字体粗细:"))
        row1_layout.addWidget(self.title_fontweight)
        
        row2_layout = QHBoxLayout()
        row2_layout.addWidget(QLabel("图例1位置:"))
        row2_layout.addWidget(self.legend1_loc)
        row2_layout.addWidget(QLabel("图例2位置:"))
        row2_layout.addWidget(self.legend2_loc)

        row3_layout = QHBoxLayout()
        row3_layout.addWidget(self.color_btn)
        row3_layout.addWidget(self.color_path)
        row3_layout.addWidget(self.save_set)

        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        main_layout.addLayout(row3_layout)
        
        self.setLayout(main_layout)
        
        # 禁用问号按钮
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # 连接保存设置按钮的信号
        self.color_btn.clicked.connect(self.choose_colorfile)
        self.save_set.clicked.connect(self.save_and_close)

    def choose_colorfile(self):
        try:
            # 打开文件选择对话框
            color_path, _ = QFileDialog.getOpenFileName(
                self, "选择文件", "", "TXT文件 (*.txt)"
            )
            if color_path:
                self.color_path.setText(color_path)  # 显示文件路径
        except Exception as e:
            QMessageBox.critical(self, "文件选择失败", e)
            print("文件选择失败:", e)
            
    def save_and_close(self):
        # 保存设置并关闭窗口
        try:
            figsize_x = float(self.figsize_x.text())
            figsize_y = float(self.figsize_y.text())
        except Exception as e:
            QMessageBox.critical(self, "画布尺寸输入错误", e)
            print("画布尺寸输入错误:", e)
            return
        
        legend1_loc = self.legend1_loc.currentText()
        legend2_loc = self.legend2_loc.currentText()  # 修正：使用 legend2_loc 而不是 legend1_loc
        title_fontweight = self.title_fontweight.currentText()
        color_path = self.color_path.text()

        # 发射信号，传递参数
        self.closed.emit((figsize_x, figsize_y), legend1_loc, legend2_loc, title_fontweight, color_path)

        # 关闭窗口
        self.close()

    def closeEvent(self, event):
        # 调用父类的 closeEvent
        super().closeEvent(event)
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("统计图表工具")
        self.setGeometry(700, 400, 600, 200)
        self.defult_title = {'Cash Flow Diagram':'Cash Flow Diagram'}
        self.figsize = (10,8)
        self.legend1_loc = 'lower right'
        self.legend2_loc = 'upper right'
        self.title_fontweight = 'bold'
        self.color_path = 'colors.txt'
        
        # 创建控件
        self.plot_type = QComboBox() # 图表类型选择框
        self.plot_type.addItems(['Cash Flow Diagram'])

        self.title_input = QLineEdit("Cash Flow Diagram") # 图表标题输入框
        
        self.file_btn = QPushButton("数据文件") # 选择文件按钮
        self.file_path = QLineEdit() # 文件路径显示框
        self.file_path.setReadOnly(True)  # 禁止用户直接编辑路径
        
        self.sheet_name = QLineEdit('Cash Flow Diagram') # 工作表名称输入框

        self.detail_btn = QPushButton("详细设置") # 详细设置按钮
        self.generate_btn = QPushButton("生成图表") # 生成图表按钮
        
        # 布局
        main_layout = QVBoxLayout()
        
        row1_layout = QHBoxLayout()
        row1_layout.addWidget(QLabel("图表类型:"))
        row1_layout.addWidget(self.plot_type)
        row1_layout.addWidget(QLabel("标题:"))
        row1_layout.addWidget(self.title_input)

        row2_layout = QHBoxLayout()
        row2_layout.addWidget(self.file_btn)
        row2_layout.addWidget(self.file_path)
        row2_layout.addWidget(QLabel("工作表名称:"))
        row2_layout.addWidget(self.sheet_name)

        row3_layout = QHBoxLayout()
        row3_layout.addWidget(self.detail_btn)
        row3_layout.addWidget(self.generate_btn)

        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)
        main_layout.addLayout(row3_layout)
        
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 连接信号
        self.file_btn.clicked.connect(self.choose_file)
        self.detail_btn.clicked.connect(self.open_sub_window)
        self.generate_btn.clicked.connect(self.generate_plot)

    def choose_file(self):
        try:
            # 打开文件选择对话框
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择文件", "", "Excel文件 (*.xlsx)"
            )
            if file_path:
                self.file_path.setText(file_path)  # 显示文件路径
        except Exception as e:
            QMessageBox.critical(self, "文件选择失败", e)
            print("文件选择失败:", e)

    def open_sub_window(self):
        # 创建副界面实例并显示
        self.sub_window = SubWindow([self.figsize,self.legend1_loc,self.legend2_loc,self.title_fontweight,self.color_path])
        self.sub_window.closed.connect(self.handle_subwindow_closed) # 连接 SubWindow 的信号
        self.sub_window.exec_()  # 使用 exec_() 显示模态对话框

    def handle_subwindow_closed(self, figsize, legend1_loc, legend2_loc, title_fontweight, color_path):
        # 处理 SubWindow 关闭时传递的参数
        self.figsize = figsize
        self.legend1_loc = legend1_loc
        self.legend2_loc = legend2_loc
        self.title_fontweight = title_fontweight
        self.color_path = color_path
        
        message = (
            f"画布尺寸: {figsize[0]} x {figsize[1]}\n"
            f"图例1位置: {legend1_loc}\n"
            f"图例2位置: {legend2_loc}\n"
            f"标题字体粗细: {title_fontweight}\n"
            f"颜色设置文件: {color_path}"
        )
        QMessageBox.information(self, "详细设置参数已保存", message)

    def generate_plot(self):        
        # 获取用户输入参数
        plot_type = self.plot_type.currentText()
        file_path = self.file_path.text()
        sheet_name = self.sheet_name.text()
        title = self.title_input.text()
        
        # 绘制图表
        if plot_type == "Cash Flow Diagram":
            # 读取Excel文件
            if file_path:
                try:
                    colorfile = open(self.color_path, 'r')
                    colors = [line.rstrip('\n') for line in colorfile.readlines() if is_color(line.rstrip('\n'))]
                    colorfile.close()
                    drawer = cash_flow_diagram.Drawer(rd=file_path, sheet_name=sheet_name, title=title,
                                                      figsize=self.figsize,legend1_loc=self.legend1_loc,
                                                      legend2_loc=self.legend2_loc, title_fontweight=self.title_fontweight,
                                                      colors=colors)
                    drawer.draw()
                except Exception as e:
                    QMessageBox.critical(self, "绘图失败", e)
                    print("绘图失败:", e)
            else:
                QMessageBox.critical(self, "错误", "未选择文件！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
