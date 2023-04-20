from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import sys

class NhanVien_view:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Menu')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Hiện thị danh sách thông tin đề án
        self.button_staff = QtWidgets.QPushButton(
            'Thông tin Cá nhân', self.main_window)
        self.button_staff.move(120, 180)
        self.button_staff.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_staff.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_staff.clicked.connect(self.clicked_information)

        # Đăng xuất
        self.button_assign = QtWidgets.QPushButton(
            'Đăng Xuất', self.main_window)
        self.button_assign.move(380, 180)
        self.button_assign.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_assign.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def clicked_information(self):
        Nhanvien_windown.closeWindow()
        global window_tab1
        window_tab1.Load_Data()
        window_tab1.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

class ThongTinCaNhan:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách đề án')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(13)
        self.table_widget.setHorizontalHeaderLabels(
            ['MANV', 'TENNV', 'PHAI', 'NGAYSINH', 'DIACHI' , 'SODT' , 'SODT' ,'PHUCAP' ,'VAITRO' ,'MANQL' , 'PHG' , 'MADA', 'THOIGIAN' ])
        
        # Tạo khung cuộn
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(390)
        scroll_area.setFixedHeight(400)

        # Đặt bảng trong khung cuộn
        scroll_area.setWidget(self.table_widget)
        # # Thêm tab_widget vào QMainWindow
        self.main_window.setCentralWidget(scroll_area)

         # Thiết lập button thêm đề án
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_back.setText("THÊM")
        self.btn_back.move(480, 100)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        # self.btn_back.clicked.connect(self.Backmenu)

        # Thiết lập button xóa đề án
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_back.setText("XÓA")
        self.btn_back.move(480, 160)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        # self.btn_back.clicked.connect(self.Backmenu)

         # Thiết lập button sửa đề án
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_back.setText("CHỈNH SỬA")
        self.btn_back.move(480, 220)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        # self.btn_back.clicked.connect(self.Backmenu)

        # Thiết lập button back
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("BACK")
        self.btn_back.move(610, 470)
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.Backmenu)

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def Backmenu(self):

        window_tab1.closeWindow()
        global Nhanvien_windown

        Nhanvien_windown.Load_Data()
        Nhanvien_windown.showWindow()

Nhanvien_windown = NhanVien_view()
window_ThongTinCaNhan = ThongTinCaNhan()
def main():
    app = QtWidgets.QApplication(sys.argv)
    global Nhanvien_windown
    Nhanvien_windown.Load_Data()
    Nhanvien_windown.showWindow()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()