Python 3.10.6 (tags/v3.10.6:9c7b4bd, Aug  1 2022, 21:53:49) [MSC v.1932 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import hou, os
from PySide2 import QtWidgets, QtCore

selected_node = hou.selectedNodes()[0]
path = selected_node.path()
mat_node_path=os.path.dirname(path)



def mtlx_basecolor(selected_node):
    base_color_path = selected_node.parm("basecolor_texture").eval()
    base_color_node = hou.node(mat_node_path).createNode("mtlximage")
    base_color_node.setName("base_color")
    base_color_node.parm("file").set(base_color_path)
    return base_color_node

def mtlx_roughness(selected_node):
    roughness_path = selected_node.parm("rough_texture").eval()
    roughness_node = hou.node(mat_node_path).createNode("mtlximage")
    roughness_node.setName("roughness")
    roughness_node.parm("file").set(roughness_path)
    return roughness_node

def mtlx_normal(selected_node):
    base_normal_path = selected_node.parm("baseNormal_texture").eval()
    base_normal_node = hou.node(mat_node_path).createNode("mtlximage")
    base_normal_node.setName("base_normal")
    base_normal_node.parm("file").set(base_normal_path)
    
    normal_node = hou.node(mat_node_path).createNode("mtlxnormalmap")
    normal_node.setName("normal_map")
    normal_node.parm("scale").set(2.0)
    normal_node.setInput(0, base_normal_node)
    return normal_node

def mtlx_metallic(selected_node):
    metallic_path = selected_node.parm("metallic_texture").eval()
    metallic_node = hou.node(mat_node_path).createNode("mtlximage")
    metallic_node.setName("metallic")
    metallic_node.parm("file").set(metallic_path)
    return metallic_node

def mtlx_opacity(selected_node):
    opacity_path = selected_node.parm("opaccolor_texture").eval()
    opacity_node = hou.node(mat_node_path).createNode("mtlximage")
    opacity_node.setName("opacity")
    opacity_node.parm("file").set(opacity_path)
    return opacity_node
    
class MaterialXConvertor(QtWidgets.QWidget):
    def __init__(self):
        super(MaterialXConvertor, self).__init__()

        self.initUI()

    def initUI(self):
        # 设置窗口标题
        self.setWindowTitle("AUTO MTLX")

        # 创建复选框
        self.basecolor_checkbox = QtWidgets.QCheckBox("Base Color", self)
        self.basecolor_checkbox.setChecked(True)  # 设置默认状态为勾选
        self.basecolor_checkbox.stateChanged.connect(self.basecolorCheckboxStateChanged)

        self.roughness_checkbox = QtWidgets.QCheckBox("Roughness", self)
        self.roughness_checkbox.setChecked(True)
        self.roughness_checkbox.stateChanged.connect(self.roughnessCheckboxStateChanged)

        self.normal_checkbox = QtWidgets.QCheckBox("Normal", self)
        self.normal_checkbox.setChecked(True)
        self.normal_checkbox.stateChanged.connect(self.normalCheckboxStateChanged)

        self.metallic_checkbox = QtWidgets.QCheckBox("Metallic", self)
        self.metallic_checkbox.setChecked(False)
        self.metallic_checkbox.stateChanged.connect(self.metallicCheckboxStateChanged)

        self.opacity_checkbox = QtWidgets.QCheckBox("Opacity", self)
        self.opacity_checkbox.setChecked(False)
        self.opacity_checkbox.stateChanged.connect(self.opacityCheckboxStateChanged)

        # 创建生成按钮
        self.generate_btn = QtWidgets.QPushButton("Generate", self)
        self.generate_btn.clicked.connect(self.generateButtonClicked)
        self.generate_btn.setFixedSize(400, 50)  # 设置按钮的大小为150x50
        
          # 创建水平布局，并将复选框添加到布局中
        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_layout.addWidget(self.basecolor_checkbox)
        checkbox_layout.addWidget(self.roughness_checkbox)
        checkbox_layout.addWidget(self.normal_checkbox)
        checkbox_layout.addWidget(self.metallic_checkbox)
        checkbox_layout.addWidget(self.opacity_checkbox)

        # 创建垂直布局，并将复选框布局和按钮添加到布局中
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(checkbox_layout)
        layout.addWidget(self.generate_btn)
        
        # 移除窗口的最小化、最大化和全屏按钮
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.Window)
        flags &= ~QtCore.Qt.WindowMaximizeButtonHint
        flags &= ~QtCore.Qt.WindowMinimizeButtonHint
        self.setWindowFlags(flags)

        # 将布局设置为窗口的主布局
        self.setLayout(layout)

    def basecolorCheckboxStateChanged(self, state):
        if state == QtCore.Qt.Checked:
            print("Base Color checkbox is checked")
            # 在这里添加处理基色复选框勾选的逻辑
        else:
            print("Base Color checkbox is unchecked")

    def roughnessCheckboxStateChanged(self, state):
        if state == QtCore.Qt.Checked:
            print("Roughness checkbox is checked")
            # 在这里添加处理粗糙度复选框勾选的逻辑
        else:
            print("Roughness checkbox is unchecked")

    def normalCheckboxStateChanged(self, state):
        if state == QtCore.Qt.Checked:
            print("Normal checkbox is checked")
            # 在这里添加处理法线复选框勾选的逻辑
        else:
            print("Normal checkbox is unchecked")

    def metallicCheckboxStateChanged(self, state):
        if state == QtCore.Qt.Checked:
            print("Metallic checkbox is checked")
            # 在这里添加处理金属度复选框勾选的逻辑
        else:
            print("Metallic checkbox is unchecked")

    def opacityCheckboxStateChanged(self, state):
        if state == QtCore.Qt.Checked:
            print("Opacity checkbox is checked")
            # 在这里添加处理透明度复选框勾选的逻辑
        else:
            print("Opacity checkbox is unchecked")

    def generateButtonClicked(self):
        standard_surface_node = hou.node(mat_node_path).createNode("mtlxstandard_surface")
        standard_surface_node.setName("standard_surface")

        if self.basecolor_checkbox.isChecked():
            base_color_node = mtlx_basecolor(selected_node)
            standard_surface_node.setInput(1, base_color_node, 0)

        if self.roughness_checkbox.isChecked():
            roughness_node = mtlx_roughness(selected_node)
            standard_surface_node.setInput(6, roughness_node, 0)

        if self.normal_checkbox.isChecked():
            normal_node = mtlx_normal(selected_node)
            standard_surface_node.setInput(40, normal_node, 0)

        if self.metallic_checkbox.isChecked():
            metallic_node = mtlx_metallic(selected_node)
            standard_surface_node.setInput(3, metallic_node, 0)

        if self.opacity_checkbox.isChecked():
            opacity_node = mtlx_opacity(selected_node)
            standard_surface_node.setInput(38, opacity_node, 0)

# 在Houdini中创建窗口
def createWindow():
    # 检查窗口是否已经存在
    if hasattr(hou.session, "materialXConvertor"):
        hou.session.materialXConvertor.close()

    # 创建窗口实例
    hou.session.materialXConvertor = MaterialXConvertor()

    # 将窗口作为Houdini主窗口的子窗口
    hou.session.materialXConvertor.show()

# 运行函数创建窗口
createWindow()