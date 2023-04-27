--File nay khong co chay 1 lan duoc dau nha!!!!!!
--Log in tai khoan nvquantri/a
--Tao role NHANSU va cap cac quyen connect
create role NHANSU;
--Tao user va gan role NHANSU


--Cs#5: Nhan su
--xem/them/cap nhat phongban
grant select, insert, update on nvquantri.PHONGBAN to NHANSU;
--bang nhanvien
create or replace view nhanvien_ns
as
    select manv, tennv, phai, ngaysinh, diachi, sodt, DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), luong, NULL) luong, DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), phucap, NULL) phucap, vaitro, manql, phg 
    from nvquantri.nhanvien;

grant select on nvquantri.nhanvien_ns to NHANSU;
grant update(TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG) on NVQUANTRI.NHANVIEN TO NHANSU;
grant insert(TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG) on NVQUANTRI.NHANVIEN TO NHANSU;
 

