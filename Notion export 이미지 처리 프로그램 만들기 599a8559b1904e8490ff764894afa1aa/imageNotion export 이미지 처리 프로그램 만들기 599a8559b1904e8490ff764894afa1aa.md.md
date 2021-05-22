# Notion export 이미지 처리 프로그램 만들기

# 🖥️ ESS(Easily Start Study) 프로그램

---

# 🤼순서

1) Notion 내보내기

2) zip 저장 위치 정하기 

3) CLI에서 저장 위치로 이동 

4) python '파일명.py'

# 🤼‍♂️요구사항 정리

- 모든 기능에 대한 gui를 제공한다.
- 워크스페이스를 선택할 수 있다.
- 디렉터리을 생성할 수 있다.
- 정해진 디렉토리 안의 저장된 zip 파일을 압축 해제한다.
- 압축해제한 폴더 내의 md 파일을 저장할 하위 디렉터리를 설정할 수 있다.
- 이미지 폴더가 있다면 이미지 파일명을 각각 재설정할 수 있어야 한다.
- 재설정 시, 사용자가 편하게 이미지 파일명을 정할 수 있게 이미지를 보여준다.
- 만약 이미지 파일 명을 정하지 않을 경우 Untitled{\d}.png 로 설정한다.
- md 파일내 이미지 markdown을 설정한 이미지 파일 명으로 변경한다.
    - 변경 시, '**하위디렉터리/image/이미지.png'**에 위치하도록 함.
- zip파일이 여러개일 경우 리스트에 쌓아두고 순차적으로 진행한다.

# 🤼‍♂️요구사항 별 개발

## 📌모든 기능에 대한 gui를 제공한다.

### (1) 가상환경 생성 및 필요 패키지 다운로드

**가상환경 패키지 생성**

`python3 -m venv venv`

**가상환경 활성화**

플랫폼: **POSIX** 쉘 → **bash/zsh: `source venv/bin/activate`**

**pyQt5 패키지 다운로드** 

`pip install pyQt5`

### (2) pyQt5 애플리케이션 생성

**ess.py**

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget

class EssApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('ESS Program')
        self.move(850,100)
        self.resize(800, 500)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EssApp()
    sys.exit(app.exec_())
```

## 📌워크스페이스를 선택할 수 있다.

### (1)  파일탐색기 다이얼로그 생성 버튼 생성

```python
def initUI(self):
        # 워크스페이스선택버튼 
        folderOpenBtn = QPushButton('워크스페이스 선택', self)
        folderOpenBtn.move(20,20)
        folderOpenBtn.setCheckable(False)
        folderOpenBtn.toggle() 
        folderOpenBtn.clicked.connect(self.openDirectory)
        # 워크스페이스 레이블
        self.curFolderLabel.move(30,60)
```

![Notion%20export%20%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%B7%20%E1%84%86%E1%85%A1%E1%86%AB%E1%84%83%E1%85%B3%E1%86%AF%E1%84%80%E1%85%B5%20599a8559b1904e8490ff764894afa1aa/Untitled.png](Notion%20export%20%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%B7%20%E1%84%86%E1%85%A1%E1%86%AB%E1%84%83%E1%85%B3%E1%86%AF%E1%84%80%E1%85%B5%20599a8559b1904e8490ff764894afa1aa/Untitled.png)

### (2) 워크스페이스 선택 시 Treeview로 파일 트리 구조 조회

```python
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
```

![Notion%20export%20%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%B7%20%E1%84%86%E1%85%A1%E1%86%AB%E1%84%83%E1%85%B3%E1%86%AF%E1%84%80%E1%85%B5%20599a8559b1904e8490ff764894afa1aa/Untitled%201.png](Notion%20export%20%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%B7%20%E1%84%86%E1%85%A1%E1%86%AB%E1%84%83%E1%85%B3%E1%86%AF%E1%84%80%E1%85%B5%20599a8559b1904e8490ff764894afa1aa/Untitled%201.png)

## 📌디렉터리를 생성할 수 있다.

### (1) 디렉토리 구조 확인

![Notion%20export%20%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%B7%20%E1%84%86%E1%85%A1%E1%86%AB%E1%84%83%E1%85%B3%E1%86%AF%E1%84%80%E1%85%B5%20599a8559b1904e8490ff764894afa1aa/Untitled%202.png](Notion%20export%20%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%B7%20%E1%84%86%E1%85%A1%E1%86%AB%E1%84%83%E1%85%B3%E1%86%AF%E1%84%80%E1%85%B5%20599a8559b1904e8490ff764894afa1aa/Untitled%202.png)

### (2)

## 📌정해진 디렉토리 안의 저장된 zip 파일을 압축 해제한다.

```python

```

## 📌압축해제한 폴더 내의 md 파일을 저장할 하위 디렉터리를 설정할 수 있다.

## 📌이미지 폴더가 있다면 이미지 파일명을 각각 재설정할 수 있어야 한다.

## 📌재설정 시, 사용자가 편하게 이미지 파일명을 정할 수 있게 이미지를 보여준다.

## 📌만약 이미지 파일 명을 정하지 않을 경우 Untitled{\d}.png 로 설정한다.

## 📌zip파일이 여러개일 경우 리스트에 쌓아두고 순차적으로 진행한다.

---

# ❓프로그램 메뉴얼❗

# 🤼‍♂️ 1) Notion 내보내기

![Notion%20export%20%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%B7%20%E1%84%86%E1%85%A1%E1%86%AB%E1%84%83%E1%85%B3%E1%86%AF%E1%84%80%E1%85%B5%20599a8559b1904e8490ff764894afa1aa/Untitled%203.png](Notion%20export%20%E1%84%8B%E1%85%B5%E1%84%86%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8E%E1%85%A5%E1%84%85%E1%85%B5%20%E1%84%91%E1%85%B3%E1%84%85%E1%85%A9%E1%84%80%E1%85%B3%E1%84%85%E1%85%A2%E1%86%B7%20%E1%84%86%E1%85%A1%E1%86%AB%E1%84%83%E1%85%B3%E1%86%AF%E1%84%80%E1%85%B5%20599a8559b1904e8490ff764894afa1aa/Untitled%203.png)

# 🤼‍♂️ 2) zip 저장 위치 정하기

# 🤼‍♂️ 3) CLI에서 저장 위치로 이동

# 🤼‍♂️ 4) python '파일명.py'

---

# 🤼‍♀️참고자료

**pyQt5**

[위키독스](https://wikidocs.net/21920)