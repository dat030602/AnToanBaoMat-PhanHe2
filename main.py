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


# Controller : DBA

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

        if result:
            global login_info
            if ("DBA",) in result:
                login_info = [username_text, password_text, "DBA"]
            elif ("NHANSU",) in result:
                login_info = [username_text, password_text, "NHANSU"]
            elif ("QLTRUCTIEP",) in result:
                login_info = [username_text, password_text, "QLTRUCTIEP"]
            elif ("TRUONGPHONG",) in result:
                login_info = [username_text, password_text, "TRUONGPHONG"]
            elif ("TAICHINH",) in result:
                login_info = [username_text, password_text, "TAICHINH"]
            elif ("TRUONGDEAN",) in result:
                login_info = [username_text, password_text, "TRUONGDEAN"]
            elif ("NHANVIEN",) in result:
                login_info = [username_text, password_text, "NHANVIEN"]
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


# Controller: Nhân viên
class NhanVien_controller:
    def get_thongtin_list(self):
        sql = "select * from nvquantri.CS_NHANVIEN"
        result = execute_query(login_info[0], login_info[1], sql)
        return result

    def update_info(self, manv, ngaysinh, diachi, sodt):
        sql = "UPDATE nvquantri.CS_NHANVIEN SET NgaySinh = '{0}', DiaChi = '{1}', SoDT = '{2}' WHERE MANV = '{3}'".format(
            ngaysinh, diachi, sodt, manv)
        result, er = execute_query(login_info[0], login_info[1], sql)
        return result, er


# Controller: Đề án


class DeAn_controller:
    def get_DeAn_list(self):
        sql = "SELECT * FROM nvquantri.DEAN"
        result = execute_query(login_info[0], login_info[1], sql)
        return result

    def update_info(self, mada, tenda, ngaybd, phong):
        sql = "UPDATE nvquantri.DEAN SET TENDA = '{0}', NGAYBD = '{1}', PHONG = '{2}' WHERE MADA = '{3}'".format(
            tenda, ngaybd, phong, mada)
        result, er = execute_query(login_info[0], login_info[1], sql)
        return result, er

    def delete_info(self, mada):
        sql = "DELETE FROM nvquantri.DEAN WHERE MADA = '{0}'".format(mada)
        result, er = execute_query(login_info[0], login_info[1], sql)
        return result, er

    def add_info(self, mada, tenda, ngaybd, phong):
        sql = "INSERT INTO nvquantri.DEAN (MADA, TENDA, NGAYBD, PHONG) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
            mada, tenda, ngaybd, phong)
        result, er = execute_query(login_info[0], login_info[1], sql)
        return result, er

    def count_existing_mada(self):
        sql = "SELECT COUNT(*) FROM nvquantri.DEAN"
        result = execute_query(login_info[0], login_info[1], sql)
        return result


# Controller: Tài chính

class Taichinh_controller:
    # def search_nhanvien(self, search_text=None):
    #     sql = "select * from nvquantri.CS_NHANVIEN"
    #     if search_text:
    #         sql += f" WHERE MANV = '{search_text}'"
    #     else:
    #         sql = "select * from nvquantri.CS_NHANVIEN"

    #     result = execute_query(login_info[0], login_info[1], sql)

    #     return result

    def get_thongtin_list(self):
        sql = "select * from nvquantri.CS_NHANVIEN"
        result = execute_query(login_info[0], login_info[1], sql)
        return result

    def get_phongbandean_list(self):
        sql = "SELECT * FROM nvquantri.PHONGBAN PB JOIN nvquantri.DEAN DA ON PB.MAPB = DA.PHONG"
        result = execute_query(login_info[0], login_info[1], sql)
        return result

    def get_nhanvien_list(self):
        sql = "SELECT * FROM nvquantri.NHANVIEN"
        result = execute_query(login_info[0], login_info[1], sql)
        return result

    def update_info(self, manv, ngaysinh, diachi, sodt):
        sql = "UPDATE nvquantri.NHANVIEN SET NgaySinh = '{0}', DiaChi = '{1}', SoDT = '{2}' WHERE MANV = '{3}'".format(
            ngaysinh, diachi, sodt, manv)
        result, er = execute_query(login_info[0], login_info[1], sql)
        return result, er

    def update_nhanvien(self, manv, luong, phucap):
        sql = "UPDATE nvquantri.NHANVIEN SET LUONG = '{0}', PHUCAP = '{1}' WHERE MANV = '{2}'".format(
            luong, phucap, manv)
        result, er = execute_query(login_info[0], login_info[1], sql)
        return result, er

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
            error_obj, = er.args
            print('Error:'+str(er))
            if cur:
                cur.close()
            return False, error_obj.code


def connection2(username, password):
    try:
        con = cx_Oracle.connect(username, password, 'localhost:1521/ORCLPDB')
        return con

    except cx_Oracle.DatabaseError as er:
        error_obj, = er.args
        print('There is an error in the Oracle database:', er)
        return False, error_obj.code

    except Exception as er:
        error_obj, = er.args
        print('Error:'+str(er))
        return False, error_obj.code


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
        self.password_input.returnPressed.connect(self.enter_login)

        #  Thiết lập button login
        self.btn_login = QPushButton(self.login_window)
        self.btn_login.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_login.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_login.setText("Login")
        self.btn_login.clicked.connect(self.clicked_login)
        self.btn_login.move(300, 190)
        # thiết lập hover cursor
        

    def clicked_login(self):
        self.user_name_text = self.username_input.text()
        self.password_text = self.password_input.text()
        result = self.login_controllers.login_connect(
            self.user_name_text, self.password_text)
        if result:
            # MessageBoxInfo("Dang nhap", "Thanh cong")
            login_window.closeWindow()
            # Đăng nhập thành công, chuyển qua trang menu

            if login_info[2] == 'DBA':
                global dba_main_window
                dba_main_window.Load_Data()
                dba_main_window.showWindow()
            elif login_info[2] == 'TRUONGPHONG':
                global truongphong
                truongphong.Load_Data()
                truongphong.showWindow()
            elif login_info[2] == 'QLTRUCTIEP':
                global qltructiep
                qltructiep.Load_Data()
                qltructiep.showWindow()
                print("Comming soon")
            elif login_info[2] == 'TAICHINH':
                global taichinh_window
                taichinh_window.Load_Data()
                taichinh_window.showWindow()
            elif login_info[2] == 'NHANSU':
                global nhansu
                nhansu.Load_Data()
                nhansu.showWindow()
            elif login_info[2] == 'TRUONGDEAN':
                global dean_window
                dean_window.Load_Data()
                dean_window.showWindow()
            elif login_info[2] == 'NHANVIEN':
                global Nhanvien_windown
                Nhanvien_windown.Load_Data()
                Nhanvien_windown.showWindow()
            self.username_input.setText('')
            self.password_input.setText('')
        else:
            MessageBoxErr("Dang nhap", "That Bai")

    def enter_login(self, e):
        if e.key() == "16777220":

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
                    global taichinh_window
                    taichinh_window.Load_Data()
                    taichinh_window.showWindow()
                elif login_info[2] == 'NHANSU':
                    global nhansu
                    nhansu.Load_Data()
                    nhansu.showWindow()
                elif login_info[2] == 'TRUONGDEAN':
                    global dean_window
                    dean_window.Load_Data()
                    dean_window.showWindow()
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
        self.main_window.setWindowTitle('Thông tin cá nhân')
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
        # self.btn_back.clicked.connect(self.Backmenu)

        # Thiết lập button xóa đề án
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_back.setText("XÓA")
        self.btn_back.move(480, 160)
        # self.btn_back.clicked.connect(self.Backmenu)

        # Thiết lập button sửa đề án
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_back.setText("CHỈNH SỬA")
        self.btn_back.move(480, 220)
        # self.btn_back.clicked.connect(self.Backmenu)

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

        # Hiện thị Thông tin cá nhân
        self.button_info = QtWidgets.QPushButton(
            'Thông tin cá nhân', self.main_window)
        self.button_info.move(120, 120)
        self.button_info.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_info.clicked.connect(self.on_click_ThongTinCaNhan)

        # Hiện thị Danh sách các phân công
        self.button_role = QtWidgets.QPushButton(
            'Danh sách các phân công ', self.main_window)
        self.button_role.move(340, 120)
        self.button_role.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_role.clicked.connect(self.on_click_assignment_list)

        # Hiện thị Danh sách nhân viên của phòng
        self.button_user = QtWidgets.QPushButton(
            'Danh sách nhân viên của phòng', self.main_window)
        self.button_user.move(120, 220)
        self.button_user.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_user.clicked.connect(self.on_click_TruongPhong_ListStaff)

        # Đăng xuất
        self.button_logout = QtWidgets.QPushButton(
            'Đăng xuất', self.main_window)
        self.button_logout.move(590, 470)
        self.button_logout.setFixedSize(80, 30)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_logout.clicked.connect(self.Logout)

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

    def on_click_ThongTinCaNhan(self):
        truongphong.closeWindow()
        global window_nhanvien_ThongTinCaNhan
        window_nhanvien_ThongTinCaNhan.Load_Data()
        window_nhanvien_ThongTinCaNhan.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def Logout(self):
        # Trưởng phòng
        global truongphong
        truongphong.closeWindow()

        global login_info
        login_info = []

        global login_window
        login_window.showWindow()

        print("Logout")


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
        

        # Thiết lập button back
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("BACK")
        self.btn_back.move(610, 470)

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
        

        # Thiết lập button back
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("BACK")
        self.btn_back.move(610, 470)

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
        
        self.button_user.clicked.connect(self.on_click_pb)

        # Hiện thị danh sách role
        self.button_role = QtWidgets.QPushButton(
            'NHANVIEN', self.main_window)
        self.button_role.move(340, 120)
        self.button_role.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_role.clicked.connect(self.on_click_nv)

        # Đăng xuất
        self.button_logout = QtWidgets.QPushButton(
            'Đăng xuất', self.main_window)
        self.button_logout.move(590, 470)
        self.button_logout.setFixedSize(80, 30)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_logout.clicked.connect(self.Logout)

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

    def closeWindow(self):
        self.main_window.close()

    def Logout(self):
        # Nhân sự
        global nhansu
        nhansu.closeWindow()

        global login_info
        login_info = []

        global login_window
        login_window.showWindow()

        print("Logout")


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
        self.button_staff.clicked.connect(self.clicked_information)

        # Đăng xuất
        self.button_assign = QtWidgets.QPushButton(
            'Đăng Xuất', self.main_window)
        self.button_assign.move(380, 180)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor

    def clicked_information(self):
        Nhanvien_windown.closeWindow()
        global window_nhanvien_ThongTinCaNhan
        window_nhanvien_ThongTinCaNhan.Load_Data()
        window_nhanvien_ThongTinCaNhan.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()


class Nhanvien_ThongTinCaNhan:
    def Load_Data(self):
        self.user_list = []
        self.datalist = NhanVien_controller()

        self.manv = ''
        self.ngaysinh = ''
        self.diachi = ''
        self.sodt = ''

        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Tab 3')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)
        self.user_list = self.datalist.get_thongtin_list()

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(13)
        self.table_widget.setHorizontalHeaderLabels(
            ['MANV', 'TENNV', 'PHAI', 'NGAYSINH', 'DIACHI', 'SODT', 'LUONG', 'PHUCAP', 'VAITRO', 'MANQL', 'PHG', 'MADA', 'THOIGIAN'])
        for item in self.user_list:
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
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(item[5])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(item[6])))
            self.table_widget.setItem(
                row_position, 7, QtWidgets.QTableWidgetItem(str(item[7])))
            self.table_widget.setItem(
                row_position, 8, QtWidgets.QTableWidgetItem(str(item[8])))
            self.table_widget.setItem(
                row_position, 9, QtWidgets.QTableWidgetItem(str(item[9])))
            self.table_widget.setItem(
                row_position, 10, QtWidgets.QTableWidgetItem(str(item[10])))
            self.table_widget.setItem(
                row_position, 11, QtWidgets.QTableWidgetItem(str(item[11])))
            self.table_widget.setItem(
                row_position, 12, QtWidgets.QTableWidgetItem(str(item[12])))
        self.update_textbox_info()
        # Tạo khung cuộn
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(700)
        scroll_area.setFixedHeight(130)

        # Đặt bảng trong khung cuộn
        scroll_area.setWidget(self.table_widget)
        # # Thêm tab_widget vào QMainWindow
        self.main_window.setCentralWidget(scroll_area)

        # Thiết lập button sửa đề án
        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_update.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_update.setText("UPDATE")
        self.btn_update.move(280, 280)
        self.btn_update.clicked.connect(self.click_update)

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

    def click_update(self):
        global window_nhanvien_update
        window_nhanvien_update.Load_Data(
            self.manv, self.ngaysinh, self.diachi, self.sodt)
        window_nhanvien_update.showWindow()

    def update_info(self):
        self.user_list = self.datalist.get_thongtin_list()
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
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
                self.table_widget.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(str(user[4])))
                self.table_widget.setItem(
                    row, 5, QtWidgets.QTableWidgetItem(str(user[5])))
                self.table_widget.setItem(
                    row, 6, QtWidgets.QTableWidgetItem(str(user[6])))
                self.table_widget.setItem(
                    row, 7, QtWidgets.QTableWidgetItem(str(user[7])))
                self.table_widget.setItem(
                    row, 8, QtWidgets.QTableWidgetItem(str(user[8])))
                self.table_widget.setItem(
                    row, 9, QtWidgets.QTableWidgetItem(str(user[9])))
                self.table_widget.setItem(
                    row, 10, QtWidgets.QTableWidgetItem(str(user[10])))
                self.table_widget.setItem(
                    row, 11, QtWidgets.QTableWidgetItem(str(user[11])))
                self.table_widget.setItem(
                    row, 12, QtWidgets.QTableWidgetItem(str(user[12])))
            self.update_textbox_info()

    def update_textbox_info(self):
        self.manv = self.table_widget.item(0, 0).text()
        date_string = self.table_widget.item(0, 3).text()
        datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        self.ngaysinh = datetime_obj.strftime('%d/%m/%Y')
        self.diachi = self.table_widget.item(0, 4).text()
        self.sodt = self.table_widget.item(0, 5).text()

    def Backmenu(self):
        window_nhanvien_ThongTinCaNhan .closeWindow()
        global Nhanvien_windown
        Nhanvien_windown.Load_Data()
        Nhanvien_windown.showWindow()


class update_thongtincanhan:
    def Load_Data(self, manv, ngaysinh, diachi, sodt):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Chỉnh sửa thông tin nhân viên')
        # Thiết lập kích thước cho widget
        self.main_window.resize(600, 420)

        # Thiết lập p hiện thị MANV
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("MANV: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 40)

        # Thiết lập textbox PK
        self.textbox1 = QtWidgets.QTextEdit(self.main_window)
        self.textbox1.setReadOnly(True)  # Thiết lập ô textbox chỉ đọc

        self.textbox1.setText(manv)

        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox1.setGeometry(QtCore.QRect(250, 40, 150, 30))

        # Thiết lập p hiện thị Tên đề án
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("NGAY SINH: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 100)

        # Thiết lập textbox PK
        self.textbox2 = QtWidgets.QTextEdit(self.main_window)

        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox2.setGeometry(QtCore.QRect(250, 100, 150, 30))

        self.textbox2.setText(ngaysinh)
        self.textbox2.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị Ngày bắt đầu
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("DIA CHI: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 160)

        self.textbox3 = QtWidgets.QTextEdit(self.main_window)

        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox3.setGeometry(QtCore.QRect(250, 160, 150, 30))

        self.textbox3.setText(diachi)
        self.textbox3.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị SODT
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("SO DT: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 220)

        self.textbox4 = QtWidgets.QTextEdit(self.main_window)

        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox4.setGeometry(QtCore.QRect(250, 220, 150, 30))

        self.textbox4.setText(sodt)
        self.textbox4.setStyleSheet("color: #6C6B6A")

        # Thiết lập button update
        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setFixedSize(80, 35)  # đặt kích thước là 80 X 35 pixel
        self.btn_update.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_update.setText("UPDATE")
        self.btn_update.move(280, 300)
        self.btn_update.clicked.connect(self.clicked_update)

    def clicked_update(self):
        manv_new = self.textbox1.toPlainText()
        ngaysinh_new = self.textbox2.toPlainText()
        diachi_new = self.textbox3.toPlainText()
        sodt_new = self.textbox4.toPlainText()

        controller = NhanVien_controller()

        result, er = controller.update_info(
            manv_new, ngaysinh_new, diachi_new, sodt_new)
        if result == False:
            if er == 0:
                MessageBoxInfo("Thông Báo", "Cập nhật thành công")
            if er == 12899:
                MessageBoxErr("Thông Báo", "Số ký tự quá dài")
            if er == int('01830'):
                MessageBoxErr("Thông Báo", "Ngày tháng năm không hợp lệ")

        global window_nhanvien_ThongTinCaNhan
        window_nhanvien_ThongTinCaNhan.update_info()

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
            'Quản lý nhân viên', self.main_window)
        self.button_staff.move(120, 100)
        self.button_staff.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_staff.clicked.connect(self.clicked_staff)

        # Hiện thị danh sách thông tin phân công
        self.button_assign = QtWidgets.QPushButton(
            'Thông tin cá nhân', self.main_window)
        self.button_assign.move(380, 100)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor
        self.button_assign.clicked.connect(self.clicked_infomation)

        # Hiện thị danh sách thông tin cá nhân
        self.button_assign = QtWidgets.QPushButton(
            'Xem phòng ban và đề án', self.main_window)
        self.button_assign.move(120, 220)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor
        self.button_assign.clicked.connect(self.clicked_Department)

        # Hiện thị danh sách phòng ban đề án
        self.button_assign = QtWidgets.QPushButton(
            'Đăng xuất', self.main_window)
        self.button_assign.move(380, 220)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor

        # Đăng xuất
        self.button_logout = QtWidgets.QPushButton(
            'Đăng xuất', self.main_window)
        self.button_logout.move(590, 470)
        self.button_logout.setFixedSize(80, 30)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_logout.clicked.connect(self.Logout)

    def clicked_staff(self):
        taichinh_window.closeWindow()
        global window_taichinh_ThongTinNhanVien
        window_taichinh_ThongTinNhanVien.Load_Data()
        window_taichinh_ThongTinNhanVien.showWindow()

    def clicked_infomation(self):
        taichinh_windown.closeWindow()
        global window_taichinh_ThongTincanhan
        window_taichinh_ThongTincanhan.Load_Data()
        window_taichinh_ThongTincanhan.showWindow()

    def clicked_Department(self):
        taichinh_windown.closeWindow()
        global window_TaiChinh_PhongBanDeAn
        window_TaiChinh_PhongBanDeAn.Load_Data()
        window_TaiChinh_PhongBanDeAn.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def Logout(self):

        # Tài chính
        global taichinh_window
        taichinh_window.closeWindow()

        global login_info
        login_info = []

        global login_window
        login_window.showWindow()

        print("Logout")


class TaiChinh_ThongTinNhanVien:
    def Load_Data(self):
        self.user_list = []

        self.datalist = Taichinh_controller()

        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Tab 1')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)

        self.user_list = self.datalist.get_nhanvien_list()

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(11)
        self.table_widget.setHorizontalHeaderLabels(
            ['MANV', 'TENNV', 'PHAI', 'NGAYSINH', 'DIACHI', 'SODT', 'LUONG', 'PHUCAP', 'VAITRO', 'MANQL', 'PHG'])

        self.table_widget.cellClicked.connect(self.display_textbox)

        for item in self.user_list:
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
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(item[5])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(item[6])))
            self.table_widget.setItem(
                row_position, 7, QtWidgets.QTableWidgetItem(str(item[7])))
            self.table_widget.setItem(
                row_position, 8, QtWidgets.QTableWidgetItem(str(item[8])))
            self.table_widget.setItem(
                row_position, 9, QtWidgets.QTableWidgetItem(str(item[9])))
            self.table_widget.setItem(
                row_position, 10, QtWidgets.QTableWidgetItem(str(item[10])))
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
        self.btn_update.clicked.connect(self.clicked_update)

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

    def display_textbox(self, row):
        manv_item = self.table_widget.item(row, 0)
        manv = manv_item.text()
        self.textbox1.setText(manv)

        luong_item = self.table_widget.item(row, 6)
        luong = luong_item.text()
        self.textbox2.setText(luong)
        self.textbox2.setStyleSheet("color: #6C6B6A")

        phucap_item = self.table_widget.item(row, 7)
        phucap = phucap_item.text()
        self.textbox3.setText(phucap)
        self.textbox3.setStyleSheet("color: #6C6B6A")

    def clicked_update(self):
        self.user_list = self.datalist.get_nhanvien_list()
        manv_new = self.textbox1.toPlainText()
        luong_new = self.textbox2.toPlainText()
        phucap_new = self.textbox3.toPlainText()
        controller = Taichinh_controller()
        result, er = controller.update_nhanvien(
            manv_new, luong_new, phucap_new)
        self.update_info()

        if result == False:
            if er == 0:
                MessageBoxInfo("Thông Báo", "Cập nhật thành công")
            if er == 12899:
                MessageBoxErr("Thông Báo", "Số ký tự quá dài")
            if er == int('01722'):
                MessageBoxErr("Thông Báo", "kiểu dữ liệu không hợp lệ")

    def update_info(self):
        self.user_list = self.datalist.get_nhanvien_list()
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
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
                self.table_widget.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(str(user[4])))
                self.table_widget.setItem(
                    row, 5, QtWidgets.QTableWidgetItem(str(user[5])))
                self.table_widget.setItem(
                    row, 6, QtWidgets.QTableWidgetItem(str(user[6])))
                self.table_widget.setItem(
                    row, 7, QtWidgets.QTableWidgetItem(str(user[7])))
                self.table_widget.setItem(
                    row, 8, QtWidgets.QTableWidgetItem(str(user[8])))
                self.table_widget.setItem(
                    row, 9, QtWidgets.QTableWidgetItem(str(user[9])))
                self.table_widget.setItem(
                    row, 10, QtWidgets.QTableWidgetItem(str(user[10])))
                self.table_widget.setItem(
                    row, 11, QtWidgets.QTableWidgetItem(str(user[11])))
                self.table_widget.setItem(
                    row, 12, QtWidgets.QTableWidgetItem(str(user[12])))

    def Backmenu(self):
        window_taichinh_ThongTinNhanVien.closeWindow()
        global taichinh_windown
        taichinh_windown.Load_Data()
        taichinh_windown.showWindow()


class TaiChinh_ThongTinCaNhan:
    def Load_Data(self):
        self.user_list = []
        self.datalist = Taichinh_controller()

        self.manv = ''
        self.ngaysinh = ''
        self.diachi = ''
        self.sodt = ''

        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Tab 3')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)
        self.user_list = self.datalist.get_thongtin_list()

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(13)
        self.table_widget.setHorizontalHeaderLabels(
            ['MANV', 'TENNV', 'PHAI', 'NGAYSINH', 'DIACHI', 'SODT', 'LUONG', 'PHUCAP', 'VAITRO', 'MANQL', 'PHG', 'MADA', 'THOIGIAN'])
        for item in self.user_list:
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
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(item[5])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(item[6])))
            self.table_widget.setItem(
                row_position, 7, QtWidgets.QTableWidgetItem(str(item[7])))
            self.table_widget.setItem(
                row_position, 8, QtWidgets.QTableWidgetItem(str(item[8])))
            self.table_widget.setItem(
                row_position, 9, QtWidgets.QTableWidgetItem(str(item[9])))
            self.table_widget.setItem(
                row_position, 10, QtWidgets.QTableWidgetItem(str(item[10])))
            self.table_widget.setItem(
                row_position, 11, QtWidgets.QTableWidgetItem(str(item[11])))
            self.table_widget.setItem(
                row_position, 12, QtWidgets.QTableWidgetItem(str(item[12])))
        self.update_textbox_info()
        # Tạo khung cuộn
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(700)
        scroll_area.setFixedHeight(130)

        # Đặt bảng trong khung cuộn
        scroll_area.setWidget(self.table_widget)
        # # Thêm tab_widget vào QMainWindow
        self.main_window.setCentralWidget(scroll_area)

        # Thiết lập button sửa đề án
        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_update.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_update.setText("UPDATE")
        self.btn_update.move(280, 280)
        self.btn_update.clicked.connect(self.click_update)

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

    def click_update(self):
        global window_taichinh_update
        window_taichinh_update.Load_Data(
            self.manv, self.ngaysinh, self.diachi, self.sodt)
        window_taichinh_update.showWindow()

    def update_info(self):
        self.user_list = self.datalist.get_thongtin_list()
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
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(user[3])))
                self.table_widget.setItem(
                    row, 4, QtWidgets.QTableWidgetItem(str(user[4])))
                self.table_widget.setItem(
                    row, 5, QtWidgets.QTableWidgetItem(str(user[5])))
                self.table_widget.setItem(
                    row, 6, QtWidgets.QTableWidgetItem(str(user[6])))
                self.table_widget.setItem(
                    row, 7, QtWidgets.QTableWidgetItem(str(user[7])))
                self.table_widget.setItem(
                    row, 8, QtWidgets.QTableWidgetItem(str(user[8])))
                self.table_widget.setItem(
                    row, 9, QtWidgets.QTableWidgetItem(str(user[9])))
                self.table_widget.setItem(
                    row, 10, QtWidgets.QTableWidgetItem(str(user[10])))
                self.table_widget.setItem(
                    row, 11, QtWidgets.QTableWidgetItem(str(user[11])))
                self.table_widget.setItem(
                    row, 12, QtWidgets.QTableWidgetItem(str(user[12])))
            self.update_textbox_info()

    def update_textbox_info(self):
        self.manv = self.table_widget.item(0, 0).text()
        date_string = self.table_widget.item(0, 3).text()
        datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        self.ngaysinh = datetime_obj.strftime('%d/%m/%Y')
        self.diachi = self.table_widget.item(0, 4).text()
        self.sodt = self.table_widget.item(0, 5).text()

    def Backmenu(self):
        window_taichinh_ThongTincanhan.closeWindow()
        global taichinh_windown
        taichinh_windown.Load_Data()
        taichinh_windown.showWindow()


class TaiChinh_PhongBanDeAn:
    def Load_Data(self):

        self.datalist = Taichinh_controller()
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Tab 3')
        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)
        self.itemlist = self.datalist.get_phongbandean_list()

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()
        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(
            ['MAPB', 'TENPB', 'TRPHG', 'MADA', 'TENDA', 'NGAYBD', 'PHONG'])

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
            self.table_widget.setItem(
                row_position, 4, QtWidgets.QTableWidgetItem(str(item[4])))
            self.table_widget.setItem(
                row_position, 5, QtWidgets.QTableWidgetItem(str(item[5])))
            self.table_widget.setItem(
                row_position, 6, QtWidgets.QTableWidgetItem(str(item[6])))
        # Tạo khung cuộn
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedWidth(580)
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

    def Backmenu(self):

        window_TaiChinh_PhongBanDeAn.closeWindow()
        global taichinh_window

        taichinh_window.Load_Data()
        taichinh_window.showWindow()


class update_nhanvien:
    def Load_Data(self, manv, ngaysinh, diachi, sodt):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Chỉnh sửa thông tin nhân viên')
        # Thiết lập kích thước cho widget
        self.main_window.resize(600, 420)

        # Thiết lập p hiện thị MANV
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("MANV: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 40)

        # Thiết lập textbox PK
        self.textbox1 = QtWidgets.QTextEdit(self.main_window)
        self.textbox1.setReadOnly(True)  # Thiết lập ô textbox chỉ đọc

        self.textbox1.setText(manv)

        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox1.setGeometry(QtCore.QRect(250, 40, 150, 30))

        # Thiết lập p hiện thị Tên đề án
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("NGAY SINH: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 100)

        # Thiết lập textbox PK
        self.textbox2 = QtWidgets.QTextEdit(self.main_window)

        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox2.setGeometry(QtCore.QRect(250, 100, 150, 30))

        self.textbox2.setText(ngaysinh)
        self.textbox2.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị Ngày bắt đầu
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("DIA CHI: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 160)

        self.textbox3 = QtWidgets.QTextEdit(self.main_window)

        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox3.setGeometry(QtCore.QRect(250, 160, 150, 30))

        self.textbox3.setText(diachi)
        self.textbox3.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị SODT
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("SO DT: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 220)

        self.textbox4 = QtWidgets.QTextEdit(self.main_window)

        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox4.setGeometry(QtCore.QRect(250, 220, 150, 30))

        self.textbox4.setText(sodt)
        self.textbox4.setStyleSheet("color: #6C6B6A")

        # Thiết lập button update
        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setFixedSize(80, 35)  # đặt kích thước là 80 X 35 pixel
        self.btn_update.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_update.setText("UPDATE")
        self.btn_update.move(280, 300)
        self.btn_update.clicked.connect(self.clicked_update)

    def clicked_update(self):
        manv_new = self.textbox1.toPlainText()
        ngaysinh_new = self.textbox2.toPlainText()
        diachi_new = self.textbox3.toPlainText()
        sodt_new = self.textbox4.toPlainText()
        controller = Taichinh_controller()
        result, er = controller.update_info(
            manv_new, ngaysinh_new, diachi_new, sodt_new)
        if result == False:
            if er == 0:
                MessageBoxInfo("Thông Báo", "Cập nhật thành công")
            if er == 12899:
                MessageBoxErr("Thông Báo", "Số ký tự quá dài")
            if er == int('01830'):
                MessageBoxErr("Thông Báo", "Ngày tháng năm không hợp lệ")

        global window_taichinh_ThongTincanhan
        window_taichinh_ThongTincanhan.update_info()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

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
        self.button_staff.clicked.connect(self.clicked_scheme)

        # Đăng xuất
        self.button_assign = QtWidgets.QPushButton(
            'Đăng Xuất', self.main_window)
        self.button_assign.move(380, 180)
        # Thiết lập kích thước cố định
        self.button_assign.setFixedSize(180, 60)
        # thiết lập hover cursor

        # Đăng xuất
        self.button_logout = QtWidgets.QPushButton(
            'Đăng xuất', self.main_window)
        self.button_logout.move(590, 470)
        self.button_logout.setFixedSize(80, 30)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_logout.clicked.connect(self.Logout)

    def clicked_scheme(self):
        dean_window.closeWindow()
        global window_danhsachdean
        window_danhsachdean.Load_Data()
        window_danhsachdean.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def Logout(self):
        # Đề án
        global dean_window
        dean_window.closeWindow()

        global login_info
        login_info = []

        global login_window
        login_window.showWindow()

        print("Logout")


class DanhSachDeAn_view:
    def Load_Data(self):
        self.user_list = []
        self.datalist = DeAn_controller()

        self.MADA = ''
        self.TENDA = ''
        self.NGAYBD = ''
        self.PHONG = ''
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Danh sách đề án')

        # Thiết lập kích thước cho widget
        self.main_window.resize(700, 520)
        self.user_list = self.datalist.get_DeAn_list()

        # Khởi tạo table widget để hiển thị danh sách người dùng
        self.table_widget = QtWidgets.QTableWidget()

        # Đặt số lượng cột cho table widget
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(
            ['MADA', 'TENDA', 'NGAYBD', 'PHONG'])

        self.table_widget.cellClicked.connect(self.display_textbox)

        for item in self.user_list:
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
        self.table_widget.cellClicked.connect(self.update_textbox_info)
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
        self.textbox1.setGeometry(QtCore.QRect(510, 40, 140, 30))

        # Thiết lập p hiện thị MADA
        self.text_MADA = QtWidgets.QLabel(self.main_window)
        self.text_MADA.setText("MADA : ")
        self.text_MADA.setStyleSheet("font-size: 15px;")
        self.text_MADA.adjustSize()
        self.text_MADA.move(430, 40)

        # Thiết lập kích thước và vị trí cho ô textbox thứ hai
        self.textbox2.setGeometry(QtCore.QRect(510, 100, 140, 30))

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
        self.btn_add.clicked.connect(self.click_add)

        # Thiết lập button xóa đề án
        self.btn_delete = QtWidgets.QPushButton(self.main_window)
        self.btn_delete.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_delete.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_delete.setText("XÓA")
        self.btn_delete.move(500, 240)
        self.btn_delete.clicked.connect(self.clicked_delete)

        # Thiết lập button sửa đề án
        self.btn_update = QtWidgets.QPushButton(self.main_window)
        self.btn_update.setFixedSize(100, 35)  # đặt kích thước là 40x40 pixel
        self.btn_update.setStyleSheet('background-color: #999999; color: #fff')
        self.btn_update.setText("CHỈNH SỬA")
        self.btn_update.move(500, 300)
        self.btn_update.clicked.connect(self.click_update)

        # Thiết lập button back
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("BACK")
        self.btn_back.move(610, 470)
        self.btn_back.clicked.connect(self.Backmenu)

    def display_textbox(self, row):
        mada_item = self.table_widget.item(row, 0)
        mada = mada_item.text()
        self.textbox1.setText(mada)

        ten_item = self.table_widget.item(row, 1)
        tenda = ten_item.text()
        self.textbox2.setText(tenda)
        self.textbox2.setStyleSheet("color: #6C6B6A")

    def update_info(self):
        self.user_list = self.datalist.get_DeAn_list()

        if self.table_widget is not None:
            self.table_widget.clearContents()  # xoa bang cu
            self.table_widget.setRowCount(0)
            self.table_widget.setRowCount(len(self.user_list))

            for row, user in enumerate(self.user_list):
                self.table_widget.setItem(
                    row, 0, QtWidgets.QTableWidgetItem(str(user[0])))
                self.table_widget.setItem(
                    row, 1, QtWidgets.QTableWidgetItem(str(user[1])))
                self.table_widget.setItem(
                    row, 2, QtWidgets.QTableWidgetItem(str(user[2])))
                self.table_widget.setItem(
                    row, 3, QtWidgets.QTableWidgetItem(str(user[3])))

            self.table_widget.cellClicked.connect(self.update_textbox_info)

    def update_textbox_info(self, row):

        self.MADA = self.table_widget.item(row, 0).text()
        self.TENDA = self.table_widget.item(row, 1).text()
        date_string = self.table_widget.item(row, 2).text()
        datetime_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        self.NGAYBD = datetime_obj.strftime('%d/%m/%Y')
        self.PHONG = self.table_widget.item(row, 3).text()

    def clicked_delete(self):
        MADA_remove = self.MADA
        controller = DeAn_controller()
        result, er = controller.delete_info(MADA_remove)
        if result == False:
            if er == int('02292'):
                MessageBoxErr("Thông báo", 'Không thể xóa')

        self.update_info()

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

        if self.MADA == '':
            MessageBoxWarn("Thông Báo", "Vui lòng chọn thông tin đề án")
            return
        window_dean_update.Load_Data(
            self.MADA, self.TENDA, self.NGAYBD, self.PHONG)

        window_dean_update.showWindow()

    def Backmenu(self):

        window_danhsachdean.closeWindow()
        global dean_window

        dean_window.Load_Data()
        dean_window.showWindow()


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

        self.textbox1 = QtWidgets.QTextEdit(self.main_window)
        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox1.setGeometry(QtCore.QRect(250, 45, 170, 30))
        # self.textbox1.setText(diachi)
        self.textbox1.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị Ngày bắt đầu
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Ngày BD : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 120)

        self.textbox2 = QtWidgets.QTextEdit(self.main_window)
        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox2.setGeometry(QtCore.QRect(250, 115, 170, 30))
        # self.textbox1.setText(diachi)
        self.textbox2.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị Phòng
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Phòng : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 200)

        self.textbox3 = QtWidgets.QTextEdit(self.main_window)
        # Thiết lập kích thước và vị trí cho ô textbox
        self.textbox3.setGeometry(QtCore.QRect(250, 195, 170, 30))
        # self.textbox1.setText(diachi)
        self.textbox3.setStyleSheet("color: #6C6B6A")

        # Thiết lập button add
        self.btn_add = QtWidgets.QPushButton(self.main_window)
        self.btn_add.setFixedSize(60, 30)  # đặt kích thước là 40x40 pixel
        self.btn_add.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_add.setText("ADD")
        self.btn_add.move(300, 270)
        self.btn_add.clicked.connect(self.clicked_add)

    def clicked_add(self):
        controller = DeAn_controller()
        existing_mada_count = controller.count_existing_mada()
        count = existing_mada_count[0][0]
        mada_new = 'DA' + str(count + 1)
        tenda_new = self.textbox1.toPlainText()
        ngaybd_new = self.textbox2.toPlainText()
        phong_new = self.textbox3.toPlainText()

        controller = DeAn_controller()

        result, er = controller.add_info(
            mada_new, tenda_new, ngaybd_new, phong_new)

        if result == False:
            if er == 0:
                MessageBoxInfo("Thông Báo", "Thêm thành công")

            if er == 12899:
                MessageBoxErr("Thông Báo", "Số ký tự quá dài")

            if er == int('01830'):
                MessageBoxErr("Thông Báo", "Ngày tháng năm không hợp lệ")

            if er == int('02291'):
                MessageBoxErr("Thông Báo", "Mã phòng không tồn tại")

            if er == int('01843'):
                MessageBoxErr("Thông Báo", "Ngày tháng năm không hợp lệ")

            if er == int('00001'):
                MessageBoxErr("Thông Báo", "Mã đề án đã tồn tại")
                mada_new = 'DA' + str(count + 1)

            if er == int('01400'):
                MessageBoxErr("Thông Báo", "Thông tin không để rỗng")

        global window_danhsachdean
        window_danhsachdean.update_info()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()


class update_dean:
    def Load_Data(self, MADA, TENDA, NGAYBD, PHONG):
        # Khởi tạo đối tượng QMainWindow
        self.main_window = QtWidgets.QMainWindow()

        # Thiết lập tiêu đề cho cửa sổ
        self.main_window.setWindowTitle('Chỉnh sửa đề án')
        # Thiết lập kích thước cho widget
        self.main_window.resize(600, 420)

        # Thiết lập p hiện thị Mã đề án
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Mã đề án: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 40)

        # Thiết lập textbox PK
        self.textbox1 = QtWidgets.QTextEdit(self.main_window)
        self.textbox1.setReadOnly(True)  # Thiết lập ô textbox chỉ đọc
        self.textbox1.setText(MADA)
        self.textbox1.setGeometry(QtCore.QRect(250, 40, 150, 30))
        self.textbox1.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị Tên đề án
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Tên Đề Án: ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 100)

        # Thiết lập textbox PK
        self.textbox2 = QtWidgets.QTextEdit(self.main_window)
        self.textbox2.setText(TENDA)
        self.textbox2.setGeometry(QtCore.QRect(250, 100, 150, 30))
        self.textbox2.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị Ngày bắt đầu
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Ngày BD : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 160)

        # Thiết lập textbox PK
        self.textbox3 = QtWidgets.QTextEdit(self.main_window)
        self.textbox3.setText(NGAYBD)
        self.textbox3.setGeometry(QtCore.QRect(250, 160, 150, 30))
        self.textbox3.setStyleSheet("color: #6C6B6A")

        # Thiết lập p hiện thị Phòng
        self.text_Manv = QtWidgets.QLabel(self.main_window)
        self.text_Manv.setText("Phòng : ")
        self.text_Manv.setStyleSheet("font-size: 15px;")
        self.text_Manv.adjustSize()
        self.text_Manv.move(100, 220)

        # Thiết lập textbox PK
        self.textbox4 = QtWidgets.QTextEdit(self.main_window)
        self.textbox4.setText(PHONG)
        self.textbox4.setGeometry(QtCore.QRect(250, 220, 150, 30))
        self.textbox4.setStyleSheet("color: #6C6B6A")

        # Thiết lập button update
        self.btn_back = QtWidgets.QPushButton(self.main_window)
        self.btn_back.setFixedSize(80, 35)  # đặt kích thước là 80 X 35 pixel
        self.btn_back.setStyleSheet('background-color: #3450D9; color: #fff')
        self.btn_back.setText("Update")
        self.btn_back.move(300, 270)
        self.btn_back.clicked.connect(self.clicked_update)

    def clicked_update(self):
        mada_new = self.textbox1.toPlainText()
        tenda_new = self.textbox2.toPlainText()
        ngaybd_new = self.textbox3.toPlainText()
        phong = self.textbox4.toPlainText()
        controller = DeAn_controller()

        result, er = controller.update_info(
            mada_new, tenda_new, ngaybd_new, phong)
        if result == False:
            if er == 0:
                MessageBoxInfo("Thông Báo", "Cập nhật thành công")
            if er == 12899:
                MessageBoxErr("Thông Báo", "Số ký tự quá dài")
            if er == int('01830'):
                MessageBoxErr("Thông Báo", "Ngày tháng năm không hợp lệ")
            if er == int('02291'):
                MessageBoxErr("Thông Báo", "Mã phòng ban không tồn tài")

        global window_danhsachdean
        window_danhsachdean.update_info()

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
        
        self.button_user.clicked.connect(self.on_click_pc)

        # Hiện thị danh sách role
        self.button_role = QtWidgets.QPushButton(
            'NHANVIEN', self.main_window)
        self.button_role.move(340, 120)
        self.button_role.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_role.clicked.connect(self.on_click_nv)

        # Đăng xuất
        self.button_logout = QtWidgets.QPushButton(
            'Đăng xuất', self.main_window)
        self.button_logout.move(590, 470)
        self.button_logout.setFixedSize(80, 30)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_logout.clicked.connect(self.Logout)

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

    def closeWindow(self):
        self.main_window.close()

    def Logout(self):
        # Quản lý trực tiếp
        global qltructiep
        qltructiep.closeWindow()

        global login_info
        login_info = []

        global login_window
        login_window.showWindow()

        print("Logout")


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

# View: DBA


class DBA_MainWindown:
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
        
        self.button_user.clicked.connect(self.on_click_user)

        # Hiện thị danh sách role
        self.button_role = QtWidgets.QPushButton(
            'Danh sách role', self.main_window)
        self.button_role.move(340, 120)
        self.button_role.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_role.clicked.connect(self.on_click_role)

        # Hiện thị danh sách quyền của role/user
        self.button_pri = QtWidgets.QPushButton(
            'Danh sách quyền User/Role', self.main_window)
        self.button_pri.move(120, 220)
        self.button_pri.setFixedSize(180, 60)  # Thiết lập kích thước cố định

        # thiết lập hover cursor
        
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
        
        self.button_pri1.clicked.connect(self.on_click_pri)

        # thiết lập hover cursor
        self.button_table.clicked.connect(self.on_click_table)

        # Đăng xuất
        self.button_logout = QtWidgets.QPushButton(
            'Đăng xuất', self.main_window)
        self.button_logout.move(590, 470)
        self.button_logout.setFixedSize(80, 30)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        
        self.button_logout.clicked.connect(self.Logout)

    def on_click_user(self):
        dba_main_window.closeWindow()
        global dba_user_window
        dba_user_window.Load_Data()
        dba_user_window.showWindow()

    def on_click_role(self):
        dba_main_window.closeWindow()
        global dba_role_window
        dba_role_window.Load_Data()
        dba_role_window.showWindow()

    def on_click_privileges(self):
        dba_main_window.closeWindow()
        global dba_privileges_window
        dba_privileges_window.Load_Data()
        dba_privileges_window.showWindow()

    def on_click_table(self):
        dba_main_window.closeWindow()
        global dba_table_window
        dba_table_window.Load_Data()
        dba_table_window.showWindow()

    def on_click_pri(self):
        dba_main_window.closeWindow()
        global dba_pri_window
        dba_pri_window.Load_Data()
        dba_pri_window.showWindow()

    def closeWindow(self):
        self.main_window.hide()

    def showWindow(self):
        self.main_window.show()

    def Logout(self):
        # DBA
        global dba_main_window
        dba_main_window.closeWindow()

        global login_info
        login_info = []

        global login_window
        login_window.showWindow()

        print("Logout")


class DBA_PriView:
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
        dba_pri_window.closeWindow()
        dba_main_window.showWindow()

    def on_selectionChanged(self, selected, deselected):
        for ix in selected.indexes():
            index = int(format(ix.row()))
            self.table_selected = self.user_list[index][0]


class DBA_RoleView:
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

        self.btn_back.clicked.connect(self.Backmenu)

    def Backmenu(self):
        dba_role_window.closeWindow()
        dba_main_window.showWindow()

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


class DBA_TableView:
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
        dba_table_window.closeWindow()
        dba_main_window.showWindow()

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


class DBA_UserList:
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
        dba_user_window.closeWindow()
        dba_main_window.showWindow()

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


class DBA_privilegesView:
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
        dba_privileges_window.closeWindow()
        dba_main_window.showWindow()


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
window_nhanvien_ThongTinCaNhan = Nhanvien_ThongTinCaNhan()
window_nhanvien_update = update_thongtincanhan()

# Đề án
dean_window = DeAn_view()
window_danhsachdean = DanhSachDeAn_view()
window_dean_add = add_dean()
window_dean_update = update_dean()

# Tài chính
taichinh_window = Taichinh_view()
window_taichinh_ThongTincanhan = TaiChinh_ThongTinCaNhan()
window_taichinh_ThongTinNhanVien = TaiChinh_ThongTinNhanVien()
window_TaiChinh_PhongBanDeAn = TaiChinh_PhongBanDeAn()
window_taichinh_update = update_nhanvien()

# Quản lý trực tiếp
qltructiep = Role_QLTructiep()
pc_window = QL_Phancongview()
pc_window2 = QL_Nhanvienview()
login_info = []

# DBA
dba_main_window = DBA_MainWindown()
dba_role_window = DBA_RoleView()
dba_user_window = DBA_UserList()
dba_privileges_window = DBA_privilegesView()
dba_table_window = DBA_TableView()
dba_pri_window = DBA_PriView()

#################################################################


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
