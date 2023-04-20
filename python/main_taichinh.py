from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import sys

class Taichinh_view:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Menu')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Hiện thị danh sách thông tin nhân viên
        self.button_staff = QtWidgets.QPushButton(
            'Thông tin nhân viên', self.main_window)
        self.button_staff.move(120, 140)
        self.button_staff.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_staff.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_staff.clicked.connect(self.clicked_staff)

        # Hiện thị danh sách thông tin phân công
        self.button_assign = QtWidgets.QPushButton(
            'Thông tin phân công', self.main_window)
        self.button_assign.move(380, 140)
        self.button_assign.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_assign.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_assign.clicked.connect(self.clicked_assign)

        # Đăng xuất
        self.button_assign = QtWidgets.QPushButton(
            'Đăng Xuất', self.main_window)
        self.button_assign.move(120, 260)
        self.button_assign.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_assign.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_assign.clicked.connect(self.clicked_assign)

    def clicked_staff(self):
        taichinh_windown.closeWindow()
        global window_taichinh_ThongTinNhanVien
        window_taichinh_ThongTinNhanVien.Load_Data()
        window_taichinh_ThongTinNhanVien.showWindow()

    def clicked_assign(self):
        taichinh_windown.closeWindow()
        global window_TaiChinh_DanhSachPhanCong
        window_TaiChinh_DanhSachPhanCong.Load_Data()
        window_TaiChinh_DanhSachPhanCong.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

class TaiChinh_ThongTinNhanVien:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Tab 1')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(11)
        self.table_widget.setHorizontalHeaderLabels(
            ['MANV', 'TENNV', 'PHAI', 'NGAYSINH', 'DIACHI' , 'SODT' , 'SODT' ,'PHUCAP' ,'VAITRO' ,'MANQL' , 'PHG' ])
        # Tạo khung cuộn
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(390)
        scroll_area.setFixedHeight(400)

        # Đặt bảng trong khung cuộn
        scroll_area.setWidget(self.table_widget)
        # # Thêm tab_widget vào QMainWindow
        self.main_window.setCentralWidget(scroll_area)
        # Tạo 2 ô textbox
        self.textbox1 = QtWidgets.QTextEdit(self.main_window)
        self.textbox1.setReadOnly(True)  # Thiết lập ô textbox chỉ đọc
        self.textbox2 = QtWidgets.QTextEdit(self.main_window)
        self.textbox3 = QtWidgets.QTextEdit(self.main_window)

        # Thiết lập p hiện thị MANV
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("MANV : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(410, 50)

        # Thiết lập kích thước và vị trí cho ô textbox thứ nhất
        self.textbox1.setGeometry(QtCore.QRect(500, 40, 100,30))

         # Thiết lập p hiện thị LUONG
        self.text_luong = QtWidgets.QLabel(self.main_window)
        self.text_luong.setText("LUONG : ")
        self.text_luong.setStyleSheet("font-size: 15px;")
        self.text_luong.adjustSize()
        self.text_luong.move(410, 140)

        # Thiết lập kích thước và vị trí cho ô textbox thứ hai
        self.textbox2.setGeometry(QtCore.QRect(500, 130, 100, 30))

        # Thiết lập p hiện thị PHUCAP
        self.text_luong = QtWidgets.QLabel(self.main_window)
        self.text_luong.setText("PHU CAP : ")
        self.text_luong.setStyleSheet("font-size: 15px;")
        self.text_luong.adjustSize()
        self.text_luong.move(410, 230)

        # Thiết lập kích thước và vị trí cho ô textbox thứ ba
        self.textbox3.setGeometry(QtCore.QRect(500, 220, 100, 30))

        # thiết lập button xem tất cả
        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setFixedSize(80, 30)  # đặt kích thước là 40x40 pixel
        self.btn_update.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_update.setText('UPDATE')
        self.btn_update.move(490,300)

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

        window_taichinh_ThongTinNhanVien.closeWindow()
        global taichinh_windown

        taichinh_windown.Load_Data()
        taichinh_windown.showWindow()

class TaiChinh_DanhSachPhanCong:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Tab 2')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(
            ['MANV', 'MADA', 'THOIGIAN' ])
        # Tạo khung cuộn
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(390)
        scroll_area.setFixedHeight(400)
         # Đặt bảng trong khung cuộn
        scroll_area.setWidget(self.table_widget)
        # # Thêm tab_widget vào QMainWindow
        self.main_window.setCentralWidget(scroll_area)

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

        window_TaiChinh_DanhSachPhanCong.closeWindow()
        global taichinh_windown

        taichinh_windown.Load_Data()
        taichinh_windown.showWindow()

taichinh_windown = Taichinh_view()
window_taichinh_ThongTinNhanVien = TaiChinh_ThongTinNhanVien()
window_TaiChinh_DanhSachPhanCong = TaiChinh_DanhSachPhanCong()
def main():

    app = QtWidgets.QApplication(sys.argv)
    global taichinh_windown
    taichinh_windown.Load_Data()
    taichinh_windown.showWindow()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()