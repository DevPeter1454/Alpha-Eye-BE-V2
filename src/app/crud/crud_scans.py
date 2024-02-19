from fastcrud import FastCRUD

from ..models.scans import Scan
from ..schemas.scans import ScanCreateInternal, ScanUpdate, ScanUpdateInternal, ScanDelete

CRUDScan = FastCRUD[Scan, ScanCreateInternal, ScanUpdateInternal, ScanUpdate, ScanDelete]

crud_scans = CRUDScan(Scan)