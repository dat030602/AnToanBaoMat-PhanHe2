import sys
import cx_Oracle
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
# import messagebox
from PyQt5.QtCore import Qt
from tkinter import messagebox
from datetime import datetime

# Controller: Login


class LoginController:
    def Load_Data(self):
        self.username_text = None
        self.password_text = None

    def login_connect(self, username_text, password_text):
        self.username_text = username_text
        self.password_text = password_text

        result = execute_query(username_text, password_text,
                               "select GRANTED_ROLE from USER_ROLE_PRIVS WHERE GRANTED_ROLE NOT IN(select GRANTED_ROLE from ROLE_ROLE_PRIVS)")
        print(result)

        if result:
            global login_info
            login_info = [username_text, password_text, result[0][0]]
        print(login_info)
        return result

    def get_username_and_password(self):
        return login_info[0], login_info[1]


# Controller: Role trưởng phòng


class AssignmentList_Controller:
    def get_staff_list(self):
        result = execute_query(
            login_info[0], login_info[1], 'select MANV, TENNV from NVQUANTRI.UV_NHANVIENPHONGBAN')
        return result

    def get_staff_ass(self):
        result = execute_query(
            login_info[0], login_info[1], 'select manv,tennv, mada, tenda from NVQUANTRI.UV_NHANVIENPHONGBAN, NVQUANTRI.UV_DEANPHONGBAN')
        return result

    def get_assignment_list(self):
        result = execute_query(
            login_info[0], login_info[1], 'select NV.MANV, NV.TENNV, DA.MADA, DA.TENDA, DA.NGAYBD, PC.THOIGIAN, PB.TENPB, PB.MAPB from NVQUANTRI.UV_PHANCONGPHONGBAN PC join NVQUANTRI.UV_DEANPHONGBAN DA ON PC.MADA=DA.MADA join NVQUANTRI.UV_NHANVIENPHONGBAN NV ON PC.MANV=NV.MANV join NVQUANTRI.UV_PHONGBANPHONGBAN PB ON DA.PHONG = PB.MAPB')
        return result

    def Delete_Staff(self, MANV, MADA):
        result = execute_query(
            login_info[0], login_info[1], f"DELETE FROM NVQUANTRI.UV_PHANCONGPHONGBAN WHERE MANV='{MANV}' AND MADA='{MADA}'")
        return result

    def Delete_Assignment(self, MADA):
        result = execute_query(
            login_info[0], login_info[1], f"DELETE FROM NVQUANTRI.UV_PHANCONGPHONGBAN WHERE MADA='{MADA}'")
        return result

    def Update_Assignment(self, THOIGIAN, MANV, MADA):
        result = execute_query(
            login_info[0], login_info[1], f"UPDATE NVQUANTRI.UV_PHANCONGPHONGBAN SET THOIGIAN = '{THOIGIAN}' WHERE MANV='{MANV}' AND MADA='{MADA}'")
        return result

    def InsertStaff(self, MANV, MADA):
        result = execute_query(
            login_info[0], login_info[1], f"INSERT INTO NVQUANTRI.UV_PHANCONGPHONGBAN VALUES ('{MANV}', '{MADA}', NULL)")
        return result


class TruongPhong_ListStaff_Controller:
    def get_staff_list(self, text):
        if (text != ""):
            result = execute_query(
                login_info[0], login_info[1], "select MANV, TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG from NVQUANTRI.UV_NHANVIENPHONGBAN where MANV like '%{0}' or MANV like '{0}%' or MANV like '%{1}' or MANV like '{1}%' or TENNV like '%{0}' or TENNV like '{0}%' or TENNV like '%{1}' or TENNV like '{1}%'".format(text, text.upper()))
        else:
            result = execute_query(
                login_info[0], login_info[1], 'select MANV, TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG from NVQUANTRI.UV_NHANVIENPHONGBAN')
        return result


# Controller: Nhân sự


class NhanSu_controller:
    def pb_list(self):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT * FROM NVQUANTRI.PHONGBAN')
        return result

    def nv_list(self):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT * FROM NVQUANTRI.NHANVIEN_NS')
        return result

    def add_pb(self, id, name, trphg):
        result = execute_query(
            login_info[0], login_info[1], 'INSERT INTO NVQUANTRI.PHONGBAN VALUES(' + "'{0}', '{1}', '{2}')".format(id, name, trphg))
        return result

    def add_nv(self, id, name, gt, ngsinh, dc, sdt, vaitro, ql, phg):
        result = execute_query(
            login_info[0], login_info[1], 'INSERT INTO NVQUANTRI.NHANVIEN(MANV, TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG) VALUES(' + "'{0}', '{1}', '{2}', TO_DATE('{3}','DD/MM/YYYY'), '{4}', '{5}', '{6}', '{7}', '{8}')".format(id, name, gt, ngsinh, dc, sdt, vaitro, ql, phg))
        return result

    def update_pb(self, clause, res, condition):
        if clause == 'Tên phòng ban':
            clause = 'TENPB'
        else:
            clause = 'TRPHG'
        result = execute_query(
            login_info[0], login_info[1], 'UPDATE NVQUANTRI.PHONGBAN SET ' + "{0} = '{1}' WHERE MAPB = '{2}'".format(clause, res, condition))
        return result

    def update_nv(self, clause, res, condition, condition_res):
        if clause == 'Tên nhân viên':
            clause = 'TENNV'
        elif clause == 'Giới tính':
            clause = 'PHAI'
        elif clause == 'Ngày sinh':
            clause = 'NGAYSINH'
        elif clause == 'Địa chỉ':
            clause = 'DIACHI'
        elif clause == 'Số điện thoại':
            clause = 'SĐT'
        elif clause == 'Vai trò':
            clause = 'VAITRO'
        elif clause == 'Quản lý':
            clause = 'MANQL'
        elif clause == 'Trưởng phòng':
            clause = 'PHG'

        if condition == 'Tên nhân viên':
            condition = 'TENNV'
        elif condition == 'Mã nhân viên':
            condition = 'MANV'
        elif condition == 'Vai trò':
            condition = 'VAITRO'
        elif condition == 'Quản lý':
            condition = 'MANQL'
        elif condition == 'Trưởng phòng':
            condition = 'PHG'

        result = execute_query(
            login_info[0], login_info[1], 'UPDATE NVQUANTRI.NHANVIEN SET ' + "{0} = '{1}' WHERE {2} = '{3}'".format(clause, res, condition, condition_res))
        return result

# Controller: Đề án


class DeAn_controller:
    def get_DeAn_list(self):
        sql = "SELECT * FROM DEAN"
        result = execute_query('Truongphong', '123', sql)
        return result


# Controller: Tài chính

# Controller: Quản lý trực tiếp
class QLTructiep_controller:
    def pc_list(self):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT * FROM NVQUANTRI.PHANCONG_QLTRUCTIEP')
        return result

    def nv_list(self):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT * FROM NVQUANTRI.NHANVIEN_QLTRUCTIEP')
        return result

#################################################################


# Function


def MessageBoxInfo(title, message):
    messagebox.showinfo(title, message)


def MessageBoxErr(title, message):
    messagebox.showerror(title, message)


def MessageBoxWarn(title, message):
    messagebox.showwarning(title, message)


#################################################################


# Database connection


def execute_query(username, password, queryString):
    try:
        con = cx_Oracle.connect(username, password, 'localhost:1521/XEPDB1')

    except cx_Oracle.DatabaseError as er:
        print('There is an error in the Oracle database:', er)

    else:
        try:
            cur = con.cursor()

            # fetchall() is used to fetch all records from result set
            cur.execute(queryString)
            con.commit()
            rows = cur.fetchall()
            if cur:
                cur.close()
            return rows

        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:', er)
            if cur:
                cur.close()
            return False

        except Exception as er:
            print('Error:'+str(er))
            if cur:
                cur.close()
            return False


def connection2(username, password):
    try:
        con = cx_Oracle.connect(username, password, 'localhost:1521/XEPDB1')
        return con

    except cx_Oracle.DatabaseError as er:
        print('There is an error in the Oracle database:', er)
        return False

    except Exception as er:
        print('Error:'+str(er))
        return False


#################################################################


# Views: Main


class LoginWindow:
    def Load_Data(self):
        self.login_controllers = LoginController()
        self.login_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.login_window.setWindowTitle('login')

        # Thiết lập kích thước cho widget
        self.login_window.resize(640, 480)

        #   Thiết lập ô hiện thị nhập username
        user_name = QLabel(self.login_window)
        user_name.setText("Nhập username: ")
        user_name.setStyleSheet("font-size: 14px;")
        user_name.move(250, 20)

        # Thiết lập ô nhập input username
        self.username_input = QLineEdit(self.login_window)
        self.username_input.setPlaceholderText("user name")
        self.username_input.setStyleSheet("QLineEdit { padding-left: 20px; }")
        self.username_input.setFixedWidth(160)
        self.username_input.move(250, 60)

        #   Thiết lập ô hiện thị nhập password
        password = QLabel(self.login_window)
        password.setText("Nhập password: ")
        password.setStyleSheet("font-size: 14px;")
        password.move(250, 110)

        # Thiết lập ô nhập input password
        self.password_input = QLineEdit(self.login_window)
        self.password_input.setPlaceholderText("password")
        self.password_input.setStyleSheet("QLineEdit { padding-left: 20px; }")
        self.password_input.setFixedWidth(160)
        self.password_input.move(250, 150)
        self.password_input.setEchoMode(QLineEdit.Password)

        #  Thiết lập button login
        self.btn_login = QPushButton(self.login_window)
        self.btn_login.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_login.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_login.setText("Login")
        self.btn_login.clicked.connect(self.clicked_login)
        self.btn_login.move(300, 190)
        # thiết lập hover cursor
        self.btn_login.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def clicked_login(self):
        self.user_name_text = self.username_input.text()
        self.password_text = self.password_input.text()
        result = self.login_controllers.login_connect(
            self.user_name_text, self.password_text)
        if result:
            # MessageBoxInfo("Dang nhap", "Thanh cong")
            login_window.closeWindow()
            # Đăng nhập thành công, chuyển qua trang menu

            if login_info[2] == 'TRUONGPHONG':
                global truongphong
                truongphong.Load_Data()
                truongphong.showWindow()
            elif login_info[2] == 'QLTRUCTIEP':
                global qltructiep
                qltructiep.Load_Data()
                qltructiep.showWindow()
                print("Comming soon")
            elif login_info[2] == 'TAICHINH':
                global taichinh_windown
                taichinh_windown.Load_Data()
                taichinh_windown.showWindow()
            elif login_info[2] == 'NHANSU':
                global nhansu
                nhansu.Load_Data()
                nhansu.showWindow()
            elif login_info[2] == 'TRUONGDEAN':
                global dean_windown
                dean_windown.Load_Data()
                dean_windown.showWindow()
        else:
            MessageBoxErr("Dang nhap", "That Bai")

    def closeWindow(self):
        self.login_window.hide()

    def showWindow(self):
        self.login_window.show()


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
            ['MANV', 'TENNV', 'PHAI', 'NGAYSINH', 'DIACHI', 'SODT', 'SODT', 'PHUCAP', 'VAITRO', 'MANQL', 'PHG', 'MADA', 'THOIGIAN'])

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


# View: Trưởng phòng

class Role_TruongPhong:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Menu')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Hiện thị Danh sách nhân viên của phòng
        self.button_user = QtWidgets.QPushButton(
            'Danh sách nhân viên của phòng', self.main_window)
        self.button_user.move(120, 120)
        self.button_user.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_user.clicked.connect(self.on_click_TruongPhong_ListStaff)

        # Hiện thị Danh sách các phân công
        self.button_role = QtWidgets.QPushButton(
            'Danh sách các phân công ', self.main_window)
        self.button_role.move(340, 120)
        self.button_role.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_role.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_role.clicked.connect(self.on_click_assignment_list)

    def on_click_TruongPhong_ListStaff(self):
        truongphong.closeWindow()
        global TruongPhong_ListStaff_window
        TruongPhong_ListStaff_window.Load_Data()
        TruongPhong_ListStaff_window.showWindow()

    def on_click_assignment_list(self):
        truongphong.closeWindow()
        global assignment_list
        assignment_list.Load_Data()
        assignment_list.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()


class AssignmentList_View:
    def Load_Data(self):
        self.controller = AssignmentList_Controller()
        self.roles = []
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách role')

        # Json data
        self.data_Roles = {"TENNV": "", "TENDA": "", "NGAYBD": "", "THOIGIAN": "",
                           "TENPB": "", "MANV": "", "MAPB": "", "MADA": ""}

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.roles = self.controller.get_assignment_list()
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(["Mã nhân viên",
                                                     "Tên nhân viên",
                                                     "Mã đề án",
                                                     "Tên đề án",
                                                     "Ngày bắt đầu",
                                                     "Thời gian",
                                                     "Mã Phòng ban", "Tên Phòng ban"])
        self.table_widget.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        # Thêm dữ liệu vào table widget
        for role in self.roles:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(role[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(role[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(role[2])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(role[3])))
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(role[4])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(role[5])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(role[7])))
            self.table_widget.setItem(
                row_position, 7, QtWidgets.QTableWidgetItem(str(role[6])))

        # Thiết lập layout cho widget
        # Tạo khung cuộn
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(450)
        self.scroll_area.setFixedHeight(400)

        # Đặt bảng trong khung cuộn
        self.scroll_area.setWidget(self.table_widget)

        # Đặt khung cuộn vào cửa sổ chính
        self.main_window.setCentralWidget(self.scroll_area)

        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # TENNV
        self.TENNV = QtWidgets.QLabel(self.main_window)
        self.TENNV.setText("TENNV: ")
        self.TENNV.setStyleSheet("font-size: 14px;")

        self.TENNV.move(480, 0)

        self.txt_TENNV = QtWidgets.QLineEdit(self.main_window)
        self.txt_TENNV.setFixedWidth(160)
        self.txt_TENNV.setText(self.data_Roles["TENNV"])
        self.txt_TENNV.move(480, 25)

        # TENDA
        self.TENDA_name = QtWidgets.QLabel(self.main_window)
        self.TENDA_name.setText("TENDA: ")
        self.TENDA_name.setStyleSheet("font-size: 14px;")

        self.TENDA_name.move(480, 50)

        self.txt_TENDA = QtWidgets.QLineEdit(self.main_window)
        self.txt_TENDA.setFixedWidth(160)
        self.txt_TENDA.setText(self.data_Roles["TENDA"])
        self.txt_TENDA.move(480, 75)

        # NGAYBD
        self.NGAYBD_name = QtWidgets.QLabel(self.main_window)
        self.NGAYBD_name.setText("NGAYBD: ")
        self.NGAYBD_name.setStyleSheet("font-size: 14px;")

        self.NGAYBD_name.move(480, 100)

        self.txt_NGAYBD = QtWidgets.QLineEdit(self.main_window)
        self.txt_NGAYBD.setFixedWidth(160)
        self.txt_NGAYBD.setText(self.data_Roles["NGAYBD"])
        self.txt_NGAYBD.move(480, 125)

        # THOIGIAN
        self.THOIGIAN_name = QtWidgets.QLabel(self.main_window)
        self.THOIGIAN_name.setText("THOIGIAN: ")
        self.THOIGIAN_name.setStyleSheet("font-size: 14px;")

        self.THOIGIAN_name.move(480, 150)

        self.txt_THOIGIAN = QtWidgets.QLineEdit(self.main_window)
        self.txt_THOIGIAN.setFixedWidth(160)
        self.txt_THOIGIAN.setText(self.data_Roles["THOIGIAN"])
        self.txt_THOIGIAN.move(480, 175)

        # TENPB
        self.TENPB_name = QtWidgets.QLabel(self.main_window)
        self.TENPB_name.setText("TENPB: ")
        self.TENPB_name.setStyleSheet("font-size: 14px;")

        self.TENPB_name.move(480, 200)

        self.txt_TENPB = QtWidgets.QLineEdit(self.main_window)
        self.txt_TENPB.setFixedWidth(160)
        self.txt_TENPB.setText(
            self.data_Roles["TENPB"])
        self.txt_TENPB.move(480, 225)

        # Thêm phân công
        self.btn_add = QtWidgets.QPushButton(self.main_window)
        self.btn_add.setText("Thêm phân công")
        self.btn_add.setMinimumWidth(80)
        self.btn_add.move(30, 410)
        self.btn_add.clicked.connect(self.Add_Assignment)

        # Thêm nhân viên
        self.btn_recall = QtWidgets.QPushButton(self.main_window)
        self.btn_recall.setText("Thêm nhân viên")
        self.btn_recall.setMinimumWidth(80)
        self.btn_recall.move(160, 410)
        self.btn_recall.clicked.connect(self.Add_Staff)

        # Xoá phân công (Nhân viên)
        self.btn_recall = QtWidgets.QPushButton(self.main_window)
        self.btn_recall.setText("Xoá phân công (Nhân viên)")
        self.btn_recall.setMinimumWidth(150)
        self.btn_recall.move(320, 410)
        self.btn_recall.clicked.connect(self.Delete_Staff)

        # Xoá phân công (Đề án)
        self.btn_delete = QtWidgets.QPushButton(self.main_window)
        self.btn_delete.setText("Xoá phân công (Đề án)")
        self.btn_delete.setMinimumWidth(150)
        self.btn_delete.move(500, 410)
        self.btn_delete.clicked.connect(self.Delete_Assignment)

        # Thiết lập p hiện thị
        self.update_date = QtWidgets.QLabel(self.main_window)
        self.update_date.setText("Nhập ngày muốn sửa : ")
        self.update_date.setStyleSheet("font-size: 14px;")
        self.update_date.adjustSize()
        self.update_date.move(45, 470)

        # Thiết lập ô nhập input
        self.update_bar = QtWidgets.QLineEdit(self.main_window)
        self.update_bar.setPlaceholderText("Nhập...")
        self.update_bar.setStyleSheet("QLineEdit { padding-left: 16px; }")
        self.update_bar.setFixedWidth(160)
        self.update_bar.setFixedHeight(30)
        self.update_bar.move(200, 465)

        # Thiết lập button update
        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_update.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_update.setText("Sửa")
        self.btn_update.clicked.connect(self.clicked_update)
        self.btn_update.move(360, 465)

        # thiết lập hover cursor
        self.btn_update.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Thiết lập button back
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("BACK")
        self.btn_back.move(610, 470)
        # self.btn_back.setCursor(Qt.PointingHandCursor)

        self.btn_back.clicked.connect(self.Backmenu)

    def Backmenu(self):
        global assignment_list
        global truongphong
        assignment_list.closeWindow()
        truongphong.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def clicked_update(self):
        if self.update_bar.text() == '':
            MessageBoxErr("Lỗi", "Vui lòng nhập dữ liệu")
        else:
            result = self.controller.Update_Assignment(
                int(self.update_bar.text()), self.data_Roles["MANV"], self.data_Roles["MADA"])
            self.update_list()
            return result

    def on_selectionChanged(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))

            self.data_Roles = {"MANV": self.roles[index][0],
                               "TENNV": self.roles[index][1],
                               "MADA": self.roles[index][2],
                               "TENDA": self.roles[index][3],
                               "NGAYBD": self.roles[index][4],
                               "THOIGIAN": self.roles[index][5],
                               "TENPB": self.roles[index][6],
                               "MAPB": self.roles[index][7]}

            self.txt_TENNV.setText(self.data_Roles["TENNV"])
            self.txt_TENDA.setText(self.data_Roles["TENDA"])

            datetimeStr = self.data_Roles["NGAYBD"]
            date_time = datetimeStr.strftime("%d/%m/%Y")
            self.txt_NGAYBD.setText(date_time)

            stringText = self.data_Roles["THOIGIAN"]
            self.txt_THOIGIAN.setText(str(stringText))

            self.txt_TENPB.setText(self.data_Roles["TENPB"])

    def update_list(self):

        self.user_list = self.controller.get_assignment_list()
        if self.table_widget != "":
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.user_list))
            for row, role in enumerate(self.user_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(role[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(role[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(role[2])))
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(role[3])))
                self.table_widget.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(str(role[4])))
                self.table_widget.setItem(
                    row, 5, QtWidgets.QTableWidgetItem(str(role[5])))
                self.table_widget.setItem(
                    row, 6, QtWidgets.QTableWidgetItem(str(role[7])))
                self.table_widget.setItem(
                    row, 7, QtWidgets.QTableWidgetItem(str(role[6])))

    def Add_Assignment(self):
        self.main_window1 = QtWidgets.QMainWindow()

        self.main_window1.setWindowTitle('Thêm phân công')

        ######################

        # Json data
        self.data_Roles1 = {"MaNV": "", "TenNV": "", "MaDA": "", "TenDA": ""}

        self.table_widget1 = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget1.setColumnCount(4)
        self.table_widget1.setHorizontalHeaderLabels(
            ["Mã nhân viên", "Tên nhân viên", "Mã đề án", "Tên đề án"])
        self.table_widget1.selectionModel().selectionChanged.connect(
            self.Change_Add_Assignment)

        self.roles1 = self.controller.get_staff_ass()

        for role in self.roles1:
            row_position = self.table_widget1.rowCount()
            self.table_widget1.insertRow(row_position)
            self.table_widget1.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(role[0])))
            self.table_widget1.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(role[1])))
            self.table_widget1.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(role[2])))
            self.table_widget1.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(role[3])))

        # Thiết lập layout cho widget
        # Tạo khung cuộn
        self.scroll_area1 = QtWidgets.QScrollArea()
        self.scroll_area1.setWidgetResizable(True)
        self.scroll_area1.setFixedWidth(600)
        self.scroll_area1.setFixedHeight(300)

        # Đặt bảng trong khung cuộn
        self.scroll_area1.setWidget(self.table_widget1)

        self.main_window1.setCentralWidget(self.scroll_area1)

        # Thiết lập kích thước cho widget
        self.main_window1.resize(640, 480)

        # Info current: Nhân viên
        self.cur_staff = QtWidgets.QLabel(self.main_window1)
        self.cur_staff.setText("Đang chọn nhân viên : ")
        self.cur_staff.setStyleSheet("font-size: 14px;")
        self.cur_staff.adjustSize()
        self.cur_staff.move(45, 405)

        # Thiết lập ô nhập input
        self.cur_staff_bar = QtWidgets.QLineEdit(self.main_window1)
        self.cur_staff_bar.setStyleSheet("QLineEdit { padding-left: 16px; }")
        self.cur_staff_bar.setText("")
        self.cur_staff_bar.setFixedWidth(160)
        self.cur_staff_bar.setFixedHeight(30)
        self.cur_staff_bar.move(100, 430)

        # Info current: đề án
        self.cur_ass = QtWidgets.QLabel(self.main_window1)
        self.cur_ass.setText("Đang chọn đề án : ")
        self.cur_ass.setStyleSheet("font-size: 14px;")
        self.cur_ass.adjustSize()
        self.cur_ass.move(380, 405)

        # Thiết lập ô nhập input
        self.cur_ass_bar = QtWidgets.QLineEdit(self.main_window1)
        self.cur_ass_bar.setStyleSheet("QLineEdit { padding-left: 16px; }")
        self.cur_ass_bar.setText("")
        self.cur_ass_bar.setFixedWidth(160)
        self.cur_ass_bar.setFixedHeight(30)
        self.cur_ass_bar.move(435, 430)

        # Buton: Thu hồi
        self.btn_recall1 = QtWidgets.QPushButton(self.main_window1)
        self.btn_recall1.setText("Thêm")
        self.btn_recall1.setMinimumWidth(100)
        self.btn_recall1.move(250, 360)
        self.btn_recall1.clicked.connect(self.Handle_Add_Assignment)

        self.main_window1.show()

    def Add_Staff(self):
        if self.data_Roles["MANV"] == '':
            MessageBoxErr("Lỗi", "Vui lòng đề án")
        else:
            self.main_window2 = QtWidgets.QMainWindow()

            self.main_window2.setWindowTitle('Phân công nhân viên vào đề án')

            # Json data
            self.data_Roles2 = {"MANV": "",
                                "TENNV": ""}

            self.table_widget2 = QtWidgets.QTableWidget()
            # Đặt số lượng cột cho table widget
            self.table_widget2.setColumnCount(2)
            self.table_widget2.setHorizontalHeaderLabels(["Mã nhân viên",
                                                          "Tên nhân viên"])
            self.table_widget2.selectionModel().selectionChanged.connect(
                self.Change_Add_Staff)

            self.roles2 = self.controller.get_staff_list()

            if self.roles2 == []:
                MessageBoxWarn("Cảnh báo", "Role không có quyền trên hệ thống")
                return

            for role in self.roles2:
                row_position = self.table_widget2.rowCount()
                self.table_widget2.insertRow(row_position)
                self.table_widget2.setItem(
                    row_position, 0, QtWidgets.QTableWidgetItem(str(role[0])))
                self.table_widget2.setItem(
                    row_position, 1, QtWidgets.QTableWidgetItem(str(role[1])))

            # Thiết lập layout cho widget
            # Tạo khung cuộn
            self.scroll_area2 = QtWidgets.QScrollArea()
            self.scroll_area2.setWidgetResizable(True)
            self.scroll_area2.setFixedWidth(400)
            self.scroll_area2.setFixedHeight(300)

            # Đặt bảng trong khung cuộn
            self.scroll_area2.setWidget(self.table_widget2)

            # Đặt khung cuộn vào cửa sổ chính
            self.main_window2.setCentralWidget(self.scroll_area2)

            # Thiết lập kích thước cho widget
            self.main_window2.resize(640, 480)

            # Button: Thu hồi
            self.btn_recall2 = QtWidgets.QPushButton(self.main_window2)
            self.btn_recall2.setText("Thêm")
            self.btn_recall2.setMinimumWidth(100)
            self.btn_recall2.move(250, 360)
            self.btn_recall2.clicked.connect(self.Handle_Add_Staff)

            self.main_window2.show()

    def Change_Add_Assignment(self, selected, deselected):
        index = -1
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Roles1 = {"MaNV": self.roles1[index][0],
                                "TenNV": self.roles1[index][1],
                                "MaDA": self.roles1[index][2],
                                "TenDA": self.roles1[index][3]}

        self.cur_ass_bar.setText(
            '{0} - {1}'.format(self.data_Roles1["MaDA"], self.data_Roles1["TenDA"]))
        self.cur_staff_bar.setText(
            '{0} - {1}'.format(self.data_Roles1["MaNV"], self.data_Roles1["TenNV"]))

    def Change_Add_Staff(self, selected, deselected):
        index = -1
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Roles2 = {"MANV": self.roles2[index][0],
                                "TENNV": self.roles2[index][1]}

    def Handle_Add_Assignment(self):
        if self.data_Roles1["MaNV"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn role, bảng, hoặc quyền")
        else:
            result = self.controller.InsertStaff(
                self.data_Roles1["MaNV"], self.data_Roles1["MaDA"])
            self.main_window1.close()
            return result

    def Handle_Add_Staff(self):
        if self.data_Roles2["MANV"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn nhân viên")
            return
        else:
            result = self.controller.InsertStaff(
                self.data_Roles2["MANV"], self.data_Roles["MADA"])
            self.main_window2.close()
            return result

    def Delete_Staff(self):
        if self.data_Roles["MANV"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn nhân viên")
        else:
            result = self.controller.Delete_Staff(
                self.data_Roles["MANV"], self.data_Roles["MADA"])
            self.update_list()
            return result

    def Delete_Assignment(self):
        if self.data_Roles["MANV"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn phân công")
        else:
            result = self.controller.Delete_Assignment(self.data_Roles["MADA"])
            self.update_list()
            return result


class TruongPhong_ListStaff_View:
    def Load_Data(self):
        self.controller = TruongPhong_ListStaff_Controller()
        self.roles = []
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách nhân viên phòng ban')

        # Json data
        self.data_Roles = {"MANV": "",
                           "TENNV": "",
                           "NGAYSINH": "",
                           "DIACHI": "",
                           "VAI TRO": "",
                           "MANQL": ""}

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.roles = self.controller.get_staff_list("")
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(["Mã nhân viên",
                                                     "Tên nhân viên",
                                                     "Giới tính",
                                                     "Ngày sinh",
                                                     "Địa chỉ",
                                                     "Số điện thoại",
                                                     "Vai trò", "Phòng ban trực thuộc"])
        self.table_widget.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        # Thêm dữ liệu vào table widget
        for role in self.roles:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(role[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(role[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(role[2])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(role[3])))
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(role[4])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(role[5])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(role[6])))
            self.table_widget.setItem(
                row_position, 7, QtWidgets.QTableWidgetItem(str(role[7])))

        # Thiết lập layout cho widget
        # Tạo khung cuộn
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(450)
        self.scroll_area.setFixedHeight(400)

        # Đặt bảng trong khung cuộn
        self.scroll_area.setWidget(self.table_widget)

        # Đặt khung cuộn vào cửa sổ chính
        self.main_window.setCentralWidget(self.scroll_area)

        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Mã nhân viên
        self.staffID = QtWidgets.QLabel(self.main_window)
        self.staffID.setText("Mã nhân viên: ")
        self.staffID.setStyleSheet("font-size: 14px;")

        self.staffID.move(480, 0)

        self.txt_staffID = QtWidgets.QLineEdit(self.main_window)
        self.txt_staffID.setFixedWidth(160)
        self.txt_staffID.setText(self.data_Roles["MANV"])
        self.txt_staffID.move(480, 25)

        # Tên nhân viên
        self.Staff_name = QtWidgets.QLabel(self.main_window)
        self.Staff_name.setText("Tên nhân viên: ")
        self.Staff_name.setStyleSheet("font-size: 14px;")

        self.Staff_name.move(480, 50)

        self.txt_Staff = QtWidgets.QLineEdit(self.main_window)
        self.txt_Staff.setFixedWidth(160)
        self.txt_Staff.setText(self.data_Roles["TENNV"])
        self.txt_Staff.move(480, 75)

        # Ngày sinh
        self.DateBirth = QtWidgets.QLabel(self.main_window)
        self.DateBirth.setText("Ngày sinh: ")
        self.DateBirth.setStyleSheet("font-size: 14px;")

        self.DateBirth.move(480, 100)

        self.txt_DateBirth = QtWidgets.QLineEdit(self.main_window)
        self.txt_DateBirth.setFixedWidth(160)
        self.txt_DateBirth.setText(self.data_Roles["NGAYSINH"])
        self.txt_DateBirth.move(480, 125)

        # Địa chỉ
        self.Address = QtWidgets.QLabel(self.main_window)
        self.Address.setText("Địa chỉ: ")
        self.Address.setStyleSheet("font-size: 14px;")

        self.Address.move(480, 150)

        self.txt_Address = QtWidgets.QLineEdit(self.main_window)
        self.txt_Address.setFixedWidth(160)
        self.txt_Address.setText(self.data_Roles["DIACHI"])
        self.txt_Address.move(480, 175)

        # Vai trò
        self.Role_name = QtWidgets.QLabel(self.main_window)
        self.Role_name.setText("Vai trò: ")
        self.Role_name.setStyleSheet("font-size: 14px;")

        self.Role_name.move(480, 200)

        self.txt_Role = QtWidgets.QLineEdit(self.main_window)
        self.txt_Role.setFixedWidth(160)
        self.txt_Role.setText(
            self.data_Roles["VAI TRO"])
        self.txt_Role.move(480, 225)

        # Người quản lý
        self.Manager_name = QtWidgets.QLabel(self.main_window)
        self.Manager_name.setText("Người quản lý: ")
        self.Manager_name.setStyleSheet("font-size: 14px;")

        self.Manager_name.move(480, 250)

        self.txt_Manager = QtWidgets.QLineEdit(self.main_window)
        self.txt_Manager.setFixedWidth(160)
        self.txt_Manager.setText(self.data_Roles["MANQL"])
        self.txt_Manager.move(480, 275)

        # Thiết lập p hiện thị nhập user
        self.user_name = QtWidgets.QLabel(self.main_window)
        self.user_name.setText("Nhập mã/tên nhân viên : ")
        self.user_name.setStyleSheet("font-size: 14px;")
        self.user_name.adjustSize()
        self.user_name.move(45, 435)

        # Thiết lập ô nhập input
        self.search_bar = QtWidgets.QLineEdit(self.main_window)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet("QLineEdit { padding-left: 16px; }")
        self.search_bar.setFixedWidth(160)
        self.search_bar.setFixedHeight(30)
        self.search_bar.move(200, 430)

        # Thiết lập button search
        self.btn_search = QtWidgets.QPushButton(self.main_window)
        self.btn_search.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_search.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_search.setText("Search")
        self.btn_search.clicked.connect(self.clicked_search)
        self.btn_search.move(360, 430)

        # thiết lập hover cursor
        self.btn_search.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # thiết lập button xem tất cả
        self.btn_all = QtWidgets.QPushButton(self.main_window)
        self.btn_all.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_all.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_all.setText('All')
        # cỡ chữ cho text all trong button
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_all.setFont(font)

        self.btn_all.clicked.connect(self.clicked_btn)
        self.btn_all.move(450, 430)
        # thiết lập hover cursor
        self.btn_all.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Thiết lập button back
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("BACK")
        self.btn_back.move(610, 470)
        # self.btn_back.setCursor(Qt.PointingHandCursor)

        self.btn_back.clicked.connect(self.Backmenu)

    def Backmenu(self):
        global TruongPhong_ListStaff_window
        global truongphong
        TruongPhong_ListStaff_window.closeWindow()
        truongphong.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def clicked_search(self):
        self.search_text = self.search_bar.text()
        self.update_user_list(self.search_text)

    def clicked_btn(self):
        self.search_text = ""
        self.update_user_list(self.search_text)

    def update_user_list(self, search_text=""):
        self.user_list = self.controller.get_staff_list(search_text)
        if self.table_widget != "":
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.user_list))
            for row, role in enumerate(self.user_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(role[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(role[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(role[2])))
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(role[3])))
                self.table_widget.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(str(role[4])))
                self.table_widget.setItem(
                    row, 5, QtWidgets.QTableWidgetItem(str(role[5])))
                self.table_widget.setItem(
                    row, 6, QtWidgets.QTableWidgetItem(str(role[6])))
                self.table_widget.setItem(
                    row, 7, QtWidgets.QTableWidgetItem(str(role[7])))

    def on_selectionChanged(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Roles = {"MANV": self.roles[index][0],
                               "TENNV": self.roles[index][1],
                               "NGAYSINH": self.roles[index][3],
                               "DIACHI": self.roles[index][4],
                               "VAI TRO": self.roles[index][6],
                               "MANQL": self.roles[index][7]}
            self.txt_staffID.setText(self.data_Roles["MANV"])
            self.txt_Staff.setText(self.data_Roles["TENNV"])

            datetimeStr = self.data_Roles["NGAYSINH"]
            date_time = datetimeStr.strftime("%d/%m/%Y")
            self.txt_DateBirth.setText(date_time)

            self.txt_Address.setText(self.data_Roles["DIACHI"])
            self.txt_Role.setText(self.data_Roles["VAI TRO"])
            self.txt_Manager.setText(self.data_Roles["MANQL"])


# View: Nhân sự

class Role_Nhan_su:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Menu')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Hiện thị danh sách user
        self.button_user = QtWidgets.QPushButton(
            'PHONGBAN', self.main_window)
        self.button_user.move(120, 120)
        self.button_user.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_user.clicked.connect(self.on_click_pb)

        # Hiện thị danh sách role
        self.button_role = QtWidgets.QPushButton(
            'NHANVIEN', self.main_window)
        self.button_role.move(340, 120)
        self.button_role.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_role.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_role.clicked.connect(self.on_click_nv)

    def on_click_pb(self):
        global pb_window
        pb_window.PHONGBAN_view()
        pb_window.showWindow()

    def on_click_nv(self):
        global pb_window2
        pb_window2.NHANVIEN_view()
        pb_window2.showWindow()

    def showWindow(self):
        self.main_window.show()


class Phongbanview:
    def PHONGBAN_view(self):
        self.pb_controller = NhanSu_controller()
        self.pb_list = self.pb_controller.pb_list()
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setWindowTitle('Danh sách phòng ban')

        self.data_pbs = {"MaPB": "",
                         "TenPB": "",
                         "TruongPB": ""}

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(
            ['Mã phòng ban', 'Tên phòng ban', 'Trưởng phòng ban'])

        # self.table_widget.selectionModel().selectionChanged.connect(self.on_sel)
        for pb in self.pb_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(pb[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(pb[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(pb[2])))

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(420)
        self.scroll_area.setFixedHeight(250)
        self.scroll_area.setWidget(self.table_widget)
        self.main_window.setCentralWidget(self.scroll_area)

        self.main_window.resize(700, 520)

        # Mã phòng ban
        self.pb_idlabel = QtWidgets.QLabel(self.main_window)
        self.pb_idlabel.setText("Mã phòng ban: ")
        self.pb_idlabel.setStyleSheet("font-size: 14px;")
        self.pb_idlabel.move(440, 0)

        self.pb_id_txt = QtWidgets.QLineEdit(self.main_window)
        self.pb_id_txt.setFixedWidth(160)
        self.pb_id_txt.move(440, 25)

        # Tên phòng ban
        self.pb_nameLabel = QtWidgets.QLabel(self.main_window)
        self.pb_nameLabel.setText("Tên phòng ban: ")
        self.pb_nameLabel.setStyleSheet("font-size: 14px;")
        self.pb_nameLabel.move(440, 60)

        self.pb_name_txt = QtWidgets.QLineEdit(self.main_window)
        self.pb_name_txt.setFixedWidth(160)
        self.pb_name_txt.move(440, 85)

        # Trưởng phòng ban
        self.lpb_idLabel = QtWidgets.QLabel(self.main_window)
        self.lpb_idLabel.setText("Trưởng phòng ban: ")
        self.lpb_idLabel.setStyleSheet("font-size: 14px;")
        self.lpb_idLabel.move(440, 120)

        self.lpb_id_txt = QtWidgets.QLineEdit(self.main_window)
        self.lpb_id_txt.setFixedWidth(160)
        self.lpb_id_txt.move(440, 145)

        # add button
        self.btn_create = QtWidgets.QPushButton(self.main_window)
        self.btn_create.setText("ADD")
        self.btn_create.setMinimumWidth(30)
        self.btn_create.move(440, 180)
        self.btn_create.clicked.connect(self.Add_PB)

        # Update
        self.cb = QtWidgets.QComboBox(self.main_window)
        self.cb.move(80, 270)
        self.cb.setFixedWidth(140)
        self.cb.addItem('Tên phòng ban')
        self.cb.addItem('Trưởng phòng')

        self.update_txt = QtWidgets.QLineEdit(self.main_window)
        self.update_txt.setFixedWidth(140)
        self.update_txt.move(80, 300)

        self.upLabel = QtWidgets.QLabel(self.main_window)
        self.upLabel.setText("Mã phòng")
        self.upLabel.setStyleSheet("font-size: 14px;")
        self.upLabel.move(250, 270)

        self.uptxt = QtWidgets.QLineEdit(self.main_window)
        self.uptxt.setFixedWidth(140)
        self.uptxt.move(250, 300)

        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setText("Cập nhật")
        self.btn_update.setMinimumWidth(50)
        self.btn_update.move(180, 340)
        self.btn_update.clicked.connect(self.UpdatePB)

    def UpdatePB(self):
        self.pb_controller.update_pb(
            self.cb.currentText(), self.update_txt.text(), self.uptxt.text())
        self.update_pb_list()

    def Add_PB(self):
        self.pb_controller.add_pb(self.pb_id_txt.text(
        ), self.pb_name_txt.text(), self.lpb_id_txt.text())
        self.update_pb_list()

    def update_pb_list(self):
        self.pb_list = self.pb_controller.pb_list()
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.pb_list))
            for row, pb in enumerate(self.pb_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(pb[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(pb[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(pb[2])))

    def showWindow(self):
        self.main_window.show()


class Nhanvienview:
    def NHANVIEN_view(self):
        self.nv_controller = NhanSu_controller()
        self.nv_list = self.nv_controller.nv_list()
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setWindowTitle('Danh sách nhân viên')

        # self.data_pbs = {"MaPB": "",
        #                    "TenPB": "",
        #                    "TruongPB": ""}

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(11)
        self.table_widget.setHorizontalHeaderLabels(
            ['Mã nhân viên', 'Tên nhân viên', 'Phái', 'Ngày sinh', 'Địa chỉ', 'SĐT', 'Lương', 'Phụ cấp', 'Vai trò', 'Mã NQL', 'Trưởng phòng'])

        # self.table_widget.selectionModel().selectionChanged.connect(self.on_sel)
        for nv in self.nv_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(nv[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(nv[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(nv[2])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(nv[3])))
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(nv[4])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(nv[5])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(nv[6])))
            self.table_widget.setItem(
                row_position, 7, QtWidgets.QTableWidgetItem(str(nv[7])))
            self.table_widget.setItem(
                row_position, 8, QtWidgets.QTableWidgetItem(str(nv[8])))
            self.table_widget.setItem(
                row_position, 9, QtWidgets.QTableWidgetItem(str(nv[9])))
            self.table_widget.setItem(
                row_position, 10, QtWidgets.QTableWidgetItem(str(nv[10])))

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(800)
        self.scroll_area.setFixedHeight(400)
        self.scroll_area.setWidget(self.table_widget)
        self.main_window.setCentralWidget(self.scroll_area)

        self.main_window.resize(1080, 720)

        # Mã nhân viên
        self.nv_idlabel = QtWidgets.QLabel(self.main_window)
        self.nv_idlabel.setText("Mã nhân viên: ")
        self.nv_idlabel.setStyleSheet("font-size: 14px;")
        self.nv_idlabel.move(890, 0)

        self.nv_id_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_id_txt.setFixedWidth(160)
        self.nv_id_txt.move(890, 25)

        # Tên nhân viên
        self.nv_nameLabel = QtWidgets.QLabel(self.main_window)
        self.nv_nameLabel.setText("Tên nhân viên: ")
        self.nv_nameLabel.setStyleSheet("font-size: 14px;")
        self.nv_nameLabel.move(890, 60)

        self.nv_name_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_name_txt.setFixedWidth(160)
        self.nv_name_txt.move(890, 85)

        # Giới tính
        self.nv_sexLabel = QtWidgets.QLabel(self.main_window)
        self.nv_sexLabel.setText("Giới tính: ")
        self.nv_sexLabel.setStyleSheet("font-size: 14px;")
        self.nv_sexLabel.move(890, 120)

        self.nv_sex_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_sex_txt.setFixedWidth(160)
        self.nv_sex_txt.move(890, 145)

        # Ngày sinh
        self.nv_birthLabel = QtWidgets.QLabel(self.main_window)
        self.nv_birthLabel.setText("Ngày sinh: ")
        self.nv_birthLabel.setStyleSheet("font-size: 14px;")
        self.nv_birthLabel.move(890, 180)

        self.nv_birth_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_birth_txt.setFixedWidth(160)
        self.nv_birth_txt.move(890, 205)

        # Địa chỉ
        self.nv_addressLabel = QtWidgets.QLabel(self.main_window)
        self.nv_addressLabel.setText("Địa chỉ: ")
        self.nv_addressLabel.setStyleSheet("font-size: 14px;")
        self.nv_addressLabel.move(890, 240)

        self.nv_address_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_address_txt.setFixedWidth(160)
        self.nv_address_txt.move(890, 265)

        # Số điện thoại
        self.nv_phoneLabel = QtWidgets.QLabel(self.main_window)
        self.nv_phoneLabel.setText("Số điện thoại: ")
        self.nv_phoneLabel.setStyleSheet("font-size: 14px;")
        self.nv_phoneLabel.move(890, 300)

        self.nv_phone_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_phone_txt.setFixedWidth(160)
        self.nv_phone_txt.move(890, 325)

        # Vai trò
        self.nv_roleLabel = QtWidgets.QLabel(self.main_window)
        self.nv_roleLabel.setText("Vai trò: ")
        self.nv_roleLabel.setStyleSheet("font-size: 14px;")
        self.nv_roleLabel.move(890, 360)

        self.nv_role_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_role_txt.setFixedWidth(160)
        self.nv_role_txt.move(890, 385)

        # Quản lý
        self.nv_mgrLabel = QtWidgets.QLabel(self.main_window)
        self.nv_mgrLabel.setText("Quản lý: ")
        self.nv_mgrLabel.setStyleSheet("font-size: 14px;")
        self.nv_mgrLabel.move(890, 420)

        self.nv_mgr_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_mgr_txt.setFixedWidth(160)
        self.nv_mgr_txt.move(890, 445)

        # Trưởng phòng
        self.nv_lpbLabel = QtWidgets.QLabel(self.main_window)
        self.nv_lpbLabel.setText("Trưởng phòng: ")
        self.nv_lpbLabel.setStyleSheet("font-size: 14px;")
        self.nv_lpbLabel.move(890, 480)

        self.nv_lpb_txt = QtWidgets.QLineEdit(self.main_window)
        self.nv_lpb_txt.setFixedWidth(160)
        self.nv_lpb_txt.move(890, 505)

        # add button
        self.btn_create = QtWidgets.QPushButton(self.main_window)
        self.btn_create.setText("ADD")
        self.btn_create.setMinimumWidth(30)
        self.btn_create.move(890, 505+35)
        self.btn_create.clicked.connect(self.Add_NV)

        # Update
        self.up1 = QtWidgets.QLabel(self.main_window)
        self.up1.setText("SET: ")
        self.up1.setStyleSheet("font-size: 14px;")
        self.up1.move(45, 430)

        self.cb = QtWidgets.QComboBox(self.main_window)
        self.cb.move(80, 430)
        self.cb.setFixedWidth(140)
        self.cb.addItem('Tên nhân viên')
        self.cb.addItem('Giới tính')
        self.cb.addItem('Ngày sinh')
        self.cb.addItem('Địa chỉ')
        self.cb.addItem('Số điện thoại')
        self.cb.addItem('Vai trò')
        self.cb.addItem('Quản lý')
        self.cb.addItem('Trưởng phòng')

        self.update_txt = QtWidgets.QLineEdit(self.main_window)
        self.update_txt.setFixedWidth(140)
        self.update_txt.move(80, 460)

        self.up2 = QtWidgets.QLabel(self.main_window)
        self.up2.setText("WHERE: ")
        self.up2.setStyleSheet("font-size: 14px;")
        self.up2.move(240, 430)

        self.cb1 = QtWidgets.QComboBox(self.main_window)
        self.cb1.move(300, 430)
        self.cb1.setFixedWidth(140)
        self.cb1.addItem('Mã nhân viên')
        self.cb1.addItem('Tên nhân viên')
        self.cb1.addItem('Vai trò')
        self.cb1.addItem('Quản lý')
        self.cb1.addItem('Trưởng phòng')

        self.uptxt = QtWidgets.QLineEdit(self.main_window)
        self.uptxt.setFixedWidth(140)
        self.uptxt.move(300, 460)

        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setText("Cập nhật")
        self.btn_update.setMinimumWidth(50)
        self.btn_update.move(195, 500)
        self.btn_update.clicked.connect(self.UpdateNV)

    def Add_NV(self):
        self.nv_controller.add_nv(self.nv_id_txt.text(), self.nv_name_txt.text(), self.nv_sex_txt.text(), self.nv_birth_txt.text(
        ), self.nv_address_txt.text(), self.nv_phone_txt.text(), self.nv_role_txt.text(), self.nv_mgr_txt.text(), self.nv_lpb_txt.text())
        self.update_nv_list()

    def UpdateNV(self):
        self.nv_controller.update_nv(self.cb.currentText(
        ), self.update_txt.text(), self.cb1.currentText(), self.uptxt.text())
        self.update_nv_list()

    def update_nv_list(self):
        self.nv_list = self.nv_controller.nv_list()
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.nv_list))
            for row_position, nv in enumerate(self.nv_list):
                self.table_widget.setItem(
                    row_position, 0, QtWidgets.QTableWidgetItem(str(nv[0])))
                self.table_widget.setItem(
                    row_position, 1, QtWidgets.QTableWidgetItem(str(nv[1])))
                self.table_widget.setItem(
                    row_position, 2, QtWidgets.QTableWidgetItem(str(nv[2])))
                self.table_widget.setItem(
                    row_position, 3, QtWidgets.QTableWidgetItem(str(nv[3])))
                self.table_widget.setItem(
                    row_position, 4, QtWidgets.QTableWidgetItem(str(nv[4])))
                self.table_widget.setItem(
                    row_position, 5, QtWidgets.QTableWidgetItem(str(nv[5])))
                self.table_widget.setItem(
                    row_position, 6, QtWidgets.QTableWidgetItem(str(nv[6])))
                self.table_widget.setItem(
                    row_position, 7, QtWidgets.QTableWidgetItem(str(nv[7])))
                self.table_widget.setItem(
                    row_position, 8, QtWidgets.QTableWidgetItem(str(nv[8])))
                self.table_widget.setItem(
                    row_position, 9, QtWidgets.QTableWidgetItem(str(nv[9])))
                self.table_widget.setItem(
                    row_position, 10, QtWidgets.QTableWidgetItem(str(nv[10])))

    def showWindow(self):
        self.main_window.show()

# View: Nhân viên


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
        self.button_staff.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_staff.clicked.connect(self.clicked_information)

        # Đăng xuất
        self.button_assign = QtWidgets.QPushButton(
            'Đăng Xuất', self.main_window)
        self.button_assign.move(380, 180)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor
        self.button_assign.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def clicked_information(self):
        Nhanvien_windown.closeWindow()
        global window_tab1
        window_tab1.Load_Data()
        window_tab1.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

# View: Tài chính


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
        self.button_staff.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_staff.clicked.connect(self.clicked_staff)

        # Hiện thị danh sách thông tin phân công
        self.button_assign = QtWidgets.QPushButton(
            'Thông tin phân công', self.main_window)
        self.button_assign.move(380, 140)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor
        self.button_assign.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_assign.clicked.connect(self.clicked_assign)

        # Đăng xuất
        self.button_assign = QtWidgets.QPushButton(
            'Đăng Xuất', self.main_window)
        self.button_assign.move(120, 260)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor
        self.button_assign.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
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
            ['MANV', 'TENNV', 'PHAI', 'NGAYSINH', 'DIACHI', 'SODT', 'SODT', 'PHUCAP', 'VAITRO', 'MANQL', 'PHG'])
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
        self.textbox1.setGeometry(QtCore.QRect(500, 40, 100, 30))

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
        self.btn_update.move(490, 300)

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
            ['MANV', 'MADA', 'THOIGIAN'])
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

# View: Đề án


class DeAn_view:
    def Load_Data(self):

        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Menu')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Hiện thị danh sách thông tin đề án
        self.button_staff = QtWidgets.QPushButton(
            'Thông tin Đề án', self.main_window)
        self.button_staff.move(120, 180)
        self.button_staff.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_staff.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_staff.clicked.connect(self.clicked_scheme)

        # Đăng xuất
        self.button_assign = QtWidgets.QPushButton(
            'Đăng Xuất', self.main_window)
        self.button_assign.move(380, 180)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor
        self.button_assign.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def clicked_scheme(self):
        dean_windown.closeWindow()
        global window_danhsachdean
        window_danhsachdean.Load_Data()
        window_danhsachdean.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()


class DanhSachDeAn_view:
    def Load_Data(self):
        self.datalist = DeAn_controller()
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách đề án')

        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)
        self.itemlist = self.datalist.get_DeAn_list()

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()

        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(
            ['MADA', 'TENDA', 'NGAYBD', 'PHONG'])

        for item in self.itemlist:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(item[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(item[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(item[2])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(item[3])))

        # Tạo khung cuộn
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(390)
        scroll_area.setFixedHeight(400)

        # Đặt bảng trong khung cuộn
        scroll_area.setWidget(self.table_widget)
        # # Thêm tab_widget vào QMainWindow
        self.main_window.setCentralWidget(scroll_area)

        # Thiết lập textbox PK
        self.textbox1 = QtWidgets.QTextEdit(self.main_window)
        self.textbox1.setReadOnly(True)  # Thiết lập ô textbox chỉ đọc
        self.textbox2 = QtWidgets.QTextEdit(self.main_window)
        self.textbox2.setReadOnly(True)  # Thiết lập ô textbox chỉ đọc

        # Thiết lập kích thước và vị trí cho ô textbox thứ nhất
        self.textbox1.setGeometry(QtCore.QRect(510, 40, 100, 30))

        # Thiết lập p hiện thị MADA
        self.text_MADA = QtWidgets.QLabel(self.main_window)
        self.text_MADA.setText("MADA : ")
        self.text_MADA.setStyleSheet("font-size: 15px;")
        self.text_MADA.adjustSize()
        self.text_MADA.move(430, 40)

        # Thiết lập kích thước và vị trí cho ô textbox thứ hai
        self.textbox2.setGeometry(QtCore.QRect(510, 100, 100, 30))

        # Thiết lập p hiện thị TENDA
        self.text_MADA = QtWidgets.QLabel(self.main_window)
        self.text_MADA.setText("TENDA : ")
        self.text_MADA.setStyleSheet("font-size: 15px;")
        self.text_MADA.adjustSize()
        self.text_MADA.move(430, 100)

        # Thiết lập button thêm đề án
        self.btn_add = QtWidgets.QPushButton(self.main_window)
        self.btn_add.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_add.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_add.setText("THÊM")
        self.btn_add.move(500, 180)
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.clicked.connect(self.click_add)

        # Thiết lập button xóa đề án
        self.btn_delete = QtWidgets.QPushButton(self.main_window)
        self.btn_delete.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_delete.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_delete.setText("XÓA")
        self.btn_delete.move(500, 240)
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        # self.btn_back.clicked.connect(self.Backmenu)

        # Thiết lập button sửa đề án
        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_update.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_update.setText("CHỈNH SỬA")
        self.btn_update.move(500, 300)
        self.btn_update.setCursor(Qt.PointingHandCursor)
        self.btn_update.clicked.connect(self.click_update)

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

    def click_add(self):
        global window_dean_add

        window_dean_add.Load_Data()
        window_dean_add.showWindow()

    def click_update(self):
        global window_dean_update

        window_dean_update.Load_Data()
        window_dean_update.showWindow()

    def Backmenu(self):

        window_danhsachdean.closeWindow()
        global dean_windown

        dean_windown.Load_Data()
        dean_windown.showWindow()


class add_dean:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Thêm đề án')
        # Thiết lập kích thước cho widget
        self.main_window.resize(600, 420)

        # Thiết lập p hiện thị Tên đề án
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Tên Đề Án: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 50)

        # Thiết lập p hiện thị Ngày bắt đầu
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Ngày BD : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 120)

        # Thiết lập p hiện thị Phòng
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Phòng : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 200)

        # Thiết lập button add
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("Thêm")
        self.btn_back.move(300, 270)
        self.btn_back.setCursor(Qt.PointingHandCursor)

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()


class update_dean:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Thêm đề án')
        # Thiết lập kích thước cho widget
        self.main_window.resize(600, 420)

        # Thiết lập p hiện thị Mã đề án
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Mã đề án: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 40)

        # Thiết lập p hiện thị Tên đề án
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Tên Đề Án: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 100)

        # Thiết lập p hiện thị Ngày bắt đầu
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Ngày BD : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 160)

        # Thiết lập p hiện thị Phòng
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Phòng : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 220)

        # Thiết lập button update
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(80, 35)  # đặt kích thước là 80 X 35 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("Chỉnh sửa")
        self.btn_back.move(300, 270)
        self.btn_back.setCursor(Qt.PointingHandCursor)

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

# View: Quản lý trực tiếp
class Role_QLTructiep:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Menu')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Hiện thị danh sách user
        self.button_user = QtWidgets.QPushButton(
            'PHANCONG', self.main_window)
        self.button_user.move(120, 120)
        self.button_user.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_user.clicked.connect(self.on_click_pc)

        # Hiện thị danh sách role
        self.button_role = QtWidgets.QPushButton(
            'NHANVIEN', self.main_window)
        self.button_role.move(340, 120)
        self.button_role.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_role.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_role.clicked.connect(self.on_click_nv)

    def on_click_pc(self):
        global pc_window
        pc_window.PHANCONG_view()
        pc_window.showWindow()

    def on_click_nv(self):
        global pc_window2
        pc_window2.NHANVIEN_view()
        pc_window2.showWindow()

    def showWindow(self):
        self.main_window.show()


class QL_Phancongview:
    def PHANCONG_view(self):
        self.pc_controller = QLTructiep_controller()
        self.pc_list = self.pc_controller.pc_list()
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setWindowTitle('Danh sách phân công')

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(
            ['Mã nhân viên', 'Mã đề án', 'Thời gian'])

        # self.table_widget.selectionModel().selectionChanged.connect(self.on_sel)
        for pc in self.pc_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(pc[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(pc[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(pc[2])))

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(420)
        self.scroll_area.setFixedHeight(250)
        self.scroll_area.setWidget(self.table_widget)
        self.main_window.setCentralWidget(self.scroll_area)

        self.main_window.resize(700, 520)

    def showWindow(self):
        self.main_window.show()


class QL_Nhanvienview:
    def NHANVIEN_view(self):
        self.nv_controller = QLTructiep_controller()
        self.nv_list = self.nv_controller.nv_list()
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setWindowTitle('Danh sách nhân viên')


        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(11)
        self.table_widget.setHorizontalHeaderLabels(
            ['Mã nhân viên', 'Tên nhân viên', 'Phái', 'Ngày sinh', 'Địa chỉ', 'SĐT', 'Lương', 'Phụ cấp', 'Vai trò', 'Mã NQL', 'Trưởng phòng'])

        # self.table_widget.selectionModel().selectionChanged.connect(self.on_sel)
        for nv in self.nv_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(nv[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(nv[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(nv[2])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(nv[3])))
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(nv[4])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(nv[5])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(nv[6])))
            self.table_widget.setItem(
                row_position, 7, QtWidgets.QTableWidgetItem(str(nv[7])))
            self.table_widget.setItem(
                row_position, 8, QtWidgets.QTableWidgetItem(str(nv[8])))
            self.table_widget.setItem(
                row_position, 9, QtWidgets.QTableWidgetItem(str(nv[9])))
            self.table_widget.setItem(
                row_position, 10, QtWidgets.QTableWidgetItem(str(nv[10])))

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(800)
        self.scroll_area.setFixedHeight(400)
        self.scroll_area.setWidget(self.table_widget)
        self.main_window.setCentralWidget(self.scroll_area)

        self.main_window.resize(1080, 720)

    def showWindow(self):
        self.main_window.show()

#################################################################


# Variable
login_window = LoginWindow()

# Trưởng phỏng
truongphong = Role_TruongPhong()
assignment_list = AssignmentList_View()
TruongPhong_ListStaff_window = TruongPhong_ListStaff_View()

# Nhân sự
nhansu = Role_Nhan_su()
pb_window = Phongbanview()
pb_window2 = Nhanvienview()

# Nhân viên
Nhanvien_windown = NhanVien_view()
window_ThongTinCaNhan = ThongTinCaNhan()

# Đề án
dean_windown = DeAn_view()
window_danhsachdean = DanhSachDeAn_view()
window_dean_add = add_dean()
window_dean_update = update_dean()

# Tài chính
taichinh_windown = Taichinh_view()
window_taichinh_ThongTinNhanVien = TaiChinh_ThongTinNhanVien()
window_TaiChinh_DanhSachPhanCong = TaiChinh_DanhSachPhanCong()

# Quản lý trực tiếp
qltructiep = Role_QLTructiep()
pc_window = QL_Phancongview()
pc_window2 = QL_Nhanvienview()
login_info = []


#################################################################


def main():
    lib_dir = r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9"
    lib_dir = "C:\oclient\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9"
    global oracle_client_initialized
    oracle_client_initialized = False
    if not oracle_client_initialized:
        try:
            cx_Oracle.init_oracle_client(lib_dir=lib_dir)
            oracle_client_initialized = True
        except Exception as err:
            print("Error initializing Oracle Client:", err)
            sys.exit(1)
    app = QtWidgets.QApplication(sys.argv)
    global login_window
    login_window.Load_Data()
    login_window.showWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
