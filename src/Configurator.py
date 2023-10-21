from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QListView, QLabel, QLineEdit
from PyQt6.QtCore import QStringListModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.left_list = QListView()
        self.right_list = QListView()
        self.label1 = QLabel()
        self.text_box1 = QLineEdit()
        self.label2 = QLabel()
        self.text_box2 = QLineEdit()
        self.label3 = QLabel()
        self.text_box3 = QLineEdit()

        self.left_model = QStringListModel(["Option 1", "Option 2", "Option 3"])
        self.right_model = QStringListModel()

        self.left_list.setModel(self.left_model)
        self.right_list.setModel(self.right_model)

        self.left_list.selectionModel().currentChanged.connect(self.update_right_list)
        self.right_list.selectionModel().currentChanged.connect(self.update_labels_and_text_boxes)

        list_layout = QHBoxLayout()
        list_layout.addWidget(self.left_list)
        list_layout.addWidget(self.right_list)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(list_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def update_right_list(self, current, previous):
        selected_option = current.data()

        if selected_option == "Option 1":
            self.right_model.setStringList(["Sub-option 1.1", "Sub-option 1.2"])
        elif selected_option == "Option 2":
            self.right_model.setStringList(["Sub-option 2.1", "Sub-option 2.2"])
        elif selected_option == "Option 3":
            self.right_model.setStringList(["Sub-option 3.1", "Sub-option 3.2"])

    def update_labels_and_text_boxes(self, current, previous):
        selected_sub_option = current.data()

        # Clear the existing widgets in the layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if selected_sub_option == "Sub-option 1.1":
            # Create new labels and text boxes
            self.label1 = QLabel("Label 1 for Sub-option 1.1")
            self.label1.setGeometry(10, 10, 100, 30)
            self.text_box1 = QLineEdit("Text box 1 for Sub-option 1.1")
            self.label2 = QLabel("Label 2 for Sub-option 1.1")
            self.text_box2 = QLineEdit("Text box 2 for Sub-option 1.1")
            self.label3 = QLabel("Label 3 for Sub-option 1.1")
            self.text_box3 = QLineEdit("Text box 3 for Sub-option 1.1")

            # Add them to the layout
            self.main_layout.addWidget(self.label1)
            self.main_layout.addWidget(self.text_box1)
            self.main_layout.addWidget(self.label2)
            self.main_layout.addWidget(self.text_box2)
            self.main_layout.addWidget(self.label3)
            self.main_layout.addWidget(self.text_box3)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
