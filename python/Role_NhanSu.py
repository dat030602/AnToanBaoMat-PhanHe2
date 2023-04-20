import sys
import cx_Oracle
from PyQt5 import QtCore, QtWidgets
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
import messagebox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox
# Controller


class LoginController:
    def Load_Data(self):
        self.username_text = None
        self.password_text = None

    def login_connect(self, username_text, password_text):
        self.username_text = username_text
        self.password_text = password_text

        result = connection2(username_text, password_text)
        if result:
            global login_info
            login_info = [username_text, password_text]
        print(login_info)
        return result

    def get_username_and_password(self):
        return login_info[0], login_info[1]


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


# Function


def MessageBoxInfo(title, message):
    messagebox.showinfo(title, message)


def MessageBoxErr(title, message):
    messagebox.showerror(title, message)


def MessageBoxWarn(title, message):
    messagebox.showwarning(title, message)

# Database connection


def execute_query(username, password, queryString):
    print(queryString)
    try:
        con = cx_Oracle.connect(username, password, 'localhost:1521/ORCLPDB')

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
        con = cx_Oracle.connect(username, password, 'localhost:1521/ORCLPDB')
        return con

    except cx_Oracle.DatabaseError as er:
        print('There is an error in the Oracle database:', er)
        return False

    except Exception as er:
        print('Error:'+str(er))
        return False

# Views


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
            MessageBoxInfo("Dang nhap", "Thanh cong")
            login_window.closeWindow()
            # Đăng nhập thành công, chuyển qua trang menu
            global window_navigation
            # window_navigation.Load_Data()
            # window_navigation.showWindow()
            nhansu.Load_Data()
            nhansu.showWindow()
        else:
            MessageBoxErr("Dang nhap", "That Bai")

    def closeWindow(self):
        self.login_window.hide()

    def showWindow(self):
        self.login_window.show()


class MainWindow:
    def Load_Data(self):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Menu')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Hiện thị danh sách user
        self.button_user = QtWidgets.QPushButton(
            'Danh sách user', self.main_window)
        self.button_user.move(120, 120)
        self.button_user.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_user.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_user.clicked.connect(self.on_click_user)

        # Hiện thị danh sách role
        self.button_role = QtWidgets.QPushButton(
            'Danh sách role', self.main_window)
        self.button_role.move(340, 120)
        self.button_role.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_role.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_role.clicked.connect(self.on_click_role)

        # Hiện thị danh sách quyền của role/user
        self.button_pri = QtWidgets.QPushButton(
            'Danh sách quyền User/Role', self.main_window)
        self.button_pri.move(120, 220)
        self.button_pri.setFixedSize(180, 60)  # Thiết lập kích thước cố định

        # thiết lập hover cursor
        self.button_pri.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_pri.clicked.connect(self.on_click_privileges)

        # Hiện thị danh sách quyền của role/user
        self.button_table = QtWidgets.QPushButton(
            'Danh sách table', self.main_window)
        self.button_table.move(340, 220)
        self.button_table.setFixedSize(180, 60)  # Thiết lập kích thước cố định

        # Hiện thị danh sách quyền của role/user
        self.button_pri1 = QtWidgets.QPushButton(
            'Danh sách quyền', self.main_window)
        self.button_pri1.move(120, 320)
        self.button_pri1.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_pri1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_pri1.clicked.connect(self.on_click_pri)

        # thiết lập hover cursor
        self.button_table.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_table.clicked.connect(self.on_click_table)

    def on_click_user(self):
        window_navigation.closeWindow()
        global user_window
        user_window.Load_Data()
        user_window.showWindow()

    def on_click_role(self):
        window_navigation.closeWindow()
        global role_window
        role_window.Load_Data()
        role_window.showWindow()

    def on_click_privileges(self):
        window_navigation.closeWindow()
        global privileges_window
        privileges_window.Load_Data()
        privileges_window.showWindow()

    def on_click_table(self):
        window_navigation.closeWindow()
        global table_window
        table_window.Load_Data()
        table_window.showWindow()

    def on_click_pri(self):
        window_navigation.closeWindow()
        global pri_window
        pri_window.Load_Data()
        pri_window.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()


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


# Variable
login_window = LoginWindow()
window_navigation = MainWindow()
login_info = []

nhansu = Role_Nhan_su()
pb_window = Phongbanview()
pb_window2 = Nhanvienview()


def main():
    # lib_dir = r"C:\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9"
    # lib_dir = "C:\oclient\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9"
    # global oracle_client_initialized
    # oracle_client_initialized = False
    # if not oracle_client_initialized:
    #     try:
    #         cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    #         oracle_client_initialized = True
    #     except Exception as err:
    #         print("Error initializing Oracle Client:", err)
    #         sys.exit(1)
    app = QtWidgets.QApplication(sys.argv)
    global login_window
    login_window.Load_Data()
    login_window.showWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
