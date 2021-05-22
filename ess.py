import sys, os, zipfile, shutil
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QPushButton, QFileDialog, QLabel, QTreeView, QFileSystemModel, QDirModel, QComboBox, QListWidget
from PyQt5.QtGui import *

class EssApp(QWidget):

    def __init__(self):
        super().__init__()
        self.curFolderLabel = QLabel('현재 선택된 워크스페이스 없음.', self)
        self.curZipLabel = QLabel('현재 선택된 압축파일 없음.',self)
        self.treeview = QTreeView(self)
        self.explorerModel = QFileSystemModel(self)
        self.curImages = []
        self.dirComboBox = QComboBox(self)
        self.dirLabel = QLabel('하위 디렉터리 : ',self)
        self.curDirs = []
        self.exceptDirs = ['.git','venv']
        self.curMdLabel = QLabel('현재 md 파일 없음.',self)
        self.curMd = ''
        self.curMdTextEdit = QTextEdit(self)
        self.curImageNoticeLabel = QLabel('현재 이미지 없음.',self)
        self.curImageLabel = QLabel('현재 사진',self)
        self.curImageTextEdit = QTextEdit(self)
        self.curImageDir = ''
        self.imageNoticeLabel = QLabel('이미지 보기',self)
        self.imageList = QListWidget(self)

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
        # 워크스페이스 treeView
        self.treeview.doubleClicked.connect(self.tree_clicked)

        # 압축해제버튼 
        # zipExtractBtn = QPushButton('압축해제', self)
        # zipExtractBtn.move(400,450)
        # zipExtractBtn.setCheckable(False)
        # zipExtractBtn.toggle() 
        # zipExtractBtn.clicked.connect(self.openDirectory)

        # 현재압축파일 레이블
        self.curZipLabel.move(250,60)

        # 디렉터리 레이블
        self.dirLabel.move(250,100)

        # 디렉터리 콤보박스
        self.dirComboBox.setGeometry(330,95,150,30)
        self.dirComboBox.addItem('None')

        # md파일 레이블
        self.curMdLabel.setGeometry(250,150,250,30)

        # md파일명 변경 레이블
        mdEditLabel = QLabel('파일명 변경 : ',self)
        mdEditLabel.setGeometry(250,180,80,30)

        # md파일명 변경 편집창
        self.curMdTextEdit.setGeometry(320,185,160,20)

        # md파일 위치이동 버튼 
        mdMoveBtn = QPushButton('md파일 이동', self)
        mdMoveBtn.setGeometry(240,210,250,30)
        mdMoveBtn.setCheckable(False)
        mdMoveBtn.toggle() 
        mdMoveBtn.clicked.connect(self.moveMd)

        # 이미지 알림 레이블 
        self.curImageNoticeLabel.setGeometry(250,240,250,30)

        # 이미지파일명 변경 레이블
        imageEditLabel = QLabel('파일명 변경 : ',self)
        imageEditLabel.setGeometry(250,270,80,30)

        # 이미지파일명 변경 편집창
        self.curImageTextEdit.setGeometry(320,275,160,20)

        # 이미지파일 위치이동 버튼 
        imageMoveBtn = QPushButton('이미지파일 이동', self)
        imageMoveBtn.setGeometry(240,300,250,30)
        imageMoveBtn.setCheckable(False)
        imageMoveBtn.toggle() 
        imageMoveBtn.clicked.connect(self.imageBtnClicked)

        # 현재 사진 레이블
        self.curImageLabel.setGeometry(500,300,150,150)

        # 이미지 리스트 알림 레이블 
        self.imageNoticeLabel.move(500,60)

        # 이미지 리스트
        self.imageList.setGeometry(500,90,200,170)

        self.setWindowTitle('ESS Program')
        self.setGeometry(850, 100, 800, 500)
        self.show()

    #워크스페이스 선택 메서드
    def openDirectory(self):
        #디렉터리 선택 
        self.directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        #하위 디렉터리 추출 
        for dir in filter(os.path.isdir, os.listdir(os.getcwd())):
            if dir not in self.exceptDirs:
                self.curDirs.append(dir)
        # 디렉터리 콤보박스 갱신
        self.dirComboBox.clear()
        self.dirComboBox.addItems(self.curDirs)
        # 현재 워크스페이스 레이블 및 treeview 설정  
        self.curFolderLabel.setText('현재 워크스페이스 : '+self.directory.split('/')[-1])
        self.treeview.setRootIndex(self.treeview.model.index(self.directory))

    def tree_clicked(self,Qmodelidx):
        path = self.explorerModel.filePath(Qmodelidx)
        filename, fileExtension = os.path.splitext(path)
        #zip 파일일 경우 
        if '.zip' in fileExtension:
            #현재압축파일 레이블 텍스트 설정
            self.curZipLabel.setText('선택된 압축파일 : '+filename.split('/')[-1])
            extractall_path = path
            with zipfile.ZipFile(extractall_path) as zip:
                zip_path = zip.extractall()
            # zip 파일 안에 파일 list을 출력
                for info in zip.infolist():
                    if '.md' in info.filename:
                        self.curMd = info.filename
                        self.curMdLabel.setText('현재 md파일 : '+self.curMd)
                        self.curMdTextEdit.setText(self.curMd)

                    if '.png' in info.filename:
                        self.curImageDir = os.path.dirname(info.filename)
                        self.curImages.append(info.filename.split('/')[-1][:-4])
                
                    
    
    def moveMd(self):
        shutil.move(self.directory+'/'+self.curMd,self.directory+'/'+self.dirComboBox.currentText()+'/'+'image'+self.curMdTextEdit.toPlainText()+'.md')
        self.imageList.addItems(self.curImages)
        self.setImage()
        
    def setImage(self):
        if self.curImages:
            self.curImageNoticeLabel.setText("현재 선택된 이미지 : "+self.curImages[0]+'.png')
            self.curImageTextEdit.setText(self.curImages[0])
            image = QPixmap(self.directory+'/'+self.curImageDir+'/'+self.curImages[0]+'.png')
            image.scaledToHeight(150)
            image.scaledToWidth(150)
            self.curImageLabel.setPixmap(image) #image path
            

    def imageBtnClicked(self):
        if self.curImages:
            self.moveImage()
            self.popImage()
            self.setImage()
        else:
            print('옮길 이미지가 없습니다.')

    def popImage(self):
        self.curImages.pop(0)
        self.imageList.takeItem(0)
        
    def moveImage(self):
        shutil.move(self.directory+'/'+self.curImageDir+'/'+self.curImages[0]+'.png',
        self.directory+'/'+self.dirComboBox.currentText()+'/image/'+self.curImageTextEdit.toPlainText()+'.png')

    def fixMdImageCode(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EssApp()
    sys.exit(app.exec_())