import sys
import cx_Oracle
from PyQt5 import QtCore, QtWidgets
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QLabel, QLineEdit, QPushButton
import messagebox
from PyQt5.QtCore import Qt

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


class pri_Controller:
    def display_table_list(self):
        result = execute_query(
            login_info[0], login_info[1], "select privilege from dba_sys_privs where grantee = 'DBA'")
        return result

    def Grant_Pri(self, name, user):
        result = execute_query(
            login_info[0], login_info[1], 'grant {0} to {1}'.format(name, user))
        return result


class PrivilegesController:

    def get_user_list(self, search_text=None):

        sql = "SELECT GRANTEE, TABLE_NAME, PRIVILEGE FROM dba_tab_privs"
        if search_text:
            sql += f" WHERE grantee = '{search_text}' FETCH FIRST 500 ROWS ONLY"
        else:
            sql = "SELECT GRANTEE, TABLE_NAME, PRIVILEGE FROM dba_tab_privs FETCH FIRST 500 ROWS ONLY"

        result = execute_query(login_info[0], login_info[1], sql)

        return result


class RoleController:
    def get_role_list(self):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT * FROM DBA_ROLES')
        return result

    def get_privileged_list_of_role_table(self, role_name):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT * FROM ROLE_TAB_PRIVS where ROLE = ' + "'{0}'".format(role_name))
        return result

    def get_privileged_list_of_role_sys(self, role_name):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT * FROM ROLE_ROLE_PRIVS where ROLE = ' + "'{0}'".format(role_name))
        return result

    def Add_Role(self, role_name, password):
        if password != '':
            result = execute_query(
                login_info[0], login_info[1], 'CREATE ROLE {0} IDENTIFIED BY {1}'.format(role_name, password))
        else:
            result = execute_query(
                login_info[0], login_info[1], 'CREATE ROLE {0}'.format(role_name))
        return result

    def Recall_Role_Table(self, role_name, table_name, privilege):
        result = execute_query(
            login_info[0], login_info[1], 'REVOKE {0} ON sys.{1} FROM {2}'.format(privilege, table_name, role_name))

        return result

    def Recall_Role_Sys(self, role_name, privilege):
        result = execute_query(
            login_info[0], login_info[1], 'REVOKE {0} FROM {1}'.format(privilege, role_name))
        return result

    def Delete_Role(self, role_name):
        result = execute_query(
            login_info[0], login_info[1], 'DROP ROLE {0}'.format(role_name))
        return result

    def Grant_Role(self, role_name, user_name):
        result = execute_query(
            login_info[0], login_info[1], 'GRANT {0} TO {1}'.format(role_name, user_name))
        return result


class table_Controller:
    def display_table_list(self):
        result = execute_query(
            login_info[0], login_info[1], "SELECT Owner, table_name FROM all_tables WHERE table_name = '" + "NHANVIEN'")
        return result

    def Grant_Pri(self, pri, name, table, option, col):
        if (col):
            sql = ''
            for coll in col:
                sql = sql + coll + ','
            sql = sql[:-1]
        if col == '' or pri == 'insert' or pri == 'delete':
            result = execute_query(
                login_info[0], login_info[1], 'grant {0} on SYS.{1} to {2} {3}'.format(pri, table, name, option))
        elif (pri == 'select'):
            result = execute_query(
                login_info[0], login_info[1], 'select view_name from sys.all_views')
            count = 0
            while count != 10:
                for x in result:
                    if x[0] == 'UV_{0}{1}'.format(table, count):
                        print("i found it!")
                        break
                count = count + 1
            result = execute_query(
                login_info[0], login_info[1], 'create view UV_{0}{1} as select {2} from sys.{0}'.format(table, count, sql))
            result = execute_query(
                login_info[0], login_info[1], 'grant {0} on UV_{0}{1} to {3} {4}'.format(pri, col, table, name, option))
        elif (pri == 'update'):
            result = execute_query(
                login_info[0], login_info[1], 'grant {0}({1}) on SYS.{2} to {3} {4}'.format(pri, sql, table, name, option))
        return result

    def get_column_name(self, table):
        result = execute_query(
            login_info[0], login_info[1], "SELECT column_name FROM all_tab_cols WHERE table_name = upper('" + table + "')")
        return result


class User_Controller:
    def display_user_list(self):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT USER_ID, USERNAME, CREATED FROM ALL_USERS')
        return result

    def Drop_User(self, user_name):
        result = execute_query(
            login_info[0], login_info[1], 'DROP USER {0}'.format(user_name))
        return result

    def New_Password(self, user_name, newpassword):
        result = execute_query(
            login_info[0], login_info[1], 'ALTER USER {0} IDENTIFIED BY {1}'.format(user_name, newpassword))
        return result

    def Create_User(self, user_name, password):
        result = execute_query(
            login_info[0], login_info[1], 'CREATE USER {0} IDENTIFIED BY {1}'.format(user_name, password))
        return result

    def display_role_of_user(self, user_name):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT granted_role, admin_option, delegate_option, default_role, common, inherited FROM SYS.DBA_ROLE_PRIVS WHERE grantee = ' + "'{0}'".format(user_name))
        return result

    def Revoke_Role_From_User(self, role_name, user_name):
        result = execute_query(
            login_info[0], login_info[1], 'REVOKE {0} FROM {1}'.format(role_name, user_name))
        return result

    def display_tabprivs_of_user(self, user_name):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT owner, table_name, grantor, privilege, grantable FROM SYS.DBA_TAB_PRIVS WHERE grantee = ' + "'{0}'".format(user_name))
        return result

    def Revoke_TabPrivs_From_User(self, pri_name, table_name, user_name):
        result = execute_query(
            login_info[0], login_info[1], 'REVOKE {0} ON {1} FROM {2}'.format(pri_name, table_name, user_name))
        return result

    def display_privs_of_user(self, user_name):
        result = execute_query(
            login_info[0], login_info[1], 'SELECT privilege, admin_option, common, inherited FROM SYS.DBA_SYS_PRIVS WHERE grantee = ' + "'{0}'".format(user_name))
        return result

    def Revoke_Privs_From_User(self, pri_name, user_name):
        result = execute_query(
            login_info[0], login_info[1], 'REVOKE {0} FROM {1}'.format(pri_name, user_name))
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
    try:
        con = cx_Oracle.connect(username, password, 'localhost:1521/ORCLPDB')

    except cx_Oracle.DatabaseError as er:
        print('There is an error in the Oracle database:', er)

    else:
        try:
            cur = con.cursor()

            # fetchall() is used to fetch all records from result set
            cur.execute(queryString)
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
            window_navigation.Load_Data()
            window_navigation.showWindow()
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


class PriView:
    def Load_Data(self):

        self.TableController = pri_Controller()

        self.user_list = []

        self.search_text = ""  # Khởi tạo biến "search_text" với giá trị rỗng

        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách quyền')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Thiết lập p hiện thị nhập user
        self.user_name = QtWidgets.QLabel(self.main_window)
        self.user_name.setText("Nhập user/role name muốn cấp quyền : ")
        self.user_name.setStyleSheet("font-size: 16px;")
        self.user_name.adjustSize()
        self.user_name.move(410, 20)

        # Thiết lập ô nhập input
        self.input = QtWidgets.QLineEdit(self.main_window)
        self.input.setPlaceholderText("User name...")
        self.input.setStyleSheet("QLineEdit { padding-left: 16px; }")
        self.input.setFixedWidth(160)
        self.input.setFixedHeight(30)
        self.input.move(410, 60)

        # Thiết lập button submit
        self.btn_submit = QtWidgets.QPushButton(self.main_window)
        self.btn_submit.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_submit.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_submit.setText("Cấp")
        self.btn_submit.clicked.connect(self.clicked_submit)
        self.btn_submit.move(570, 60)

        # thiết lập hover cursor
        self.btn_submit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.user_list = self.TableController.display_table_list()

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(1)
        self.table_widget.setHorizontalHeaderLabels(['PRIVILEGES'])

        self.table_widget.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        # Thêm dữ liệu vào table widget

        for user in self.user_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(user[0])))
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
        self.btn_back.clicked.connect(self.Backmenu)

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def clicked_submit(self):
        if self.input.text() == '':
            MessageBoxErr("Lỗi", "Vui lòng nhập đủ thông tin ")
        else:
            result = self.TableController.Grant_Pri(
                self.table_selected, self.input.text())
            return result

    def Backmenu(self):
        global pri_window
        global window_navigation
        pri_window.closeWindow()
        window_navigation.showWindow()

    def on_selectionChanged(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.table_selected = self.user_list[index][0]


class privilegesView:
    def Load_Data(self):

        self.PrivilegesController = PrivilegesController()

        self.user_list = []

        self.search_text = ""  # Khởi tạo biến "search_text" với giá trị rỗng

        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách thông tin quyền')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Thiết lập p hiện thị nhập user
        self.user_name = QtWidgets.QLabel(self.main_window)
        self.user_name.setText("Nhập user/role : ")
        self.user_name.setStyleSheet("font-size: 16px;")
        self.user_name.adjustSize()
        self.user_name.move(410, 20)

        # Thiết lập ô nhập input
        self.search_bar = QtWidgets.QLineEdit(self.main_window)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setStyleSheet("QLineEdit { padding-left: 16px; }")
        self.search_bar.setFixedWidth(160)
        self.search_bar.setFixedHeight(30)
        self.search_bar.move(410, 60)

        # Thiết lập button search
        self.btn_search = QtWidgets.QPushButton(self.main_window)
        self.btn_search.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_search.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_search.setText("Search")
        self.btn_search.clicked.connect(self.clicked_search)
        self.btn_search.move(570, 60)

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
        self.btn_all.move(470, 140)
        # thiết lập hover cursor
        self.btn_all.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.user_list = self.PrivilegesController.get_user_list(
            self.search_text)

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(
            ['GRANTEE', 'PRIVILEGE', 'TABLENAME'])
        # Thêm dữ liệu vào table widget

        for user in self.user_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(user[2])))
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
        # # self.btn_back.setCursor(Qt.PointingHandCursor)

        self.btn_back.clicked.connect(self.Backmenu)

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def update_user_list(self, search_text=None):
        self.user_list = self.PrivilegesController.get_user_list(search_text)
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.user_list))
            for row, user in enumerate(self.user_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(user[2])))

    def clicked_search(self):
        self.search_text = self.search_bar.text()
        self.update_user_list(self.search_text)

    def clicked_btn(self):
        self.search_text = None
        self.update_user_list(self.search_text)

    def Backmenu(self):
        global privileges_window
        global window_navigation
        privileges_window.closeWindow()
        window_navigation.showWindow()


class RoleView:
    def Load_Data(self):
        self.role_controller = RoleController()
        self.roles = []
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách role')

        # Json data
        self.data_Roles = {"Role Name": "",
                           "Password": "",
                           "Authentication": "",
                           "Common": "",
                           "Oracle maintained": "",
                           "Inherited": "",
                           "Implicit": ""}

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.roles = self.role_controller.get_role_list()
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["Role Name",
                                                     "Password",
                                                     "Authentication",
                                                     "Common",
                                                     "Oracle maintained",
                                                     "Inherited",
                                                     "Implicit"])
        self.table_widget.selectionModel().selectionChanged.connect(self.on_selectionChanged)
        # Thêm dữ liệu vào table widget
        for role in self.roles:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(role[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(role[2])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(role[3])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(role[4])))
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(role[5])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(role[6])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(role[7])))

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

        # Role Name
        self.role_name = QtWidgets.QLabel(self.main_window)
        self.role_name.setText("Role Name: ")
        self.role_name.setStyleSheet("font-size: 14px;")

        self.role_name.move(480, 0)

        self.txt_role = QtWidgets.QLineEdit(self.main_window)
        self.txt_role.setFixedWidth(160)
        self.txt_role.setText(self.data_Roles["Role Name"])
        self.txt_role.move(480, 25)

        # Password
        self.Password_name = QtWidgets.QLabel(self.main_window)
        self.Password_name.setText("Password: ")
        self.Password_name.setStyleSheet("font-size: 14px;")

        self.Password_name.move(480, 50)

        self.txt_Password = QtWidgets.QLineEdit(self.main_window)
        self.txt_Password.setFixedWidth(160)
        self.txt_Password.setText(self.data_Roles["Password"])
        self.txt_Password.move(480, 75)

        # Authentication
        self.Authentication_name = QtWidgets.QLabel(self.main_window)
        self.Authentication_name.setText("Authentication: ")
        self.Authentication_name.setStyleSheet("font-size: 14px;")

        self.Authentication_name.move(480, 100)

        self.txt_Authentication = QtWidgets.QLineEdit(self.main_window)
        self.txt_Authentication.setFixedWidth(160)
        self.txt_Authentication.setText(self.data_Roles["Authentication"])
        self.txt_Authentication.move(480, 125)

        # Common
        self.Common_name = QtWidgets.QLabel(self.main_window)
        self.Common_name.setText("Common: ")
        self.Common_name.setStyleSheet("font-size: 14px;")

        self.Common_name.move(480, 150)

        self.txt_Common = QtWidgets.QLineEdit(self.main_window)
        self.txt_Common.setFixedWidth(160)
        self.txt_Common.setText(self.data_Roles["Common"])
        self.txt_Common.move(480, 175)

        # Oracle maintained
        self.Oracle_Maintained_name = QtWidgets.QLabel(self.main_window)
        self.Oracle_Maintained_name.setText("Oracle maintained: ")
        self.Oracle_Maintained_name.setStyleSheet("font-size: 14px;")

        self.Oracle_Maintained_name.move(480, 200)

        self.txt_Oracle_Maintained = QtWidgets.QLineEdit(self.main_window)
        self.txt_Oracle_Maintained.setFixedWidth(160)
        self.txt_Oracle_Maintained.setText(
            self.data_Roles["Oracle maintained"])
        self.txt_Oracle_Maintained.move(480, 225)

        # Inherited
        self.Inherited_name = QtWidgets.QLabel(self.main_window)
        self.Inherited_name.setText("Inherited: ")
        self.Inherited_name.setStyleSheet("font-size: 14px;")

        self.Inherited_name.move(480, 250)

        self.txt_Inherited = QtWidgets.QLineEdit(self.main_window)
        self.txt_Inherited.setFixedWidth(160)
        self.txt_Inherited.setText(self.data_Roles["Inherited"])
        self.txt_Inherited.move(480, 275)

        # Implicit
        self.Implicit_name = QtWidgets.QLabel(self.main_window)
        self.Implicit_name.setText("Implicit: ")
        self.Implicit_name.setStyleSheet("font-size: 14px;")

        self.Implicit_name.move(480, 300)

        self.txt_Implicit = QtWidgets.QLineEdit(self.main_window)
        self.txt_Implicit.setFixedWidth(160)
        self.txt_Implicit.setText(self.data_Roles["Implicit"])
        self.txt_Implicit.move(480, 325)

        # Add button
        self.btn_add = QtWidgets.QPushButton(self.main_window)
        self.btn_add.setText("Thêm role")
        self.btn_add.setMinimumWidth(100)
        self.btn_add.move(30, 410)
        self.btn_add.clicked.connect(self.Add_Role)

        # Recall table button
        self.btn_recall = QtWidgets.QPushButton(self.main_window)
        self.btn_recall.setText("Thu hồi quyền bảng")
        self.btn_recall.setMinimumWidth(150)
        self.btn_recall.move(160, 410)
        self.btn_recall.clicked.connect(self.Recall_Role_Table)

        # Recall Sys button
        self.btn_recall = QtWidgets.QPushButton(self.main_window)
        self.btn_recall.setText("Thu hồi quyền hệ thống")
        self.btn_recall.setMinimumWidth(150)
        self.btn_recall.move(320, 410)
        self.btn_recall.clicked.connect(self.Recall_Role_Sys)

        # Delete button
        self.btn_delete = QtWidgets.QPushButton(self.main_window)
        self.btn_delete.setText("Xoá role")
        self.btn_delete.setMinimumWidth(100)
        self.btn_delete.move(500, 410)
        self.btn_delete.clicked.connect(self.Delete_Role)

        # Title: Thêm role

        self.title_role_create = QtWidgets.QLabel(self.main_window)
        self.title_role_create.setText("Thêm role")
        self.title_role_create.setStyleSheet("font-size: 15px;")

        self.title_role_create.move(200, 450)

        # Create role name
        self.role_name_create = QtWidgets.QLabel(self.main_window)
        self.role_name_create.setText("Role Name: ")
        self.role_name_create.setStyleSheet("font-size: 14px;")

        self.role_name_create.move(20, 445)

        self.txt_role_name_create = QtWidgets.QLineEdit(self.main_window)
        self.txt_role_name_create.setFixedWidth(160)
        self.txt_role_name_create.setText("")
        self.txt_role_name_create.move(20, 470)

        # Create role password
        self.role_password_create = QtWidgets.QLabel(self.main_window)
        self.role_password_create.setText("Role password: ")
        self.role_password_create.setStyleSheet("font-size: 14px;")

        self.role_password_create.move(340, 445)

        self.txt_role_password_create = QtWidgets.QLineEdit(self.main_window)
        self.txt_role_password_create.setFixedWidth(160)
        self.txt_role_password_create.setText("")
        self.txt_role_password_create.move(340, 470)

        # Thiết lập button back
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("BACK")
        self.btn_back.move(610, 470)
        # self.btn_back.setCursor(Qt.PointingHandCursor)

        self.btn_back.clicked.connect(self.Backmenu)

    def Backmenu(self):
        global role_window
        global window_navigation
        role_window.closeWindow()
        window_navigation.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def on_selectionChanged(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Roles = {"Role Name": self.roles[index][0],
                               "Password": self.roles[index][2],
                               "Authentication": self.roles[index][3],
                               "Common": self.roles[index][4],
                               "Oracle maintained": self.roles[index][5],
                               "Inherited": self.roles[index][6],
                               "Implicit": self.roles[index][7]}
            self.txt_role.setText(self.data_Roles["Role Name"])
            self.txt_Password.setText(self.data_Roles["Password"])
            self.txt_Authentication.setText(self.data_Roles["Authentication"])
            self.txt_Common.setText(self.data_Roles["Common"])
            self.txt_Oracle_Maintained.setText(
                self.data_Roles["Oracle maintained"])
            self.txt_Inherited.setText(self.data_Roles["Inherited"])
            self.txt_Implicit.setText(self.data_Roles["Implicit"])

    def update_list(self):

        self.roles = self.role_controller.get_role_list()
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.roles))
            self.table_widget.selectionModel().selectionChanged.connect(self.on_selectionChanged)
            for row, role in enumerate(self.roles):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(role[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(role[2])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(role[3])))
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(role[4])))
                self.table_widget.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(str(role[5])))
                self.table_widget.setItem(
                    row, 5, QtWidgets.QTableWidgetItem(str(role[6])))
                self.table_widget.setItem(
                    row, 6, QtWidgets.QTableWidgetItem(str(role[7])))

    def Add_Role(self):
        if self.txt_role_name_create.text() == '':
            MessageBoxErr("Lỗi", "Vui lòng nhập role name")
        else:
            result = self.role_controller.Add_Role(
                self.txt_role_name_create.text(), self.txt_role_password_create.text())
            self.role = self.role_controller.get_role_list()
            self.update_list()
            return result

    def Recall_Role_Table(self):
        if self.data_Roles["Role Name"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn role, bảng hoặc quyền")
        else:
            self.main_window1 = QtWidgets.QMainWindow()

            self.main_window1.setWindowTitle('Thu hồi quyền trên bảng')

            # Json data
            self.data_Roles1 = {"Role Name": "",
                                "Password": "",
                                "Authentication": "",
                                "Common": "",
                                "Oracle maintained": "",
                                "Inherited": "",
                                "Implicit": ""}

            self.table_widget1 = QtWidgets.QTableWidget()
            # Đặt số lượng cột cho table widget
            self.table_widget1.setColumnCount(7)
            self.table_widget1.setHorizontalHeaderLabels(["Role Name",
                                                          "Table Name",
                                                          "Column Name",
                                                          "Privilege",
                                                          "Grantable",
                                                          "Common",
                                                          "Inherited"])
            self.table_widget1.selectionModel().selectionChanged.connect(
                self.Change_Recall_Role_Table)

            self.roles1 = self.role_controller.get_privileged_list_of_role_table(
                self.data_Roles["Role Name"])
            if self.roles1 == []:
                MessageBoxWarn("Cảnh báo", "Role không có quyền trên bảng")
                return

            for role in self.roles1:
                row_position = self.table_widget1.rowCount()
                self.table_widget1.insertRow(row_position)
                self.table_widget1.setItem(
                    row_position, 0, QtWidgets.QTableWidgetItem(str(role[0])))
                self.table_widget1.setItem(
                    row_position, 1, QtWidgets.QTableWidgetItem(str(role[2])))
                self.table_widget1.setItem(
                    row_position, 2, QtWidgets.QTableWidgetItem(str(role[3])))
                self.table_widget1.setItem(
                    row_position, 3, QtWidgets.QTableWidgetItem(str(role[4])))
                self.table_widget1.setItem(
                    row_position, 4, QtWidgets.QTableWidgetItem(str(role[5])))
                self.table_widget1.setItem(
                    row_position, 5, QtWidgets.QTableWidgetItem(str(role[6])))
                self.table_widget1.setItem(
                    row_position, 6, QtWidgets.QTableWidgetItem(str(role[7])))

            # Thiết lập layout cho widget
            # Tạo khung cuộn
            self.scroll_area1 = QtWidgets.QScrollArea()
            self.scroll_area1.setWidgetResizable(True)
            self.scroll_area1.setFixedWidth(400)
            self.scroll_area1.setFixedHeight(300)

            # Đặt bảng trong khung cuộn
            self.scroll_area1.setWidget(self.table_widget1)

            # Đặt khung cuộn vào cửa sổ chính
            self.main_window1.setCentralWidget(self.scroll_area1)

            # Thiết lập kích thước cho widget
            self.main_window1.resize(640, 480)

            # Role Name
            self.role_name_recall_table = QtWidgets.QLabel(self.main_window1)
            self.role_name_recall_table.setText("Role Name: ")
            self.role_name_recall_table.setStyleSheet("font-size: 14px;")

            self.role_name_recall_table.move(410, 0)

            self.txt_role_recall_table = QtWidgets.QLineEdit(self.main_window1)
            self.txt_role_recall_table.setFixedWidth(160)
            self.txt_role_recall_table.setText("")
            self.txt_role_recall_table.move(410, 25)

            # Table Name
            self.table_name_recall_table = QtWidgets.QLabel(self.main_window1)
            self.table_name_recall_table.setText("Table Name: ")
            self.table_name_recall_table.setStyleSheet("font-size: 14px;")

            self.table_name_recall_table.move(410, 50)

            self.txt_table_recall_table = QtWidgets.QLineEdit(
                self.main_window1)
            self.txt_table_recall_table.setFixedWidth(160)
            self.txt_table_recall_table.setText("")
            self.txt_table_recall_table.move(410, 75)

            # Column Name
            self.Column_name_recall_table = QtWidgets.QLabel(self.main_window1)
            self.Column_name_recall_table.setText("Column: ")
            self.Column_name_recall_table.setStyleSheet("font-size: 14px;")

            self.Column_name_recall_table.move(410, 100)

            self.txt_Column_recall_table = QtWidgets.QLineEdit(
                self.main_window1)
            self.txt_Column_recall_table.setFixedWidth(160)
            self.txt_Column_recall_table.setText("")
            self.txt_Column_recall_table.move(410, 125)

            # Privilege
            self.Privilege_name_recall_table = QtWidgets.QLabel(
                self.main_window1)
            self.Privilege_name_recall_table.setText("Privilege: ")
            self.Privilege_name_recall_table.setStyleSheet("font-size: 14px;")

            self.Privilege_name_recall_table.move(410, 150)

            self.txt_Privilege_recall_table = QtWidgets.QLineEdit(
                self.main_window1)
            self.txt_Privilege_recall_table.setFixedWidth(160)
            self.txt_Privilege_recall_table.setText("")
            self.txt_Privilege_recall_table.move(410, 175)

            # Buton: Thu hồi
            self.btn_recall1 = QtWidgets.QPushButton(self.main_window1)
            self.btn_recall1.setText("Thu hồi")
            self.btn_recall1.setMinimumWidth(100)
            self.btn_recall1.move(250, 360)
            self.btn_recall1.clicked.connect(self.Handle_Recall_Role_Table)

            self.main_window1.show()

    def Recall_Role_Sys(self):
        if self.data_Roles["Role Name"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn role, bảng hoặc quyền")
        else:
            self.main_window2 = QtWidgets.QMainWindow()

            self.main_window2.setWindowTitle('Thu hồi quyền trên hệ thống')

            # Json data
            self.data_Roles2 = {"Role Name": "",
                                "Privilege": "",
                                "Admin option": "",
                                "Common": "",
                                "Inherited": ""}

            self.table_widget2 = QtWidgets.QTableWidget()
            # Đặt số lượng cột cho table widget
            self.table_widget2.setColumnCount(5)
            self.table_widget2.setHorizontalHeaderLabels(["Role Name",
                                                          "Privilege",
                                                          "Admin option",
                                                          "Common",
                                                          "Inherited"])
            self.table_widget2.selectionModel().selectionChanged.connect(
                self.Change_Recall_Role_Sys)

            self.roles2 = self.role_controller.get_privileged_list_of_role_sys(
                self.data_Roles["Role Name"])

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
                self.table_widget2.setItem(
                    row_position, 2, QtWidgets.QTableWidgetItem(str(role[2])))
                self.table_widget2.setItem(
                    row_position, 3, QtWidgets.QTableWidgetItem(str(role[3])))
                self.table_widget2.setItem(
                    row_position, 4, QtWidgets.QTableWidgetItem(str(role[4])))

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

            # Role Name
            self.role_name_recall_sys = QtWidgets.QLabel(self.main_window2)
            self.role_name_recall_sys.setText("Role Name: ")
            self.role_name_recall_sys.setStyleSheet("font-size: 14px;")

            self.role_name_recall_sys.move(410, 0)

            self.txt_role_recall_sys = QtWidgets.QLineEdit(self.main_window2)
            self.txt_role_recall_sys.setFixedWidth(160)
            self.txt_role_recall_sys.setText("")
            self.txt_role_recall_sys.move(410, 25)

            # Privilege
            self.Privilege_name_recall_sys = QtWidgets.QLabel(
                self.main_window2)
            self.Privilege_name_recall_sys.setText("Privilege: ")
            self.Privilege_name_recall_sys.setStyleSheet("font-size: 14px;")

            self.Privilege_name_recall_sys.move(410, 50)

            self.txt_Privilege_recall_sys = QtWidgets.QLineEdit(
                self.main_window2)
            self.txt_Privilege_recall_sys.setFixedWidth(160)
            self.txt_Privilege_recall_sys.setText("")
            self.txt_Privilege_recall_sys.move(410, 75)

            # Button: Thu hồi
            self.btn_recall2 = QtWidgets.QPushButton(self.main_window2)
            self.btn_recall2.setText("Thu hồi")
            self.btn_recall2.setMinimumWidth(100)
            self.btn_recall2.move(250, 360)
            self.btn_recall2.clicked.connect(self.Handle_Recall_Role_Sys)

            self.main_window2.show()

    def Change_Recall_Role_Table(self, selected, deselected):
        index = -1
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Roles1 = {"Role Name": self.roles1[index][0],
                                "Table Name": self.roles1[index][2],
                                "Column Name": self.roles1[index][3],
                                "Privilege": self.roles1[index][4],
                                "Grantable": self.roles1[index][5],
                                "Common": self.roles1[index][6],
                                "Inherited": self.roles1[index][7]}
            self.txt_role_recall_table.setText(self.data_Roles1["Role Name"])
            self.txt_table_recall_table.setText(self.data_Roles1["Table Name"])
            self.txt_Column_recall_table.setText(
                self.data_Roles1["Column Name"])
            self.txt_Privilege_recall_table.setText(
                self.data_Roles1["Privilege"])

    def Change_Recall_Role_Sys(self, selected, deselected):
        index = -1
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Roles2 = {"Role Name": self.roles2[index][0],
                                "Privilege": self.roles2[index][1],
                                "Admin option": self.roles2[index][2],
                                "Common": self.roles2[index][3],
                                "Inherited": self.roles2[index][4]}
        self.txt_role_recall_sys.setText(self.data_Roles2["Role Name"])
        self.txt_Privilege_recall_sys.setText(self.data_Roles2["Privilege"])

    def Handle_Recall_Role_Table(self):
        if self.data_Roles1["Role Name"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn role, bảng, hoặc quyền")
        elif self.roles1 == []:
            MessageBoxWarn("Cảnh báo", "Role không có quyền trên bảng")
            return
        else:
            result = self.role_controller.Recall_Role_Table(
                self.data_Roles1["Role Name"], self.data_Roles1["Table Name"], self.data_Roles1["Privilege"])
            self.main_window1.close()
            return result

    def Handle_Recall_Role_Sys(self):
        if self.data_Roles2["Role Name"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn role hoặc quyền")
            return
        elif self.roles2 == []:
            MessageBoxWarn("Cảnh báo", "Role không có quyền trên hệ thống")
            return
        else:
            result = self.role_controller.Recall_Role_Sys(
                self.data_Roles2["Role Name"], self.data_Roles2["Privilege"])
            self.main_window2.close()
            return result

    def Delete_Role(self):
        if self.data_Roles["Role Name"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn role")
        else:
            result = self.role_controller.Delete_Role(
                self.data_Roles["Role Name"])
            self.update_list()
            return result


class TableView:
    def Load_Data(self):

        self.noneOption = False
        self.grantOption = False
        self.selectOption = False
        self.insertOption = False
        self.updateOption = False
        self.deleteOption = False

        self.TableController = table_Controller()

        self.user_list = []

        self.column_selected = []

        self.search_text = ""  # Khởi tạo biến "search_text" với giá trị rỗng

        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách bảng')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        # Thiết lập p hiện thị nhập user
        self.user_name = QtWidgets.QLabel(self.main_window)
        self.user_name.setText("Nhập user/role name muốn cấp quyền : ")
        self.user_name.setStyleSheet("font-size: 16px;")
        self.user_name.adjustSize()
        self.user_name.move(410, 20)

        # Radio button for none option
        self.radioButton_none = QtWidgets.QRadioButton(self.main_window)
        self.radioButton_none.setGeometry(QtCore.QRect(410, 50, 160, 20))
        self.radioButton_none.setText("NONE")
        self.radioButton_none.toggled.connect(self.selectedNone)

        # Radio button for grant option
        self.radioButton_grant = QtWidgets.QRadioButton(self.main_window)
        self.radioButton_grant.setGeometry(QtCore.QRect(410, 80, 160, 20))
        self.radioButton_grant.setText("WITH GRANT OPTION")
        self.radioButton_grant.toggled.connect(self.selectedGrant)

        # Thiết lập ô nhập input
        self.input = QtWidgets.QLineEdit(self.main_window)
        self.input.setPlaceholderText("User name...")
        self.input.setStyleSheet("QLineEdit { padding-left: 16px; }")
        self.input.setFixedWidth(160)
        self.input.setFixedHeight(30)
        self.input.move(410, 110)

        # Thiết lập button submit
        self.btn_submit = QtWidgets.QPushButton(self.main_window)
        self.btn_submit.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_submit.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_submit.setText("Cấp")
        self.btn_submit.clicked.connect(self.clicked_submit)
        self.btn_submit.move(570, 110)

        # thiết lập hover cursor
        self.btn_submit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.user_list = self.TableController.display_table_list()

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(['OWNER', 'TABLENAME'])

        self.table_widget.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        # Thêm dữ liệu vào table widget

        for user in self.user_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(user[1])))
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
        # # self.btn_back.setCursor(Qt.PointingHandCursor)

        self.btn_back.clicked.connect(self.Backmenu)

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def selectedNone(self, selected):
        if selected:
            self.noneOption = True
            self.grantOption = False

    def selectedGrant(self, selected):
        if selected:
            self.noneOption = False
            self.grantOption = True

    def selectedInsert(self, selected):
        if selected:
            self.selectOption = False
            self.insertOption = True
            self.deleteOption = False
            self.updateOption = False

    def selectedSelect(self, selected):
        if selected:
            self.selectOption = True
            self.insertOption = False
            self.deleteOption = False
            self.updateOption = False

    def selectedUpdate(self, selected):
        if selected:
            self.selectOption = False
            self.insertOption = False
            self.deleteOption = False
            self.updateOption = True

    def selectedDelete(self, selected):
        if selected:
            self.selectOption = False
            self.insertOption = False
            self.deleteOption = True
            self.updateOption = False

    def update_user_list(self, search_text=None):
        self.user_list = self.TableController.get_user_list(search_text)
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.user_list))
            for row, user in enumerate(self.user_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(user[2])))

    def clicked_submit(self):
        if self.input.text() == '' or self.noneOption == self.grantOption:
            MessageBoxErr("Lỗi", "Vui lòng nhập đủ thông tin ")
        else:
            self.main_window1 = QtWidgets.QMainWindow()

            self.user_list1 = []

            self.user_list1 = self.TableController.get_column_name(
                self.table_selected)

            self.main_window1.setWindowTitle('Cấp quyền user trên bảng')

            # Thiết lập kích thước cho widget
            self.main_window1.resize(700, 520)

            # Khởi tạo table widget để hiển thị danh sách người dùng
            self.table_widget1 = QtWidgets.QTableWidget()
            # Đặt số lượng cột cho table widget
            self.table_widget1.setColumnCount(1)
            self.table_widget1.setHorizontalHeaderLabels(['COLUMN NAME'])
            self.table_widget1.selectionModel().selectionChanged.connect(
                self.on_selectionChanged_column)
            # Thêm dữ liệu vào table widget

            for user in self.user_list1:
                row_position = self.table_widget1.rowCount()
                self.table_widget1.insertRow(row_position)
                self.table_widget1.setItem(
                    row_position, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            # Tạo khung cuộn
            scroll_area1 = QtWidgets.QScrollArea()
            scroll_area1.setWidgetResizable(True)
            scroll_area1.setFixedWidth(390)
            scroll_area1.setFixedHeight(400)

            # Đặt bảng trong khung cuộn
            scroll_area1.setWidget(self.table_widget1)
            # # Thêm tab_widget vào QMainWindow
            self.main_window1.setCentralWidget(scroll_area1)

            # Radio button for none select
            self.radioButton_select = QtWidgets.QRadioButton(self.main_window1)
            self.radioButton_select.setGeometry(QtCore.QRect(410, 50, 160, 20))
            self.radioButton_select.setText("SELECT")
            self.radioButton_select.toggled.connect(self.selectedSelect)

            # Radio button for grant insert
            self.radioButton_insert = QtWidgets.QRadioButton(self.main_window1)
            self.radioButton_insert.setGeometry(QtCore.QRect(410, 80, 160, 20))
            self.radioButton_insert.setText("INSERT")
            self.radioButton_insert.toggled.connect(self.selectedInsert)

            # Radio button for grant update
            self.radioButton_update = QtWidgets.QRadioButton(self.main_window1)
            self.radioButton_update.setGeometry(
                QtCore.QRect(410, 110, 160, 20))
            self.radioButton_update.setText("UPDATE")
            self.radioButton_update.toggled.connect(self.selectedUpdate)

            # Radio button for grant delete
            self.radioButton_delete = QtWidgets.QRadioButton(self.main_window1)
            self.radioButton_delete.setGeometry(
                QtCore.QRect(410, 140, 160, 20))
            self.radioButton_delete.setText("DELETE")
            self.radioButton_delete.toggled.connect(self.selectedDelete)

            # Buton: Cấp
            self.btn_grant_submid = QtWidgets.QPushButton(self.main_window1)
            self.btn_grant_submid.setText("Cấp quyền")
            self.btn_grant_submid.setMinimumWidth(100)
            self.btn_grant_submid.move(250, 460)
            self.btn_grant_submid.clicked.connect(self.click_grant_submit)

            self.main_window1.show()

    def Backmenu(self):
        global table_window
        global window_navigation
        table_window.closeWindow()
        window_navigation.showWindow()

    def on_selectionChanged(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.table_selected = self.user_list[index][1]

    def on_selectionChanged_column(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.column_selected.append(self.user_list1[index][0])

            alternative_color = QtGui.QColor("salmon")

            current_brush = ix.data(QtCore.Qt.BackgroundRole)
            new_brush = (
                QtGui.QBrush(alternative_color)
                if current_brush in (None, QtGui.QBrush())
                else QtGui.QBrush()
            )
            self.table_widget1.model().setData(ix, new_brush, QtCore.Qt.BackgroundRole)

    def click_grant_submit(self):
        if self.selectOption == False and self.insertOption == False and self.updateOption == False and self.deleteOption == False:
            # print(self.column_selected)
            MessageBoxErr("Lỗi", "Vui lòng chọn đủ thông tin")
        else:
            if self.selectOption:
                pri = 'select'
            elif self.insertOption:
                pri = 'insert'
            elif self.updateOption:
                pri = 'update'
            elif self.deleteOption:
                pri = 'delete'
            if self.grantOption:
                op = 'WITH GRANT OPTION'
            else:
                op = ''
            result = self.TableController.Grant_Pri(
                pri, self.input.text(), self.table_selected, op, self.column_selected)
            return result


class UserList:
    def Load_Data(self):
        self.user_controller = User_Controller()
        self.user_list = self.user_controller.display_user_list()
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setWindowTitle('Danh sách User')

        self.data_Users = {"ID": "",
                           "User Name": "",
                           "Date Created": ""}

        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(
            ['ID', 'User Name', 'Date created'])

        self.table_widget.selectionModel().selectionChanged.connect(self.on_sel)
        for user in self.user_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(user[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(user[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(user[2])))

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(420)
        self.scroll_area.setFixedHeight(450)
        self.scroll_area.setWidget(self.table_widget)
        self.main_window.setCentralWidget(self.scroll_area)

        self.main_window.resize(700, 520)

        # User Name
        self.user_name = QtWidgets.QLabel(self.main_window)
        self.user_name.setText("User Name: ")
        self.user_name.setStyleSheet("font-size: 14px;")
        self.user_name.move(480, 0)

        self.txt_role = QtWidgets.QLineEdit(self.main_window)
        self.txt_role.setFixedWidth(160)
        self.txt_role.setText(self.data_Users["User Name"])
        self.txt_role.move(440, 25)

        # Drop Button
        self.btn_delete = QtWidgets.QPushButton(self.main_window)
        self.btn_delete.setText("DROP USER")
        self.btn_delete.setMinimumWidth(100)
        self.btn_delete.move(470, 70)
        self.btn_delete.clicked.connect(self.Drop_User)

        # Add Button
        self.btn_delete = QtWidgets.QPushButton(self.main_window)
        self.btn_delete.setText("ADD USER")
        self.btn_delete.setMinimumWidth(100)
        self.btn_delete.move(470, 110)
        self.btn_delete.clicked.connect(self.Create_User_View)

        # Revoke Role Button
        self.btn_rRole = QtWidgets.QPushButton(self.main_window)
        self.btn_rRole.setText("Revoke Role")
        self.btn_rRole.setMinimumWidth(100)
        self.btn_rRole.move(470, 150)
        self.btn_rRole.clicked.connect(self.Revoke_Role_View)

        # Revoke Table_Privs Button
        self.btn_rTab = QtWidgets.QPushButton(self.main_window)
        self.btn_rTab.setText("Revoke Table Privs")
        self.btn_rTab.setMinimumWidth(150)
        self.btn_rTab.move(470, 190)
        self.btn_rTab.clicked.connect(self.Revoke_TabPrivs_View)

        # Revoke Privs Button
        self.btn_rPri = QtWidgets.QPushButton(self.main_window)
        self.btn_rPri.setText("Revoke System Privs")
        self.btn_rPri.setMinimumWidth(150)
        self.btn_rPri.move(470, 230)
        self.btn_rPri.clicked.connect(self.Revoke_Privs_View)

        # Grant Role Button
        self.btn_gRole = QtWidgets.QPushButton(self.main_window)
        self.btn_gRole.setText("Grant Role")
        self.btn_gRole.setMinimumWidth(150)
        self.btn_gRole.move(470, 270)
        self.btn_gRole.clicked.connect(self.Grant_Role_View)

        # Thiết lập button back
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("BACK")
        self.btn_back.move(610, 470)
        # self.btn_back.setCursor(Qt.PointingHandCursor)

        self.btn_back.clicked.connect(self.Backmenu)

    def on_sel(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Users = {"ID": self.user_list[index][0],
                               "User Name": self.user_list[index][1],
                               "Date Created": self.user_list[index][2]}
            self.txt_role.setText(self.data_Users["User Name"])

    def Drop_User(self):
        if self.data_Users["User Name"] == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn tên user")
        else:
            self.user_controller.Drop_User(self.data_Users["User Name"])
            self.update_user_list()

    def update_user_list(self):
        self.user_list = self.user_controller.display_user_list()
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.user_list))
            for row, user in enumerate(self.user_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(user[2])))

    def New_password(self):
        self.user_controller.New_Password(
            self.data_Users["User Name"], self.txt_change.text())
# Grant Role

    def Grant_Role_View(self):

        self.sub_window = QtWidgets.QMainWindow()
        self.sub_window.setWindowTitle(
            'USER: {0}'.format(self.txt_role.text()))
        self.user_controller4 = RoleController()
        self.role_list = self.user_controller4.get_role_list()
        self.data_Roles = {"Role Name": "",
                           "Password": "",
                           "Authentication": "",
                           "Common": "",
                           "Oracle maintained": "",
                           "Inherited": "",
                           "Implicit": ""}
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["Role Name",
                                                     "Password",
                                                     "Authentication",
                                                     "Common",
                                                     "Oracle maintained",
                                                     "Inherited",
                                                     "Implicit"])
        self.table_widget.selectionModel().selectionChanged.connect(self.on_sel4)
        for role in self.role_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(role[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(role[2])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(role[3])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(role[4])))
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(role[5])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(role[6])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(role[7])))

        # Thiết lập layout cho widget
        # Tạo khung cuộn
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(420)
        self.scroll_area.setFixedHeight(450)

        # Đặt bảng trong khung cuộn
        self.scroll_area.setWidget(self.table_widget)

        # Đặt khung cuộn vào cửa sổ chính
        self.sub_window.setCentralWidget(self.scroll_area)

        # Thiết lập kích thước cho widget
        self.sub_window.resize(640, 480)

        # Role Name
        self.role_name = QtWidgets.QLabel(self.sub_window)
        self.role_name.setText("Role Name: ")
        self.role_name.setStyleSheet("font-size: 14px;")
        self.role_name.move(480, 0)

        self.txt_role1 = QtWidgets.QLineEdit(self.sub_window)
        self.txt_role1.setFixedWidth(160)
        self.txt_role1.setText(self.data_Roles["Role Name"])
        self.txt_role1.move(440, 25)

        # Revoke Button
        self.btn_revoke = QtWidgets.QPushButton(self.sub_window)
        self.btn_revoke.setText("GRANT")
        self.btn_revoke.setMinimumWidth(100)
        self.btn_revoke.move(470, 70)
        self.btn_revoke.clicked.connect(self.Grant_Role)

        self.sub_window.show()

    def Grant_Role(self):
        if self.txt_role1.text() == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn role")
        else:
            self.user_controller4.Grant_Role(
                self.txt_role1.text(), self.txt_role.text())

    def on_sel4(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Roles = {"Role Name": self.role_list[index][0]}
            self.txt_role1.setText(self.data_Roles["Role Name"])

# Create User
    def Create_User_View(self):
        self.sub_window = QtWidgets.QMainWindow()
        self.sub_window.resize(580, 400)
        self.sub_window.setWindowTitle('Them User')
        # UserName
        self.user_name = QtWidgets.QLabel(self.sub_window)
        self.user_name.setText("User Name: ")
        self.user_name.setStyleSheet("font-size: 14px;")

        self.user_name.move(150, 25)

        self.txt_user_name = QtWidgets.QLineEdit(self.sub_window)
        self.txt_user_name.setFixedWidth(160)
        self.txt_user_name.move(260, 25)

        # Password
        self.password = QtWidgets.QLabel(self.sub_window)
        self.password.setText("Password: ")
        self.password.setStyleSheet("font-size: 14px;")

        self.password.move(150, 80)

        self.txt_password = QtWidgets.QLineEdit(self.sub_window)
        self.txt_password.setFixedWidth(160)
        self.txt_password.move(260, 80)

        # Create Button
        self.btn_create = QtWidgets.QPushButton(self.sub_window)
        self.btn_create.setText("CREATE")
        self.btn_create.setMinimumWidth(30)
        self.btn_create.move(230, 140)
        self.btn_create.clicked.connect(self.Create_User)
        self.sub_window.show()

    def Create_User(self):
        if self.txt_user_name.text() == '':
            MessageBoxErr("Lỗi", "Vui lòng nhập tên user")
        else:
            self.user_controller.Create_User(
                self.txt_user_name.text(), self.txt_password.text())
            self.update_user_list()

    def Backmenu(self):
        global user_window
        global window_navigation
        user_window.closeWindow()
        window_navigation.showWindow()

# Revoke Role
    def Revoke_Role_View(self):

        self.sub_window = QtWidgets.QMainWindow()
        self.sub_window.setWindowTitle(
            'USER: {0}'.format(self.txt_role.text()))
        self.user_controller1 = User_Controller()
        self.role_list = self.user_controller1.display_role_of_user(
            self.txt_role.text())
        self.data_Roles = {"Role": ""}
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(
            ['Role', 'Admin Option', 'Delegate_Option', 'Default_Role', 'Common', 'Inherited'])
        self.table_widget.selectionModel().selectionChanged.connect(self.on_sel1)
        for role in self.role_list:
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

        # Thiết lập layout cho widget
        # Tạo khung cuộn
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(420)
        self.scroll_area.setFixedHeight(450)

        # Đặt bảng trong khung cuộn
        self.scroll_area.setWidget(self.table_widget)

        # Đặt khung cuộn vào cửa sổ chính
        self.sub_window.setCentralWidget(self.scroll_area)

        # Thiết lập kích thước cho widget
        self.sub_window.resize(640, 480)

        # Role Name
        self.role_name = QtWidgets.QLabel(self.sub_window)
        self.role_name.setText("Role Name: ")
        self.role_name.setStyleSheet("font-size: 14px;")
        self.role_name.move(480, 0)

        self.txt_role1 = QtWidgets.QLineEdit(self.sub_window)
        self.txt_role1.setFixedWidth(160)
        self.txt_role1.setText(self.data_Roles["Role"])
        self.txt_role1.move(440, 25)

        # Revoke Button
        self.btn_revoke = QtWidgets.QPushButton(self.sub_window)
        self.btn_revoke.setText("REVOKE")
        self.btn_revoke.setMinimumWidth(100)
        self.btn_revoke.move(470, 70)
        self.btn_revoke.clicked.connect(self.Revoke_Role)

        self.sub_window.show()

    def Revoke_Role(self):
        if self.txt_role1.text() == '':
            MessageBoxErr("Lỗi", "Vui lòng chọn role")
        else:
            self.user_controller1.Revoke_Role_From_User(
                self.txt_role1.text(), self.txt_role.text())
            self.update_role_list()

    def on_sel1(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Roles = {"Role": self.role_list[index][0]}
            self.txt_role1.setText(self.data_Roles["Role"])

    def update_role_list(self):
        self.role_list = self.user_controller1.display_role_of_user(
            self.txt_role.text())
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.user_list))
            for row, role in enumerate(self.role_list):
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
# Revoke Tab Privs

    def Revoke_TabPrivs_View(self):
        self.sub_window = QtWidgets.QMainWindow()
        self.sub_window.setWindowTitle(
            'USER: {0}'.format(self.txt_role.text()))
        self.user_controller2 = User_Controller()
        self.tabprivs_list = self.user_controller2.display_tabprivs_of_user(
            self.txt_role.text())
        self.data_TabPrivs = {"Table_Name": "",
                              "Privilege": ""}
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(
            ['Owner', 'Table_Name', 'Grantor', 'Privilege', 'Grantable'])
        self.table_widget.selectionModel().selectionChanged.connect(self.on_sel2)
        for priv in self.tabprivs_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(priv[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(priv[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(priv[2])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(priv[3])))
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(priv[4])))

        # Thiết lập layout cho widget
        # Tạo khung cuộn
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(420)
        self.scroll_area.setFixedHeight(450)

        # Đặt bảng trong khung cuộn
        self.scroll_area.setWidget(self.table_widget)

        # Đặt khung cuộn vào cửa sổ chính
        self.sub_window.setCentralWidget(self.scroll_area)

        # Thiết lập kích thước cho widget
        self.sub_window.resize(640, 480)

        # Table Name
        self.table_name = QtWidgets.QLabel(self.sub_window)
        self.table_name.setText("Table Name: ")
        self.table_name.setStyleSheet("font-size: 14px;")
        self.table_name.move(480, 0)

        self.txt_tab = QtWidgets.QLineEdit(self.sub_window)
        self.txt_tab.setFixedWidth(160)
        self.txt_tab.setText(self.data_TabPrivs["Table_Name"])
        self.txt_tab.move(440, 25)

        # Privilege
        self.tabpriv_name = QtWidgets.QLabel(self.sub_window)
        self.tabpriv_name.setText("Privilege: ")
        self.tabpriv_name.setStyleSheet("font-size: 14px;")
        self.tabpriv_name.move(480, 50)

        self.txt_tabpriv = QtWidgets.QLineEdit(self.sub_window)
        self.txt_tabpriv.setFixedWidth(160)
        self.txt_tabpriv.setText(self.data_TabPrivs["Privilege"])
        self.txt_tabpriv.move(440, 75)

        # Revoke Button
        self.btn_revoke1 = QtWidgets.QPushButton(self.sub_window)
        self.btn_revoke1.setText("REVOKE")
        self.btn_revoke1.setMinimumWidth(100)
        self.btn_revoke1.move(470, 125)
        self.btn_revoke1.clicked.connect(self.Revoke_TabPrivs)

        self.sub_window.show()

    def Revoke_TabPrivs(self):
        if self.txt_tabpriv.text() == '' or self.txt_tab.text() == '':
            MessageBoxErr("Lỗi", "Vui lòng không nhập thiếu thông tin")
        else:
            self.user_controller2.Revoke_TabPrivs_From_User(
                self.txt_tabpriv.text(), self.txt_tab.text(), self.txt_role.text())
            self.update_tabprivs_list()

    def on_sel2(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_TabPrivs = {"Table_Name": self.tabprivs_list[index][1],
                                  "Privilege": self.tabprivs_list[index][3]}
            self.txt_tab.setText(self.data_TabPrivs["Table_Name"])
            self.txt_tabpriv.setText(self.data_TabPrivs["Privilege"])

    def update_tabprivs_list(self):
        self.tabprivs_list = self.user_controller2.display_tabprivs_of_user(
            self.txt_role.text())
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.tabprivs_list))
            for row, priv in enumerate(self.tabprivs_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(priv[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(priv[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(priv[2])))
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(priv[3])))
                self.table_widget.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(str(priv[4])))
# Revoke System Privs

    def Revoke_Privs_View(self):
        self.sub_window = QtWidgets.QMainWindow()
        self.sub_window.setWindowTitle(
            'USER: {0}'.format(self.txt_role.text()))
        self.user_controller3 = User_Controller()
        self.privs_list = self.user_controller3.display_privs_of_user(
            self.txt_role.text())
        self.data_Privs = {"Privilege": ""}
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(
            ['Privilege', 'Admin_Option', 'Common', 'Inherited'])
        self.table_widget.selectionModel().selectionChanged.connect(self.on_sel3)
        for priv in self.privs_list:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(
                row_position, 0, QtWidgets.QTableWidgetItem(str(priv[0])))
            self.table_widget.setItem(
                row_position, 1, QtWidgets.QTableWidgetItem(str(priv[1])))
            self.table_widget.setItem(
                row_position, 2, QtWidgets.QTableWidgetItem(str(priv[2])))
            self.table_widget.setItem(
                row_position, 3, QtWidgets.QTableWidgetItem(str(priv[3])))

        # Thiết lập layout cho widget
        # Tạo khung cuộn
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(420)
        self.scroll_area.setFixedHeight(450)

        # Đặt bảng trong khung cuộn
        self.scroll_area.setWidget(self.table_widget)

        # Đặt khung cuộn vào cửa sổ chính
        self.sub_window.setCentralWidget(self.scroll_area)

        # Thiết lập kích thước cho widget
        self.sub_window.resize(640, 480)

        # Privilege Name
        self.pri_name = QtWidgets.QLabel(self.sub_window)
        self.pri_name.setText("Privilege Name: ")
        self.pri_name.setStyleSheet("font-size: 14px;")
        self.pri_name.move(480, 0)

        self.txt_pri = QtWidgets.QLineEdit(self.sub_window)
        self.txt_pri.setFixedWidth(160)
        self.txt_pri.setText(self.data_Privs["Privilege"])
        self.txt_pri.move(440, 25)

        # Revoke Button
        self.btn_revoke2 = QtWidgets.QPushButton(self.sub_window)
        self.btn_revoke2.setText("REVOKE")
        self.btn_revoke2.setMinimumWidth(100)
        self.btn_revoke2.move(470, 75)
        self.btn_revoke2.clicked.connect(self.Revoke_Privs)

        self.sub_window.show()

    def Revoke_Privs(self):
        if self.txt_pri.text() == '':
            MessageBoxErr("Lỗi", "Vui lòng nhập tên quyền")
        else:
            self.user_controller3.Revoke_Privs_From_User(
                self.txt_pri.text(), self.txt_role.text())
            self.update_priv_list()

    def on_sel3(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.data_Privs = {"Privilege": self.privs_list[index][0]}
            self.txt_pri.setText(self.data_Privs["Privilege"])

    def update_priv_list(self):
        self.privs_list = self.user_controller3.display_privs_of_user(
            self.txt_role.text())
        if self.table_widget is not None:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.privs_list))
            for row, priv in enumerate(self.privs_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(priv[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(priv[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(priv[2])))
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(priv[3])))

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

# Variable
login_window = LoginWindow()
window_navigation = MainWindow()
role_window = RoleView()
user_window = UserList()
privileges_window = privilegesView()
table_window = TableView()
pri_window = PriView()
login_info = []

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
