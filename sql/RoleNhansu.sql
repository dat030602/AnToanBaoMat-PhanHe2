create role NHANSU;
grant NHANSU to MICHAELSHARP;

grant select, insert, update on PHONGBAN to NHANSU;
grant select on DEAN to NHANSU;

create or replace view UV_PHANCONG_NHANSU
as
    SELECT pc.MANV, pc.MADA, pc.THOIGIAN
    FROM PHANCONG pc JOIN NHANVIEN nv ON pc.MANV = nv.MANV
    WHERE nv.USERNAME = SYS_CONTEXT('USERENV','SESSION_USER');

grant select on UV_PHANCONG_NHANSU to NHANSU;

create or replace view UV_NHANVIEN_NHANSU
as
    select manv, tennv, phai, ngaysinh, diachi, sodt, DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), F_DECRYPT_NHANVIEN(luong), NULL) luong, DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), F_DECRYPT_NHANVIEN(phucap), NULL) phucap, vaitro, manql, phg 
    from nvquantri.nhanvien;

grant select on nvquantri.UV_NHANVIEN_NHANSU to NHANSU;
grant update(TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG) on nvquantri.UV_NHANVIEN_NHANSU TO NHANSU;
grant insert(TENNV, PHAI, NGAYSINH, DIACHI, SODT, VAITRO, MANQL, PHG) on nvquantri.UV_NHANVIEN_NHANSU TO NHANSU;
 

