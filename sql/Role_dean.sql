---------------
--Tao role TRUONGDEAN va cap cac quyen connect
--DROP ROLE TRUONGDEAN
create role TRUONGDEAN;

CREATE OR REPLACE PROCEDURE Create_user_TRUONGDEAN
AS
    PASS VARCHAR2(30);
    --Su dung CURSOR de lay MATRUONGDEAN(TRUONGDEAN) ma chua co tai khoan nguoi dung
    CURSOR CUR IS ( SELECT USERNAME, MATKHAU 
                        FROM nvquantri.NHANVIEN
                        WHERE VAITRO ='TRUONGDEAN' AND  MANV NOT IN( SELECT USERNAME 
                                            FROM ALL_USERS));

    strSQL VARCHAR(2000);    -- luu tru chuoi truy van
    ck_User int;             -- luu tru ket qua kiem tra user da tao chua
    Usr varchar2(30);        -- luu tru ma doc gia duoc lay tu cursor

    BEGIN
    OPEN CUR;
    strSQL := 'ALTER SESSION SET "_ORACLE_SCRIPT"=TRUE';
    EXECUTE IMMEDIATE (strSQL);
    LOOP
        FETCH CUR INTO Usr, pass;    --Lay MATRUONGDEAN tu CURSOR vao bien usr
        EXIT WHEN CUR%NOTFOUND;   -- kiem tra MATRUONGDEAN chua co tai khoan, neu het th? thoat vong lap

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

EXEC Create_user_TRUONGDEAN

-- Gan cac user vao cac role TRUONGDEAN
--DROP PROCEDURE Add_User_To_RoleTRUONGDEAN;

CREATE OR REPLACE PROCEDURE  Add_User_To_RoleTRUONGDEAN
AS
    --Su dung CURSOR de lay MADOCGIA(DOCGIA) da co tai khoan nguoi dung
    CURSOR CUR IS (SELECT MANV 
                        FROM nvquantri.NHANVIEN
                            WHERE VAITRO = 'TRUONGDEAN' AND MANV IN (SELECT USERNAME 
                                            FROM ALL_USERS));                   
    strSQL VARCHAR(2000);
    ck_User int;
    Usr varchar2(30);
BEGIN
    OPEN CUR;
    LOOP
        FETCH CUR INTO Usr;
        EXIT WHEN CUR%NOTFOUND;

        strSQL := 'GRANT TRUONGDEAN TO '||Usr;
        EXECUTE IMMEDIATE (strSQL);
    END LOOP;
    CLOSE CUR;
END;
--thuc thi PROCEDURE Add_User_To_Role TAICHINH
EXEC Add_User_To_RoleTRUONGDEAN;


--Cac quyen cua nhanvien
grant UPDATE(NGAYSINH, DIACHI, SODT) on nvquantri.NHANVIEN to TRUONGDEAN;
GRANT SELECT ON nvquantri.PHANCONG TO TRUONGDEAN;
GRANT SELECT ON nvquantri.PHONGBAN TO TRUONGDEAN;
GRANT SELECT ON nvquantri.DEAN TO TRUONGDEAN;

--Cac quyen cua TRUONGDEAN
grant UPDATE,INSERT,SELECT,DELETE on nvquantri.DEAN to TRUONGDEAN;

GRANT CREATE VIEW TO nvquantri;
connect nvquantri/a
--DROP VIEW CS_TRUONGDEAN;
--bang TRUONGDEAN
CREATE OR REPLACE VIEW CS_TRUONGDEAN AS
        SELECT NV.MANV, NV.TENNV, NV.PHAI, NV.NGAYSINH, NV.DIACHI, NV.SODT, NV.LUONG, NV.PHUCAP, NV.VAITRO, NV.MANQL, NV.PHG, PC.MADA, PC.THOIGIAN 
        FROM nvquantri.NHANVIEN NV 
        INNER JOIN nvquantri.PHANCONG PC ON NV.MANV = PC.MANV
        WHERE NV.MANV = (SYS_CONTEXT('USERENV', 'SESSION_USER'))
        WITH CHECK OPTION;

grant select on nvquantri.CS_TRUONGDEAN to TRUONGDEAN;