--Admin
--Phan he 1:
--drop USER NVQuanTri CASCADE;
CREATE USER NVQuanTri IDENTIFIED BY a;
GRANT CREATE SESSION TO NVQuanTri WITH ADMIN OPTION;
GRANT CONNECT TO NVQuanTri WITH ADMIN OPTION;

GRANT CREATE ROLE TO NVQuanTri WITH ADMIN OPTION;
GRANT ALTER USER TO NVQuanTri WITH ADMIN OPTION;
GRANT CREATE USER TO NVQuanTri WITH ADMIN OPTION;
GRANT ALTER ANY ROLE TO NVQuanTri WITH ADMIN OPTION;
GRANT DROP USER TO NVQuanTri WITH ADMIN OPTION;
GRANT DROP ANY ROLE TO NVQuanTri WITH ADMIN OPTION;
GRANT SELECT ANY DICTIONARY TO NVQuanTri WITH ADMIN OPTION;
GRANT CREATE ANY VIEW TO NVQUANTRI WITH ADMIN OPTION;
GRANT DBA TO NVQUANTRI WITH ADMIN OPTION;
grant execute on sys.dbms_crypto to NVQUANTRI;

------------------------------------------------------------------------------
CONNECT NVQuanTri/a;

alter table NHANVIEN drop constraint FK_NHANVIEN_MANQL;
alter table NHANVIEN drop constraint FK_NHANVIEN_PHG;
alter table PHONGBAN drop constraint FK_PHONGBAN_TRPHG;
alter table DEAN drop constraint FK_DEAN_PHONG;
alter table PHANCONG drop constraint FK_PHANCONG_PHG;
alter table PHANCONG drop constraint FK_PHANCONG_MANV;

drop table NHANVIEN;
drop table PHONGBAN;
drop table DEAN;
drop table PHANCONG;

create table NHANVIEN
(
	MANV varchar2(7),
	TENNV nvarchar2(100),
	PHAI nvarchar2(6),
	NGAYSINH date,
    DIACHI nvarchar2(600),
	SODT varchar2(20),
	LUONG varchar2(100),
	PHUCAP varchar2(100),
    VAITRO nvarchar2(30),
    MANQL varchar2(7),
    PHG varchar2(7),
    USERNAME varchar2(20),
	Constraint PK_NHANVIEN primary key (MANV)
);

create table PHONGBAN
(
	MAPB varchar2(7),
	TENPB nvarchar2(100),
	TRPHG varchar2(7),
	Constraint PK_PHONGBAN primary key (MAPB)
);

create table DEAN
(
	MADA varchar2(7),
	TENDA nvarchar2(100),
	NGAYBD date,
    PHONG varchar2(7),
	Constraint PK_DEAN primary key (MADA)
);

create table PHANCONG
(
	MANV varchar2(7),
	MADA varchar2(7),
	THOIGIAN number(2),
	Constraint PK_PHANCONG primary key (MANV, MADA)
);

alter table NHANVIEN add constraint FK_NHANVIEN_MANQL Foreign key (MANQL) references NHANVIEN(MANV);
alter table NHANVIEN add constraint FK_NHANVIEN_PHG Foreign key (PHG) references PHONGBAN(MAPB);

alter table PHONGBAN add constraint FK_PHONGBAN_TRPHG Foreign key (TRPHG) references NHANVIEN(MANV);

alter table DEAN add constraint FK_DEAN_PHONG Foreign key (PHONG) references PHONGBAN(MAPB);

alter table PHANCONG add constraint FK_PHANCONG_PHG Foreign key (MADA) references DEAN(MADA);
alter table PHANCONG add constraint FK_PHANCONG_MANV Foreign key (MANV) references NHANVIEN(MANV);

--TRIGGER
/
CREATE OR REPLACE TRIGGER TRIGGER_UPPER_USERNAME_SINHVIEN
BEFORE INSERT
ON NHANVIEN 
FOR EACH ROW
BEGIN
    :NEW.USERNAME := UPPER(:NEW.USERNAME);
END;
/
--Ma hoa luong
CREATE OR REPLACE TRIGGER TRIGGER_ENCRYPT_NHANVIEN_LUONG
BEFORE INSERT OR UPDATE
ON NHANVIEN
FOR EACH ROW
DECLARE
    encrypted_raw     RAW(2000);
    raw_key           RAW(2000)        := UTL_RAW.CAST_TO_RAW('rO0ABXVyXvTTaw==');
BEGIN
    --luong
    encrypted_raw := DBMS_CRYPTO.ENCRYPT( src => UTL_RAW.cast_to_raw(:NEW.LUONG),
                                          typ => DBMS_CRYPTO.DES_CBC_PKCS5,
                                          key => raw_key);
    :NEW.LUONG := encrypted_raw;
END;
/
--Ma hoa phu cap
CREATE OR REPLACE TRIGGER TRIGGER_ENCRYPT_NHANVIEN_PHUCAP
BEFORE INSERT OR UPDATE
ON NHANVIEN
FOR EACH ROW
DECLARE
    encrypted_raw     RAW(2000);
    raw_key           RAW(2000)        := UTL_RAW.CAST_TO_RAW('rO0ABXVyXvTTaw==');
BEGIN
    --phucap
    encrypted_raw := DBMS_CRYPTO.ENCRYPT( src => UTL_RAW.cast_to_raw(:NEW.PHUCAP),
                                          typ => DBMS_CRYPTO.DES_CBC_PKCS5,
                                          key => raw_key);
    :NEW.PHUCAP := encrypted_raw;
END;
/

--Giai ma
CREATE OR REPLACE FUNCTION F_DECRYPT_NHANVIEN(val varchar2)
RETURN VARCHAR2
AS
    decrypted_raw     RAW(2000);
    raw_key           RAW(2000)        := UTL_RAW.CAST_TO_RAW('rO0ABXVyXvTTaw==');
BEGIN
    --decrypted_raw := DBMS_CRYPTO.DECRYPT( src => UTL_RAW.cast_to_raw(val),
    decrypted_raw := DBMS_CRYPTO.DECRYPT( src => val,
                                          typ => DBMS_CRYPTO.DES_CBC_PKCS5,
                                          key => raw_key);
    return UTL_I18N.RAW_TO_CHAR(decrypted_raw, 'AL32UTF8');
END;
/

INSERT INTO PHONGBAN VALUES('PB001', 'Phong Nhan Su', null);
INSERT INTO PHONGBAN VALUES('PB002', 'Phong Tai Chinh', null);

INSERT INTO NHANVIEN VALUES ('NV001','Jose Lopez', 'Male','21-10-2002','TPHCM','+1-971-533-4552x1542', 6000000,60000,'Giam Doc', null, null,'JoseLopez');
INSERT INTO NHANVIEN VALUES ('NV002','Diane Carter', 'Female','21-10-2002','TPHCM','881.633.0107', 11500000,115000,'Nhan Vien', null, 'PB001','DianeCarter');
INSERT INTO NHANVIEN VALUES ('NV003','Sherry Foster', 'Female','21-10-2002','TPHCM','001-966-861-0065x493', 11000000,110000,'QL Truc Tiep', null, 'PB001','SherryFoster');
INSERT INTO NHANVIEN VALUES ('NV004','Brenda Fisher', 'Female','21-10-2002','TPHCM','001-574-564-4648', 17000000,170000,'QL Truc Tiep', null, 'PB001','BrendaFisher');
INSERT INTO NHANVIEN VALUES ('NV005','Sharon Hunter', 'Female','21-10-2002','TPHCM','5838355842', 10500000,105000,'Truong Phong', 'NV003', 'PB001','SharonHunter');
INSERT INTO NHANVIEN VALUES ('NV006','Kimberly Jacobs', 'Female','21-10-2002','TPHCM','053-913-2609', 9000000,90000,'Truong Phong', 'NV004', 'PB002','KimberlyJacobs');
INSERT INTO NHANVIEN VALUES ('NV007','Brianna Marshall', 'Female','21-10-2002','TPHCM','701-932-8553', 7500000,75000,'Tai Chinh', 'NV003', 'PB002','BriannaMarshall');
INSERT INTO NHANVIEN VALUES ('NV008','Karen Tate', 'Female','21-10-2002','TPHCM','001-889-992-5260', 7500000,75000,'Truong De An', 'NV004', 'PB002','KarenTate');
INSERT INTO NHANVIEN VALUES ('NV009','Jillian Byrd', 'Female','21-10-2002','TPHCM','077-635-0084x1647', 13000000,130000,'Truong De An', 'NV003', 'PB002','JillianByrd');
INSERT INTO NHANVIEN VALUES ('NV010','Michael Sharp', 'Male','21-10-2002','TPHCM','(848)212-0230', 16000000,160000,'Nhan Su', 'NV004', 'PB002','MichaelSharp');
INSERT INTO NHANVIEN VALUES ('NV011','Robert Simpson', 'Male','21-10-2002','TPHCM','001-085-315-6112x464', 9500000,95000,'Nhan Vien', 'NV003', 'PB002','RobertSimpson');
INSERT INTO NHANVIEN VALUES ('NV012','Chad Mckee', 'Male','21-10-2002','TPHCM','496-469-5331x659', 6500000,65000,'Nhan Vien', 'NV004', 'PB002','ChadMckee');
INSERT INTO NHANVIEN VALUES ('NV013','George Mckenzie', 'Male','21-10-2002','TPHCM','(843)416-2489', 15500000,155000,'Nhan Vien', null, 'PB001','GeorgeMckenzie');
INSERT INTO NHANVIEN VALUES ('NV014','Kelly Smith', 'Female','21-10-2002','TPHCM','+1-380-230-4166', 11000000,110000,'Giam Doc', 'NV003', 'PB001','KellySmith');
INSERT INTO NHANVIEN VALUES ('NV015','David Crawford', 'Male','21-10-2002','TPHCM','(848)716-0019x0240', 11500000,115000,'Nhan Vien', 'NV004', 'PB001','DavidCrawford');
INSERT INTO NHANVIEN VALUES ('NV016','Carrie Benson', 'Female','21-10-2002','TPHCM','+1-368-801-2914x8616', 13000000,130000,'Nhan Vien', 'NV003', 'PB001','CarrieBenson');

UPDATE PHONGBAN SET TRPHG='NV006' WHERE MAPB='PB001';
UPDATE PHONGBAN SET TRPHG='NV005' WHERE MAPB='PB002';

INSERT INTO DEAN VALUES('DA001','Cafe meo', '20-10-2020','PB001');
INSERT INTO DEAN VALUES('DA002','Cafe tieng anh','3-4-2019','PB001');
INSERT INTO DEAN VALUES('DA003','Xe om cong nghe','5-7-2022','PB002');
INSERT INTO DEAN VALUES('DA004','Nuoc mia muon noi','11-12-2021','PB002');

INSERT INTO PHANCONG VALUES('NV009', 'DA001', 31);
INSERT INTO PHANCONG VALUES('NV002', 'DA001', 44);
INSERT INTO PHANCONG VALUES('NV005', 'DA001', 83);
INSERT INTO PHANCONG VALUES('NV007', 'DA001', 30);

INSERT INTO PHANCONG VALUES('NV003', 'DA002', 51);
INSERT INTO PHANCONG VALUES('NV004', 'DA002', 34);
INSERT INTO PHANCONG VALUES('NV010', 'DA002', 89);
INSERT INTO PHANCONG VALUES('NV011', 'DA002', 76);

INSERT INTO PHANCONG VALUES('NV012', 'DA003', 11);
INSERT INTO PHANCONG VALUES('NV013', 'DA003', 22);
INSERT INTO PHANCONG VALUES('NV014', 'DA003', 33);
INSERT INTO PHANCONG VALUES('NV015', 'DA003', 88);

INSERT INTO PHANCONG VALUES('NV016', 'DA004', 41);
INSERT INTO PHANCONG VALUES('NV008', 'DA004', 21);
INSERT INTO PHANCONG VALUES('NV010', 'DA004', 97);
INSERT INTO PHANCONG VALUES('NV005', 'DA004', 62);

COMMIT WORK;
------------------------------------------------------------------------------
------ Xoa User
CREATE OR REPLACE PROCEDURE USP_DROP_USER
AS
    CURSOR CUR IS (SELECT USERNAME
                    FROM NHANVIEN
                    WHERE USERNAME IN(SELECT USERNAME
                                        FROM ALL_USERS));
    strSQL VARCHAR(2000);
    CK_USER INT;
    Usr varchar2(30);
BEGIN
    OPEN CUR;
    LOOP
        FETCH CUR INTO Usr;
        EXIT WHEN CUR%NOTFOUND;
        strSQL := 'DROP USER ' || Usr;
        EXECUTE IMMEDIATE(strSQL);
    END LOOP;
END;
/
EXEC USP_DROP_USER;
/
------ Tao User, gan quyen dang nhap va ket noi database
CREATE OR REPLACE PROCEDURE USP_CREATE_USER
AS
    CURSOR CUR IS (SELECT USERNAME
                    FROM NHANVIEN
                    WHERE USERNAME NOT IN(SELECT USERNAME
                                        FROM ALL_USERS));
    strSQL VARCHAR(2000);
    CK_USER INT;
    Usr varchar2(30);
BEGIN
    OPEN CUR;
    LOOP
        FETCH CUR INTO Usr;
        EXIT WHEN CUR%NOTFOUND;
        strSQL := 'create user ' || Usr || ' IDENTIFIED BY a';
        EXECUTE IMMEDIATE(strSQL);
        strSQL := 'GRANT CREATE SESSION TO '|| Usr;
        EXECUTE IMMEDIATE(strSQL);
        strSQL := 'GRANT CONNECT TO ' || Usr;
        EXECUTE IMMEDIATE(strSQL);
    END LOOP;
END;
/
EXEC USP_CREATE_USER;
/
------------------------------------------------------------------------------
--Role: Truong phong


--drop USER NVTruongPhong;
--drop ROLE TRUONGPHONG;
--CREATE USER NVTruongPhong IDENTIFIED BY a;
---------------
drop ROLE TRUONGPHONG;
CREATE ROLE TRUONGPHONG;
--Tao view
CREATE OR REPLACE VIEW UV_NHANVIENPHONGBAN
AS
    SELECT NV1.manv, NV1.tennv, NV1.phai, NV1.ngaysinh, NV1.diachi, NV1.sodt,
        DECODE (NV1.username, SYS_CONTEXT('USERENV','SESSION_USER'), F_DECRYPT_NHANVIEN(NV1.luong), NULL) luong,
        DECODE (NV1.username, SYS_CONTEXT('USERENV','SESSION_USER'), F_DECRYPT_NHANVIEN(NV1.phucap), NULL) phucap,
        NV1.vaitro, NV1.manql, NV1.phg
    FROM NHANVIEN NV1 where NV1.PHG in(
            SELECT NV2.PHG
            FROM NHANVIEN NV2
            where NV2.username = SYS_CONTEXT('USERENV','SESSION_USER'));

CREATE OR REPLACE VIEW UV_PHANCONGPHONGBAN
AS
    SELECT *
    FROM PHANCONG PC where PC.MADA in(
            SELECT DA.MADA
            FROM DEAN DA
            where DA.PHONG IN(SELECT NV.PHG
                                FROM NHANVIEN NV
                                WHERE USERNAME=SYS_CONTEXT('USERENV','SESSION_USER')));
    
--Cap quyen tren bang
GRANT SELECT ON UV_NHANVIENPHONGBAN TO TRUONGPHONG;
GRANT SELECT, UPDATE, DELETE ON UV_PHANCONGPHONGBAN TO TRUONGPHONG;

--Cap quyen he thong
GRANT CREATE SESSION TO TRUONGPHONG;
GRANT CONNECT TO TRUONGPHONG;
--Gan quyen
GRANT TRUONGPHONG TO NVTruongPhong;

------------------------------------------------------------------------------
--Role: Nhan Su

drop role NHANSU;
create role NHANSU;

grant select, insert, update on nvquantri.PHONGBAN to NHANSU;
create or replace view nhanvien_ns
as
    select manv, tennv, phai, ngaysinh, diachi, sodt,
        DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), F_DECRYPT_NHANVIEN(luong), NULL) luong,
        DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), F_DECRYPT_NHANVIEN(phucap), NULL) phucap, vaitro, manql, phg 
    from nvquantri.nhanvien;

grant select on nvquantri.nhanvien_ns to NHANSU;
grant update(TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG) on NVQUANTRI.NHANVIEN TO NHANSU;
grant insert(TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG) on NVQUANTRI.NHANVIEN TO NHANSU;

------------------------------------------------------------------------------
--Role: Truong de an
drop role TRUONGDEAN;
create role TRUONGDEAN;

--Cac quyen cua nhanvien
grant UPDATE(NGAYSINH, DIACHI, SODT) on nvquantri.NHANVIEN to TRUONGDEAN;
GRANT SELECT ON nvquantri.PHANCONG TO TRUONGDEAN;
GRANT SELECT ON nvquantri.PHONGBAN TO TRUONGDEAN;
GRANT SELECT ON nvquantri.DEAN TO TRUONGDEAN;

--Cac quyen cua TRUONGDEAN
grant UPDATE,INSERT,SELECT,DELETE on nvquantri.DEAN to TRUONGDEAN;

GRANT CREATE VIEW TO nvquantri;
-- connect nvquantri/a;

--DROP VIEW CS_TRUONGDEAN;
--bang TRUONGDEAN
CREATE OR REPLACE VIEW CS_TRUONGDEAN AS
        SELECT NV.MANV, NV.TENNV, NV.PHAI, NV.NGAYSINH, NV.DIACHI, NV.SODT,
            F_DECRYPT_NHANVIEN(NV.LUONG) LUONG, F_DECRYPT_NHANVIEN(NV.PHUCAP) PHUCAP,
            NV.VAITRO, NV.MANQL, NV.PHG, PC.MADA, PC.THOIGIAN 
        FROM nvquantri.NHANVIEN NV 
        INNER JOIN nvquantri.PHANCONG PC ON NV.MANV = PC.MANV
        WHERE NV.USERNAME = (SYS_CONTEXT('USERENV', 'SESSION_USER'))
        WITH CHECK OPTION;

grant select on nvquantri.CS_TRUONGDEAN to TRUONGDEAN;

------------------------------------------------------------------------------
--Role: Nhan Vien
drop role NHANVIEN;
create role NHANVIEN;

--Cac quyen cua nhanvien
grant UPDATE(NGAYSINH, DIACHI, SODT) on nvquantri.NHANVIEN to NHANVIEN;
GRANT SELECT ON nvquantri.PHANCONG TO NHANVIEN;
GRANT SELECT ON nvquantri.PHONGBAN TO NHANVIEN;
GRANT SELECT ON nvquantri.DEAN TO NHANVIEN;
GRANT CREATE VIEW TO nvquantri;

--connect nvquantri/a
--DROP VIEW CS_NHANVIEN;
--bang nhanvien
CREATE OR REPLACE VIEW CS_NHANVIEN AS
        SELECT NV.MANV, NV.TENNV, NV.PHAI, NV.NGAYSINH, NV.DIACHI, NV.SODT, F_DECRYPT_NHANVIEN(NV.LUONG) LUONG, F_DECRYPT_NHANVIEN(NV.PHUCAP) PHUCAP, NV.VAITRO, NV.MANQL, NV.PHG, PC.MADA, PC.THOIGIAN 
        FROM nvquantri.NHANVIEN NV 
        INNER JOIN nvquantri.PHANCONG PC ON NV.MANV = PC.MANV
        WHERE NV.USERNAME = (SYS_CONTEXT('USERENV', 'SESSION_USER'))   
        WITH CHECK OPTION;

grant select on nvquantri.CS_NHANVIEN to NHANVIEN;
------------------------------------------------------------------------------
drop role TAICHINH;
create role TAICHINH;
--Cs#4: Taichinh
--Cac quyen cua nhanvien
grant UPDATE(NGAYSINH, DIACHI, SODT) on nvquantri.NHANVIEN to TAICHINH;
GRANT SELECT ON nvquantri.PHONGBAN TO TAICHINH;
GRANT SELECT ON nvquantri.DEAN TO TAICHINH;

--xem/them/cap nhat NHANVIEN va PHONGBAN
grant select on nvquantri.NHANVIEN to TAICHINH;
grant UPDATE(LUONG, PHUCAP) on nvquantri.NHANVIEN to TAICHINH;

grant select on nvquantri.PHANCONG to TAICHINH;


--connect nvquantri/1234;
--DROP VIEW CS_NHANVIEN;
--bang nhanvien
CREATE OR REPLACE VIEW CS_NHANVIEN AS
        SELECT NV.MANV, NV.TENNV, NV.PHAI, NV.NGAYSINH, NV.DIACHI, NV.SODT,
            F_DECRYPT_NHANVIEN(NV.LUONG) LUONG, F_DECRYPT_NHANVIEN(NV.PHUCAP) PHUCAP,
            NV.VAITRO, NV.MANQL, NV.PHG, PC.MADA, PC.THOIGIAN 
        FROM nvquantri.NHANVIEN NV 
        INNER JOIN nvquantri.PHANCONG PC ON NV.MANV = PC.MANV
        WHERE NV.USERNAME = (SYS_CONTEXT('USERENV', 'SESSION_USER'))
        WITH CHECK OPTION;

SELECT * FROM nvquantri.PHONGBAN PB JOIN nvquantri.DEAN DA ON PB.MAPB = DA.PHONG;


grant select on nvquantri.CS_NHANVIEN to TAICHINH;

------------------------------------------------------------------------------
drop role QLTRUCTIEP;
create role QLTRUCTIEP;
grant create session to QLTRUCTIEP;
--
create or replace view nhanvien_qltructiep
as
    select manv, tennv, phai, ngaysinh, diachi, sodt,
        DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), F_DECRYPT_NHANVIEN(luong), NULL) luong,
        DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), F_DECRYPT_NHANVIEN(phucap), NULL) phucap, vaitro, manql, phg 
    from nvquantri.nhanvien nv1
    where nv1.username = SYS_CONTEXT('USERENV','SESSION_USER') or nv1.manql in 
    (select nv2.manv from nvquantri.nhanvien nv2 where nv2.username = SYS_CONTEXT('USERENV','SESSION_USER'));

--
create or replace view phancong_qltructiep
as
    select pc.manv, pc.mada, pc.thoigian
    from nvquantri.phancong pc join nvquantri.nhanvien nv on pc.manv = nv.manv
    where nv.username = SYS_CONTEXT('USERENV','SESSION_USER') or nv.manql in 
    (select nv2.manv from nvquantri.nhanvien nv2 where nv2.username = SYS_CONTEXT('USERENV','SESSION_USER'));
    
grant select on phancong_qltructiep to QLTRUCTIEP; 
grant select on nhanvien_qltructiep to QLTRUCTIEP;


/
--GRANT QUYEN
CREATE OR REPLACE PROCEDURE USP_GRANT_PRIVS
AS
    CURSOR CUR IS (SELECT USERNAME, VAITRO
                    FROM NHANVIEN
                    WHERE USERNAME IN(SELECT USERNAME
                                        FROM ALL_USERS));
    strSQL VARCHAR(2000);
    CK_USER INT;
    Usr varchar2(30);
    VT Nvarchar2(30);
BEGIN
    OPEN CUR;
    LOOP
        FETCH CUR INTO Usr, VT;
        EXIT WHEN CUR%NOTFOUND;
        
        IF VT = 'Nhan Su' THEN
            strSQL := 'GRANT NHANSU TO '|| Usr;
            EXECUTE IMMEDIATE(strSQL);
        ELSIF VT = 'QL Truc Tiep' THEN
            strSQL := 'GRANT QLTRUCTIEP TO '|| Usr;
            EXECUTE IMMEDIATE(strSQL);
        ELSIF VT = 'Truong Phong' THEN
            strSQL := 'GRANT TRUONGPHONG TO '|| Usr;
            EXECUTE IMMEDIATE(strSQL);
        ELSIF VT = 'Tai Chinh' THEN
            strSQL := 'GRANT TAICHINH TO '|| Usr;
            EXECUTE IMMEDIATE(strSQL);
        ELSIF VT = 'Truong De An' THEN
            strSQL := 'GRANT TRUONGDEAN TO '|| Usr;
            EXECUTE IMMEDIATE(strSQL);
        END IF;
        
        strSQL := 'GRANT NHANVIEN TO '|| Usr;
        EXECUTE IMMEDIATE(strSQL);

    END LOOP;
END;
/
EXEC USP_GRANT_PRIVS;
/