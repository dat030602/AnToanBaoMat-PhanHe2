SELECT VALUE FROM v$option WHERE parameter = 'Oracle Label Security';
SELECT status FROM dba_ols_status WHERE name = 'OLS_CONFIGURE_STATUS';
EXEC LBACSYS.CONFIGURE_OLS;
EXEC LBACSYS.OLS_ENFORCEMENT.ENABLE_OLS;
shutdown IMMEDIATE;
startup;
-----------------------
GRANT CONNECT,RESOURCE,SELECT_CATALOG_ROLE TO NVQuanTri;
GRANT UNLIMITED TABLESPACE TO NVQuanTri;
GRANT SELECT ANY DICTIONARY TO NVQuanTri;
GRANT EXECUTE ON sa_components TO NVQuanTri WITH GRANT OPTION;
GRANT EXECUTE ON sa_user_admin TO NVQuanTri WITH GRANT OPTION;
GRANT EXECUTE ON sa_label_admin TO NVQuanTri WITH GRANT OPTION;
GRANT EXECUTE ON sa_policy_admin TO NVQuanTri WITH GRANT OPTION;
GRANT EXECUTE ON sa_audit_admin TO NVQuanTri WITH GRANT OPTION;
GRANT EXECUTE ON SA_SESSION TO NVQuanTri WITH GRANT OPTION;
GRANT LBAC_DBA TO NVQuanTri;
GRANT EXECUTE ON sa_sysdba TO NVQuanTri;
GRANT EXECUTE ON to_lbac_data_label TO NVQuanTri;
GRANT INHERIT PRIVILEGES ON USER SYS TO LBACSYS;

BEGIN
SA_SYSDBA.DROP_POLICY(
    policy_name => 'region_policy'
);
END;

BEGIN
SA_SYSDBA.CREATE_POLICY(
    policy_name => 'region_policy',
    column_name => 'region_label',
    default_options => 'read_control, write_control, update_control'
);
END;
/
GRANT region_policy_DBA TO NVQuanTri;

EXEC SA_SYSDBA.ENABLE_POLICY ('region_policy');
--Disconenct
EXECUTE SA_COMPONENTS.CREATE_LEVEL('region_policy',20,'NV','NHANVIEN');
EXECUTE SA_COMPONENTS.CREATE_LEVEL('region_policy',40,'TP','TRUONGPHONG');
EXECUTE SA_COMPONENTS.CREATE_LEVEL('region_policy',60,'GD','GIAMDOC');
--tao compartment
EXECUTE SA_COMPONENTS.CREATE_COMPARTMENT('region_policy',100,'MB1','MUABAN');
EXECUTE SA_COMPONENTS.CREATE_COMPARTMENT('region_policy',120,'SX','SANXUAT');
EXECUTE SA_COMPONENTS.CREATE_COMPARTMENT('region_policy',140,'GC','GIACONG');
--tao group
EXECUTE SA_COMPONENTS.CREATE_GROUP('region_policy',20,'MB','MIENBAC');
EXECUTE SA_COMPONENTS.CREATE_GROUP('region_policy',40,'MT','MIENTRUNG');
EXECUTE SA_COMPONENTS.CREATE_GROUP('region_policy',60,'MN','MIENNAM');

SELECT * FROM dba_sa_levels;
SELECT * FROM DBA_SA_COMPARTMENTS;
SELECT * FROM DBA_SA_GROUPS;
SELECT * FROM DBA_SA_GROUP_HIERARCHY;

EXECUTE SA_USER_ADMIN.SET_USER_PRIVS('region_policy','NVQuanTri','FULL,PROFILE_ACCESS');

drop TABLE THONGBAO;
CREATE TABLE THONGBAO (
    id NUMBER(10) NOT NULL,
    noidung VARCHAR2(100),
    khuvuc VARCHAR2(30),
    linhvuc VARCHAR2(30),
    vaitro VARCHAR2(30),
    CONSTRAINT THONGBAO_pk PRIMARY KEY (id));
    
GRANT SELECT, INSERT, UPDATE, DELETE ON THONGBAO TO PUBLIC;

INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 1, 'Thong bao 1', 'MIENNAM', 'MUABAN', 'GIAMDOC');
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 2, 'Thong bao 2', 'MIENNAM', 'SANXUAT', 'TRUONGPHONG');
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 3, 'Thong bao 3', 'MIENNAM', 'GIACONG', 'NHANVIEN');
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 4, 'Thong bao 4', 'MIENBAC', 'MUABAN', 'TRUONGPHONG');
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 5, 'Thong bao 5', 'MIENBAC', 'SANXUAT', 'NHANVIEN');
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 6, 'Thong bao 6', 'MIENTRUNG', 'MUABAN', 'TRUONGPHONG');
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 7, 'Thong bao 7', 'MIENTRUNG', 'SANXUAT', 'NHANVIEN');
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 8, 'Thong bao 8', 'MIENNAM', 'SANXUAT', 'NHANVIEN');
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro)
VALUES ( 9, 'Thong bao 9', 'MIENBAC', 'SANXUAT', 'GIAMDOC');
commit;
/
CREATE OR REPLACE FUNCTION get_thongbao_label (
    p_vaitro IN VARCHAR2,
    p_linhvuc IN VARCHAR2,
    p_khuvuc IN VARCHAR2)
RETURN varchar --LBACSYS.LBAC_LABEL
AS
    v_label VARCHAR2(80);
BEGIN
    IF p_vaitro = 'GIAMDOC' THEN
        v_label := 'GD:';
    ELSIF p_vaitro = 'TRUONGPHONG' THEN
        v_label := 'TP:';
    ELSE
        v_label := 'NV:';
    END IF;
    
    IF p_linhvuc = 'MUABAN' THEN
        v_label := v_label || 'MB1:';
    ELSIF p_linhvuc = 'SANXUAT' THEN
        v_label := v_label || 'SX:';
    ELSIF p_linhvuc = 'GIACONG' THEN
        v_label := v_label || 'GC:';
    END IF;
    
    IF p_khuvuc = 'MIENBAC' THEN
        v_label := v_label || 'MB';
    ELSIF p_khuvuc = 'MIENTRUNG' THEN
        v_label := v_label || 'MT';
    ELSIF p_khuvuc = 'MIENNAM' THEN
        v_label := v_label || 'MN';
    END IF;
    
    RETURN CHAR_TO_LABEL('region_policy',v_label);
    
END get_thongbao_label;
/
BEGIN
SA_POLICY_ADMIN.REMOVE_TABLE_POLICY('region_policy','NVQuanTri','THONGBAO'); 
SA_POLICY_ADMIN.APPLY_TABLE_POLICY (
    policy_name => 'region_policy',
    schema_name => 'NVQuanTri',
    table_name => 'THONGBAO',
    table_options => 'READ_CONTROL,WRITE_CONTROL,CHECK_CONTROL',
    predicate => NULL);
END;
/
DECLARE
    CURSOR CUR IS SELECT vaitro,linhvuc, khuvuc,id FROM THONGBAO;
    custype VARCHAR(30);
    reg VARCHAR(30);
    cred VARCHAR(30);
    p int;
BEGIN
    OPEN CUR;
    LOOP
        FETCH cur into custype, reg,cred,p;
        IF cur%NOTFOUND THEN
            EXIT;
        END IF;
        
        UPDATE THONGBAO
            SET region_label = get_thongbao_label(custype,reg,cred)
            where id = p;
    END LOOP;
    CLOSE CUR;
END; 
/
BEGIN
    SA_USER_ADMIN.SET_USER_LABELS('region_policy','NVQuanTri','GD:MB1,SX,GC:MB,MT,MN');
    SA_USER_ADMIN.SET_USER_LABELS('region_policy','JOSELOPEZ','GD:MB1,SX,GC:MB,MT,MN'); -- GIAM DOC
    SA_USER_ADMIN.SET_USER_LABELS('region_policy','SHARONHUNTER','TP:SX:MN'); -- TRUONG PHONG
    SA_USER_ADMIN.SET_USER_LABELS('region_policy','KELLYSMITH','GD:MB1,SX,GC:MB'); --GIAM DOC
END;
/
INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro, region_label)
VALUES ( 12, 'Thong bao 12', 'MIENBAC', 'SANXUAT', 'GIAMDOC', get_thongbao_label('GIAMDOC','SANXUAT','MIENBAC'));

INSERT INTO THONGBAO (id, noidung, khuvuc, linhvuc, vaitro, region_label)
VALUES ( {id}, {noidung}, {khuvuc}, {linhvuc}, {vaitro}, get_thongbao_label({vaitro},{linhvuc},{khuvuc}));