import os
import shutil
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog, QMessageBox, QLineEdit, QVBoxLayout, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # настройки главного окна
        self.setWindowTitle("Копирование RAW файлов")
        self.setFixedSize(640, 140)

        self.jpg_files = []  # список файлов с расширением jpg
        self.raw_files = []  # список файлов с расширением из line edit

        self.layoutMain = QVBoxLayout()
        self.layoutMain.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layoutJPG = QHBoxLayout()
        self.layoutJPG.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # создадим кнопку и лейбл для выбора папки с файлами JPG
        self.buttonFolderJpg = QPushButton('Папка с JPG', self)
        self.buttonFolderJpg.clicked.connect(self.select_jpg_folder)
        self.layoutJPG.addWidget(self.buttonFolderJpg)
        self.labelFolderJpg = QLabel(self)
        self.layoutJPG.addWidget(self.labelFolderJpg)
        # создадим текст лейблы с информацией о количестве найденных файлов с расширением jpg
        self.labelFilesJpg = QLabel(self)
        self.layoutJPG.addWidget(self.labelFilesJpg)
        self.layoutMain.addLayout(self.layoutJPG)

        self.layoutRAWEdit = QHBoxLayout()
        self.layoutRAWEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # создадим поле ввода для расширения RAW файлов и кнопку выбора папки с этими файлами
        self.labelFileRawExt = QLabel(self)
        self.labelFileRawExt.setText('Расширение RAW:')
        self.labelFileRawExt.setFixedWidth(140)
        self.layoutRAWEdit.addWidget(self.labelFileRawExt)
        self.rawExt = 'RAF'  # исходное значение расширения RAW
        self.editFileRawExt = QLineEdit(self)
        self.editFileRawExt.setText(self.rawExt)
        self.editFileRawExt.setFixedWidth(48)
        self.editFileRawExt.setInputMask('AAA')
        self.layoutRAWEdit.addWidget(self.editFileRawExt)
        self.layoutMain.addLayout(self.layoutRAWEdit)

        self.layoutRAW = QHBoxLayout()
        self.layoutRAW.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.buttonFolderRaw = QPushButton('Папка с RAW', self)
        self.buttonFolderRaw.clicked.connect(self.select_raw_folder)
        self.layoutRAW.addWidget(self.buttonFolderRaw)
        # создадим текст лейблы с информацией о количестве найденных файлов с расширением из line edit
        self.labelFolderRaw = QLabel(self)
        self.layoutRAW.addWidget(self.labelFolderRaw)
        self.labelFilesRaw = QLabel(self)
        self.layoutRAW.addWidget(self.labelFilesRaw)
        self.layoutMain.addLayout(self.layoutRAW)

        # создадим кнопку копирования RAW файлов
        self.buttonCopy = QPushButton("Копировать одноименные RAW", self)
        self.buttonCopy.clicked.connect(self.copy_raw_files)
        self.layoutMain.addWidget(self.buttonCopy)

        self.container = QWidget()
        self.container.setLayout(self.layoutMain)
        self.setCentralWidget(self.container)

    def get_file_names_by_extension(self, folder_path, extensions):
        file_list = []
        for file in os.listdir(folder_path):
            name, extension = os.path.splitext(file)
            if extension[1:].lower() in extensions:
                file_list.append(name)
        return file_list
  
    def select_jpg_folder(self):
        jpg_folder = QFileDialog.getExistingDirectory(self, 'Выбрать папку с JPG')
        self.new_raw_folder = jpg_folder+'/raw'

        if jpg_folder:
            self.jpg_folder = jpg_folder
            self.labelFolderJpg.setText(jpg_folder)

            self.jpg_files = self.get_file_names_by_extension(jpg_folder, ['jpg', 'jpeg'])
            self.labelFilesJpg.setText(f'Найдено {len(self.jpg_files)} файлов')
            print(f'Найдено {len(self.jpg_files)} файлов')
            print(self.jpg_files)

    def select_raw_folder(self):
        raw_folder = QFileDialog.getExistingDirectory(self, 'Выбрать папку с RAW')

        if raw_folder:
            self.raw_folder = raw_folder
            self.labelFolderRaw.setText(raw_folder)

            self.raw_files = self.get_file_names_by_extension(raw_folder, [self.rawExt.upper(), self.rawExt.lower()])
            self.labelFilesRaw.setText(f'Найдено {len(self.raw_files)} файлов')
            print(f'Найдено {len(self.raw_files)} файлов')
            print(self.raw_files)


    def copy_raw_files(self):
        if not self.jpg_files:
            QMessageBox.about(self, 'Ошибка', 'Выберите папку с файлами JPG!')
            return

        if not self.raw_files:
            QMessageBox.about(self, 'Ошибка', 'Выберите папку с файлами RAW!')
            return
        
        # сравниваем массивы, ищем одинаковые имена 
        to_copy = []
        not_found = []

        for jpg_file in self.jpg_files:
            if jpg_file in self.raw_files:
                to_copy.append(jpg_file)
            else:
                not_found.append(jpg_file)
        print(f"Найдено {len(to_copy)} файлов из {len(self.jpg_files)}")

        # создаем папку для сохранения копий RAW файлов
        if not os.path.exists(self.new_raw_folder):
            os.makedirs(self.new_raw_folder)

        for file_name in to_copy:
            file_name+='.RAF'
            file_path = os.path.join(self.raw_folder, file_name)
            dest = self.new_raw_folder
            print(f"{file_path} -> {dest}")
            try:
                shutil.copy(file_path, dest)
                print(f"{file_name} copied")
            except Exception as e:
                print(f"{file_name} failed: {e}")

        if len(not_found)>0:
            QMessageBox.about(self, 'Почти успешно!',f'Скопировано {len(to_copy)}файлов, отсутствуют: {not_found}')
        else:
            QMessageBox.about(self, 'Успешно!',f'Скопировано {len(to_copy)}файлов.')
            

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()