---------------
--Tao role NHANVIEN va cap cac quyen connect
--DROP ROLE NHANVIEN
create role NHANVIEN;

CREATE OR REPLACE PROCEDURE Create_user_NHANVIEN
AS
    PASS VARCHAR2(30);
    --Su dung CURSOR de lay MANHANVIEN(NHANVIEN) ma chua co tai khoan nguoi dung
    CURSOR CUR IS ( SELECT USERNAME, MATKHAU 
                        FROM nvquantri.NHANVIEN
                        WHERE VAITRO ='NHANVIEN' AND  MANV NOT IN( SELECT USERNAME 
                                            FROM ALL_USERS));

    strSQL VARCHAR(2000);    -- luu tru chuoi truy van
    ck_User int;             -- luu tru ket qua kiem tra user da tao chua
    Usr varchar2(30);        -- luu tru ma doc gia duoc lay tu cursor

    BEGIN
    OPEN CUR;
    strSQL := 'ALTER SESSION SET "_ORACLE_SCRIPT"=TRUE';
    EXECUTE IMMEDIATE (strSQL);
    LOOP
        FETCH CUR INTO Usr, pass;    --Lay MANHANVIEN tu CURSOR vao bien usr
        EXIT WHEN CUR%NOTFOUND;   -- kiem tra MANHANVIEN chua co tai khoan, neu het th? thoat vong lap

        -- Tao tai khoan nguoi dung
        strSQL := 'CREATE USER '||Usr||' IDENTIFIED BY "'|| pass || '"';
        EXECUTE IMMEDIATE (strSQL);
        strSQL := 'GRANT CREATE SESSION TO '||Usr;
        EXECUTE IMMEDIATE (strSQL);
        strSQL := 'GRANT CONNECT TO '||Usr;
        EXECUTE IMMEDIATE (strSQL);
      END LOOP;
      CLOSE CUR;
    strSQL := 'ALTER SESSION SET "_ORACLE_SCRIPT"=FALSE'; 
    EXECUTE IMMEDIATE (strSQL);
    END;

EXEC Create_user_NHANVIEN

-- Gan cac user vao cac role NHANVIEN
--DROP PROCEDURE Add_User_To_RoleNHANVIEN;

CREATE OR REPLACE PROCEDURE  Add_User_To_RoleNHANVIEN
AS
    --Su dung CURSOR de lay MADOCGIA(DOCGIA) da co tai khoan nguoi dung
    CURSOR CUR IS (SELECT MANV 
                        FROM nvquantri.NHANVIEN
                            WHERE VAITRO = 'NHANVIEN' AND MANV IN (SELECT USERNAME 
                                            FROM ALL_USERS));                   
    strSQL VARCHAR(2000);
    ck_User int;
    Usr varchar2(30);
BEGIN
    OPEN CUR;
    LOOP
        FETCH CUR INTO Usr;
        EXIT WHEN CUR%NOTFOUND;

        strSQL := 'GRANT NHANVIEN TO '||Usr;
        EXECUTE IMMEDIATE (strSQL);
    END LOOP;
    CLOSE CUR;
END;
--thuc thi PROCEDURE Add_User_To_Role TAICHINH
EXEC Add_User_To_RoleNHANVIEN;

--Cac quyen cua nhanvien
grant UPDATE(NGAYSINH, DIACHI, SODT) on nvquantri.NHANVIEN to NHANVIEN;
GRANT SELECT ON nvquantri.PHANCONG TO NHANVIEN;
GRANT SELECT ON nvquantri.PHONGBAN TO NHANVIEN;
GRANT SELECT ON nvquantri.DEAN TO NHANVIEN;
GRANT CREATE VIEW TO nvquantri;

connect nvquantri/a
--DROP VIEW CS_NHANVIEN;
--bang nhanvien
CREATE OR REPLACE VIEW CS_NHANVIEN AS
        SELECT NV.MANV, NV.TENNV, NV.PHAI, NV.NGAYSINH, NV.DIACHI, NV.SODT, NV.LUONG, NV.PHUCAP, NV.VAITRO, NV.MANQL, NV.PHG, PC.MADA, PC.THOIGIAN 
        FROM nvquantri.NHANVIEN NV 
        INNER JOIN nvquantri.PHANCONG PC ON NV.MANV = PC.MANV
        WHERE NV.MANV = (SYS_CONTEXT('USERENV', 'SESSION_USER'))   
        WITH CHECK OPTION;

grant select on nvquantri.CS_NHANVIEN to NHANVIEN;