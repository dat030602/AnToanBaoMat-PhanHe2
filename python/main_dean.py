from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt
import sys
import cx_Oracle

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
        
class DeAn_controller:
    def get_DeAn_list(self):
        sql = "SELECT * FROM DEAN"
        result = execute_query('Truongphong','123',sql)
        return result

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
        self.button_staff.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.button_staff.clicked.connect(self.clicked_scheme)

        # Đăng xuất
        self.button_assign = QtWidgets.QPushButton(
            'Đăng Xuất', self.main_window)
        self.button_assign.move(380, 180)
        self.button_assign.setFixedSize(180, 60)  # Thiết lập kích thước cố định
        # thiết lập hover cursor
        self.button_assign.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

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
        self.textbox1.setGeometry(QtCore.QRect(510, 40, 100,30))

        # Thiết lập p hiện thị MADA
        self.text_MADA = QtWidgets.QLabel(self.main_window)
        self.text_MADA.setText("MADA : ")
        self.text_MADA.setStyleSheet("font-size: 15px;")
        self.text_MADA.adjustSize()
        self.text_MADA.move(430, 40)

        # Thiết lập kích thước và vị trí cho ô textbox thứ hai
        self.textbox2.setGeometry(QtCore.QRect(510, 100, 100,30))

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


dean_windown = DeAn_view()
window_danhsachdean = DanhSachDeAn_view()
window_dean_add = add_dean()
window_dean_update =update_dean()

def main():
    # lib_dir = "D:\Download\instantclient-basic-windows.x64-21.9.0.0.0dbru\instantclient_21_9"
    # global oracle_client_initialized
    # oracle_client_initialized = False
    # if not oracle_client_initialized:
    #      try:
    #          cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    #          oracle_client_initialized = True
    #      except Exception as err:
    #          print("Error initializing Oracle Client:", err)
    #          sys.exit(1)
    app = QtWidgets.QApplication(sys.argv)
    global dean_windown
    dean_windown.Load_Data()
    dean_windown.showWindow()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()