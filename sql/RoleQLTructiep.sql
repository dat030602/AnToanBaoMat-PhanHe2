create role QLTRUCTIEP;
grant create session to QLTRUCTIEP;
--
create or replace view nhanvien_qltructiep
as
    select manv, tennv, phai, ngaysinh, diachi, sodt, DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), luong, NULL) luong, DECODE (username, SYS_CONTEXT('USERENV','SESSION_USER'), phucap, NULL) phucap, vaitro, manql, phg 
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