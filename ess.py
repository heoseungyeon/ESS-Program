import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QTreeView, QFileSystemModel, QDirModel
from PyQt5.Qt import * 

class EssApp(QWidget):

    def __init__(self):
        super().__init__()
        self.curFolderLabel = QLabel('현재 선택된 워크스페이스 없음.', self)
        self.treeview = QTreeView(self)
        self.explorerModel = QFileSystemModel(self)
        
        self.initUI()

    def initUI(self):
        # 워크스페이스선택버튼 
        folderOpenBtn = QPushButton('워크스페이스 선택', self)
        folderOpenBtn.move(20,20)
        folderOpenBtn.setCheckable(False)
        folderOpenBtn.toggle() 
        folderOpenBtn.clicked.connect(self.openDirectory)
        # 워크스페이스 레이블
        self.curFolderLabel.move(30,60)

        # 워크스페이스 treeView
        self.treeview.model = self.explorerModel
        self.treeview.model.setRootPath('/')
        self.treeview.setModel(self.treeview.model)
        self.treeview.setGeometry(30,90,200,350)

        self.setWindowTitle('ESS Program')
        self.setGeometry(850, 100, 800, 500)
        self.show()

    def openDirectory(self):
        #디렉터리 선택 
        self.directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        self.curFolderLabel.setText('현재 워크스페이스 : '+self.directory.split('/')[-1])
        self.treeview.setRootIndex(self.treeview.model.index(self.directory))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EssApp()
    sys.exit(app.exec_())