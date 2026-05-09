#Импортирование
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap, QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt
from PIL import Image
from PIL import ImageOps
from PIL import ImageEnhance
import os 

#Основы приложения
app = QApplication([])
window = QWidget()
window.setWindowTitle('Easy Editor')
window.resize(770, 500)


#workdir
workdir = ''

#Функции
def choose_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files: list, extensions: list) -> list:
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result

def show_filenames_list():
    choose_workdir()
    extensions = ['.jpg', '.jpeg', '.bmp', '.png']
    files = os.listdir(workdir)
    result = filter(files, extensions)
    list_widget.clear()
    for i in result:
        list_widget.addItem(i)
    

    
#Классы 
class ImageProcessor():
    def __init__(self):
        self.picture = None
        self.filename = None
        self.dir = None
        self.save_dir = 'Modified/'
        self.original_image = None
    
    def load_image(self, dir, filename): 
        self.filename = filename
        self.dir = dir 
        image_path = os.path.join(dir, filename)
        self.picture = Image.open(image_path)
        self.original_image = self.picture.copy()
    
    def show_image(self, path):
        pixmapimage = QPixmap(path)
        if pixmapimage.isNull():
            print('Не удалось открыть QPixmap')
            return
        label_width, label_height = picture.width(), picture.height() 
        scaled_pixmap = pixmapimage.scaled(label_width, label_height, Qt.KeepAspectRatio)
        picture.setPixmap(scaled_pixmap)
        picture.setVisible(True)
    
    def save_image(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path) 
        image_path = os.path.join(path, self.filename)
        self.picture.save(image_path)

    def reset_image(self):
        self.picture = self.original_image.copy()
        self.show_image(os.path.join(workdir, self.filename))
        
    def image_bw(self):
        self.picture = self.picture.convert('L')
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def image_left(self):
        self.picture = self.picture.rotate(90)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def image_right(self):
        self.picture = self.picture.rotate(-90)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def image_mirror(self):
        self.picture = ImageOps.mirror(self.picture)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)

    def image_sharp(self):
        self.picture = ImageEnhance.Contrast(self.picture)
        self.picture = self.picture.enhance(1.5)
        self.save_image()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.show_image(image_path)
        
    

#Объекты
image = ImageProcessor()
font_path = 'TAWOGTheSpoon-Regular.otf'
font_id = QFontDatabase.addApplicationFont(font_path)
if font_id == -1:
    print('Error')
else:
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    if font_families:
        font_name = font_families[0]
        print(f'Шрифт {font_name} загружен')

def show_chosen_image():
    if list_widget.currentRow() >= 0:
        filename = list_widget.currentItem().text()
        image.load_image(workdir, filename)
        image_path = os.path.join(image.dir, image.filename)
        image.show_image(image_path)


#Виджеты1
folder_button = QPushButton('Папка')
left_button = QPushButton('Лево')
right_button = QPushButton('Право')
mirror_button = QPushButton('Зеркало')
sharpness_button = QPushButton("Резкость")
bw_button = QPushButton("Ч/Б")
save_button = QPushButton("Сохранить")
reset_button = QPushButton("Сбросить фильтры")
picture = QLabel('Картинка')
list_widget = QListWidget()

#Лейауты
main_h_layout = QHBoxLayout()
h_layout = QHBoxLayout()

v1_layout = QVBoxLayout()
v2_layout = QVBoxLayout()

#Соеденения
h_layout.addWidget(left_button)
h_layout.addWidget(right_button)
h_layout.addWidget(mirror_button)
h_layout.addWidget(sharpness_button)
h_layout.addWidget(bw_button)
h_layout.addWidget(save_button)
h_layout.addWidget(reset_button)

v1_layout.addWidget(folder_button)
v1_layout.addWidget(list_widget)

v2_layout.addWidget(picture)
v2_layout.addLayout(h_layout)

main_h_layout.addLayout(v1_layout)
main_h_layout.addLayout(v2_layout)

window.setLayout(main_h_layout)

#Подсоеденение кнопок
folder_button.clicked.connect(show_filenames_list)
list_widget.currentRowChanged.connect(show_chosen_image)
bw_button.clicked.connect(image.image_bw)
left_button.clicked.connect(image.image_left)
right_button.clicked.connect(image.image_right)
mirror_button.clicked.connect(image.image_mirror)
sharpness_button.clicked.connect(image.image_sharp)
reset_button.clicked.connect(image.reset_image)

#Стиль
window.setStyleSheet(
    '''

    QWidget {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #710fb7, stop: 1 #890fcb);
    } 

    QTextEdit {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #9f5afa, stop: 1 #ca0ffa);
        font-size: 14;
    }

    QLineEdit{
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #9f5afa, stop: 1 #ca0ffa);
    }

    QPushButton{
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #730faf, stop: 1 #7a0fb9);
        color: white;
        font-size: 16px;
        font-weight: 400;
        padding: 5px 8px;
    }

    QPushButton:hover{
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #880fc1, stop: 1 #7f0fc1);
        border: 2px dotted #8950a4;
    }

    QPushButton:pressed{
        background-color: #7f0fc1;
        border: 2px solid #8950a4;
    }

    QLabel{
        color: white;
        font-size: 14px;
    }
    
    '''


)

#Запуск
window.show()
app.exec()
